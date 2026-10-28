#!/usr/bin/env python3
"""Translate and proofread check.openline.com strings through OpenRouter.

Pipeline per locale (English source: scripts/i18n/en.json):
  1. translate  — fast multilingual model writes the full dictionary
  2. proofread  — a different model family reviews it as a native speaker,
                  against the English source, and returns the corrected dictionary
  3. validate   — keys, {placeholders}, HTML tags and plural categories must match;
                  failures are retried once, then reported

Accepted results are cached in scripts/i18n/translations/<code>.json together with a
hash of the English source, so unchanged locales are never re-translated.

Requires an OpenRouter key: OPENROUTER_API_KEY in the environment, or an HTTPS proxy
that injects it (e.g. `pplx credentials run <handle> -- python3 scripts/translate_i18n.py`).

Usage: python3 scripts/translate_i18n.py [--only fr,de] [--force] [--workers 6]
"""
import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import re
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I18N = os.path.join(ROOT, "scripts", "i18n")
OUT = os.path.join(I18N, "translations")
TRANSLATOR = os.environ.get("OL_TRANSLATOR", "google/gemini-3.7-flash")
REVIEWER = os.environ.get("OL_REVIEWER", "anthropic/claude-sonnet-5.5")
API = "https://openrouter.ai/api/v1/chat/completions"

TONE = {
    "de": "Address the reader informally with “du” (as openline.com/de does).",
    "fr": "Address the reader with “vous” (as openline.com/fr does).",
    "ja": "Use polite です/ます style (as openline.com/ja does).",
    "pt": "European Portuguese (Portugal) spelling and vocabulary, e.g. “telemóvel”, “ecrã”, “definições”; never Brazilian forms.",
    "pt-BR": "Brazilian Portuguese, e.g. “celular”, “configurações”, “chip”; address the reader as “você”.",
    "es": "Spanish from Spain, e.g. “móvil”; address the reader as “tú”.",
    "es-419": "Neutral Latin American Spanish, e.g. “celular”; address the reader as “tú”; avoid Spain-only words like “móvil” or “vosotros”.",
    "zh": "Simplified Chinese for mainland China readers.",
    "zh-TW": "Traditional Chinese with Taiwan vocabulary (e.g. 手機, 設定, 行動網路).",
    "ko": "Polite 해요체 / 합니다체 as is usual in Korean consumer apps.",
    "no": "Norwegian Bokmål.",
    "tl": "Natural modern Filipino as used in apps in the Philippines; common English tech words (eSIM, SIM, Wi-Fi, model number) may stay in English as Filipinos say them.",
    "hi": "Natural modern Hindi as used in Indian consumer apps; common tech words may stay in English if that is how people say them.",
    "bn": "Natural modern Bengali as used in consumer apps.",
    "ms": "Bahasa Melayu (Malaysia), not Indonesian.",
}

RULES = """You are localizing the UI of "Openline Check" (check.openline.com), a free web tool where people
search a phone, tablet, smartwatch or hotspot and see whether it supports eSIM. Openline is a travel eSIM brand.

Return ONLY a JSON object with exactly the same keys as the input.
Hard rules:
- Keep every {placeholder} exactly as written (e.g. {n}, {q}, {total}, {brands}, {network}, {regions}, {max}, {note}, {status}).
- Keys ending in "Html" contain HTML: keep every tag and attribute exactly (same tags, same order is not required but same set); translate only the text.
- Plural values are objects: return an object whose keys are exactly the CLDR categories listed for this language: {plural_cats}. Each form must read correctly for that count.
- Never translate: Openline, eSIM, EID, eUICC, SIM, nano-SIM, micro-SIM, QR, Wi-Fi, LTE, 4G/5G/3G/2G, GPS, CDMA, iDEN, KaiOS, HarmonyOS, Windows Phone, model codes (SM-S921B, A3717), product and carrier names (iPhone, iPad, Apple Watch, Galaxy, Pixel, Redmi, POCO, Nighthawk, Verizon, Sprint, T-Mobile, AT&T, Google Fi, Nextel, Boost, NTT DoCoMo, au, SoftBank, Rakuten, KT, SKT, LGU+...), USSD code *#06#, URLs, e-mail addresses, @handles.
- Region codes in short labels (US, CN, HK, MO, JP, CA, KR, IN, EU, AU, TW, SEA) may stay as codes; keep labels whose keys start with "note." very short (they are small badges, ideally under 28 characters).
- Settings paths such as “Settings › Cellular” must use the official menu names of iOS/Android in this language when you know them; keep the › separator.
- Dates, numbers and facts must stay identical in meaning. Do not add or remove information.
- Write as a native speaker would for a polished consumer product: natural, concise, friendly, never word-for-word. Use the language's own typographic conventions (quotes, spacing before punctuation in French, etc.).
- "meta.title" is an SEO page title: keep it natural and include the local word people search for (eSIM + phone/compatibility).
"""

