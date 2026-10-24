(function () {
  "use strict";

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
    let out = escapeHtml(text);
    if (!tokens.length) return out;
    const sorted = tokens.slice().sort((a, b) => b.length - a.length).filter((t) => t.length >= 2);
    for (const t of sorted) {
      const re = new RegExp("(" + t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "gi");
      out = out.replace(re, "<mark>$1</mark>");
    }
    return out;
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
      return "Cellular smartwatches get their eSIM through a carrier watch plan, set up from the paired phone’s companion app (Apple Watch app, Galaxy Wearable, Pixel Watch app). Phone or travel eSIM QR codes can’t be installed on the watch directly, so check that your carrier offers a plan for this watch.";
    }
    if (/GPS only/i.test(note)) {
      return "This is the GPS-only version. It has no cellular radio, so it can’t use any eSIM. The GPS + Cellular version of the same watch has a different model number.";
    }
    if (/CN\/HK\/MO: dual nano-SIM/i.test(note)) {
      return "iPhones sold in mainland China, Hong Kong and Macao for this generation have two physical nano-SIM slots and no eSIM. Openline can’t install on these units. Check the model number under Settings › General › About.";
    }
    if (/CN: dual nano-SIM/i.test(note)) {
      return "The mainland China version of this phone uses two physical nano-SIM cards and has no eSIM. Models sold everywhere else support eSIM. Check the model number under Settings › General › About.";
    }
    if (/CN: local eSIM rules/i.test(note)) {
      return "The mainland China version supports eSIM, but Chinese carriers only activate eSIM in their stores with ID checks, and overseas eSIM profiles can’t be installed while you’re in mainland China. Outside China, travel eSIMs such as Openline install normally.";
    }
    if (/eSIM only in US\/JP\/CA\/Gulf/i.test(note)) {
      return "Units sold in the United States, Canada, Japan, Mexico and the Gulf states have no SIM tray and work with eSIM only. Elsewhere the phone also has a nano-SIM tray, and mainland China units may lack eSIM. Openline works on every eSIM-capable version.";
    }
    if (/no SIM tray/i.test(note)) {
      return "This version has no physical SIM tray: every line, including Openline, is added as an eSIM. You can store several eSIMs and switch between them in Settings.";
    }
    if (/iDEN/i.test(note)) {
      return "This device runs on Motorola’s iDEN network (Nextel / Boost push-to-talk), which was fully decommissioned by Sprint in June 2013. It cannot connect to any modern cellular network — eSIM or otherwise. Museum/collector item only.";
    }
    if (/CDMA · Verizon/i.test(note)) {
      return "This is a CDMA-only device built for Verizon’s legacy 2G/3G CDMA network, which was shut down on December 31, 2022. It has no SIM slot at all (physical or eSIM) — CDMA authenticates on the network via the device’s ESN/MEID, not a SIM. It cannot be used with Openline or any modern carrier.";
    }
    if (/CDMA · Sprint/i.test(note)) {
      return "This is a CDMA device built for Sprint’s legacy network, which T-Mobile shut down permanently on May 31, 2022. Newer Sprint models added LTE/GSM but earlier ones are CDMA-only and cannot connect to any modern network — with or without eSIM.";
    }
    if (/3G\/4G · sunset|3G free · deprecated|No eSIM in most regions/i.test(note)) {
      return "This device relies on 3G or older 4G networks that carriers have shut down (AT&T 3G ended February 2022, T-Mobile February 2022, Verizon December 2022, most European 3G by 2025). Even if it has a working SIM slot, there’s no network for it to connect to in most countries.";
    }
    if (/Windows Phone/i.test(note)) {
      return "This runs Windows Phone (or Windows 10 Mobile), which Microsoft discontinued in 2019 — the Store, security patches, and most first-party services are all shut down. It has no eSIM hardware and virtually no modern app support. Unusable as a daily driver.";
    }
    if (/KaiOS/i.test(note)) {
      return "This is a KaiOS feature phone. Almost no KaiOS device supports eSIM — they use a physical SIM (usually a nano-SIM) and are targeted at cheap 4G-only feature-phone markets like India (JioPhone) and Africa. Openline cannot install here.";
    }
    if (/Vehicle telematics/i.test(note)) {
      return "This is a vehicle telematics module (Tesla, BMW, Audi, etc.) with a factory-embedded eSIM soldered onto the car’s connectivity board. The eSIM is provisioned by the automaker at the factory and cannot be swapped for a user-installed profile like Openline. Not user-serviceable.";
    }
    if (/GPS\/satellite tracker/i.test(note)) {
      return "This is a satellite/GPS communicator (Garmin inReach, SPOT, Zoleo, Iridium GO) that uses the Iridium or Globalstar satellite network — not GSM/LTE cellular. It cannot use an eSIM in the conventional sense; connectivity is tied to a proprietary subscription with the tracker’s manufacturer.";
    }
    if (/Medical alert/i.test(note)) {
      return "This is a medical alert or PERS (personal emergency response) device. Its cellular radio is locked to the service provider (Lively, Medical Guardian, Life Alert, Bay Alarm) and only works with their monitoring subscription. It cannot install third-party eSIMs.";
    }
    if (/Enterprise rugged/i.test(note)) {
      return "This is a Samsung Enterprise / Rugged (Galaxy XCover series) device intended for field workforces — warehouses, healthcare, hospitality. It supports eSIM but activation may go through your employer’s Samsung Knox MDM configuration. Openline installs like on any consumer phone if the device is unlocked.";
    }
    if (/HarmonyOS/i.test(note)) {
      return "This device runs HarmonyOS (Huawei) with no Google Mobile Services. eSIM activation typically requires the Huawei EMUI/HarmonyOS carrier-services app; Openline profiles will provision via the QR code, but Google Wallet-based activations do not work. Devices sold in mainland China may additionally reject international eSIM profiles due to CN firmware restrictions.";
    }
    if (/dual[- ]eSIM only/i.test(note)) {
      return "This variant supports two eSIMs simultaneously but has no physical SIM tray. Openline works — you just cannot combine it with a nano-SIM. On some regional builds only one eSIM can be active at a time.";
    }
    if (/EU carrier/i.test(note)) {
      return "Some European carrier-locked variants of this device shipped with eSIM disabled at the firmware level. Unlocked/global-open models support eSIM normally. Check with your original carrier if activation fails.";
    }
    if (/US carrier variant/i.test(note)) {
      return "This is a US-carrier-branded variant (AT&T, T-Mobile, Verizon, Sprint) with locked firmware and often carrier-specific band support. eSIM may be disabled or restricted to the branding carrier’s profiles. Unlocked international units of the same model typically work with Openline; carrier-branded units may not.";
    }
    if (/Verizon/i.test(note)) {
      return "Verizon-branded units of this Pixel had eSIM disabled at launch on the Verizon network. Unlocked and non-Verizon carrier units support eSIM normally.";
    }
    if (/Google Fi/i.test(note)) {
      return "On this generation of Pixel, eSIM was only available through Google Fi in the US. Other carriers used physical SIM only. Global unlocked units support eSIM everywhere.";
    }
    if (/US: eSIM only/i.test(note)) {
      return "On US-purchased units of this iPhone, Apple removed the physical SIM tray entirely — you must use an eSIM. Everywhere else, the phone has a physical SIM tray in addition to eSIM. Openline still works either way.";
    }
    if (/CN[- ]only|activation may fail abroad|CN\/HK\/KR excluded/i.test(note)) {
      return "This device ships with China-domestic firmware. eSIM support is present on paper but international profiles frequently fail to activate outside mainland China. If you plan to travel, verify eSIM activation with the seller before purchase.";
    }
    if (/JP domestic|Rakuten/i.test(note)) {
      return "Japanese carrier-branded phones (NTT DoCoMo, au, SoftBank, Rakuten) are usually band-locked to Japan’s frequency plan. eSIM hardware works in Japan; overseas activation depends on band overlap with local networks.";
    }
    if (/region[- ]locked/i.test(note)) {
      return "This device’s eSIM activation is region-locked at the firmware level. It only accepts eSIM profiles from carriers in the country/region it was sold in.";
    }
    if (/KR only/i.test(note)) {
      return "This model is only sold in South Korea and uses KT/SKT/LGU+ carrier bands. eSIM hardware is present but activation abroad is unreliable.";
    }
    if (/Foldable/i.test(note)) {
      return "This is a foldable device — the eSIM slot is present but note that some foldable variants sold in China omit international eSIM support. Verify the model code matches the global SKU.";
    }
    if (/Mobile hotspot/i.test(note)) {
      return "This is a portable Wi-Fi hotspot / MiFi router rather than a phone. It accepts an eSIM to share cellular data with your other devices. Openline provisions the same way as on a phone.";
    }
    if (/SIM tray only/i.test(note)) {
      return "This device has a cellular radio, but only accepts a physical nano-SIM or micro-SIM — there’s no eSIM chip. You can’t install Openline as an eSIM here; you’d need a physical SIM plan instead.";
    }
    if (/Wi-Fi \+ Cellular only|Wi-Fi only/i.test(note)) {
      return "This variant is Wi-Fi only — no cellular modem. It cannot install any eSIM. Look for the LTE / 5G / Cellular version of the same model.";
    }
    if (/E-reader/i.test(note)) {
      return "This is an e-reader with a factory-embedded cellular modem tied to the manufacturer’s free-data plan (Amazon Whispernet, B&N nook, etc.). The eSIM/SIM is not user-provisionable — you can’t swap in an Openline profile.";
    }
    if (/Cellular · eSIM only/i.test(note)) {
      return "This variant has cellular connectivity via eSIM only — there’s no physical SIM tray on the device. Openline installs directly via QR code.";
    }
    if (/Unverified variant/i.test(note)) {
      return "Our data links this model code to more than one product family. That usually means Apple/Samsung/Google reused an internal number across generations, or a regional SKU was renamed. Openline should still work, but if the model number on the box doesn’t match the device you’re looking at, double-check with the manufacturer before purchase.";
    }
    if (/Cross-brand model code/i.test(note)) {
      return "This model code also appears on a device from a different brand (Vivo/iQOO, Xiaomi/POCO, Nokia/HMD, Nubia/ZTE etc.). That’s usually a corporate sibling — the hardware is often identical, sometimes rebadged — but eSIM support and carrier certification can differ between the two brands. Verify against your unit’s actual retail packaging.";
    }
    if (/Model code unverified/i.test(note)) {
      return "We don’t have an authoritative model/part number for this device — usually because it’s a wearable, vehicle telematics unit, hotspot, or accessory whose SKU isn’t publicly published. eSIM support is on the manufacturer’s spec sheet, but Openline can’t match a specific hardware code to guarantee compatibility. Verify with the maker before relying on it.";
    }
    if (/Ambiguous name/i.test(note)) {
      return "The product name here is very short (“13”, “F7”, “M6”…) and easy to confuse with same-numbered models from other brands or generations. Check the brand and model code on your device to make sure this entry actually matches what you own.";
    }
    if (/CN firmware/i.test(note)) {
      return "This unit ships with China-domestic firmware. eSIM hardware is present, but the Chinese firmware often blocks activation of international eSIM profiles. If you plan to use Openline outside mainland China, verify with the seller that the firmware isn’t region-locked before purchase.";
    }
    // Fallback — "excluded" pattern
    const raw = note.replace(/\s+excluded/i, "").trim();
    const regionMap = {
      US: "the United States",
      HK: "Hong Kong",
      CN: "mainland China",
      KR: "South Korea",
      JP: "Japan",
      AU: "Australia",
      TW: "Taiwan",
      SEA: "Southeast Asia",
      EU: "the European Union",
      IN: "India",
      UK: "the United Kingdom",
    };
    const parts = raw.split("/").map((p) => regionMap[p.trim()] || p.trim());
    const list =
      parts.length === 1 ? parts[0] :
      parts.length === 2 ? parts.join(" or ") :
      parts.slice(0, -1).join(", ") + ", or " + parts[parts.length - 1];
    return (
      "Units of this device sold in " + list + " ship without eSIM hardware — only the physical SIM tray works. " +
      "Everywhere else, eSIM is supported and Openline will activate normally. " +
      "If you bought yours abroad or through a grey-market importer, check the model number against the manufacturer's list."
    );
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
      <span class="cat-count">${count} device${count === 1 ? "" : "s"}</span>
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

  $compatCats.appendChild(catButton({ value: "yes", name: "Compatible", count: COMPAT_COUNTS.yes, group: "compat" }));
  $compatCats.appendChild(catButton({ value: "no", name: "Not compatible", count: COMPAT_COUNTS.no, group: "compat" }));

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
          const status = d.esim ? "Compatible" : "Not compatible";
          const nameHtml = highlight(`${d.brand} ${d.name}`, tokens);
          const modelHtml = highlight(d.model, tokens);
          let note = "";
          if (d.note) {
            if (isRegionalNote(d.note)) {
              note = `<button type="button" class="note-warn" data-note="${escapeHtml(d.note)}" aria-label="Regional caveat: ${escapeHtml(d.note)}">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 9v4"/><path d="M12 17h.01"/><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/></svg>
                <span>${escapeHtml(d.note)}</span>
              </button>`;
            } else {
              note = `<span class="note">${escapeHtml(d.note)}</span>`;
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
              <span class="badge" aria-label="eSIM ${status}">${status}</span>
            </li>
          `;
        })
        .join("");
    }

    // Counts, title & summary
    const total = DEVICES.length;
    if ($footerTotal) $footerTotal.textContent = total.toLocaleString();

    const active = tokens.length || selectedCompat.size || selectedBrands.size;
    if (active) {
      $title.textContent = "Matching devices";
      const shownN = Math.min(matches.length, MAX);
      const suffix = matches.length > MAX ? ` · showing first ${MAX}` : "";
      $count.innerHTML = `<strong>${matches.length.toLocaleString()}</strong> of ${total.toLocaleString()}${suffix}`;
    } else {
      $title.textContent = "All devices";
      $count.innerHTML = `<strong>${total.toLocaleString()}</strong> total`;
    }

    // Summary in filter bar
    const bits = [];
    if (selectedCompat.size === 1) bits.push(selectedCompat.has("yes") ? "Compatible only" : "Not compatible only");
    else if (selectedCompat.size === 2) bits.push("All statuses");
    if (selectedBrands.size) {
      const list = Array.from(selectedBrands);
      bits.push(list.length <= 2 ? list.join(", ") : `${list.length} brands`);
    }
    $filtersSummary.textContent = bits.length ? bits.join(" · ") : "All devices · All brands";

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
      $filtersCountSummary.innerHTML = `<strong>${matches.length.toLocaleString()}</strong> device${matches.length === 1 ? "" : "s"} match`;
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
      $emptyTitle.textContent = "No devices match both your search and filters.";
      $emptyBody.innerHTML =
        "Your search for " + "<em>" + escapeHtml(rawQuery) + "</em>" +
        " returns " + "<strong>" + matchesSansFilters.toLocaleString() + "</strong>" +
        " device" + (matchesSansFilters === 1 ? "" : "s") + " overall, but none of them match your current filter selection. Maybe your filters are causing the conflict?";
      $emptyActions.hidden = false;
      $emptyActions.querySelector('[data-action="reset-filters"]').hidden = false;
      $emptyActions.querySelector('[data-action="clear-search"]').hidden = false;
      return;
    }

    // Case B: only filters set, no results
    if (!hasSearch && hasFilters) {
      $emptyTitle.textContent = "No devices match your filters.";
      $emptyBody.innerHTML = "Try loosening your filter selection — combining rare compatibility statuses with narrow brands can leave nothing behind.";
      $emptyActions.hidden = false;
      $emptyActions.querySelector('[data-action="reset-filters"]').hidden = false;
      $emptyActions.querySelector('[data-action="clear-search"]').hidden = true;
      return;
    }

    // Case C: only search, no results
    if (hasSearch && !hasFilters) {
      $emptyTitle.textContent = "No exact match.";
      $emptyBody.innerHTML =
        "Try the brand alone (e.g. " + "<em>Samsung</em>" + ") or the exact model number (e.g. " +
        "<em>SM-S921B</em>" + "). If your phone is newer than 2021 and released outside mainland China, chances are very high that it supports eSIM.";
      $emptyActions.hidden = false;
      $emptyActions.querySelector('[data-action="reset-filters"]').hidden = true;
      $emptyActions.querySelector('[data-action="clear-search"]').hidden = false;
      return;
    }

    // Case D: unlikely fallback (no search, no filters, but empty)
    $emptyTitle.textContent = "Nothing here yet.";
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
    pop.setAttribute("aria-label", "Regional caveat");
    pop.innerHTML = `
      <div class="note-popover-head">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 9v4"/><path d="M12 17h.01"/><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/></svg>
        <strong>${escapeHtml(note)}</strong>
        <button type="button" class="note-popover-close" aria-label="Close">
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
  $statTotal.textContent = DEVICES.length.toLocaleString();
  $statYes.textContent = COMPAT_COUNTS.yes.toLocaleString();
  $statNo.textContent = COMPAT_COUNTS.no.toLocaleString();
  $statBrands.textContent = BRANDS.length.toLocaleString();

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
        document.title = q ? q + " eSIM compatibility · Openline" : BASE_TITLE;
      } catch (e) {}
    }, 350);
  }
  $q.addEventListener("input", syncUrl);
  $q.addEventListener("search", syncUrl);
  document.addEventListener("click", (e) => {
    if (e.target.closest("#clear, button[data-action='clear-search']")) syncUrl();
  });

  render();
  if ($q.value) syncUrl();
})();
