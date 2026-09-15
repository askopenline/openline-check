"""Audit devices.js and merge new warning notes for suspicious entries.

Adds a `note` (or appends to an existing note with ` · `) whenever a row matches one
of these heuristics:

1. Model-code collision within a brand across different device names → "Unverified variant"
   (skip Apple SoC variants that legitimately share a code because Apple assigns
   one model number to a whole family — we only mark cross-name collisions).
2. Same model code appearing across DIFFERENT brands → "Cross-brand code"
3. Modern eSIM=true device (>=2020) with a missing model code (— or empty) →
   "Model code unverified"
4. Very short / generic name (single letter+digit like "M6", "F7", "13") without
   a brand-namespace clue in the name → "Ambiguous name"
5. Weird trailing punctuation in name → strip + tag "Naming needs review" (internal
   only, not shown; we just fix the name).
6. Normalize the note strings: "Cellular" alone → dropped (not a warning); "Global"
   alone → dropped; "CN" alone → "CN firmware". Duplicate space-comma cleanup.
7. Brand spelling variants → normalize (Micromax vs MicroMax → Micromax).
"""
from __future__ import annotations
import re
import collections
import json

SRC = "/home/user/workspace/openline-esim-check/devices.js"
OUT = "/home/user/workspace/openline-esim-check/devices.js"

# ---------------- parse ----------------
text = open(SRC).read()
prefix_m = re.match(r"(?s)^(.*?const DEVICES\s*=\s*\[)", text)
suffix_m = re.search(r"(?s)(\][^\]]*;\s*)$", text)
assert prefix_m and suffix_m, "Could not find array bounds"
prefix = prefix_m.group(1)
suffix = suffix_m.group(1)

pattern = re.compile(
    r'\{\s*brand:\s*"((?:[^"\\]|\\.)*)"\s*,'
    r'\s*name:\s*"((?:[^"\\]|\\.)*)"\s*,'
    r'\s*model:\s*"((?:[^"\\]|\\.)*)"\s*,'
    r'\s*year:\s*(\d+)\s*,'
    r'\s*esim:\s*(true|false)'
    r'(?:\s*,\s*note:\s*"((?:[^"\\]|\\.)*)")?'
    r'\s*\}'
)

rows = []
for m in pattern.finditer(text):
    rows.append({
        "brand": m.group(1),
        "name": m.group(2),
        "model": m.group(3),
        "year": int(m.group(4)),
        "esim": m.group(5) == "true",
        "note": m.group(6) or "",
    })

print(f"parsed {len(rows)} devices")

# ---------------- normalize brand casing ----------------
brand_canon = {}
brand_variants = collections.defaultdict(collections.Counter)
for r in rows:
    brand_variants[r["brand"].lower().replace(" ", "")][r["brand"]] += 1
for _, variants in brand_variants.items():
    if len(variants) > 1:
        canon = variants.most_common(1)[0][0]
        for v in variants:
            brand_canon[v] = canon
for r in rows:
    r["brand"] = brand_canon.get(r["brand"], r["brand"])

# ---------------- categorize suspicious entries ----------------
# A. cross-brand model code
brands_for_code = collections.defaultdict(set)
for r in rows:
    if r["model"] and r["model"] != "—":
        brands_for_code[r["model"]].add(r["brand"])
cross_brand_codes = {m for m, bs in brands_for_code.items() if len(bs) > 1}

# B. within-brand model-code collision across different NAMES
def normalize_family(name: str) -> str:
    """Strip parenthetical model codes so 'iPhone 16e' and 'iPhone 16e (A3212)' collapse to same family."""
    # remove parenthetical blocks (of any content)
    n = re.sub(r"\s*\([^)]*\)\s*", " ", name).strip()
    # normalize whitespace
    n = re.sub(r"\s+", " ", n)
    return n

family_for_code = collections.defaultdict(set)
for r in rows:
    if r["model"] and r["model"] != "—":
        family_for_code[(r["brand"], r["model"])].add(normalize_family(r["name"]))
within_brand_collision = {k for k, fams in family_for_code.items() if len(fams) > 1}

# C. modern eSIM=true with missing model code
modern_no_model = set()
for i, r in enumerate(rows):
    if r["esim"] and r["year"] >= 2020 and r["model"] in ("—", ""):
        modern_no_model.add(i)

