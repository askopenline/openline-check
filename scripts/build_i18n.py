#!/usr/bin/env python3
"""Build the localized pages of check.openline.com.

Sources (English is the source of truth):
  scripts/i18n/en.json              English strings
  scripts/i18n/translations/<code>.json   reviewed translations (OpenRouter pipeline)
  scripts/i18n/locales.json         locale list (same codes/paths as openline.com)
  scripts/i18n/index.template.html  page template with {{key}} placeholders

Outputs:
  index.html, <path>/index.html for every locale
  i18n/<code>.js                    runtime dictionary for app.js
  404.html                          multilingual not-found page
  sitemap.xml                       all locales with hreflang alternates

Usage: python3 scripts/build_i18n.py [--version 24]
"""
import argparse
import datetime
import html
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I18N = os.path.join(ROOT, "scripts", "i18n")
SITE = "https://check.openline.com"


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def device_stats():
    js = (
        'eval(require("fs").readFileSync(%r,"utf8").replace("const DEVICES","global.DEVICES"));'
        "console.log(JSON.stringify({total:DEVICES.length,brands:new Set(DEVICES.map(d=>d.brand)).size}))"
    ) % os.path.join(ROOT, "devices.js")
    return json.loads(subprocess.check_output(["node", "-e", js], text=True))


def number_formats(codes, values):
    js = (
        "const c=%s,v=%s,o={};for(const l of c){o[l]={};for(const n of v)"
        "o[l][n]=new Intl.NumberFormat(l,{numberingSystem:'latn'}).format(n)}console.log(JSON.stringify(o))"
    ) % (json.dumps(codes), json.dumps(values))
    return json.loads(subprocess.check_output(["node", "-e", js], text=True))


def url_for(loc):
    return SITE + "/" + (loc["path"] + "/" if loc["path"] else "")


def french_spacing(v):
    """French typography: keep ? ! : ; » glued to the previous word and « to the next."""
    if isinstance(v, dict):
        return {k: french_spacing(x) for k, x in v.items()}
    v = re.sub(r"[ \u00a0\u202f]+([?!:;»])", "\u00a0\\1", v)
    v = re.sub(r"(«)[ \u00a0\u202f]+", "\\1\u00a0", v)
    return v


def plural_other(v):
    return v.get("other", "") if isinstance(v, dict) else v