REVIEW = """You are a native {lang_name} copy editor and proofreader. Below is the English source and a draft
translation of the "Openline Check" UI (a free eSIM compatibility checker on check.openline.com).

Review every string against the English source as a demanding native speaker:
- fix mistranslations, omissions, additions, wrong facts or numbers, and anything that sounds translated or unnatural;
- fix grammar, agreement, plural forms, spelling, punctuation and typography for {lang_name};
- keep terminology consistent across all strings; keep "note." badge labels short;
- keep every {{placeholder}}, HTML tag, brand/product/carrier name and model code exactly;
- plural objects must have exactly these categories: {plural_cats}.
{tone}
Return ONLY a JSON object: {{"strings": <the full corrected dictionary with exactly the same keys>, "changes": <number of strings you changed>, "notes": "<one short sentence on the main fixes>"}}.
"""


def src_hash(en):
    return hashlib.sha256(json.dumps(en, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]


def plural_categories(code):
    js = "console.log(JSON.stringify(new Intl.PluralRules(%r).resolvedOptions().pluralCategories))" % code
    return json.loads(subprocess.check_output(["node", "-e", js], text=True))


def call(model, system, user, max_tokens=24000, effort="low"):
    body = {
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "response_format": {"type": "json_object"},
        "temperature": 0.2,
        "max_tokens": max_tokens,
        "reasoning": {"effort": effort},
        "usage": {"include": True},
    }
    cmd = ["curl", "-sS", "--max-time", "600", API, "-H", "Content-Type: application/json", "--data-binary", "@-"]
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        cmd[1:1] = ["-H", "Authorization: Bearer " + key]
    for attempt in range(3):
        res = subprocess.run(cmd, input=json.dumps(body), capture_output=True, text=True)
        try:
            data = json.loads(res.stdout)
            content = data["choices"][0]["message"]["content"]
            content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content.strip())
            return json.loads(content), data.get("usage", {})
        except Exception as e:  # noqa: BLE001
            err = res.stdout[:300] or res.stderr[:300]
            time.sleep(4 * (attempt + 1))
    raise RuntimeError("%s failed: %s" % (model, err))


TAG = re.compile(r"</?[a-zA-Z][^>]*>")
PH = re.compile(r"\{\w+\}")


def validate(en, tr, cats):
    problems = []
    for k, v in en.items():
        if k not in tr:
            problems.append("missing " + k)
            continue
        t = tr[k]
        if isinstance(v, dict):
            if not isinstance(t, dict) or sorted(t) != sorted(cats):
                problems.append("plural categories %s: %s" % (k, sorted(t) if isinstance(t, dict) else type(t).__name__))
                continue
            pairs = [(v.get("other"), t[c]) for c in cats]
        else:
            if not isinstance(t, str) or not t.strip():
                problems.append("empty " + k)
                continue
            pairs = [(v, t)]
        for s, d in pairs:
            if sorted(set(PH.findall(s))) != sorted(set(PH.findall(d))):
                problems.append("placeholders %s: %s vs %s" % (k, PH.findall(s), PH.findall(d)))
            if k.endswith("Html") and sorted(TAG.findall(s)) != sorted(TAG.findall(d)):
                problems.append("html %s" % k)
            if not k.endswith("Html") and TAG.search(d):
                problems.append("stray html %s" % k)
    extra = [k for k in tr if k not in en]
    if extra:
        problems.append("extra keys " + ", ".join(extra[:5]))
    return problems


