(function () {
  "use strict";

  // ---------- i18n ----------
  // Each page loads /i18n/<lang>.js before this file, which sets
  // window.OL_I18N = { lang, dict }. English is the source (i18n/en.json).
  const I18N = window.OL_I18N || { lang: "en", dict: {} };
  const LANG = I18N.lang || "en";
  const DICT = I18N.dict || {};
  const PLURAL = (() => {
    try { return new Intl.PluralRules(LANG); } catch (e) { return new Intl.PluralRules("en"); }
  })();
  const NUM = (() => {
    try { return new Intl.NumberFormat(LANG, { numberingSystem: "latn" }); } catch (e) { return new Intl.NumberFormat("en"); }
  })();
  function fmt(n) { return NUM.format(n); }
  function has(key) { return Object.prototype.hasOwnProperty.call(DICT, key); }
  function fill(str, vars) {
    return String(str).replace(/\{(\w+)\}/g, (m, k) => (vars && k in vars ? vars[k] : m));
  }
  function t(key, vars) {
    const v = has(key) ? DICT[key] : key;
    return fill(typeof v === "object" ? (v.other || "") : v, vars);
  }
  function tn(key, n, vars) {
    const v = DICT[key];
    const all = Object.assign({ n: fmt(n) }, vars || {});
    if (!v || typeof v !== "object") return fill(v || key, all);
    const cat = PLURAL.select(n);
    return fill(v[cat] != null ? v[cat] : v.other, all);
  }
  function listFormat(parts) {
    try {
      return new Intl.ListFormat(LANG, { style: "long", type: "disjunction" }).format(parts);
    } catch (e) {
      return parts.join(", ");
    }
  }
  // Device notes are short English labels joined with " · ".
  // Translate each label; the raw English note still drives the explanation lookup.
  function noteLabel(note) {
    return String(note)
      .split(" · ")
      .map((p) => (has("note." + p) ? DICT["note." + p] : p))
      .join(" · ");
  }

  const $q = document.getElementById("q");
  const $clear = document.getElementById("clear");
  const $list = document.getElementById("list");
  const $count = document.getElementById("results-count");
  const $title = document.getElementById("results-title");
  const $empty = document.getElementById("empty");
  const $emptyTitle = document.getElementById("empty-title");
  const $emptyBody = document.getElementById("empty-body");
  const $emptyActions = document.getElementById("empty-actions");
  const $footerTotal = document.getElementById("footer-total");

  const $filtersToggle = document.getElementById("filters-toggle");
  const $filtersPanel = document.getElementById("filters-panel");
  const $filtersSummary = document.getElementById("filters-summary");
  const $filtersBadge = document.getElementById("filters-count-badge");
  const $filtersClear = document.getElementById("filters-clear");
  const $filtersCountSummary = document.getElementById("filters-count-summary");
  const $compatCats = document.getElementById("compat-cats");
  const $brandCats = document.getElementById("brand-cats");
  const $statTotal = document.getElementById("stat-total");
  const $statYes = document.getElementById("stat-yes");
  const $statNo = document.getElementById("stat-no");
  const $statBrands = document.getElementById("stat-brands");

  // Selected filters
  const selectedCompat = new Set(); // {"yes", "no"}
  const selectedBrands = new Set(); // brand names

  // ---------- helpers ----------
  function normalize(s) {
    return (s || "")
      .toLowerCase()
      .normalize("NFKD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/[^a-z0-9]+/g, " ")
      .trim();
  }

  // ---------- Query expansion ----------
  // Brand aliases & common typos — map any input token to a canonical form.
  // Ordered from most‑specific to most‑general.
  const ALIASES = [
    // Apple family
    [/^iphon(e|es)?$/i, "iphone"],
    [/^(ipone|ifone|iphne|iphoen|ihpone|iphoene|iphine|iphon)$/i, "iphone"],
    [/^aiphone$/i, "iphone"],
    [/^ipad(s)?$/i, "ipad"],
    [/^apll?e$/i, "apple"],
    [/^applewatch$/i, "apple watch"],
    [/^watch\s*ultra$/i, "watch ultra"],
    // Samsung family
    [/^(sams?ung|samsng|samsug|smsung|samsun|samsong|shamsung|sansung)$/i, "samsung"],
    [/^(gala?xy|glaxy|galxy|gallaxy|galsxy|galsy)$/i, "galaxy"],
    [/^gs(\d+)$/i, "galaxy s$1"],
    [/^s(\d+)(ultra|plus|fe|edge|\+)?$/i, "galaxy s$1 $2"],
    [/^note(\d+)$/i, "galaxy note $1"],
    // Foldable canonical expansions — always emit 'samsung' + brand context to outrank Nubia/Pixel Fold
    [/^flip(\d+)$/i, "samsung galaxy z flip$1"],
    [/^fold(\d+)$/i, "samsung galaxy z fold$1"],
    [/^zflip(\d+)?$/i, "samsung galaxy z flip$1"],
    [/^zfold(\d+)?$/i, "samsung galaxy z fold$1"],
    // Google
    [/^(googl|goolge|gogle|goole|gogl|googlee|gooogle|gogel)$/i, "google"],
    [/^(pixl|pxel|pixell|pixle|pxil)$/i, "pixel"],
    // Xiaomi
    [/^(xaomi|xioami|xiami|xiomi|xiaom|xami|xiaomii|xiaomy|shiaomi)$/i, "xiaomi"],
    [/^(redm|readmi|redmy|redmi)$/i, "redmi"],
    // Huawei / Honor
    [/^(huwaei|huawe|huawi|hawai|huaweii|huwei|hawei)$/i, "huawei"],
    [/^(honr|hnor|honnor)$/i, "honor"],
    // Motorola
    [/^(moto|motrola|motorla|motorolla|moturola|motrolla|motorolla)$/i, "motorola"],
    [/^razr(\d+)$/i, "razr $1"],
    // OnePlus
    [/^(oneplus|1plus|1\+)$/i, "oneplus"],
    // Sony
    [/^(sony|soni)$/i, "sony"],
    [/^xperia$/i, "xperia"],
    // Nokia
    [/^(nokia|noki|nokya)$/i, "nokia"],
    // HMD
    [/^hmd$/i, "hmd"],
    // Realme, Oppo, Vivo, iQOO, POCO
    [/^(realm|realme|realmi)$/i, "realme"],
    [/^(oppo|oppp)$/i, "oppo"],
    [/^(vivo|vivvo)$/i, "vivo"],
    [/^(iqoo|iqqoo|iqo)$/i, "iqoo"],
    [/^(poco|pooco)$/i, "poco"],
    // Nothing / Fairphone / Rakuten
    [/^(nothing|nothng)$/i, "nothing"],
    [/^fairphone$/i, "fairphone"],
    [/^(rakuten|rakten)$/i, "rakuten"],
    // Hotspots
    [/^(nighthwk|nighthawk)$/i, "nighthawk"],
    [/^(netgar|netger|netgear)$/i, "netgear"],
    // Common casual synonyms
    [/^watch$/i, "watch"],
    [/^tablet$/i, "tab"],
    [/^tab$/i, "tab"],
    [/^hotspot$/i, "hotspot"],
  ];

  // Known product prefixes for smooshed-input splitting (e.g. 'iphone15pro' → 'iphone 15 pro')
  // Emitted in longest-first order so 'galaxy' beats 'ga', etc.
  const KNOWN_PREFIXES = [
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
  ].sort((a, b) => b.length - a.length);

  // Split 'iphone15pro' → ['iphone', '15', 'pro'] by finding known prefixes + digit boundaries.
  // Two-pass: first extract all known prefixes greedily, then handle letter↔digit boundaries.
  function splitSmooshed(t) {
    if (t.length < 5) return [t];
    if (t.includes(" ")) return [t];
    // A whole known word ('oneplus', 'zenfone', 'thinkphone') must never be split.
    if (KNOWN_PREFIXES.includes(t.toLowerCase())) return [t];
    // A misspelled known word ('motorolla', 'samsnug') must reach fuzzy matching whole.
    if (!/\d/.test(t)) {
      const lt = t.toLowerCase();
      for (const p of KNOWN_PREFIXES) {
        if (p.length >= 6 && editDistance(lt, p, 2) <= 2) return [t];
      }
    }
    // Pass 1: greedily extract known prefixes from the front and body of the token.
    // Repeat until no more prefixes are found or the token is exhausted.
    let remaining = t.toLowerCase();
    const extracted = [];
    let guard = 0;
    while (remaining.length > 0 && guard++ < 10) {
      let matched = false;
      for (const p of KNOWN_PREFIXES) {
        if (remaining.startsWith(p) && p.length < remaining.length) {
          extracted.push(p);
          remaining = remaining.slice(p.length);
          matched = true;
          break;
        }
        // Also match prefix anywhere — e.g. 'galaxys25ultra': after we peel 'galaxy',
        // the leftover 's25ultra' starts with 's' but 's' is not a prefix.
        // Handle digit-boundary insertion instead.
      }
      if (!matched) break;
    }
    // Pass 2: on whatever remains (or the whole token if no prefix matched), insert
    // spaces at letter↔digit boundaries so 's25ultra' → 's 25 ultra'.
    let rest = remaining
      .replace(/([a-z])(\d)/gi, "$1 $2")
      .replace(/(\d)([a-z])/gi, "$1 $2");
    // Also insert space before any known prefix that appears mid-word in `rest`.
    for (const p of KNOWN_PREFIXES) {
      if (p.length < 4) continue;
      const re = new RegExp("(\\S)(" + p + ")", "gi");
      rest = rest.replace(re, "$1 $2");
    }
    const restParts = rest.split(/\s+/).filter(Boolean);
    const parts = [...extracted, ...restParts];
    return parts.length > 1 ? parts : [t];
  }

  function expandTokens(tokens) {
    // First pass: split smooshed tokens like 'iphone15pro' or 'galaxys25ultra'
    let pre = [];
    for (const t of tokens) pre.push(...splitSmooshed(t));
    // Second pass: coalesce '<letter> <digit>' back into '<letter><digit>' for letters
    // that are meaningful only as prefixes ('s' + '25' → 's25').
    const meaningfulPrefixes = new Set(["s", "m", "a", "f", "e", "p", "g", "j", "c", "k", "v", "y"]);
    const coalesced = [];
    for (let i = 0; i < pre.length; i++) {
      if (i + 1 < pre.length && meaningfulPrefixes.has(pre[i]) && /^\d+$/.test(pre[i + 1])) {
        coalesced.push(pre[i] + pre[i + 1]);
        i++;
      } else {
        coalesced.push(pre[i]);
      }
    }
    // Third pass: apply aliases (REPLACE, not append — so 'zflip6' becomes
    // ['samsung','galaxy','z','flip6'] cleanly)
    const out = [];
    for (const t of coalesced) {
      let replaced = null;
      for (const [re, repl] of ALIASES) {
        if (re.test(t)) { replaced = t.replace(re, repl).trim(); break; }
      }
      if (replaced) out.push(...replaced.split(/\s+/).filter(Boolean));
      else out.push(t);
    }
    // Fourth pass: compound-adjacent (flip 6 → also add 'flip6' variant)
    const compact = [];
    for (let i = 0; i < out.length; i++) {
      compact.push(out[i]);
      if (i + 1 < out.length && /^(flip|fold)$/i.test(out[i]) && /^\d+$/.test(out[i + 1])) {
        compact.push(out[i] + out[i + 1]);
      }
    }
    // Filter out standalone 'flip'/'fold' and the trailing digit when a compound 'flipN'/'foldN' exists
    const compoundDigits = new Set();
    for (const t of compact) {
      const m = t.match(/^(flip|fold)(\d+)$/i);
      if (m) compoundDigits.add(m[2]);
    }
    let filtered = compact;
    if (compoundDigits.size > 0) {
      filtered = compact.filter((t) => {
        if (/^(flip|fold)$/i.test(t)) return false;
        if (compoundDigits.has(t)) return false; // drop bare '6' when we already have 'flip6'
        return true;
      });
    }
    // Also filter out standalone 'z' (Samsung foldable naming) — too weak to require
    filtered = filtered.filter((t) => t !== "z");
    // Dedupe while preserving order
    return [...new Set(filtered)];
  }

  // ---------- Fuzzy matching (Damerau–Levenshtein) ----------
  // Returns edit distance up to `max`; short-circuits if exceeded.
  function editDistance(a, b, max) {
    if (a === b) return 0;
    const la = a.length, lb = b.length;
    if (Math.abs(la - lb) > max) return max + 1;
    if (la === 0) return lb;
    if (lb === 0) return la;
    let prev2 = new Array(lb + 1);
    let prev = new Array(lb + 1);
    let curr = new Array(lb + 1);
    for (let j = 0; j <= lb; j++) prev[j] = j;
    for (let i = 1; i <= la; i++) {
      curr[0] = i;
      let rowMin = curr[0];
      for (let j = 1; j <= lb; j++) {
        const cost = a[i - 1] === b[j - 1] ? 0 : 1;
        curr[j] = Math.min(
          prev[j] + 1,        // deletion
          curr[j - 1] + 1,    // insertion
          prev[j - 1] + cost, // substitution
        );
        // transposition (Damerau)
        if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) {
          curr[j] = Math.min(curr[j], prev2[j - 2] + 1);
        }
        if (curr[j] < rowMin) rowMin = curr[j];
      }
      if (rowMin > max) return max + 1;
      prev2 = prev.slice();
      prev = curr.slice();
    }
    return prev[lb];
  }

  // Threshold: 1 edit for short tokens (≤5 chars), 2 for 6-8 chars, 3 for longer.
  function fuzzyMatch(needle, hay) {
    if (!needle) return true;
    if (hay.includes(needle)) return true;
    if (needle.length < 3) return false; // too short for safe fuzz
    // Also try prefix match — 'cph' should match 'cph2653'
    if (needle.length >= 3) {
      const words = hay.split(" ");
      for (const w of words) {
        if (w.startsWith(needle) && w.length - needle.length <= 6) return true;
      }
    }
    if (needle.length < 4) return false;
    const max = needle.length <= 5 ? 1 : (needle.length <= 8 ? 2 : 3);
    // Slide over hay tokens
    const words = hay.split(" ");
    for (const w of words) {
      if (!w) continue;
      if (Math.abs(w.length - needle.length) > max + 1) continue;
      if (editDistance(needle, w, max) <= max) return true;
    }
    return false;
  }
  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])
    );
  }
  function highlight(text, tokens) {
    const raw = String(text);
    const list = (tokens || []).filter((t) => t && t.length >= 2);
    if (!list.length) return escapeHtml(raw);
    // Collect match ranges on the raw text, then merge them, so markup is
    // never matched by a later token and entities are never split.
    const lower = raw.toLowerCase();
    const ranges = [];
    for (const t of list) {
      const n = t.toLowerCase();
      let i = lower.indexOf(n);
      while (i !== -1) {
        ranges.push([i, i + n.length]);
        i = lower.indexOf(n, i + 1);
      }
    }
    if (!ranges.length) return escapeHtml(raw);
    ranges.sort((a, b) => a[0] - b[0] || b[1] - a[1]);
    const merged = [ranges[0].slice()];
    for (const r of ranges.slice(1)) {
      const last = merged[merged.length - 1];
      if (r[0] <= last[1]) last[1] = Math.max(last[1], r[1]);
      else merged.push(r.slice());
    }
    let out = "";
    let pos = 0;
    for (const [a, b] of merged) {
      out += escapeHtml(raw.slice(pos, a)) + "<mark>" + escapeHtml(raw.slice(a, b)) + "</mark>";
      pos = b;
    }
    return out + escapeHtml(raw.slice(pos));
  }

  // Detect which notes are regional caveats (open in a popover) vs plain info.
  const REGIONAL_PATTERNS = [
    /excluded/i,
    /\bUS: eSIM only\b/i,
    /\bmost regions\b/i,
    /HarmonyOS/i,
    /dual[- ]eSIM only/i,
    /EU carrier/i,
    /Verizon/i,
    /Google Fi/i,
    /CN[- ]only/i,
    /CN\/HK\/KR excluded/i,
    /region[- ]locked/i,
    /grey[- ]market/i,
    /JP domestic/i,
    /activation may fail/i,
    /KR only/i,
    /Foldable/i,
    /Mobile hotspot/i,
    /CDMA/i,
    /iDEN/i,
    /Windows Phone/i,
    /KaiOS/i,
    /3G\/4G · sunset/i,
    /3G free · deprecated/i,
    /No eSIM in most regions/i,
    /Vehicle telematics/i,
    /GPS\/satellite tracker/i,
    /Medical alert/i,
    /Enterprise rugged/i,
    /US carrier variant/i,
    /SIM tray only/i,
    /Wi-Fi only/i,
    /Wi-Fi \+ Cellular only/i,
    /Cellular · eSIM only/i,
    /Cellular · 3G\/4G/i,
    /Cellular · HarmonyOS/i,
    /E-reader/i,
    /Unverified variant/i,
    /Cross-brand model code/i,
    /Model code unverified/i,
    /Ambiguous name/i,
    /CN firmware/i,
    /no SIM tray/i,
    /eSIM only in US\/JP\/CA\/Gulf/i,
    /dual nano-SIM/i,
    /CN: local eSIM rules/i,
    /Carrier watch plan/i,
    /GPS only/i,
  ];
  function isRegionalNote(note) {
    return REGIONAL_PATTERNS.some((re) => re.test(note));
  }
  function regionalExplanation(note) {
    // Order matters — most specific first.
    if (/Carrier watch plan/i.test(note)) {
      return t("exp.carrierWatch");
    }
    if (/GPS only/i.test(note)) {
      return t("exp.gpsOnly");
    }
    if (/CN\/HK\/MO: dual nano-SIM/i.test(note)) {
      return t("exp.cnHkMoDualNano");
    }
    if (/CN: dual nano-SIM/i.test(note)) {
      return t("exp.cnDualNano");
    }
    if (/CN: local eSIM rules/i.test(note)) {
      return t("exp.cnLocalRules");
    }
    if (/eSIM only in US\/JP\/CA\/Gulf/i.test(note)) {
      return t("exp.esimOnlyUsJpCaGulf");
    }
    if (/no SIM tray/i.test(note)) {
      return t("exp.noSimTray");
    }
    if (/iDEN/i.test(note)) {
      return t("exp.iden");
    }
    if (/CDMA · Verizon/i.test(note)) {
      return t("exp.cdmaVerizon");
    }
    if (/CDMA · Sprint/i.test(note)) {
      return t("exp.cdmaSprint");
    }
    if (/3G\/4G · sunset|3G free · deprecated|No eSIM in most regions/i.test(note)) {
      return t("exp.sunset");
    }
    if (/Windows Phone/i.test(note)) {
      return t("exp.windowsPhone");
    }
    if (/KaiOS/i.test(note)) {
      return t("exp.kaios");
    }
    if (/Vehicle telematics/i.test(note)) {
      return t("exp.telematics");
    }
    if (/GPS\/satellite tracker/i.test(note)) {
      return t("exp.satellite");
    }
    if (/Medical alert/i.test(note)) {
      return t("exp.medical");
    }
    if (/Enterprise rugged/i.test(note)) {
      return t("exp.rugged");
    }
    if (/HarmonyOS/i.test(note)) {
      return t("exp.harmony");
    }
    if (/dual[- ]eSIM only/i.test(note)) {
      return t("exp.dualEsimOnly");
    }
    if (/EU carrier/i.test(note)) {
      return t("exp.euCarrier");
    }
    if (/US carrier variant/i.test(note)) {
      return t("exp.usCarrier");
    }
    if (/Verizon/i.test(note)) {
      return t("exp.verizon");
    }
    if (/Google Fi/i.test(note)) {
      return t("exp.googleFi");
    }
    if (/US: eSIM only/i.test(note)) {
      return t("exp.usEsimOnly");
    }
    if (/CN[- ]only|activation may fail abroad|CN\/HK\/KR excluded/i.test(note)) {
      return t("exp.cnOnly");
    }
    if (/JP domestic|Rakuten/i.test(note)) {
      return t("exp.jpDomestic");
    }
    if (/region[- ]locked/i.test(note)) {
      return t("exp.regionLocked");
    }
    if (/KR only/i.test(note)) {
      return t("exp.krOnly");
    }
    if (/Foldable/i.test(note)) {
      return t("exp.foldable");
    }
    if (/Mobile hotspot/i.test(note)) {
      return t("exp.hotspot");
    }
    if (/SIM tray only/i.test(note)) {
      return t("exp.simTrayOnly");
    }
    if (/Wi-Fi \+ Cellular only|Wi-Fi only/i.test(note)) {
      return t("exp.wifiOnly");
    }
    if (/E-reader/i.test(note)) {
      return t("exp.ereader");
    }
    if (/Cellular · eSIM only/i.test(note)) {
      return t("exp.cellularEsimOnly");
    }
    if (/Unverified variant/i.test(note)) {
      return t("exp.unverifiedVariant");
    }
    if (/Cross-brand model code/i.test(note)) {
      return t("exp.crossBrand");
    }
    if (/Model code unverified/i.test(note)) {
      return t("exp.modelUnverified");
    }
    if (/Ambiguous name/i.test(note)) {
      return t("exp.ambiguous");
    }
    if (/CN firmware/i.test(note)) {
      return t("exp.cnFirmware");
    }
    // Fallback — "excluded" pattern
    const raw = note.replace(/\s+excluded/i, "").trim();
    const parts = raw.split("/").map((p) => {
      const code = p.trim();
      const k = "region." + code;
      return has(k) ? t(k) : code;
    });
    return t("exp.regionExcluded", { regions: listFormat(parts) });
  }

  // Pre-index
  const INDEX = DEVICES.map((d) => {
    const hay = normalize([d.brand, d.name, d.model, String(d.year), d.note || ""].join(" "));
    const nameNorm = normalize(d.name || "");
    return {
      d,
      hay,
      nameNorm,
      words: new Set(hay.split(" ").filter(Boolean)),
      isVariant: /\(\s*[A-Z]{2,}[\-\dA-Z]+\s*\)/.test(d.name || ""),
      isTablet: /\btab(let)?\b|\bipad\b|\bmatepad\b|\bmi ?pad\b/i.test(d.name || ""),
      isWatch: /\bwatch\b/i.test(d.name || ""),
      // Plus/+ flag — does the name literally end in '+' or contain 'plus'?
      hasPlus: /\+/.test(d.name || "") || /\bplus\b/i.test(d.name || ""),
    };
  });

  // Brand counts (for filter labels)
  const BRAND_COUNTS = {};
  for (const d of DEVICES) BRAND_COUNTS[d.brand] = (BRAND_COUNTS[d.brand] || 0) + 1;
  const BRANDS = Object.keys(BRAND_COUNTS).sort((a, b) => BRAND_COUNTS[b] - BRAND_COUNTS[a] || a.localeCompare(b));

  const COMPAT_COUNTS = {
    yes: DEVICES.filter((d) => d.esim).length,
    no: DEVICES.filter((d) => !d.esim).length,
  };

  // ---------- Build filter UIs ----------
  function catButton({ value, name, count, group }) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "cat-btn";
    btn.dataset.value = value;
    btn.dataset.group = group;
    btn.setAttribute("aria-pressed", "false");
    btn.innerHTML = `
      <span class="cat-name">${escapeHtml(name)}</span>
      <span class="cat-count">${escapeHtml(tn("cat.count", count))}</span>
    `;
    btn.addEventListener("click", () => {
      const set = group === "compat" ? selectedCompat : selectedBrands;
      if (set.has(value)) set.delete(value); else set.add(value);
      btn.classList.toggle("active");
      btn.setAttribute("aria-pressed", set.has(value) ? "true" : "false");
      render();
    });
    return btn;
  }

  $compatCats.appendChild(catButton({ value: "yes", name: t("status.ok"), count: COMPAT_COUNTS.yes, group: "compat" }));
  $compatCats.appendChild(catButton({ value: "no", name: t("status.no"), count: COMPAT_COUNTS.no, group: "compat" }));

  for (const b of BRANDS) {
    $brandCats.appendChild(catButton({ value: b, name: b, count: BRAND_COUNTS[b], group: "brand" }));
  }

  // ---------- Filter toggle (collapsible) ----------
  $filtersToggle.addEventListener("click", () => {
    const open = $filtersToggle.getAttribute("aria-expanded") === "true";
    $filtersToggle.setAttribute("aria-expanded", open ? "false" : "true");
    $filtersPanel.hidden = open;
  });

  $filtersClear.addEventListener("click", () => {
    selectedCompat.clear();
    selectedBrands.clear();
    document.querySelectorAll(".cat-btn.active").forEach((el) => {
      el.classList.remove("active");
      el.setAttribute("aria-pressed", "false");
    });
    render();
  });

  // ---------- Search ----------
  $q.addEventListener("input", render);
  $clear.addEventListener("click", () => {
    $q.value = "";
    $q.focus();
    render();
  });

  // ---------- Render ----------
  function render() {
    const rawQuery = $q.value.trim();
    const query = normalize(rawQuery).replace(/\bone plus\b/g, "oneplus");
    const rawTokens = query.split(" ").filter(Boolean);
    const tokens = expandTokens(rawTokens);
    $clear.hidden = rawQuery.length === 0;

    // Apply filters + fuzzy tokens (two-pass: exact-substring first, then fuzzy fallback)
    let matches = INDEX;
    let usedFuzzy = false;
    if (tokens.length) {
      // Numeric-only tokens ($\d+$) must match a word inside hay OR appear inside a
      // hay word that also contains an alpha prefix from another query token (so 'CPH' + '2653'
      // matches 'cph2653', but bare '12345' only matches word-boundary '12345').
      const isNumericOnly = (t) => /^\d+$/.test(t);
      const isAlphaOnly = (t) => /^[a-z]+$/i.test(t);
      const numTokens = tokens.filter(isNumericOnly);
      const otherTokens = tokens.filter((t) => !isNumericOnly(t));
      const alphaTokens = tokens.filter(isAlphaOnly);
      const pureNumericOnly = otherTokens.length === 0 && numTokens.every((t) => t.length >= 4);
      // Model-code detection: query has BOTH alpha and numeric tokens where numeric is 3+ digits.
      // In that case, allow numeric tokens to match anywhere in hay (compound with alpha prefix).
      const looksLikeModelCode = numTokens.some((t) => t.length >= 3) &&
                                  alphaTokens.some((t) => t.length >= 2 && t.length <= 4);
      function tokenMatchesHay(t, hay, wordSet) {
        if (isNumericOnly(t)) {
          if (wordSet.has(t)) return true;
          if (looksLikeModelCode) return hay.includes(t);
          return false;
        }
        return hay.includes(t);
      }
      const exact = matches.filter(({ hay, words }) =>
        tokens.every((t) => tokenMatchesHay(t, hay, words))
      );
      if (pureNumericOnly && exact.length > 200) {
        matches = [];
      } else if (exact.length > 0) {
        matches = exact;
      } else {
        // Fallback: fuzzy match — non-numeric tokens fuzzy-match somewhere in hay;
        // numeric tokens use the same relaxed model-code rule.
        usedFuzzy = true;
        matches = matches.filter(({ hay, words }) =>
          tokens.every((t) => isNumericOnly(t) ? tokenMatchesHay(t, hay, words) : fuzzyMatch(t, hay))
        );
        // If still empty AND we have 3+ tokens, try dropping the weakest (single-char or 'plus'/'max')
        // to handle 'note 10 plus' (no such device — real name is 'Note 10+') and 'ipad pro max'.
        if (matches.length === 0 && tokens.length >= 2) {
          // Only these modifiers get dropped — they're commonly appended even when not real product names
          const droppableModifiers = new Set(["plus", "max"]);
          const primaryTokens = tokens.filter((t) => !droppableModifiers.has(t));
          if (primaryTokens.length < tokens.length && primaryTokens.length >= 1) {
            matches = INDEX.filter(({ hay, words }) =>
              primaryTokens.every((t) => isNumericOnly(t) ? tokenMatchesHay(t, hay, words) : hay.includes(t))
            );
          }
        }
      }
    }
    if (selectedCompat.size) {
      matches = matches.filter(({ d }) => selectedCompat.has(d.esim ? "yes" : "no"));
    }
    if (selectedBrands.size) {
      matches = matches.filter(({ d }) => selectedBrands.has(d.brand));
    }

    // Sort by relevance score, then compat-yes first, then newest
    if (tokens.length) {
      const brandNorms = new Map();
      for (const { d, hay } of matches) {
        if (!brandNorms.has(d.brand)) brandNorms.set(d.brand, normalize(d.brand));
      }
      const nameNorms = new Map();
      for (const { d } of matches) {
        const key = d.brand + "\0" + d.name;
        if (!nameNorms.has(key)) nameNorms.set(key, normalize(d.name));
      }
      const modelNorms = new Map();
      for (const { d } of matches) {
        const key = d.brand + "\0" + d.model;
        if (!modelNorms.has(key)) modelNorms.set(key, normalize(d.model || ""));
      }

      // Detect if the query looks like it's for a phone (has 'phone'/'iphone'/etc, or plain single-letter+digit like 's10')
      const queryLooksPhone = tokens.some((t) =>
        /^(iphone|galaxy|pixel|xiaomi|honor|huawei|oneplus|motorola|razr|edge|nokia|sony|xperia|realme|oppo|vivo|redmi|poco|nothing|fairphone|zenfone|rog|rakuten)$/.test(t) ||
        /^s\d+$/.test(t) || /^note\d+$/.test(t) || /^fold\d+$/.test(t) || /^flip\d+$/.test(t) ||
        /^razr$/.test(t) || /^mate$/.test(t) || /^p\d+$/.test(t)
      );
      const queryLooksTablet = tokens.some((t) => /^(ipad|tab|tablet|matepad|pad)$/.test(t));
      const queryLooksWatch = tokens.some((t) => /^watch$/.test(t));
      // Query has a Plus/+ qualifier?
      const queryHasPlus = tokens.some((t) => t === "plus") || /\+/.test(rawQuery);
      // Build the bigram list (adjacent token pairs from the original raw query, expanded)
      // Used to boost entries whose name contains the token sequence contiguously.
      const bigrams = [];
      for (let i = 0; i < tokens.length - 1; i++) {
        // skip artificial tokens (all-uppercase-single-char or numeric-word bigram is meaningless)
        if (tokens[i].length < 1 || tokens[i + 1].length < 1) continue;
        bigrams.push(tokens[i] + " " + tokens[i + 1]);
      }

      function score(entry) {
        const { d, hay, nameNorm, isVariant, isTablet, isWatch, hasPlus } = entry;
        const brandN = brandNorms.get(d.brand);
        const nameN = nameNorms.get(d.brand + "\0" + d.name);
        const modelN = modelNorms.get(d.brand + "\0" + d.model);
        const nameWords = new Set(nameN.split(" ").filter(Boolean));
        let s = 0;
        for (const t of tokens) {
          if (brandN === t) s += 100;
          else if (nameN === t) s += 90;
          else if (nameWords.has(t)) s += 80;
          else if (brandN.startsWith(t)) s += 60;
          else if (nameN.startsWith(t)) s += 55;
          else if (modelN.startsWith(t)) s += 50;
          else if (brandN.includes(t)) s += 30;
          else if (nameN.includes(t)) s += 25;
          else if (modelN.includes(t)) s += 12;
          else if (hay.includes(t)) s += 10;
          else s += 3;
        }
        // BIGRAM BONUS: boost entries whose name contains the query token pair contiguously
        // (fixes 'xiaomi 12 pro' → prefer 'Xiaomi 12 Pro' over 'Pad 6S Pro 12.4' since
        // '12 pro' appears as a phrase only in the phone)
        for (const bg of bigrams) {
          if (nameNorm.includes(bg)) s += 50;
        }
        // PLUS BOOST: strongly prefer entries with '+' in the name when query has 'plus'
        if (queryHasPlus) {
          if (hasPlus) s += 45;
          else s -= 15;
        }
        if (isVariant) s -= 15;
        if (queryLooksPhone && !queryLooksTablet && !queryLooksWatch) {
          if (isTablet) s -= 40;
          if (isWatch) s -= 40;
        }
        s += (d.year - 2000) * 0.1;
        return s;
      }
      matches.sort((a, b) => {
        const dif = score(b) - score(a);
        if (dif !== 0) return dif;
        if (a.d.esim !== b.d.esim) return a.d.esim ? -1 : 1;
        return b.d.year - a.d.year;
      });
    }

    const MAX = 500;
    const visible = matches.slice(0, MAX);

    if (matches.length === 0) {
      $list.innerHTML = "";
      $list.hidden = true;
      $empty.hidden = false;
      renderEmpty(tokens, rawQuery);
    } else {
      $empty.hidden = true;
      $list.hidden = false;
      $list.innerHTML = visible
        .map(({ d }) => {
          const cls = d.esim ? "ok" : "err";
          const status = d.esim ? t("status.ok") : t("status.no");
          const nameHtml = highlight(`${d.brand} ${d.name}`, tokens);
          const modelHtml = highlight(d.model, tokens);
          let note = "";
          if (d.note) {
            if (isRegionalNote(d.note)) {
              note = `<button type="button" class="note-warn" data-note="${escapeHtml(d.note)}" aria-label="${escapeHtml(t("note.caveatAria", { note: noteLabel(d.note) }))}">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 9v4"/><path d="M12 17h.01"/><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/></svg>
                <span>${escapeHtml(noteLabel(d.note))}</span>
              </button>`;
            } else {
              note = `<span class="note">${escapeHtml(noteLabel(d.note))}</span>`;
            }
          }
          return `
            <li class="row ${cls}">
              <span class="indicator" aria-hidden="true"></span>
              <div class="meta">
                <div class="name">${nameHtml}</div>
                <div class="sub">
                  <span class="code">${modelHtml}</span>
                  <span>${d.year}</span>
                  ${note}
                </div>
              </div>
              <span class="badge" aria-label="${escapeHtml(d.esim ? t("status.okAria") : t("status.noAria"))}">${status}</span>
            </li>
          `;
        })
        .join("");
    }

    // Counts, title & summary
    const total = DEVICES.length;
    if ($footerTotal) $footerTotal.textContent = fmt(total);

    const active = tokens.length || selectedCompat.size || selectedBrands.size;
    if (active) {
      $title.textContent = t("results.matching");
      const shownN = Math.min(matches.length, MAX);
      const suffix = matches.length > MAX ? t("results.showingFirst", { max: fmt(MAX) }) : "";
      $count.innerHTML = t("results.ofTotalHtml", { n: fmt(matches.length), total: fmt(total) }) + escapeHtml(suffix);
    } else {
      $title.textContent = t("results.all");
      $count.innerHTML = t("results.totalHtml", { n: fmt(total) });
    }

    // Summary in filter bar
    const bits = [];
    if (selectedCompat.size === 1) bits.push(selectedCompat.has("yes") ? t("filters.compatOnly") : t("filters.notCompatOnly"));
    else if (selectedCompat.size === 2) bits.push(t("filters.allStatuses"));
    if (selectedBrands.size) {
      const list = Array.from(selectedBrands);
      bits.push(list.length <= 2 ? list.join(", ") : tn("filters.nBrands", list.length));
    }
    $filtersSummary.textContent = bits.length ? bits.join(" · ") : t("filters.summaryAll");

    // Active-filter badge next to the Filters label
    const activeFilters = selectedCompat.size + selectedBrands.size;
    if (activeFilters > 0) {
      $filtersBadge.textContent = activeFilters;
      $filtersBadge.hidden = false;
    } else {
      $filtersBadge.hidden = true;
    }

    // Panel footer summary
    if (active) {
      $filtersCountSummary.innerHTML = tn("filters.matchHtml", matches.length);
    } else {
      $filtersCountSummary.innerHTML = "";
    }

    // Enable/disable clear
    $filtersClear.disabled = selectedCompat.size === 0 && selectedBrands.size === 0;
  }

  // ---------- Empty-state helper ----------
  function renderEmpty(tokens, rawQuery) {
    const hasSearch = tokens.length > 0;
    const hasFilters = selectedCompat.size + selectedBrands.size > 0;

    // Would-the-search-alone-work check: run it without filters
    let matchesSansFilters = 0;
    if (hasSearch && hasFilters) {
      // Reuse the same two-pass logic as render()
      const isNumericOnly = (t) => /^\d+$/.test(t);
      const exact = INDEX.filter(({ hay, words }) =>
        tokens.every((t) => isNumericOnly(t) ? words.has(t) : hay.includes(t))
      );
      matchesSansFilters = exact.length > 0
        ? exact.length
        : INDEX.filter(({ hay, words }) =>
            tokens.every((t) => isNumericOnly(t) ? words.has(t) : fuzzyMatch(t, hay))
          ).length;
    }

    // Case A: search + filters, and clearing filters would surface matches
    if (hasSearch && hasFilters && matchesSansFilters > 0) {
      $emptyTitle.textContent = t("empty.bothTitle");
      $emptyBody.innerHTML = tn("empty.bothBodyHtml", matchesSansFilters, { q: escapeHtml(rawQuery) });
      $emptyActions.hidden = false;
      $emptyActions.querySelector('[data-action="reset-filters"]').hidden = false;
      $emptyActions.querySelector('[data-action="clear-search"]').hidden = false;
      return;
    }

    // Case B: only filters set, no results
    if (!hasSearch && hasFilters) {
      $emptyTitle.textContent = t("empty.filtersTitle");
      $emptyBody.innerHTML = escapeHtml(t("empty.filtersBody"));
      $emptyActions.hidden = false;
      $emptyActions.querySelector('[data-action="reset-filters"]').hidden = false;
      $emptyActions.querySelector('[data-action="clear-search"]').hidden = true;
      return;
    }

    // Case C: only search, no results
    if (hasSearch && !hasFilters) {
      $emptyTitle.textContent = t("empty.noMatchTitle");
      $emptyBody.innerHTML = t("empty.noMatchBodyHtml");
      $emptyActions.hidden = false;
      $emptyActions.querySelector('[data-action="reset-filters"]').hidden = true;
      $emptyActions.querySelector('[data-action="clear-search"]').hidden = false;
      return;
    }

    // Case D: unlikely fallback (no search, no filters, but empty)
    $emptyTitle.textContent = t("empty.nothing");
    $emptyBody.textContent = "";
    $emptyActions.hidden = true;
  }

  // ---------- Regional-note popover ----------
  let $popover = null;
  function closePopover() {
    if ($popover) {
      $popover.remove();
      $popover = null;
    }
    document.removeEventListener("click", onDocClickForPopover, true);
    document.removeEventListener("keydown", onKeyForPopover);
    window.removeEventListener("scroll", closePopover, true);
    window.removeEventListener("resize", closePopover);
  }
  function onDocClickForPopover(e) {
    if (!$popover) return;
    if ($popover.contains(e.target)) return;
    if (e.target.closest(".note-warn")) return;
    closePopover();
  }
  function onKeyForPopover(e) {
    if (e.key === "Escape") closePopover();
  }
  function openPopover(anchor, note) {
    closePopover();
    const explanation = regionalExplanation(note);
    const pop = document.createElement("div");
    pop.className = "note-popover";
    pop.setAttribute("role", "dialog");
    pop.setAttribute("aria-label", t("popover.aria"));
    pop.innerHTML = `
      <div class="note-popover-head">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 9v4"/><path d="M12 17h.01"/><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/></svg>
        <strong>${escapeHtml(noteLabel(note))}</strong>
        <button type="button" class="note-popover-close" aria-label="${escapeHtml(t("popover.close"))}">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 6L6 18M6 6l12 12"/></svg>
        </button>
      </div>
      <p>${escapeHtml(explanation)}</p>
    `;
    document.body.appendChild(pop);

    // Position: center on the anchor, below it, but flip up if not enough room.
    // Re-measure after each style write so we always work with the popover's
    // real final size (CSS max-width may shrink it below the initial rect on
    // narrow viewports).
    const ar = anchor.getBoundingClientRect();
    const vw = window.innerWidth;
    const vh = window.innerHeight;
    const margin = 8;  // gap between popover and viewport edge on very narrow screens
    let pr = pop.getBoundingClientRect();
    let popW = pr.width;
    let popH = pr.height;
    // If popover is too wide for viewport minus margins, cap it and remeasure
    if (popW > vw - margin * 2) {
      pop.style.maxWidth = (vw - margin * 2) + "px";
      pr = pop.getBoundingClientRect();
      popW = pr.width;
      popH = pr.height;
    }
    let top = ar.bottom + 8;
    let left = ar.left + ar.width / 2 - popW / 2;
    // Clamp horizontally with symmetric margins
    if (left < margin) left = margin;
    if (left + popW > vw - margin) left = Math.max(margin, vw - margin - popW);
    // Flip vertically if needed
    if (top + popH > vh - margin) top = Math.max(margin, ar.top - popH - 8);
    pop.style.top = top + "px";
    pop.style.left = left + "px";

    $popover = pop;
    pop.querySelector(".note-popover-close").addEventListener("click", closePopover);
    // Attach listeners with a slight delay so the opening click doesn't immediately close
    setTimeout(() => {
      document.addEventListener("click", onDocClickForPopover, true);
      document.addEventListener("keydown", onKeyForPopover);
      window.addEventListener("scroll", closePopover, true);
      window.addEventListener("resize", closePopover);
    }, 0);
  }
  // Delegate clicks on any .note-warn button (list re-renders often)
  $list.addEventListener("click", (e) => {
    const btn = e.target.closest(".note-warn");
    if (!btn) return;
    e.preventDefault();
    e.stopPropagation();
    openPopover(btn, btn.dataset.note);
  });

  // Wire up empty-state action buttons
  $emptyActions.addEventListener("click", (e) => {
    const btn = e.target.closest("button[data-action]");
    if (!btn) return;
    if (btn.dataset.action === "reset-filters") {
      selectedCompat.clear();
      selectedBrands.clear();
      document.querySelectorAll(".cat-btn.active").forEach((el) => {
        el.classList.remove("active");
        el.setAttribute("aria-pressed", "false");
      });
    } else if (btn.dataset.action === "clear-search") {
      $q.value = "";
    }
    render();
    $q.focus();
  });

  // ---------- Initial stats ----------
  $statTotal.textContent = fmt(DEVICES.length);
  $statYes.textContent = fmt(COMPAT_COUNTS.yes);
  $statNo.textContent = fmt(COMPAT_COUNTS.no);
  $statBrands.textContent = fmt(BRANDS.length);

  // ---------- Shareable search links (?q=pixel+9) ----------
  const BASE_TITLE = document.title;
  try {
    const initial = new URLSearchParams(location.search).get("q");
    if (initial) $q.value = initial.slice(0, 80);
  } catch (e) {}
  let urlTimer = null;
  function syncUrl() {
    clearTimeout(urlTimer);
    urlTimer = setTimeout(() => {
      try {
        const q = $q.value.trim();
        const params = new URLSearchParams(location.search);
        if (q) params.set("q", q); else params.delete("q");
        const qs = params.toString();
        history.replaceState(null, "", location.pathname + (qs ? "?" + qs : "") + location.hash);
        document.title = q ? t("meta.searchTitle", { q: q }) : BASE_TITLE;
      } catch (e) {}
    }, 350);
  }
  $q.addEventListener("input", syncUrl);
  $q.addEventListener("search", syncUrl);
  document.addEventListener("click", (e) => {
    if (e.target.closest("#clear, button[data-action='clear-search']")) syncUrl();
  });

  // ---------- Language switcher ----------
  const $lang = document.getElementById("lang");
  if ($lang) {
    const $btn = $lang.querySelector(".lang-btn");
    const $menu = $lang.querySelector(".lang-menu");
    const setOpen = (open) => {
      $btn.setAttribute("aria-expanded", open ? "true" : "false");
      $menu.hidden = !open;
      if (open) {
        const cur = $menu.querySelector('[aria-current="true"]') || $menu.querySelector("a");
        if (cur) cur.focus();
      }
    };
    $btn.addEventListener("click", (e) => {
      e.stopPropagation();
      setOpen($menu.hidden);
    });
    document.addEventListener("click", (e) => {
      if (!$menu.hidden && !$lang.contains(e.target)) setOpen(false);
    });
    $lang.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && !$menu.hidden) {
        setOpen(false);
        $btn.focus();
      }
      if ((e.key === "ArrowDown" || e.key === "ArrowUp") && !$menu.hidden) {
        e.preventDefault();
        const items = Array.from($menu.querySelectorAll("a"));
        const i = items.indexOf(document.activeElement);
        const next = e.key === "ArrowDown" ? Math.min(items.length - 1, i + 1) : Math.max(0, i - 1);
        items[next].focus();
      }
    });
    $menu.addEventListener("click", (e) => {
      const a = e.target.closest("a[data-lang]");
      if (!a) return;
      try { localStorage.setItem("ol-lang", a.dataset.lang); } catch (err) {}
      const params = new URLSearchParams(location.search);
      const q = $q.value.trim();
      if (q) params.set("q", q); else params.delete("q");
      const qs = params.toString();
      if (qs) {
        e.preventDefault();
        location.href = a.getAttribute("href") + "?" + qs;
      }
    });
  }

  render();
  if ($q.value) syncUrl();
})();