def build(version):
    en = load(os.path.join(I18N, "en.json"))
    locales = load(os.path.join(I18N, "locales.json"))
    tpl = open(os.path.join(I18N, "index.template.html"), encoding="utf-8").read()
    stats = device_stats()
    nums = number_formats([l["code"] for l in locales], [stats["total"], stats["brands"]])

    dicts = {}
    missing = {}
    for loc in locales:
        code = loc["code"]
        if code == "en":
            d = dict(en)
        else:
            p = os.path.join(I18N, "translations", code + ".json")
            tr = load(p) if os.path.exists(p) else {}
            miss = [k for k in en if k not in tr]
            if miss:
                missing[code] = miss
            d = {k: tr.get(k, en[k]) for k in en}
            if code == "fr":
                d = {k: french_spacing(v) for k, v in d.items()}
        dicts[code] = d
    if missing:
        for c, m in missing.items():
            print("WARN %s missing %d keys (English fallback): %s" % (c, len(m), ", ".join(m[:6])), file=sys.stderr)

    alternates = "\n".join(
        '    <link rel="alternate" hreflang="%s" href="%s" />' % (l["code"], url_for(l)) for l in locales
    ) + '\n    <link rel="alternate" hreflang="x-default" href="%s/" />' % SITE

    # Path → code map for the root-page language redirect (first visit only).
    redirect_map = {l["code"].lower(): ("/" + l["path"] + "/" if l["path"] else "/") for l in locales}

    for loc in locales:
        code = loc["code"]
        d = dicts[code]
        total = nums[code][str(stats["total"])]
        brands = nums[code][str(stats["brands"])]
        canonical = url_for(loc)

        def val(key, arg=None):
            v = plural_other(d[key])
            v = v.replace("{total}", total).replace("{brands}", brands)
            if key == "footer.indexedHtml":
                v = v.replace("{n}", total)
            if arg is not None:
                v = v.replace("{network}", arg)
            return v

        og_alts = "\n".join(
            '    <meta property="og:locale:alternate" content="%s" />' % l["og"] for l in locales if l["code"] != code
        )

        faq = []
        for i in range(1, 6):
            faq.append({
                "@type": "Question",
                "name": val("faq.q%d" % i),
                "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", val("faq.a%dHtml" % i))},
            })
        ld = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Organization", "@id": "https://openline.com/#org", "name": "Openline",
                    "url": "https://openline.com/", "logo": SITE + "/icons/icon-512.png", "email": "ask@openline.com",
                    "sameAs": ["https://x.com/askopenline", "https://instagram.com/askopenline",
                               "https://facebook.com/askopenline", "https://youtube.com/@askopenline",
                               "https://github.com/askopenline"],
                },
                {
                    "@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/",
                    "name": val("meta.appName"), "inLanguage": [l["code"] for l in locales],
                    "publisher": {"@id": "https://openline.com/#org"},
                },
                {
                    "@type": "WebApplication", "@id": canonical + "#app", "name": val("meta.appName"),
                    "url": canonical, "inLanguage": code, "applicationCategory": "UtilitiesApplication",
                    "operatingSystem": "Any", "browserRequirements": "Requires JavaScript",
                    "description": val("meta.description"), "image": SITE + "/og.png?v=2",
                    "isAccessibleForFree": True,
                    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
                    "publisher": {"@id": "https://openline.com/#org"},
                    "potentialAction": {
                        "@type": "SearchAction",
                        "target": {"@type": "EntryPoint", "urlTemplate": canonical + "?q={search_term_string}"},
                        "query-input": "required name=search_term_string",
                    },
                },
                {"@type": "FAQPage", "@id": canonical + "#faq", "inLanguage": code, "mainEntity": faq},
            ],
        }
        jsonld = json.dumps(ld, ensure_ascii=False, indent=2).replace("</", "<\\/")

        cur = loc
        items = []
        for l in locales:
            href = "/" + l["path"] + "/" if l["path"] else "/"
            items.append(
                '          <li><a href="%s" hreflang="%s" lang="%s" data-lang="%s"%s>'
                '<img class="lang-flag" src="/flags/%s.png" width="20" height="15" alt="" loading="lazy" decoding="async" />'
                "<span>%s</span></a></li>"
                % (href, l["code"], l["code"], l["code"], ' aria-current="true"' if l is cur else "", l["flag"], html.escape(l["name"]))
            )
        switcher = (
            '      <div class="lang" id="lang">\n'
            '        <button class="lang-btn" type="button" aria-haspopup="true" aria-expanded="false" aria-controls="lang-menu"'
            ' aria-label="%s: %s" title="%s">\n'
            '          <img class="lang-flag" src="/flags/%s.png" width="20" height="15" alt="" />\n'
            '          <span class="lang-code">%s</span>\n'
            '          <svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><path fill="none" stroke="currentColor"'
            ' stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M6 9l6 6 6-6" /></svg>\n'
            "        </button>\n"
            '        <ul class="lang-menu" id="lang-menu" aria-label="%s" hidden>\n%s\n        </ul>\n'
            "      </div>"
        ) % (
            html.escape(val("lang.aria")), html.escape(cur["name"]), html.escape(val("lang.label")),
            cur["flag"], (cur["path"] or "en").upper() if cur["path"] not in ("latam", "br", "tw") else {"latam": "ES", "br": "PT", "tw": "ZH"}[cur["path"]],
            html.escape(val("lang.label")), "\n".join(items),
        )

        redirect = ""
        if code == "en":
            redirect = (
                "    <script>\n"
                "      // First visit only: send visitors to their language. A choice made in the switcher is remembered.\n"
                "      (function () {\n"
                "        try {\n"
                "          if (document.documentElement.getAttribute(\"data-embed\") === \"1\") return;\n"
                "          var saved = localStorage.getItem(\"ol-lang\");\n"
                "          var map = %s;\n"
                "          var pick = function (tag) {\n"
                "            tag = String(tag || \"\").toLowerCase();\n"
                "            if (map[tag]) return map[tag];\n"
                "            var base = tag.split(\"-\")[0];\n"
                "            if (base === \"zh\") return /-(tw|hk|mo|hant)/.test(tag) ? map[\"zh-tw\"] : map.zh;\n"
                "            if (base === \"pt\") return /-br/.test(tag) ? map[\"pt-br\"] : map.pt;\n"
                "            if (base === \"es\") return tag === \"es\" || /-es/.test(tag) ? map.es : map[\"es-419\"];\n"
                "            if (base === \"nb\" || base === \"nn\") return map.no;\n"
                "            if (base === \"fil\") return map.tl;\n"
                "            return map[base];\n"
                "          };\n"
                "          var target = saved ? pick(saved) : null;\n"
                "          if (!saved) {\n"
                "            var langs = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language];\n"
                "            for (var i = 0; i < langs.length && !target; i++) target = pick(langs[i]);\n"
                "          }\n"
                "          if (target && target !== \"/\") location.replace(target + location.search + location.hash);\n"
                "        } catch (e) {}\n"
                "      })();\n"
                "    </script>"
            ) % json.dumps(redirect_map, separators=(",", ":"))

        special = {
            "@htmlLang": code, "@canonical": canonical, "@alternates": alternates, "@ogLocale": loc["og"],
            "@ogAlternates": og_alts, "@jsonld": jsonld, "@v": str(version), "@redirect": redirect,
            "@home": "/" + loc["path"] + "/" if loc["path"] else "/", "@switcher": switcher, "@lang": code,
        }

        def sub(m):
            key, _, arg = m.group(1).partition("|")
            if key in special:
                return special[key]
            if key not in d:
                raise KeyError("template key %s missing in en.json" % key)
            v = val(key, arg or None)
            return v if key.endswith("Html") else html.escape(v, quote=True)

        out = re.sub(r"\{\{([@\w.|-]+)\}\}", sub, tpl)
        out = re.sub(r"\n\s*\n(\s*<link rel=\"preconnect\")", r"\n\1", out)
        dest = os.path.join(ROOT, loc["path"], "index.html") if loc["path"] else os.path.join(ROOT, "index.html")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(out)

        os.makedirs(os.path.join(ROOT, "i18n"), exist_ok=True)
        runtime = {k: v for k, v in d.items() if not k.startswith(("faq.", "rules.", "nf.")) and k not in ("meta.title", "meta.description", "meta.ogTitle", "meta.ogDescription", "meta.ogImageAlt")}
        with open(os.path.join(ROOT, "i18n", code + ".js"), "w", encoding="utf-8") as f:
            f.write("// Generated by scripts/build_i18n.py from scripts/i18n/. Do not edit by hand.\n")
            f.write("window.OL_I18N = " + json.dumps({"lang": code, "dict": runtime}, ensure_ascii=False, separators=(",", ":")) + ";\n")

    # 404 page: picks the language from the URL prefix, the saved choice, then the browser.
    nf = {l["code"]: {k: dicts[l["code"]][k] for k in ("nf.title", "nf.h1", "nf.p", "nf.btn")} for l in locales}
    paths = {l["path"]: l["code"] for l in locales if l["path"]}
    home = {l["code"]: ("/" + l["path"] + "/" if l["path"] else "/") for l in locales}
    page404 = open(os.path.join(I18N, "404.template.html"), encoding="utf-8").read()
    page404 = page404.replace("{{@nf}}", json.dumps(nf, ensure_ascii=False, separators=(",", ":")))
    page404 = page404.replace("{{@paths}}", json.dumps(paths, separators=(",", ":")))
    page404 = page404.replace("{{@home}}", json.dumps(home, separators=(",", ":")))
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
        f.write(page404)

    today = datetime.date.today().isoformat()
    urls = []
    for loc in locales:
        alts = "\n".join(
            '    <xhtml:link rel="alternate" hreflang="%s" href="%s" />' % (l["code"], url_for(l)) for l in locales
        ) + '\n    <xhtml:link rel="alternate" hreflang="x-default" href="%s/" />' % SITE
        urls.append(
            "  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>monthly</changefreq>\n"
            "    <priority>%s</priority>\n%s\n    <image:image><image:loc>%s/og.png</image:loc></image:image>\n  </url>"
            % (url_for(loc), today, "1.0" if loc["code"] == "en" else "0.8", alts, SITE)
        )
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                'xmlns:xhtml="http://www.w3.org/1999/xhtml" '
                'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
                + "\n".join(urls) + "\n</urlset>\n")
    print("Built %d locales (%s devices, %s brands), v=%s" % (len(locales), stats["total"], stats["brands"], version))
    return 1 if missing else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", default="24")
    sys.exit(build(ap.parse_args().version))