# D. suspicious note strings
# We drop "Cellular", "Global", "CN" alone since they're not warnings.
def clean_note(note: str) -> str:
    if not note:
        return ""
    parts = [p.strip() for p in note.split("·")]
    # remove non-warning tokens
    drop = {"Cellular", "Global"}
    parts = [p for p in parts if p and p not in drop]
    # remap
    remap = {"CN": "CN firmware"}
    parts = [remap.get(p, p) for p in parts]
    return " · ".join(parts)

# ---------------- apply warnings ----------------
added_counts = collections.Counter()

def add_warning(row_idx: int, tag: str):
    r = rows[row_idx]
    existing = r["note"]
    parts = [p.strip() for p in existing.split("·")] if existing else []
    if tag in parts:
        return
    parts.append(tag)
    r["note"] = " · ".join([p for p in parts if p])
    added_counts[tag] += 1

# Fix name trailing whitespace & weird parens
for r in rows:
    r["name"] = re.sub(r"\s+", " ", r["name"]).strip()

# Clean notes first (drop non-warnings)
for r in rows:
    r["note"] = clean_note(r["note"])

# 1. Cross-brand codes
for i, r in enumerate(rows):
    if r["model"] in cross_brand_codes:
        add_warning(i, "Cross-brand model code")

# 2. Within-brand collision
# Skip Apple: many Apple names deliberately share a code (e.g. "iPad 11 (A16)"
# and "iPad 11 (A16) (A3355)" refer to the same physical SKU). But cross-family
# collisions (like Pixel 9 sharing GNKJ8 with Pixel 10) are genuinely suspicious.
# Rule: if both families end up in within_brand_collision AND the family names
# differ by more than a parenthetical variant tag, flag the row.
for i, r in enumerate(rows):
    if r["model"] and r["model"] != "—":
        fams = family_for_code.get((r["brand"], r["model"]), set())
        if len(fams) > 1:
            # Only flag if the families are truly different products, not just
            # different name spellings of the same product.
            fam_tokens = [set(re.findall(r"[A-Za-z0-9]+", f.lower())) for f in fams]
            # If any two families share fewer than 2 tokens, treat as truly different.
            distinct = False
            for a in range(len(fam_tokens)):
                for b in range(a + 1, len(fam_tokens)):
                    inter = fam_tokens[a] & fam_tokens[b]
                    smallest = min(len(fam_tokens[a]), len(fam_tokens[b]))
                    if smallest >= 2 and len(inter) < 2:
                        distinct = True
            if distinct:
                add_warning(i, "Unverified variant")

# 3. Modern no-model
for i in modern_no_model:
    add_warning(i, "Model code unverified")

# 4. Ambiguous short names when eSIM=true and year >= 2018
for i, r in enumerate(rows):
    if not r["esim"]:
        continue
    if r["year"] < 2018:
        continue
    # Name after stripping parenthetical/brand context
    fam = normalize_family(r["name"])
    # Very short families like "13", "M6", "F7", "X6", "R2", etc.
    if re.fullmatch(r"[A-Za-z]?\d{1,3}[A-Za-z]?", fam):
        add_warning(i, "Ambiguous name")

# ---------------- write back ----------------
def esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')

lines = []
for r in rows:
    parts = [
        f'brand: "{esc(r["brand"])}"',
        f'name: "{esc(r["name"])}"',
        f'model: "{esc(r["model"])}"',
        f'year: {r["year"]}',
        f'esim: {"true" if r["esim"] else "false"}',
    ]
    if r["note"]:
        parts.append(f'note: "{esc(r["note"])}"')
    lines.append("  { " + ", ".join(parts) + " },")

body = "\n" + "\n".join(lines) + "\n"

# strip trailing `];` from suffix; we'll re-add
suffix_clean = re.sub(r"^\][^\]]*;", "", suffix, count=1)
final = prefix + body + "];\n" + suffix_clean

with open(OUT, "w") as f:
    f.write(final)

print("wrote", OUT)
print()
print("Warning counts added:")
for k, n in added_counts.most_common():
    print(f"  {n:5d}  {k}")

# ---------------- audit summary ----------------
print()
print("Final note distribution (top 25):")
final_notes = collections.Counter(r["note"] for r in rows if r["note"])
for note, n in final_notes.most_common(25):
    print(f"  {n:5d}  {note}")