def run_locale(loc, en, h, force):
    code = loc["code"]
    path = os.path.join(OUT, code + ".json")
    if not force and os.path.exists(path):
        cached = json.load(open(path, encoding="utf-8"))
        if cached.get("_source") == h:
            return code, "cached", None
    cats = plural_categories(code)
    tone = TONE.get(code, "")
    system = RULES.replace("{plural_cats}", json.dumps(cats))
    user = "Target language: %s (%s). %s\n\nJSON to translate:\n%s" % (
        loc["english"], code, tone, json.dumps(en, ensure_ascii=False, indent=1))
    usage = []
    draft, u = call(TRANSLATOR, system, user)
    usage.append(u)
    probs = validate(en, draft, cats)
    if probs:
        fix = user + "\n\nYour previous answer had these problems, fix them:\n- " + "\n- ".join(probs[:40])
        draft, u = call(TRANSLATOR, system, fix)
        usage.append(u)
    review_sys = REVIEW.format(lang_name=loc["english"], plural_cats=json.dumps(cats), tone=tone)
    review_user = "English source:\n%s\n\nDraft %s translation:\n%s" % (
        json.dumps(en, ensure_ascii=False, indent=1), loc["english"], json.dumps(draft, ensure_ascii=False, indent=1))
    rev, u = call(REVIEWER, review_sys, review_user, effort="medium")
    usage.append(u)
    final = rev.get("strings", rev)
    probs = validate(en, final, cats)
    if probs:
        # Keep the reviewer's wording where valid; fall back to the validated draft entry otherwise.
        bad = {p.split(" ")[1].rstrip(":") for p in probs if " " in p}
        for k in bad:
            if k in draft:
                final[k] = draft[k]
        final = {k: final[k] for k in en if k in final}
        probs = validate(en, final, cats)
    if probs:
        return code, "failed", probs
    out = {"_source": h, "_translator": TRANSLATOR, "_reviewer": REVIEWER,
           "_review_changes": rev.get("changes"), "_review_notes": rev.get("notes"),
           "_cost_usd": round(sum(float(x.get("cost") or 0) for x in usage), 4)}
    out.update({k: final[k] for k in en})
    os.makedirs(OUT, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    return code, "ok", out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()
    en = json.load(open(os.path.join(I18N, "en.json"), encoding="utf-8"))
    h = src_hash(en)
    locales = [l for l in json.load(open(os.path.join(I18N, "locales.json"), encoding="utf-8")) if l["code"] != "en"]
    if a.only:
        want = set(a.only.split(","))
        locales = [l for l in locales if l["code"] in want]
    failed = 0
    total_cost = 0.0
    with cf.ThreadPoolExecutor(a.workers) as ex:
        futs = {ex.submit(run_locale, l, en, h, a.force): l for l in locales}
        for f in cf.as_completed(futs):
            try:
                code, status, info = f.result()
            except Exception as e:  # noqa: BLE001
                code, status, info = futs[f]["code"], "error", str(e)[:300]
            if status == "ok":
                total_cost += info["_cost_usd"]
                print("%-6s ok   review changes=%s cost=$%.4f  %s" % (code, info["_review_changes"], info["_cost_usd"], (info["_review_notes"] or "")[:140]), flush=True)
            else:
                if status != "cached":
                    failed += 1
                print("%-6s %s %s" % (code, status, info if info else ""), flush=True)
    print("Total OpenRouter cost this run: $%.4f" % total_cost)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
