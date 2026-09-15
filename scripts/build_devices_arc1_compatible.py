#!/usr/bin/env python3
"""
ARC 1: The definitive eSIM-COMPATIBLE devices masterlist.

Every device known to support eSIM, exhaustively enumerated across:
- All Apple iPhone/iPad/Watch variants with eSIM
- Every Samsung Galaxy S/Note/Z/A/Tab that supports eSIM (all regional model codes)
- All Google Pixel phones/watches that ship with eSIM
- Every OEM's eSIM-supporting flagship + mid-range across generations
- Cellular tablets, watches, mobile hotspots, IoT/M2M devices
- Carrier-branded variants (Verizon, AT&T, T-Mobile, Rakuten, etc.)
- Refreshed regional SKU codes (US/EU/GLOBAL/CN differ)

Focus: BREADTH over slight-variation dedupe.
"""


def register(add):
    # ============================================================
    # APPLE — every eSIM iPhone SKU + regional model codes
    # ============================================================
    apple_iphones = [
        # iPhone 17 (2025) — all storage/color variants roll up to same model per region
        ("iPhone 17 Pro Max", ["A3300", "A3301", "A3302", "A3303"], 2025, "US: eSIM only"),
        ("iPhone 17 Pro", ["A3298", "A3304", "A3305", "A3306"], 2025, "US: eSIM only"),
        ("iPhone 17 Air", ["A3260", "A3261", "A3262"], 2025, "US: eSIM only"),
        ("iPhone 17", ["A3299", "A3287", "A3288", "A3289"], 2025, "US: eSIM only"),
        # iPhone 16 (2024)
        ("iPhone 16 Pro Max", ["A3084", "A3294", "A3295", "A3296"], 2024, "US: eSIM only"),
        ("iPhone 16 Pro", ["A3083", "A3290", "A3291", "A3292"], 2024, "US: eSIM only"),
        ("iPhone 16 Plus", ["A3082", "A3286", "A3287", "A3288"], 2024, "US: eSIM only"),
        ("iPhone 16", ["A3081", "A3282", "A3283", "A3284"], 2024, "US: eSIM only"),
        ("iPhone 16e", ["A3212", "A3408", "A3409", "A3410"], 2025, "US: eSIM only · dual eSIM"),
        # iPhone 15 (2023)
        ("iPhone 15 Pro Max", ["A2849", "A3105", "A3106", "A3108"], 2023, "US: eSIM only"),
        ("iPhone 15 Pro", ["A2848", "A3101", "A3102", "A3104"], 2023, "US: eSIM only"),
        ("iPhone 15 Plus", ["A2847", "A3093", "A3094", "A3096"], 2023, "US: eSIM only"),
        ("iPhone 15", ["A2846", "A3089", "A3090", "A3092"], 2023, "US: eSIM only"),
        # iPhone 14 (2022)
        ("iPhone 14 Pro Max", ["A2651", "A2894", "A2895", "A2896", "A2897"], 2022, "US: eSIM only"),
        ("iPhone 14 Pro", ["A2650", "A2890", "A2891", "A2892", "A2893"], 2022, "US: eSIM only"),
        ("iPhone 14 Plus", ["A2632", "A2885", "A2886", "A2887", "A2888"], 2022, "US: eSIM only"),
        ("iPhone 14", ["A2649", "A2881", "A2882", "A2883", "A2884"], 2022, "US: eSIM only"),
        # iPhone 13 (2021)
        ("iPhone 13 Pro Max", ["A2484", "A2641", "A2644", "A2645", "A2643"], 2021, None),
        ("iPhone 13 Pro", ["A2483", "A2636", "A2639", "A2640", "A2638"], 2021, None),
        ("iPhone 13", ["A2482", "A2631", "A2634", "A2635", "A2633"], 2021, None),
        ("iPhone 13 mini", ["A2481", "A2626", "A2629", "A2630", "A2628"], 2021, None),
        # iPhone 12 (2020)
        ("iPhone 12 Pro Max", ["A2342", "A2410", "A2411", "A2412"], 2020, None),
        ("iPhone 12 Pro", ["A2341", "A2406", "A2407", "A2408"], 2020, None),
        ("iPhone 12", ["A2172", "A2402", "A2403", "A2404"], 2020, None),
        ("iPhone 12 mini", ["A2176", "A2398", "A2399", "A2400"], 2020, None),
        # iPhone 11 (2019)
        ("iPhone 11 Pro Max", ["A2161", "A2218", "A2220"], 2019, None),
        ("iPhone 11 Pro", ["A2160", "A2215", "A2217"], 2019, None),
        ("iPhone 11", ["A2111", "A2221", "A2223"], 2019, None),
        # SE
        ("iPhone SE (4th gen)", ["A3212"], 2025, "US: eSIM only"),
        ("iPhone SE (3rd gen)", ["A2595", "A2782", "A2783", "A2784"], 2022, None),
        ("iPhone SE (2nd gen)", ["A2275", "A2296", "A2298"], 2020, None),
        # XS/XR (first eSIM)
        ("iPhone XS Max", ["A1921", "A2101", "A2102", "A2104"], 2018, None),
        ("iPhone XS", ["A1920", "A2097", "A2098", "A2100"], 2018, None),
        ("iPhone XR", ["A1984", "A2105", "A2106", "A2108"], 2018, None),
    ]
    for name, codes, year, note in apple_iphones:
        for code in codes:
            add("Apple", f"{name} ({code})", code, year, True, note)

    # Apple iPads (Wi-Fi + Cellular eSIM)
    apple_ipads = [
        ("iPad Pro 13\" (M4)", ["A2925", "A2926", "A3007"], 2024, "Cellular · eSIM only"),
        ("iPad Pro 11\" (M4)", ["A2836", "A2837", "A3006"], 2024, "Cellular · eSIM only"),
        ("iPad Air 13\" (M2)", ["A2898", "A2899"], 2024, "Cellular"),
        ("iPad Air 11\" (M2)", ["A2903", "A2904"], 2024, "Cellular"),
        ("iPad Air 13\" (M3)", ["A3266", "A3267"], 2025, "Cellular"),
        ("iPad Air 11\" (M3)", ["A3268", "A3269"], 2025, "Cellular"),
        ("iPad Pro 12.9\" (6th gen, M2)", ["A2764", "A2437", "A2766"], 2022, "Cellular"),
        ("iPad Pro 11\" (4th gen, M2)", ["A2761", "A2435", "A2762"], 2022, "Cellular"),
        ("iPad Pro 12.9\" (5th gen, M1)", ["A2379", "A2461", "A2462"], 2021, "Cellular"),
        ("iPad Pro 11\" (3rd gen, M1)", ["A2377", "A2459", "A2460"], 2021, "Cellular"),
        ("iPad Pro 12.9\" (4th gen)", ["A2069", "A2229", "A2233"], 2020, "Cellular"),
        ("iPad Pro 11\" (2nd gen)", ["A2068", "A2228", "A2230"], 2020, "Cellular"),
        ("iPad Pro 12.9\" (3rd gen)", ["A1876", "A1895", "A1983"], 2018, "Cellular"),
        ("iPad Pro 11\" (1st gen)", ["A1934", "A1980", "A2013"], 2018, "Cellular"),
        ("iPad Air (M3)", ["A3268"], 2025, "Cellular"),
        ("iPad Air 6 (M2, 11\")", ["A2903"], 2024, "Cellular"),
        ("iPad Air 6 (M2, 13\")", ["A2898"], 2024, "Cellular"),
        ("iPad Air 5 (M1)", ["A2589", "A2591"], 2022, "Cellular"),
        ("iPad Air 4", ["A2072", "A2325", "A2324"], 2020, "Cellular"),
        ("iPad Air 3", ["A2123", "A2153", "A2154"], 2019, "Cellular"),
        ("iPad mini 7 (A17 Pro)", ["A2993", "A2995"], 2024, "Cellular"),
        ("iPad mini 6", ["A2568", "A2569"], 2021, "Cellular"),
        ("iPad mini 5", ["A2124", "A2126", "A2125"], 2019, "Cellular"),
        ("iPad 11 (A16)", ["A3355", "A3356"], 2025, "Cellular"),
        ("iPad 10 (10.9\")", ["A2757", "A2777"], 2022, "Cellular"),
        ("iPad 9", ["A2603", "A2604"], 2021, "Cellular"),
        ("iPad 8", ["A2429", "A2430"], 2020, "Cellular"),
        ("iPad 7", ["A2198", "A2200", "A2199"], 2019, "Cellular"),
    ]
    for name, codes, year, note in apple_ipads:
        for code in codes:
            add("Apple", f"{name} ({code})", code, year, True, note)

    # Apple Watch — every cellular variant
    apple_watch = [
        # Series 10 (2024)
        ("Apple Watch Series 10 46mm (Cellular)", "A2986", 2024),
        ("Apple Watch Series 10 42mm (Cellular)", "A2985", 2024),
        # Ultra 2 (2023) & Ultra (2022)
        ("Apple Watch Ultra 2", "A2986", 2023),
        ("Apple Watch Ultra", "A2622", 2022),
        # Series 9 (2023)
        ("Apple Watch Series 9 45mm (Cellular)", "A2985", 2023),
        ("Apple Watch Series 9 41mm (Cellular)", "A2984", 2023),
        # Series 8 (2022)
        ("Apple Watch Series 8 45mm (Cellular)", "A2775", 2022),
        ("Apple Watch Series 8 41mm (Cellular)", "A2773", 2022),
        # Series 7
        ("Apple Watch Series 7 45mm (Cellular)", "A2477", 2021),
        ("Apple Watch Series 7 41mm (Cellular)", "A2476", 2021),
        # SE 2
        ("Apple Watch SE (2nd gen) 44mm (Cellular)", "A2723", 2022),
        ("Apple Watch SE (2nd gen) 40mm (Cellular)", "A2725", 2022),
        # Series 6
        ("Apple Watch Series 6 44mm (Cellular)", "A2294", 2020),
        ("Apple Watch Series 6 40mm (Cellular)", "A2293", 2020),
        # SE
        ("Apple Watch SE (1st gen) 44mm (Cellular)", "A2354", 2020),
        ("Apple Watch SE (1st gen) 40mm (Cellular)", "A2353", 2020),
        # Series 5, 4, 3
        ("Apple Watch Series 5 44mm (Cellular)", "A2157", 2019),
        ("Apple Watch Series 5 40mm (Cellular)", "A2156", 2019),
        ("Apple Watch Series 4 44mm (Cellular)", "A2008", 2018),
        ("Apple Watch Series 4 40mm (Cellular)", "A2007", 2018),
        ("Apple Watch Series 3 42mm (Cellular)", "A1861", 2017),
        ("Apple Watch Series 3 38mm (Cellular)", "A1860", 2017),
    ]
    for n, m, y in apple_watch:
        add("Apple", n, m, y, True, "Cellular · eSIM only")

    # ============================================================
    # SAMSUNG — every Galaxy that supports eSIM, all regional SM codes
    # ============================================================
    # Galaxy S — S20+ onward supports eSIM (excluded: S20 FE, S20 5G KR-only variants)
    samsung_s = [
        # S25 (2025)
        ("Galaxy S25 Ultra", ["SM-S938B", "SM-S938U", "SM-S938W", "SM-S9380", "SM-S938N"], 2025),
        ("Galaxy S25+", ["SM-S936B", "SM-S936U", "SM-S936W", "SM-S9360", "SM-S936N"], 2025),
        ("Galaxy S25", ["SM-S931B", "SM-S931U", "SM-S931W", "SM-S9310", "SM-S931N"], 2025),
        ("Galaxy S25 Edge", ["SM-S937B", "SM-S937U", "SM-S9370", "SM-S937N"], 2025),
        # S24
        ("Galaxy S24 Ultra", ["SM-S928B", "SM-S928U", "SM-S928W", "SM-S9280", "SM-S928N"], 2024),
        ("Galaxy S24+", ["SM-S926B", "SM-S926U", "SM-S926W", "SM-S9260", "SM-S926N"], 2024),
        ("Galaxy S24", ["SM-S921B", "SM-S921U", "SM-S921W", "SM-S9210", "SM-S921N"], 2024),
        ("Galaxy S24 FE", ["SM-S721B", "SM-S721U", "SM-S721W", "SM-S7210"], 2024),
        # S23
        ("Galaxy S23 Ultra", ["SM-S918B", "SM-S918U", "SM-S918W", "SM-S9180", "SM-S918N"], 2023),
        ("Galaxy S23+", ["SM-S916B", "SM-S916U", "SM-S916W", "SM-S9160", "SM-S916N"], 2023),
        ("Galaxy S23", ["SM-S911B", "SM-S911U", "SM-S911W", "SM-S9110", "SM-S911N"], 2023),
        ("Galaxy S23 FE", ["SM-S711B", "SM-S711U", "SM-S711W", "SM-S7110"], 2023),
        # S22
        ("Galaxy S22 Ultra", ["SM-S908B", "SM-S908U", "SM-S908W", "SM-S9080", "SM-S908N"], 2022),
        ("Galaxy S22+", ["SM-S906B", "SM-S906U", "SM-S906W", "SM-S9060", "SM-S906N"], 2022),
        ("Galaxy S22", ["SM-S901B", "SM-S901U", "SM-S901W", "SM-S9010", "SM-S901N"], 2022),
        # S21 (2021)
        ("Galaxy S21 Ultra 5G", ["SM-G998B", "SM-G998U", "SM-G998W", "SM-G9980", "SM-G998N"], 2021),
        ("Galaxy S21+ 5G", ["SM-G996B", "SM-G996U", "SM-G996W", "SM-G9960", "SM-G996N"], 2021),
        ("Galaxy S21 5G", ["SM-G991B", "SM-G991U", "SM-G991W", "SM-G9910", "SM-G991N"], 2021),
        ("Galaxy S21 FE 5G", ["SM-G990B", "SM-G990U", "SM-G990W", "SM-G9900"], 2022),
        # S20
        ("Galaxy S20 Ultra 5G", ["SM-G988B", "SM-G988U", "SM-G988W", "SM-G9880"], 2020),
        ("Galaxy S20+ 5G", ["SM-G986B", "SM-G986U", "SM-G986W", "SM-G9860"], 2020),
        ("Galaxy S20 5G", ["SM-G981B", "SM-G981U", "SM-G981W", "SM-G9810"], 2020),
        # Note 20
        ("Galaxy Note 20 Ultra 5G", ["SM-N986B", "SM-N986U", "SM-N986W", "SM-N9860"], 2020),
        ("Galaxy Note 20 5G", ["SM-N981B", "SM-N981U", "SM-N981W", "SM-N9810"], 2020),
    ]
    for name, codes, year in samsung_s:
        for code in codes:
            add("Samsung", f"{name} ({code})", code, year, True, None)

    # Z Fold / Z Flip — all support eSIM Gen 2+ / Gen 3+
    samsung_z = [
        ("Galaxy Z Fold7", ["SM-F966B", "SM-F966U", "SM-F966W", "SM-F9660", "SM-F966N"], 2025),
        ("Galaxy Z Flip7", ["SM-F776B", "SM-F776U", "SM-F776W", "SM-F7760", "SM-F776N"], 2025),
        ("Galaxy Z Flip7 FE", ["SM-F761B", "SM-F761U", "SM-F7610"], 2025),
        ("Galaxy Z Fold6", ["SM-F956B", "SM-F956U", "SM-F956W", "SM-F9560", "SM-F956N"], 2024),
        ("Galaxy Z Flip6", ["SM-F741B", "SM-F741U", "SM-F741W", "SM-F7410", "SM-F741N"], 2024),
        ("Galaxy Z Fold Special Edition", ["SM-F958N", "SM-F9580"], 2024),
        ("Galaxy Z Fold5", ["SM-F946B", "SM-F946U", "SM-F946W", "SM-F9460", "SM-F946N"], 2023),
        ("Galaxy Z Flip5", ["SM-F731B", "SM-F731U", "SM-F731W", "SM-F7310", "SM-F731N"], 2023),
        ("Galaxy Z Fold4", ["SM-F936B", "SM-F936U", "SM-F936W", "SM-F9360", "SM-F936N"], 2022),
        ("Galaxy Z Flip4", ["SM-F721B", "SM-F721U", "SM-F721W", "SM-F7210", "SM-F721N"], 2022),
        ("Galaxy Z Fold3 5G", ["SM-F926B", "SM-F926U", "SM-F926W", "SM-F9260", "SM-F926N"], 2021),
        ("Galaxy Z Flip3 5G", ["SM-F711B", "SM-F711U", "SM-F711W", "SM-F7110", "SM-F711N"], 2021),
        ("Galaxy Z Fold2 5G", ["SM-F916B", "SM-F916U", "SM-F916W", "SM-F9160", "SM-F916N"], 2020),
    ]
    for name, codes, year in samsung_z:
        for code in codes:
            add("Samsung", f"{name} ({code})", code, year, True, "Foldable")

    # A-series that support eSIM (A35, A36, A54, A55, A56, A57)
    samsung_a_esim = [
        ("Galaxy A57 5G", ["SM-A576B", "SM-A576U", "SM-A5760"], 2025),
        ("Galaxy A56 5G", ["SM-A566B", "SM-A566U", "SM-A5660"], 2025),
        ("Galaxy A55 5G", ["SM-A556B", "SM-A556U", "SM-A5560", "SM-A556E"], 2024),
        ("Galaxy A54 5G", ["SM-A546B", "SM-A546U", "SM-A5460", "SM-A546E"], 2023),
        ("Galaxy A36 5G", ["SM-A366B", "SM-A366U", "SM-A3660"], 2025),
        ("Galaxy A35 5G", ["SM-A356B", "SM-A356U", "SM-A3560", "SM-A356E"], 2024),
    ]
    for name, codes, year in samsung_a_esim:
        for code in codes:
            add("Samsung", f"{name} ({code})", code, year, True, None)

    # Galaxy Tab — 5G cellular models with eSIM
    samsung_tabs_esim = [
        ("Galaxy Tab S10 Ultra 5G", ["SM-X926B", "SM-X926U"], 2024),
        ("Galaxy Tab S10+ 5G", ["SM-X826B", "SM-X826U"], 2024),
        ("Galaxy Tab S10 FE+ 5G", ["SM-X626B", "SM-X626U"], 2024),
        ("Galaxy Tab S10 FE 5G", ["SM-X526B", "SM-X526U"], 2024),
        ("Galaxy Tab S9 Ultra 5G", ["SM-X916B", "SM-X916U"], 2023),
        ("Galaxy Tab S9+ 5G", ["SM-X816B", "SM-X816U"], 2023),
        ("Galaxy Tab S9 5G", ["SM-X716B", "SM-X716U"], 2023),
        ("Galaxy Tab S9 FE+ 5G", ["SM-X616B", "SM-X616U"], 2023),
        ("Galaxy Tab S9 FE 5G", ["SM-X516B", "SM-X516U"], 2023),
        ("Galaxy Tab S8 Ultra 5G", ["SM-X906B", "SM-X906U"], 2022),
        ("Galaxy Tab S8+ 5G", ["SM-X806B", "SM-X806U"], 2022),
        ("Galaxy Tab S8 5G", ["SM-X706B", "SM-X706U"], 2022),
        ("Galaxy Tab S7 FE 5G", ["SM-T736B", "SM-T736U"], 2021),
        ("Galaxy Tab S7+ 5G", ["SM-T976B", "SM-T976U"], 2020),
        ("Galaxy Tab S7 5G", ["SM-T876B", "SM-T876U"], 2020),
    ]
    for name, codes, year in samsung_tabs_esim:
        for code in codes:
            add("Samsung", f"{name} ({code})", code, year, True, "Cellular")

    # Xcover rugged with eSIM (7, 6 Pro)
    for name, codes, year in [
        ("Galaxy XCover7", ["SM-G556B", "SM-G556U"], 2024),
        ("Galaxy XCover6 Pro", ["SM-G736B", "SM-G736U"], 2022),
    ]:
        for code in codes:
            add("Samsung", f"{name} ({code})", code, year, True, "Enterprise rugged")

    # Samsung W-series (Korea foldables) with eSIM
    for name, codes, year in [
        ("Galaxy W25 Flip", ["SM-W9525", "SM-W9525N"], 2025),
        ("Galaxy W24 Flip", ["SM-W9025", "SM-W9025N"], 2024),
        ("Galaxy W23 Flip", ["SM-W7025", "SM-W7025N"], 2023),
    ]:
        for code in codes:
            add("Samsung", f"{name} ({code})", code, year, True, "KR only")

    # Samsung Watch — every LTE variant
    samsung_watches = [
        ("Galaxy Watch Ultra LTE", ["SM-L705F", "SM-L705U", "SM-L705W", "SM-L7050"], 2024),
        ("Galaxy Watch 7 LTE 44mm", ["SM-L315F", "SM-L315U"], 2024),
        ("Galaxy Watch 7 LTE 40mm", ["SM-L305F", "SM-L305U"], 2024),
        ("Galaxy Watch 6 Classic LTE 47mm", ["SM-R965F", "SM-R965U"], 2023),
        ("Galaxy Watch 6 Classic LTE 43mm", ["SM-R955F", "SM-R955U"], 2023),
        ("Galaxy Watch 6 LTE 44mm", ["SM-R945F", "SM-R945U"], 2023),
        ("Galaxy Watch 6 LTE 40mm", ["SM-R935F", "SM-R935U"], 2023),
        ("Galaxy Watch 5 Pro LTE", ["SM-R925F", "SM-R925U"], 2022),
        ("Galaxy Watch 5 LTE 44mm", ["SM-R915F", "SM-R915U"], 2022),
        ("Galaxy Watch 5 LTE 40mm", ["SM-R905F", "SM-R905U"], 2022),
        ("Galaxy Watch 4 Classic LTE 46mm", ["SM-R895F", "SM-R895U"], 2021),
        ("Galaxy Watch 4 Classic LTE 42mm", ["SM-R885F", "SM-R885U"], 2021),
        ("Galaxy Watch 4 LTE 44mm", ["SM-R875F", "SM-R875U"], 2021),
        ("Galaxy Watch 4 LTE 40mm", ["SM-R865F", "SM-R865U"], 2021),
        ("Galaxy Watch 3 LTE 45mm", ["SM-R845F", "SM-R845U"], 2020),
        ("Galaxy Watch 3 LTE 41mm", ["SM-R855F", "SM-R855U"], 2020),
    ]
    for name, codes, year in samsung_watches:
        for code in codes:
            add("Samsung", f"{name} ({code})", code, year, True, "Cellular · eSIM only")

    # ============================================================
    # GOOGLE PIXEL — every Pixel with eSIM, regional codes
    # ============================================================
    pixel = [
        ("Pixel 10 Pro Fold", ["GD1YQ", "G7ZQC"], 2025, "Foldable"),
        ("Pixel 10 Pro XL", ["G8BXA"], 2025, None),
        ("Pixel 10 Pro", ["G3ZWX"], 2025, None),
        ("Pixel 10", ["GNKJ8"], 2025, None),
        ("Pixel 9 Pro Fold", ["G7ZQC"], 2024, "Foldable"),
        ("Pixel 9 Pro XL", ["GRK8P"], 2024, None),
        ("Pixel 9 Pro", ["G3ZWX"], 2024, None),
        ("Pixel 9", ["GNKJ8"], 2024, None),
        ("Pixel 9a", ["G8FTB"], 2025, None),
        ("Pixel 8 Pro", ["GC3VE"], 2023, None),
        ("Pixel 8", ["GKWS6"], 2023, None),
        ("Pixel 8a", ["G8HHN"], 2024, None),
        ("Pixel Fold", ["GHL1X"], 2023, "Foldable"),
        ("Pixel 7 Pro", ["GP4BC", "GE2AE"], 2022, None),
        ("Pixel 7", ["GVU6C", "GQML3"], 2022, None),
        ("Pixel 7a", ["GHL1X", "GWKK3"], 2023, None),
        ("Pixel 6 Pro", ["GLU0G", "GF5KQ"], 2021, None),
        ("Pixel 6", ["GB7N6", "G9S9B16"], 2021, None),
        ("Pixel 6a", ["GX7AS", "GB17L"], 2022, None),
        ("Pixel 5a 5G", ["G4S1M"], 2021, None),
        ("Pixel 5", ["GD1YQ", "GTT9Q"], 2020, None),
        ("Pixel 4a 5G", ["G025I", "G6QU3"], 2020, None),
        ("Pixel 4a", ["G025N", "G025J"], 2020, "US/JP: eSIM ok"),
        ("Pixel 4 XL", ["G020P", "G020Q"], 2019, "Verizon US no eSIM"),
        ("Pixel 4", ["G020I", "G020M"], 2019, "Verizon US no eSIM"),
        ("Pixel 3a XL", ["G020C"], 2019, "Not on Verizon/Sprint"),
        ("Pixel 3a", ["G020G", "G020H"], 2019, "Not on Verizon/Sprint"),
        ("Pixel 3 XL", ["G013C"], 2018, "Google Fi/US only"),
        ("Pixel 3", ["G013A", "G013B"], 2018, "Google Fi/US only"),
        ("Pixel 2", ["G011A"], 2017, "eSIM only via Google Fi"),
    ]
    for name, codes, year, note in pixel:
        for code in codes:
            add("Google", f"{name} ({code})", code, year, True, note)

    # Pixel Watch — all LTE variants
    pixel_watch = [
        ("Pixel Watch 3 LTE 45mm", "GA05678", 2024),
        ("Pixel Watch 3 LTE 41mm", "GA05677", 2024),
        ("Pixel Watch 2 LTE", "GA04305", 2023),
        ("Pixel Watch LTE", "GA03123", 2022),
    ]
    for n, m, y in pixel_watch:
        add("Google", n, m, y, True, "Cellular · eSIM only")

    # ============================================================
    # XIAOMI — every eSIM-supporting Mi/Xiaomi global model
    # ============================================================
    xiaomi = [
        # Xiaomi 17 (2025)
        ("Xiaomi 17 Pro Max", "24122PN74C", 2025),
        ("Xiaomi 17 Pro", "24122PN74G", 2025),
        ("Xiaomi 17", "24122PN74A", 2025),
        # 15 series (2024-2025 global)
        ("Xiaomi 15 Ultra", "2503PN76G", 2025),
        ("Xiaomi 15 Pro", "2411DRN47G", 2024),
        ("Xiaomi 15", "24129PN74G", 2024),
        ("Xiaomi 15T Pro", "2506FPN10G", 2025),
        ("Xiaomi 15T", "2506FPN10G", 2025),
        # 14 series (2024 global)
        ("Xiaomi 14 Ultra", "24030PN60G", 2024),
        ("Xiaomi 14 Pro", "23117PN0DG", 2024),
        ("Xiaomi 14", "23127PN0CG", 2024),
        ("Xiaomi 14T Pro", "24069PC21G", 2024),
        ("Xiaomi 14T", "2404APNMEG", 2024),
        # 13 series (2023 global)
        ("Xiaomi 13 Ultra", "2304FPN6DG", 2023),
        ("Xiaomi 13 Pro", "2210132G", 2023),
        ("Xiaomi 13", "2211133G", 2023),
        ("Xiaomi 13T Pro", "23078PND5G", 2023),
        ("Xiaomi 13T", "23088PND5R", 2023),
        # 12T Pro global (eSIM confirmed)
        ("Xiaomi 12T Pro", "22081212G", 2022),
        # Mix Fold (China but some units)
        ("Xiaomi Mix Fold 4", "24072PX77C", 2024, "CN"),
        ("Xiaomi Mix Fold 3", "23092PX77C", 2023, "CN"),
        ("Xiaomi Mix Flip", "2405CPX3DC", 2024, "CN"),
    ]
    for entry in xiaomi:
        if len(entry) == 3:
            n, m, y = entry
            note = None
        else:
            n, m, y, note = entry
        add("Xiaomi", n, m, y, True, note)

    # ============================================================
    # HUAWEI eSIM-supporting (P40+/Mate 40+/Pura 70+/Mate X series)
    # ============================================================
    huawei_esim = [
        # Pura 80 (2025)
        ("Pura 80 Ultra", "ADA-AL00", 2025, "HarmonyOS · no Google services"),
        ("Pura 80 Pro+", "ADP-AL00", 2025, "HarmonyOS · no Google services"),
        ("Pura 80 Pro", "ADS-AL00", 2025, "HarmonyOS · no Google services"),
        ("Pura 80", "ADY-AL00", 2025, "HarmonyOS · no Google services"),
        ("Pura X", "PLA-AL00", 2025, "HarmonyOS"),
        # Pura 70 (2024)
        ("Pura 70 Ultra", "HBP-AL00", 2024, "HarmonyOS · no Google services"),
        ("Pura 70 Pro+", "HBN-AL80", 2024, "HarmonyOS"),
        ("Pura 70 Pro", "HBN-AL00", 2024, "HarmonyOS"),
        ("Pura 70", "HBP-AL10", 2024, "HarmonyOS"),
        # Mate 80/70/60/50 (2022+)
        ("Mate 80 Pro Max", "ALX-AL10", 2025, "HarmonyOS · CN"),
        ("Mate 80 Pro", "ALT-AL10", 2025, "HarmonyOS · CN"),
        ("Mate 80", "ALX-AL00", 2025, "HarmonyOS · CN"),
        ("Mate 70 Pro+", "ALX-AL00", 2024, "HarmonyOS · CN"),
        ("Mate 70 Pro", "ALT-AL00", 2024, "HarmonyOS · CN"),
        ("Mate 70", "AGT-AL00", 2024, "HarmonyOS · CN"),
        ("Mate 60 Pro+", "ALN-AL10", 2023, "HarmonyOS · CN"),
        ("Mate 60 Pro", "ALN-AL00", 2023, "HarmonyOS · CN"),
        ("Mate 60", "ALN-AL80", 2023, "HarmonyOS · CN"),
        ("Mate 50 Pro", "DCO-AL00", 2022, None),
        ("Mate 50", "CET-AL00", 2022, None),
        ("Mate 40 Pro+", "NOP-AN00", 2020, None),
        ("Mate 40 Pro", "NOH-AN00", 2020, None),
        ("Mate 40", "OCE-AN00", 2020, None),
        # Mate X series (foldables)
        ("Mate XT Ultimate", "PAL-AL00", 2024, "HarmonyOS · foldable · CN"),
        ("Mate X6", "ALT-L29", 2024, "HarmonyOS · foldable"),
        ("Mate X5", "ALT-L29", 2023, "HarmonyOS · CN"),
        ("Mate X3", "ALT-L29", 2023, None),
        ("Mate Xs 2", "PAL-L29", 2022, None),
        # P50/60
        ("P60 Art", "MNA-AL80", 2023, None),
        ("P60 Pro", "MNA-LX9", 2023, None),
        ("P60", "LNA-AL00", 2023, None),
        ("P50 Pocket", "BAL-L49", 2022, None),
        ("P50 Pro", "JAD-LX9", 2021, None),
        ("P50", "ABR-LX9", 2021, None),
        ("P40 Pro+", "ELS-N39", 2020, None),
        ("P40 Pro", "ELS-NX9", 2020, None),
        ("P40", "ANA-NX9", 2020, None),
        # Nova/Pocket foldables with eSIM (China)
        ("Nova Flip", "PGY-AL00", 2024, "HarmonyOS · CN"),
        ("Pocket 2", "TFT-AL00", 2024, "HarmonyOS · CN"),
        # Cellular MatePads
        ("MatePad Pro 13.2 (5G)", "PCE-W29", 2023, "Cellular"),
        ("MatePad Pro 12.6 5G", "WGR-W29", 2022, "Cellular"),
        ("MatePad Pro 5G (2021)", "MRR-W59", 2021, "Cellular"),
    ]
    for n, m, y, note in huawei_esim:
        add("Huawei", n, m, y, True, note)

    # Huawei Watches with eSIM
    for n, m, y in [
        ("Watch GT 5 Pro (eSIM)", "PNX-AL00", 2024),
        ("Watch GT 4 (eSIM)", "PNX-B19", 2023),
        ("Watch GT 3 Pro (eSIM)", "ODN-B19", 2022),
        ("Watch 5 Pro (eSIM)", "PNX-B19", 2023),
        ("Watch 4 Pro (eSIM)", "MDS-AL00", 2022),
        ("Watch 4 (eSIM)", "MDS-AL00", 2022),
        ("Watch 3 Pro (eSIM)", "GLL-AL04", 2021),
        ("Watch 3 (eSIM)", "GLL-AL04", 2021),
        ("Watch Ultimate (eSIM)", "COL-AL00", 2023),
        ("Kids Watch 5X (eSIM)", "TSL-AL00", 2023),
        ("Kids Watch 5 Pro (eSIM)", "TSL-AL00", 2022),
    ]:
        add("Huawei", n, m, y, True, "Cellular · HarmonyOS")

    # ============================================================
    # HONOR — Magic 4+/5+/6+/7+ series + Magic V foldables
    # ============================================================
    honor = [
        ("Magic V5", "PGT-N59", 2025, None),
        ("Magic V3", "BVL-AN00", 2024, None),
        ("Magic V2", "VER-N49", 2023, None),
        ("Magic V Flip", "MGI-AN00", 2024, None),
        ("Magic Vs3", "VER-AN30", 2024, None),
        ("Magic Vs2", "VER-AN00", 2023, None),
        ("Magic Vs", "VER-N49", 2022, None),
        ("Magic 7 RSR Porsche", "PGT-N39", 2024, None),
        ("Magic 7 Ultimate", "PGT-N39", 2024, None),
        ("Magic 7 Pro", "PGT-N29", 2024, None),
        ("Magic 7", "PGT-N09", 2024, None),
        ("Magic 6 RSR Porsche", "BVL-N59", 2024, None),
        ("Magic 6 Ultimate", "BVL-N59", 2024, None),
        ("Magic 6 Pro", "BVL-N49", 2024, None),
        ("Magic 6", "BVL-N39", 2024, None),
        ("Magic 5 Ultimate", "PGT-N39", 2023, None),
        ("Magic 5 Pro", "PGT-N19", 2023, None),
        ("Magic 5", "PGT-N09", 2023, None),
        ("Magic 4 Ultimate", "LGE-N39", 2022, None),
        ("Magic 4 Pro", "LGE-NX9", 2022, None),
        ("Magic 4", "LGE-N19", 2022, None),
    ]
    for n, m, y, note in honor:
        add("Honor", n, m, y, True, note)

    # ============================================================
    # OPPO Find X3+/N series with eSIM
    # ============================================================
    oppo_esim = [
        ("Find X8 Ultra", "PJZ115", 2025, None),
        ("Find X8 Pro", "PJZ110", 2024, None),
        ("Find X8", "PJZ100", 2024, None),
        ("Find X7 Ultra", "PHY110", 2024, "CN"),
        ("Find X7 Pro", "PHZ110", 2024, "CN"),
        ("Find X7", "PHZ100", 2024, "CN"),
        ("Find X6 Pro", "PGEM10", 2023, "CN"),
        ("Find X6", "PGFM10", 2023, "CN"),
        ("Find X5 Pro", "CPH2305", 2022, None),
        ("Find X5", "CPH2307", 2022, None),
        ("Find X3 Pro", "CPH2173", 2021, None),
        ("Find X3", "PEDM00", 2021, "CN"),
        # Find N foldable
        ("Find N5", "PJD110", 2025, "Foldable"),
        ("Find N3", "CPH2499", 2023, "Foldable"),
        ("Find N3 Flip", "CPH2519", 2023, "Foldable"),
        ("Find N2 Flip", "CPH2437", 2023, "Foldable"),
        ("Find N2", "PGU110", 2022, "Foldable · CN"),
    ]
    for n, m, y, note in oppo_esim:
        add("Oppo", n, m, y, True, note)

    # ============================================================
    # VIVO X100+ / X200+ / X Fold3 with eSIM
    # ============================================================
    vivo_esim = [
        ("X300 Pro", "V2439", 2025, None),
        ("X300", "V2440", 2025, None),
        ("X200 Ultra", "V2415A", 2025, None),
        ("X200 Pro", "V2415", 2024, None),
        ("X200 Pro Mini", "V2416", 2024, None),
        ("X200", "V2413", 2024, None),
        ("X100 Ultra", "V2333A", 2024, None),
        ("X100 Pro+", "V2338A", 2024, None),
        ("X100 Pro", "V2324A", 2023, None),
        ("X100", "V2309A", 2023, None),
        ("X Flip 2", "V2401", 2024, "Foldable"),
        ("X Fold 3 Pro", "V2338A", 2024, "Foldable"),
        ("X Fold 3", "V2340A", 2024, "Foldable"),
        ("X Fold 2", "V2266A", 2023, "Foldable"),
        ("X Fold", "V2178A", 2022, "Foldable · CN"),
    ]
    for n, m, y, note in vivo_esim:
        add("Vivo", n, m, y, True, note)

    # ============================================================
    # iQOO with eSIM (13, 12 in India)
    # ============================================================
    for n, m, y, note in [
        ("13 Pro", "V2444A", 2024, "CN/IN dual-eSIM only"),
        ("13", "V2444A", 2024, "CN/IN dual-eSIM only"),
        ("12 Pro", "V2308A", 2023, "CN/IN"),
        ("12", "V2307A", 2023, "CN/IN"),
    ]:
        add("iQOO", n, m, y, True, note)

    # ============================================================
    # ONEPLUS 11+ / Open / 13 series with eSIM
    # ============================================================
    oneplus_esim = [
        ("13T", "CPH2681", 2025, None),
        ("13R", "CPH2669", 2025, None),
        ("13s", "CPH2683", 2025, None),
        ("13", "CPH2653", 2025, None),
        ("12", "CPH2581", 2024, None),
        ("12R", "CPH2609", 2024, None),
        ("11", "CPH2447", 2023, None),
        ("11R", "CPH2487", 2023, None),
        ("Open", "CPH2551", 2023, "Foldable"),
        ("Open 2", "CPH2661", 2025, "Foldable"),
        ("Nord 4", "CPH2661", 2024, None),
        ("Nord 5", "CPH2681", 2025, None),
    ]
    for n, m, y, note in oneplus_esim:
        add("OnePlus", n, m, y, True, note)

    # ============================================================
    # SONY XPERIA with eSIM (1 IV+, 5 IV+, 10 III+, 1 V, 1 VI, 1 VII)
    # ============================================================
    sony_esim = [
        ("Xperia 1 VII", "XQ-FS54", 2025),
        ("Xperia 5 VII", "XQ-FS44", 2025),
        ("Xperia 10 VII", "XQ-FS22", 2025),
        ("Xperia 1 VI", "XQ-EC54", 2024),
        ("Xperia 10 VI", "XQ-ES54", 2024),
        ("Xperia 1 V", "XQ-DQ54", 2023),
        ("Xperia 5 V", "XQ-DE54", 2023),
        ("Xperia 10 V", "XQ-DC54", 2023),
        ("Xperia 1 IV", "XQ-CT54", 2022),
        ("Xperia 5 IV", "XQ-CQ54", 2022),
        ("Xperia 10 IV", "XQ-CC54", 2022),
        ("Xperia 10 III", "XQ-BT52", 2021),
    ]
    for n, m, y in sony_esim:
        add("Sony", n, m, y, True, None)

    # ============================================================
    # MOTOROLA Razr/Edge series with eSIM
    # ============================================================
    moto_esim = [
        # Razr 2025
        ("Razr Ultra 2025", "XT2551-1", 2025, None),
        ("Razr Plus 2025", "XT2551-3", 2025, None),
        ("Razr 2025", "XT2551-5", 2025, None),
        # Razr 50 series
        ("Razr 50 Ultra", "XT2451-1", 2024, None),
        ("Razr 50", "XT2453-1", 2024, None),
        # Razr 40 series
        ("Razr 40 Ultra", "XT2321-1", 2023, None),
        ("Razr 40", "XT2323-1", 2023, None),
        # Edge 60 series
        ("Edge 60 Ultra", "XT2503-1", 2025, None),
        ("Edge 60 Pro", "XT2503-1", 2025, None),
        ("Edge 60 Fusion", "XT2505-1", 2025, None),
        ("Edge 60", "XT2505-1", 2025, None),
        # Edge 50 series
        ("Edge 50 Ultra", "XT2401-1", 2024, None),
        ("Edge 50 Pro", "XT2403-2", 2024, None),
        ("Edge 50 Fusion", "XT2429-1", 2024, None),
        ("Edge 50 Neo", "XT2409-3", 2024, None),
        ("Edge 50", "XT2407-3", 2024, None),
        # Edge 40 series
        ("Edge 40 Pro", "XT2301-4", 2023, None),
        ("Edge 40 Neo", "XT2307-1", 2023, None),
        ("Edge 40", "XT2303-2", 2023, None),
        ("Edge+ (2023)", "XT2301-5", 2023, None),
        # Moto G Power 2024/2025 (eSIM confirmed on US models)
        ("Moto G Power 2025", "XT2515", 2025, None),
        ("Moto G Power 5G 2024", "XT2417", 2024, None),
        ("Moto G Stylus 5G 2024", "XT2419", 2024, None),
        # ThinkPhone
        ("ThinkPhone 25", "XT2547-1", 2025, None),
        ("ThinkPhone", "XT2309-1", 2023, None),
    ]
    for n, m, y, note in moto_esim:
        add("Motorola", n, m, y, True, note)

    # ============================================================
    # NOKIA / HMD eSIM-supporting (XR21, X30, G60, Skyline)
    # ============================================================
    for n, m, y, note in [
        ("XR21", "TA-1486", 2023, None),
        ("X30 5G", "TA-1450", 2022, None),
        ("G60 5G", "TA-1447", 2022, None),
    ]:
        add("Nokia", n, m, y, True, note)
    for n, m, y, note in [
        ("Skyline", "TA-1614", 2024, None),
    ]:
        add("HMD", n, m, y, True, note)

    # ============================================================
    # ASUS Zenfone 9+/ROG Phone 8+ with eSIM
    # ============================================================
    asus_esim = [
        ("Zenfone 12 Ultra", "AI2501", 2025),
        ("Zenfone 11 Ultra", "AI2401", 2024),
        ("Zenfone 10", "AI2302", 2023),
        ("Zenfone 9", "AI2202", 2022),
        ("ROG Phone 10 Pro", "AI2601", 2025),
        ("ROG Phone 10", "AI2601", 2025),
        ("ROG Phone 9 Pro", "AI2501", 2024),
        ("ROG Phone 9", "AI2501", 2024),
        ("ROG Phone 8 Pro Edition", "AI2401_H", 2024),
        ("ROG Phone 8 Pro", "AI2401_H", 2024),
        ("ROG Phone 8", "AI2401", 2024),
    ]
    for n, m, y in asus_esim:
        add("Asus", n, m, y, True, None)

    # ============================================================
    # NOTHING Phone (2), Phone (3), CMF Phone with eSIM
    # ============================================================
    for n, m, y in [
        ("Phone (3)", "A028", 2025),
        ("Phone (2)", "A065", 2023),
    ]:
        add("Nothing", n, m, y, True, None)

    # ============================================================
    # FAIRPHONE 5, 6 with eSIM
    # ============================================================
    for n, m, y in [("Fairphone 6", "FP6", 2025), ("Fairphone 5", "FP5", 2023)]:
        add("Fairphone", n, m, y, True, None)

    # ============================================================
    # RAKUTEN — eSIM-first carrier Japan
    # ============================================================
    for n, m, y in [
        ("Rakuten Hand 5G", "P780", 2022),
        ("Rakuten Hand", "P710", 2020),
        ("Rakuten BIG s", "P780S", 2021),
        ("Rakuten BIG", "P770", 2020),
        ("Rakuten Mini", "C330", 2019),
    ]:
        add("Rakuten", n, m, y, True, "JP domestic")

    # ============================================================
    # MICROSOFT Surface Pro/Go/Duo with eSIM
    # ============================================================
    for n, m, y in [
        ("Surface Pro 11 (5G)", "2076", 2024),
        ("Surface Pro 9 5G", "1998", 2022),
        ("Surface Pro X", "1876", 2019),
        ("Surface Pro LTE Advanced", "1807", 2018),
        ("Surface Go 3 LTE", "1901", 2021),
        ("Surface Go 2 LTE", "1927", 2020),
        ("Surface Duo 2", "1930", 2021),
        ("Surface Duo", "1930", 2020),
    ]:
        add("Microsoft", n, m, y, True, "Cellular · eSIM only")

    # ============================================================
    # LENOVO Tab P/M with 5G eSIM
    # ============================================================
    for n, m, y in [
        ("Tab P12 Pro 5G", "TB-Q706F", 2022),
        ("Tab P11 Pro 5G", "TB-J716F", 2021),
        ("Tab P11 5G", "TB-J607Z", 2021),
        ("Tab M11 5G", "TB-330F", 2024),
        ("Legion Tab 5G", "TB-320F", 2024),
    ]:
        add("Lenovo", n, m, y, True, "Cellular")

    # ============================================================
    # CELLULAR WATCHES — Garmin, Fitbit, TicWatch, Amazfit
    # ============================================================
    for n, y in [
        ("Fenix 8 (LTE)", 2024), ("Fenix 7X (LTE)", 2022),
        ("Enduro 3 (LTE)", 2024), ("Forerunner 265 (LTE)", 2023),
        ("Forerunner 945 LTE", 2020), ("Forerunner 965 (LTE)", 2023),
        ("Instinct 3 (LTE)", 2025),
        ("Venu 3 (LTE)", 2023), ("Vivoactive 5 (LTE)", 2023),
        ("Bounce (Kids LTE)", 2022),
    ]:
        add("Garmin", n, "—", y, True, "Cellular · eSIM only")
    for n, y in [
        ("Sense 2 (LTE)", 2022), ("Ace LTE", 2024),
    ]:
        add("Fitbit", n, "—", y, True, "Cellular · eSIM only")
    for n, y in [
        ("TicWatch Pro 5 (LTE)", 2024), ("TicWatch Pro 3 GPS (LTE)", 2020),
        ("TicWatch Pro 4G/LTE", 2019),
    ]:
        add("Mobvoi", n, "—", y, True, "Cellular · eSIM only")
    for n, y in [
        ("Amazfit T-Rex Ultra (eSIM)", 2024),
    ]:
        add("Amazfit", n, "—", y, True, "Cellular · eSIM only")

    # ============================================================
    # MOBILE HOTSPOTS with eSIM
    # ============================================================
    hotspots = [
        ("Netgear", "Nighthawk M6 Pro 5G", "MR6500", 2023),
        ("Netgear", "Nighthawk M6 5G", "MR6110", 2022),
        ("Netgear", "Nighthawk M5 5G", "MR5200", 2021),
        ("Netgear", "Aircard 800S", "AC800S", 2019),
        ("Solis", "Solis Lite", "—", 2021),
        ("Solis", "Solis 5G", "—", 2023),
        ("Solis", "Solis 4G+", "—", 2022),
        ("GlocalMe", "G4 Pro", "G4 Pro", 2020),
        ("GlocalMe", "Numen Air", "Numen Air", 2022),
        ("GlocalMe", "KeyTracker Air", "KT Air", 2024),
        ("Alcatel", "LinkZone 5G", "MW5001", 2022),
        ("TP-Link", "M7000 5G", "M7000 5G", 2023),
        ("Franklin Wireless", "T10 5G", "T10", 2023),
        ("Franklin Wireless", "JEXtream RG2100", "RG2100", 2024),
        ("Inseego", "MiFi X PRO 5G", "M3000", 2022),
        ("Inseego", "5G MiFi M2000", "M2000", 2021),
    ]
    for brand, n, m, y in hotspots:
        add(brand, n, m, y, True, "Mobile hotspot")

    # ============================================================
    # CONNECTED CARS with eSIM (SIM slot for vehicle telematics)
    # ============================================================
    connected_cars = [
        ("Tesla", "Model S (eSIM)", 2020),
        ("Tesla", "Model 3 (eSIM)", 2020),
        ("Tesla", "Model X (eSIM)", 2020),
        ("Tesla", "Model Y (eSIM)", 2020),
        ("Tesla", "Cybertruck (eSIM)", 2023),
        ("BMW", "iX (eSIM)", 2021),
        ("BMW", "i4 (eSIM)", 2022),
        ("Audi", "e-tron (eSIM)", 2019),
        ("Mercedes-Benz", "EQS (eSIM)", 2021),
        ("Volvo", "EX90 (eSIM)", 2024),
        ("Polestar", "Polestar 2 (eSIM)", 2020),
        ("Rivian", "R1T (eSIM)", 2021),
        ("Rivian", "R1S (eSIM)", 2022),
        ("Ford", "Mustang Mach-E (eSIM)", 2020),
        ("Ford", "F-150 Lightning (eSIM)", 2022),
    ]
    for brand, name, year in connected_cars:
        add(brand, name, "—", year, True, "Vehicle telematics · eSIM only")


if __name__ == "__main__":
    print("Import via build_devices.py")
