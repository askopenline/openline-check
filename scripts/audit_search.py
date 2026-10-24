#!/usr/bin/env python3
"""
Audit real-user search queries against the JS logic (reimplemented in Python).
Runs a fixed corpus of representative queries and prints top-5 hits per query
so we can eyeball whether ranking is right.
"""
import json
import re
import unicodedata

# Load devices from generated JS
raw = open("devices.js").read()
# Pull each { brand: "...", name: "...", model: "...", year: N, esim: true|false, note?: "..." }
DEVICES = []
for m in re.finditer(r"\{\s*brand:\s*\"([^\"]*)\",\s*name:\s*\"([^\"]*)\",\s*model:\s*\"([^\"]*)\",\s*year:\s*(\d+),\s*esim:\s*(true|false)(?:,\s*note:\s*\"([^\"]*)\")?\s*\}", raw):
    DEVICES.append({
        "brand": m.group(1),
        "name": m.group(2),
        "model": m.group(3),
        "year": int(m.group(4)),
        "esim": m.group(5) == "true",
        "note": m.group(6),
    })

def normalize(s):
    s = unicodedata.normalize("NFKD", s or "").lower()
    s = re.sub(r"[\u0300-\u036f]", "", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return s.strip()

def is_variant(name):
    return bool(re.search(r"\(\s*[A-Z]{2,}[\-\dA-Z]+\s*\)", name or ""))

def is_tablet(name):
    return bool(re.search(r"\btab(let)?\b|\bipad\b|\bmatepad\b|\bmi ?pad\b", name or "", re.IGNORECASE))

def is_watch(name):
    return bool(re.search(r"\bwatch\b", name or "", re.IGNORECASE))

INDEX = []
for d in DEVICES:
    hay = normalize(f"{d['brand']} {d['name']} {d['model']} {d['year']} {d.get('note') or ''}")
    name_raw = d.get('name') or ''
    INDEX.append({
        "d": d,
        "hay": hay,
        "name_norm": normalize(name_raw),
        "words": set(hay.split()),
        "is_variant": is_variant(name_raw),
        "is_tablet": is_tablet(name_raw),
        "is_watch": is_watch(name_raw),
        "has_plus": ("+" in name_raw) or bool(re.search(r"\bplus\b", name_raw, re.IGNORECASE)),
    })

# Aliases (same as JS)
ALIASES = [
    (r"^iphon(e|es)?$", "iphone"),
    (r"^(ipone|ifone|iphne|iphoen|ihpone|iphoene|iphine|iphon)$", "iphone"),
    (r"^aiphone$", "iphone"),
    (r"^ipad(s)?$", "ipad"),
    (r"^apll?e$", "apple"),
    (r"^applewatch$", "apple watch"),
    (r"^(sams?ung|samsng|samsug|smsung|samsun|samsong|shamsung|sansung)$", "samsung"),
    (r"^(gala?xy|glaxy|galxy|gallaxy|galsxy|galsy)$", "galaxy"),
    (r"^gs(\d+)$", r"galaxy s\1"),
    (r"^s(\d+)(ultra|plus|fe|edge|\+)?$", r"galaxy s\1 \2"),
    (r"^note(\d+)$", r"galaxy note \1"),
    (r"^flip(\d+)$", r"samsung galaxy z flip\1"),
    (r"^fold(\d+)$", r"samsung galaxy z fold\1"),
    (r"^zflip(\d+)?$", r"samsung galaxy z flip\1"),
    (r"^zfold(\d+)?$", r"samsung galaxy z fold\1"),
    (r"^(googl|goolge|gogle|goole|gogl|googlee|gooogle|gogel)$", "google"),
    (r"^(pixl|pxel|pixell|pixle|pxil)$", "pixel"),
    (r"^(xaomi|xioami|xiami|xiomi|xiaom|xami|xiaomii|xiaomy|shiaomi)$", "xiaomi"),
    (r"^(redm|readmi|redmy|redmi)$", "redmi"),
    (r"^(huwaei|huawe|huawi|hawai|huaweii|huwei|hawei)$", "huawei"),
    (r"^(honr|hnor|honnor)$", "honor"),
    (r"^(moto|motrola|motorla|motorolla|moturola|motrolla)$", "motorola"),
    (r"^razr(\d+)$", r"razr \1"),
    (r"^(oneplus|1plus|1\+)$", "oneplus"),
    (r"^(sony|soni)$", "sony"),
    (r"^xperia$", "xperia"),
    (r"^(nokia|noki|nokya)$", "nokia"),
    (r"^hmd$", "hmd"),
    (r"^(realm|realme|realmi)$", "realme"),
    (r"^(oppo|oppp)$", "oppo"),
    (r"^(vivo|vivvo)$", "vivo"),
    (r"^(iqoo|iqqoo|iqo)$", "iqoo"),
    (r"^(poco|pooco)$", "poco"),
    (r"^(nothing|nothng)$", "nothing"),
    (r"^fairphone$", "fairphone"),
    (r"^(rakuten|rakten)$", "rakuten"),
    (r"^(nighthwk|nighthawk)$", "nighthawk"),
    (r"^(netgar|netger|netgear)$", "netgear"),
    (r"^watch$", "watch"),
    (r"^tablet$", "tab"),
    (r"^tab$", "tab"),
    (r"^hotspot$", "hotspot"),
]

KNOWN_PREFIXES = sorted([
    "iphone", "ipad", "applewatch", "apple", "macbook",
    "samsung", "galaxy", "note", "fold", "flip", "zfold", "zflip", "xcover",
    "pixel", "google",
    "xiaomi", "redmi", "poco",
    "huawei", "honor",
    "nokia", "hmd", "skyline",
    "motorola", "moto", "razr", "edge", "thinkphone",
    "oneplus", "nord",
    "sony", "xperia",
    "oppo", "vivo", "iqoo", "realme", "narzo",
    "nothing", "fairphone", "rakuten",
    "nighthawk", "netgear", "solis", "glocalme", "inseego", "franklin",
    "kindle", "fitbit", "garmin", "amazfit", "mobvoi", "ticwatch",
    "tesla", "surface", "lenovo", "asus", "zenfone", "rog",
    "pro", "ultra", "plus", "max", "mini", "lite", "fe", "neo", "active",
], key=len, reverse=True)

def split_smooshed(t):
    if len(t) < 5: return [t]
    if " " in t: return [t]
    if t.lower() in KNOWN_PREFIXES: return [t]  # never split a whole known word (oneplus)
    if not re.search(r'\d', t):
        lt = t.lower()
        for p in KNOWN_PREFIXES:
            if len(p) >= 6 and edit_distance(lt, p, 2) <= 2: return [t]
    remaining = t.lower()
    extracted = []
    guard = 0
    while remaining and guard < 10:
        guard += 1
        matched = False
        for p in KNOWN_PREFIXES:
            if remaining.startswith(p) and len(p) < len(remaining):
                extracted.append(p)
                remaining = remaining[len(p):]
                matched = True
                break
        if not matched:
            break
    rest = re.sub(r"([a-z])(\d)", r"\1 \2", remaining, flags=re.IGNORECASE)
    rest = re.sub(r"(\d)([a-z])", r"\1 \2", rest, flags=re.IGNORECASE)
    for p in KNOWN_PREFIXES:
        if len(p) < 4: continue
        rest = re.sub(r"(\S)(" + p + r")", r"\1 \2", rest, flags=re.IGNORECASE)
    rest_parts = rest.split()
    parts = extracted + rest_parts
    return parts if len(parts) > 1 else [t]

MEANINGFUL_PREFIXES = set("s m a f e p g j c k v y".split())

def expand_tokens(tokens):
    pre = []
    for t in tokens:
        pre.extend(split_smooshed(t))
    # Coalesce single-letter + digit
    coalesced = []
    i = 0
    while i < len(pre):
        if i + 1 < len(pre) and pre[i] in MEANINGFUL_PREFIXES and re.fullmatch(r"\d+", pre[i+1]):
            coalesced.append(pre[i] + pre[i+1])
            i += 2
        else:
            coalesced.append(pre[i])
            i += 1
    out = []
    for t in coalesced:
        replaced = None
        for pat, repl in ALIASES:
            if re.fullmatch(pat, t, flags=re.IGNORECASE):
                replaced = re.sub(pat, repl, t, flags=re.IGNORECASE).strip()
                break
        if replaced:
            out.extend(replaced.split())
        else:
            out.append(t)
    compact = []
    for i, tok in enumerate(out):
        compact.append(tok)
        if i + 1 < len(out) and re.fullmatch(r"flip|fold", tok, re.IGNORECASE) and re.fullmatch(r"\d+", out[i+1]):
            compact.append(tok + out[i+1])
    compound_digits = set()
    for t in compact:
        m = re.fullmatch(r"(flip|fold)(\d+)", t, re.IGNORECASE)
        if m: compound_digits.add(m.group(2))
    filtered = compact
    if compound_digits:
        filtered = [t for t in compact
                    if not re.fullmatch(r"flip|fold", t, re.IGNORECASE)
                    and t not in compound_digits]
    filtered = [t for t in filtered if t != "z"]
    seen = set(); result = []
    for t in filtered:
        if t not in seen:
            seen.add(t); result.append(t)
    return result

# Damerau-Levenshtein
def edit_distance(a, b, mx):
    if a == b: return 0
    la, lb = len(a), len(b)
    if abs(la - lb) > mx: return mx + 1
    if la == 0: return lb
    if lb == 0: return la
    prev2 = list(range(lb + 1))
    prev = list(range(lb + 1))
    curr = [0] * (lb + 1)
    for i in range(1, la + 1):
        curr[0] = i
        row_min = curr[0]
        for j in range(1, lb + 1):
            cost = 0 if a[i-1] == b[j-1] else 1
            curr[j] = min(
                prev[j] + 1,
                curr[j-1] + 1,
                prev[j-1] + cost,
            )
            if i > 1 and j > 1 and a[i-1] == b[j-2] and a[i-2] == b[j-1]:
                curr[j] = min(curr[j], prev2[j-2] + 1)
            if curr[j] < row_min:
                row_min = curr[j]
        if row_min > mx: return mx + 1
        prev2 = prev[:]
        prev = curr[:]
    return prev[lb]

def fuzzy_match(needle, hay):
    if not needle: return True
    if needle in hay: return True
    if len(needle) < 3: return False
    # Prefix match
    if len(needle) >= 3:
        for w in hay.split():
            if w.startswith(needle) and len(w) - len(needle) <= 6:
                return True
    if len(needle) < 4: return False
    mx = 1 if len(needle) <= 5 else (2 if len(needle) <= 8 else 3)
    for w in hay.split(" "):
        if not w: continue
        if abs(len(w) - len(needle)) > mx + 1: continue
        if edit_distance(needle, w, mx) <= mx:
            return True
    return False

def search(raw_query):
    tokens = expand_tokens(re.sub(r'\bone plus\b', 'oneplus', normalize(raw_query)).split())
    matches = INDEX
    used_fuzzy = False
    if tokens:
        is_num = lambda t: bool(re.fullmatch(r"\d+", t))
        is_alpha = lambda t: bool(re.fullmatch(r"[a-z]+", t, re.IGNORECASE))
        num_tokens = [t for t in tokens if is_num(t)]
        other_tokens = [t for t in tokens if not is_num(t)]
        alpha_tokens = [t for t in tokens if is_alpha(t)]
        pure_numeric_only = not other_tokens and all(len(t) >= 4 for t in num_tokens)
        looks_like_model_code = (
            any(len(t) >= 3 for t in num_tokens)
            and any(2 <= len(t) <= 4 for t in alpha_tokens)
        )
        def token_matches(t, hay, words):
            if is_num(t):
                if t in words: return True
                if looks_like_model_code: return t in hay
                return False
            return t in hay
        exact = [m for m in matches if all(token_matches(t, m["hay"], m["words"]) for t in tokens)]
        if pure_numeric_only and len(exact) > 200:
            matches = []
        elif exact:
            matches = exact
        else:
            used_fuzzy = True
            matches = [m for m in matches if all(
                token_matches(t, m["hay"], m["words"]) if is_num(t) else fuzzy_match(t, m["hay"])
                for t in tokens
            )]
            if not matches and len(tokens) >= 2:
                weak = {"plus", "max"}
                primary = [t for t in tokens if t not in weak]
                if len(primary) < len(tokens) and len(primary) >= 1:
                    matches = [m for m in INDEX if all(
                        token_matches(t, m["hay"], m["words"]) if is_num(t) else t in m["hay"]
                        for t in primary
                    )]
    # Query heuristics
    phone_regex = re.compile(r"^(iphone|galaxy|pixel|xiaomi|honor|huawei|oneplus|motorola|razr|edge|nokia|sony|xperia|realme|oppo|vivo|redmi|poco|nothing|fairphone|zenfone|rog|rakuten)$")
    query_phone = any(
        phone_regex.match(t) or re.fullmatch(r"s\d+|note\d+|fold\d+|flip\d+|p\d+|mate|razr", t)
        for t in tokens
    )
    query_tablet = any(re.fullmatch(r"ipad|tab|tablet|matepad|pad", t) for t in tokens)
    query_watch = any(t == "watch" for t in tokens)
    query_has_plus = any(t == "plus" for t in tokens) or ("+" in raw_query)
    bigrams = [f"{tokens[i]} {tokens[i+1]}" for i in range(len(tokens)-1)]

    def score(entry):
        d = entry["d"]; hay = entry["hay"]; name_norm = entry["name_norm"]
        brand_n = normalize(d["brand"])
        name_n = normalize(d["name"])
        model_n = normalize(d.get("model") or "")
        name_words = set(name_n.split())
        s = 0
        for t in tokens:
            if brand_n == t: s += 100
            elif name_n == t: s += 90
            elif t in name_words: s += 80
            elif brand_n.startswith(t): s += 60
            elif name_n.startswith(t): s += 55
            elif model_n.startswith(t): s += 50
            elif t in brand_n: s += 30
            elif t in name_n: s += 25
            elif t in model_n: s += 12
            elif t in hay: s += 10
            else: s += 3
        for bg in bigrams:
            if bg in name_norm: s += 50
        if query_has_plus:
            if entry["has_plus"]: s += 45
            else: s -= 15
        if entry["is_variant"]:
            s -= 15
        if query_phone and not query_tablet and not query_watch:
            if entry["is_tablet"]: s -= 40
            if entry["is_watch"]: s -= 40
        s += (d["year"] - 2000) * 0.1
        return s
    matches = sorted(matches, key=lambda e: (-score(e), 0 if e["d"]["esim"] else 1, -e["d"]["year"]))
    return matches[:5], tokens, used_fuzzy


QUERIES = [
    # Browser-audit failures we must fix
    "ifone 16",
    "gogl pixel 9",
    "iphone15pro",
    "galaxys25ultra",
    "pixelwatch3",
    "zflip6",
    "zfold5",
    "applewatchultra",
    "ipadpromax",
    "s10",
    "s10+",
    "xiaomi 12 pro",
    "note 10 plus",
    "12345",
    # Sanity from browser audit (should not regress)
    "iphone 15",
    "galaxy s24",
    "pixel 8",
    "samsong s24",
    "galxy s24 ultra",
    "xiaomii 14 ultra",
    "moturola razr",
    "motorolla edge 50",
    "huaweii mate 60",
    "honr magic v3",
    "pxel 8 pro",
    "pxel watch",
    "s25 ultra",
    "note20",
    "fold6",
    "flip5",
    "z fold 7",
    "z flip 7",
    "SM-S928B",
    "SM-F946U",
    "A2483",
    "TA-1450",
    "CPH2653",
    "nighthawk m6 pro",
    "solis 5g",
    "glocalme",
    "tesla model 3",
    "surface pro",
    "iphone 6",
    "iphone 7 plus",
    "galaxy note 8",
    "s20 fe",
    "redmi note 13",
    "ihpone",
    "shamsung",
    "gooogle",
    "asdlkfj",
    "xxxxx",
]

for q in QUERIES:
    hits, tokens, fuzzy = search(q)
    marker = " (fuzzy)" if fuzzy else ""
    print(f"\n▶ '{q}'  → tokens={tokens}{marker}")
    if not hits:
        print("   (no results)")
    for i, m in enumerate(hits, 1):
        d = m["d"]
        badge = "✓ eSIM" if d["esim"] else "✗ no eSIM"
        note = f" [{d['note']}]" if d.get("note") else ""
        print(f"   {i}. {d['brand']} {d['name']} ({d['year']}) — {badge}{note}")
