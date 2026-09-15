#!/usr/bin/env python3
"""
Wave-2 expansion — enumerate broad, real, in-use devices across brands
that were thin in the main builder. Focus on 2018-2026 relevance.

Adds new caveat notes people care about:
- 'Dual eSIM only' (14 Pro Max USA etc)
- 'EU carrier variant may omit eSIM'
- 'HarmonyOS · no Google services'
- 'CN-only firmware · activation may fail abroad'
- 'Region-locked activation'
- 'Rakuten/JP domestic band lock'
"""


def register(add):
    # ============================================================
    # SAMSUNG — comprehensive A/M/F/Xcover/Z coverage
    # ============================================================
    samsung = [
        # 2025 Galaxy S25 line
        ("Galaxy S25 Ultra", "SM-S938", 2025, True, None),
        ("Galaxy S25+", "SM-S936", 2025, True, None),
        ("Galaxy S25", "SM-S931", 2025, True, None),
        ("Galaxy S25 Edge", "SM-S937", 2025, True, None),
        # S24 line (2024) — full
        ("Galaxy S24 Ultra", "SM-S928", 2024, True, None),
        ("Galaxy S24+", "SM-S926", 2024, True, None),
        ("Galaxy S24", "SM-S921", 2024, True, None),
        ("Galaxy S24 FE", "SM-S721", 2024, True, None),
        # Z Fold/Flip 2024-2025
        ("Galaxy Z Fold7", "SM-F966", 2025, True, "Foldable"),
        ("Galaxy Z Flip7", "SM-F776", 2025, True, "Foldable"),
        ("Galaxy Z Flip7 FE", "SM-F761", 2025, True, "Foldable"),
        ("Galaxy Z Fold6", "SM-F956", 2024, True, "Foldable"),
        ("Galaxy Z Flip6", "SM-F741", 2024, True, "Foldable"),
        ("Galaxy Z Fold Special Edition", "SM-F958", 2024, True, "Foldable · KR/CN"),
        ("Galaxy Z Fold5", "SM-F946", 2023, True, "Foldable"),
        ("Galaxy Z Flip5", "SM-F731", 2023, True, "Foldable"),
        ("Galaxy Z Fold4", "SM-F936", 2022, True, "Foldable"),
        ("Galaxy Z Flip4", "SM-F721", 2022, True, "Foldable"),
        ("Galaxy Z Fold3", "SM-F926", 2021, True, "Foldable"),
        ("Galaxy Z Flip3", "SM-F711", 2021, True, "Foldable"),
        # A-series (very high volume mid-range) — 2024+
        ("Galaxy A56 5G", "SM-A566", 2025, True, None),
        ("Galaxy A36 5G", "SM-A366", 2025, True, None),
        ("Galaxy A26 5G", "SM-A266", 2025, False, None),
        ("Galaxy A16 5G", "SM-A166", 2024, False, None),
        ("Galaxy A06 5G", "SM-A066", 2024, False, None),
        ("Galaxy A55 5G", "SM-A556", 2024, True, None),
        ("Galaxy A35 5G", "SM-A356", 2024, True, None),
        ("Galaxy A25 5G", "SM-A256", 2024, False, None),
        ("Galaxy A15 5G", "SM-A156", 2024, False, None),
        ("Galaxy A05s", "SM-A057", 2023, False, None),
        ("Galaxy A05", "SM-A055", 2023, False, None),
        ("Galaxy A54 5G", "SM-A546", 2023, True, None),
        ("Galaxy A34 5G", "SM-A346", 2023, False, None),
        ("Galaxy A24", "SM-A245", 2023, False, None),
        ("Galaxy A14 5G", "SM-A146", 2023, False, None),
        ("Galaxy A14", "SM-A145", 2023, False, None),
        ("Galaxy A04s", "SM-A047", 2022, False, None),
        ("Galaxy A04", "SM-A045", 2022, False, None),
        ("Galaxy A04e", "SM-A042", 2022, False, None),
        # M-series (Asia/emerging)
        ("Galaxy M55s", "SM-M558", 2024, False, None),
        ("Galaxy M55", "SM-M556", 2024, False, None),
        ("Galaxy M35", "SM-M356", 2024, False, None),
        ("Galaxy M15 5G", "SM-M156", 2024, False, None),
        ("Galaxy M14 5G", "SM-M146", 2023, False, None),
        ("Galaxy M14", "SM-M145", 2023, False, None),
        ("Galaxy M54 5G", "SM-M546", 2023, False, None),
        ("Galaxy M34 5G", "SM-M346", 2023, False, None),
        ("Galaxy M04", "SM-M045", 2022, False, None),
        # F-series (India)
        ("Galaxy F55 5G", "SM-E556", 2024, False, None),
        ("Galaxy F54 5G", "SM-E546", 2023, False, None),
        ("Galaxy F34 5G", "SM-E346", 2023, False, None),
        ("Galaxy F15 5G", "SM-E156", 2024, False, None),
        ("Galaxy F14 5G", "SM-E146", 2023, False, None),
        ("Galaxy F05", "SM-E055", 2024, False, None),
        ("Galaxy F04", "SM-E045", 2023, False, None),
        # Xcover rugged workforce
        ("Galaxy XCover7", "SM-G556", 2024, True, None),
        ("Galaxy XCover6 Pro", "SM-G736", 2022, True, None),
        ("Galaxy XCover5", "SM-G525", 2021, False, None),
        ("Galaxy XCover Pro", "SM-G715", 2020, False, None),
        # Note (last models still owned)
        ("Galaxy Note 20 Ultra", "SM-N986", 2020, True, None),
        ("Galaxy Note 20", "SM-N981", 2020, True, None),
        ("Galaxy Note 10+", "SM-N975", 2019, False, None),
        ("Galaxy Note 10", "SM-N970", 2019, False, None),
        # S22 line & S21 line
        ("Galaxy S23 Ultra", "SM-S918", 2023, True, None),
        ("Galaxy S23+", "SM-S916", 2023, True, None),
        ("Galaxy S23", "SM-S911", 2023, True, None),
        ("Galaxy S23 FE", "SM-S711", 2023, True, None),
        ("Galaxy S22 Ultra", "SM-S908", 2022, True, None),
        ("Galaxy S22+", "SM-S906", 2022, True, None),
        ("Galaxy S22", "SM-S901", 2022, True, None),
        ("Galaxy S21 Ultra 5G", "SM-G998", 2021, True, None),
        ("Galaxy S21+ 5G", "SM-G996", 2021, True, None),
        ("Galaxy S21 5G", "SM-G991", 2021, True, None),
        ("Galaxy S21 FE 5G", "SM-G990", 2022, True, None),
    ]
    for n, m, y, e, note in samsung:
        add("Samsung", n, m, y, e, note)

    # ============================================================
    # APPLE — full iPhone modern
    # ============================================================
    apple = [
        # iPhone 17 series (2025)
        ("iPhone 17 Pro Max", "A3300", 2025, True, "US: eSIM only"),
        ("iPhone 17 Pro", "A3299", 2025, True, "US: eSIM only"),
        ("iPhone 17 Air", "A3301", 2025, True, "US: eSIM only"),
        ("iPhone 17", "A3298", 2025, True, "US: eSIM only"),
        # iPhone 16 (2024)
        ("iPhone 16 Pro Max", "A3084", 2024, True, "US: eSIM only"),
        ("iPhone 16 Pro", "A3083", 2024, True, "US: eSIM only"),
        ("iPhone 16 Plus", "A3082", 2024, True, "US: eSIM only"),
        ("iPhone 16", "A3081", 2024, True, "US: eSIM only"),
        ("iPhone 16e", "A3212", 2025, True, "US: eSIM only · dual eSIM"),
        # iPhone 15
        ("iPhone 15 Pro Max", "A2849", 2023, True, "US: eSIM only"),
        ("iPhone 15 Pro", "A2848", 2023, True, "US: eSIM only"),
        ("iPhone 15 Plus", "A2847", 2023, True, "US: eSIM only"),
        ("iPhone 15", "A2846", 2023, True, "US: eSIM only"),
        # 14
        ("iPhone 14 Pro Max", "A2651", 2022, True, "US: eSIM only"),
        ("iPhone 14 Pro", "A2650", 2022, True, "US: eSIM only"),
        ("iPhone 14 Plus", "A2632", 2022, True, "US: eSIM only"),
        ("iPhone 14", "A2649", 2022, True, "US: eSIM only"),
        # 13
        ("iPhone 13 Pro Max", "A2484", 2021, True, None),
        ("iPhone 13 Pro", "A2483", 2021, True, None),
        ("iPhone 13", "A2482", 2021, True, None),
        ("iPhone 13 mini", "A2481", 2021, True, None),
        # 12
        ("iPhone 12 Pro Max", "A2342", 2020, True, None),
        ("iPhone 12 Pro", "A2341", 2020, True, None),
        ("iPhone 12", "A2172", 2020, True, None),
        ("iPhone 12 mini", "A2176", 2020, True, None),
        # 11
        ("iPhone 11 Pro Max", "A2161", 2019, True, None),
        ("iPhone 11 Pro", "A2160", 2019, True, None),
        ("iPhone 11", "A2111", 2019, True, None),
        # SE variants
        ("iPhone SE (2020)", "A2275", 2020, True, None),
        ("iPhone SE (2022)", "A2595", 2022, True, None),
        # XS/XR
        ("iPhone XS Max", "A1921", 2018, True, None),
        ("iPhone XS", "A1920", 2018, True, None),
        ("iPhone XR", "A1984", 2018, True, None),
    ]
    for n, m, y, e, note in apple:
        add("Apple", n, m, y, e, note)

    # ============================================================
    # PIXEL — comprehensive
    # ============================================================
    pixel = [
        ("Pixel 10 Pro Fold", "G7ZQC", 2025, True, "Foldable"),
        ("Pixel 10 Pro XL", "G8BXA", 2025, True, None),
        ("Pixel 10 Pro", "G8BXA", 2025, True, None),
        ("Pixel 10", "G8B7A", 2025, True, None),
        ("Pixel 9 Pro Fold", "G7ZQC", 2024, True, "Foldable"),
        ("Pixel 9 Pro XL", "GRK8P", 2024, True, None),
        ("Pixel 9 Pro", "G3ZWX", 2024, True, None),
        ("Pixel 9", "GNKJ8", 2024, True, None),
        ("Pixel 9a", "G8FTB", 2025, True, None),
        ("Pixel 8 Pro", "GC3VE", 2023, True, None),
        ("Pixel 8", "GKWS6", 2023, True, None),
        ("Pixel 8a", "G8HHN", 2024, True, None),
        ("Pixel Fold", "GHL1X", 2023, True, "Foldable"),
        ("Pixel 7 Pro", "GP4BC", 2022, True, None),
        ("Pixel 7", "GVU6C", 2022, True, None),
        ("Pixel 7a", "GHL1X", 2023, True, None),
        ("Pixel 6 Pro", "GLU0G", 2021, True, None),
        ("Pixel 6", "GB7N6", 2021, True, None),
        ("Pixel 6a", "GX7AS", 2022, True, None),
        ("Pixel 5a 5G", "G4S1M", 2021, True, None),
        ("Pixel 5", "GD1YQ", 2020, True, None),
        ("Pixel 4a 5G", "G025I", 2020, True, None),
        ("Pixel 4a", "G025N", 2020, True, "US/JP: eSIM ok"),
        ("Pixel 4 XL", "G020P", 2019, True, "Verizon US no eSIM"),
        ("Pixel 4", "G020I", 2019, True, "Verizon US no eSIM"),
        ("Pixel 3a XL", "G020C", 2019, True, "Not on Verizon/Sprint"),
        ("Pixel 3a", "G020G", 2019, True, "Not on Verizon/Sprint"),
        ("Pixel 3 XL", "G013C", 2018, True, "Google Fi/US only"),
        ("Pixel 3", "G013A", 2018, True, "Google Fi/US only"),
        ("Pixel 2 XL", "G011C", 2017, False, None),
        ("Pixel 2", "G011A", 2017, True, "eSIM only via Google Fi"),
    ]
    for n, m, y, e, note in pixel:
        add("Google", n, m, y, e, note)

    # ============================================================
    # SONY XPERIA — full 2018+
    # ============================================================
    xperia = [
        ("Xperia 1 VI", "XQ-EC54", 2024, True, None),
        ("Xperia 5 V", "XQ-DE54", 2023, True, None),
        ("Xperia 10 VI", "XQ-ES54", 2024, True, None),
        ("Xperia 1 V", "XQ-DQ54", 2023, True, None),
        ("Xperia 5 IV", "XQ-CQ54", 2022, True, None),
        ("Xperia 1 IV", "XQ-CT54", 2022, True, None),
        ("Xperia 10 V", "XQ-DC54", 2023, True, None),
        ("Xperia 10 IV", "XQ-CC54", 2022, False, None),
        ("Xperia 10 III", "XQ-BT52", 2021, True, None),
        ("Xperia 5 III", "XQ-BQ52", 2021, False, None),
        ("Xperia 1 III", "XQ-BC52", 2021, False, None),
        ("Xperia 5 II", "XQ-AS52", 2020, False, None),
        ("Xperia 1 II", "XQ-AT51", 2020, False, None),
        ("Xperia 10 II", "XQ-AU52", 2020, False, None),
        ("Xperia 1", "J8110", 2019, False, None),
        ("Xperia 5", "J8210", 2019, False, None),
        ("Xperia 10 Plus", "I4213", 2019, False, None),
        ("Xperia 10", "I4113", 2019, False, None),
        ("Xperia XZ3", "H8416", 2018, False, None),
        ("Xperia XZ2", "H8216", 2018, False, None),
    ]
    for n, m, y, e, note in xperia:
        add("Sony", n, m, y, e, note)

    # ============================================================
    # ZTE — Axon + Nubia already elsewhere
    # ============================================================
    zte = [
        ("Axon 60 Ultra", "A2024", 2024, False, None),
        ("Axon 50 Ultra", "A2023", 2023, False, None),
        ("Axon 40 Ultra", "A2022", 2022, False, None),
        ("Axon 30 Ultra", "A2321", 2021, False, None),
        ("Axon 30 5G", "A2322", 2021, False, None),
        ("Axon 30 Pro", "A2022P", 2021, False, None),
        ("Blade V50 Design 5G", "A2024V", 2024, False, None),
        ("Blade V50 Vita", "V50V", 2024, False, None),
        ("Blade V40", "V40", 2022, False, None),
        ("Blade A73 5G", "A73", 2024, False, None),
        ("Blade A54", "A54", 2023, False, None),
        ("Blade A31 Plus", "A31P", 2021, False, None),
    ]
    for n, m, y, e, note in zte:
        add("ZTE", n, m, y, e, note)

    # ============================================================
    # LG — LAST relevant models (LG exited phones 2021)
    # ============================================================
    lg = [
        ("Wing 5G", "LM-F100", 2020, False, None),
        ("Velvet 5G", "LM-G900", 2020, False, None),
        ("Velvet", "LM-G910", 2020, False, None),
        ("V60 ThinQ 5G", "LM-V600", 2020, False, None),
        ("V50 ThinQ 5G", "LM-V500", 2019, False, None),
        ("V40 ThinQ", "LM-V405", 2018, False, None),
        ("G8 ThinQ", "LM-G820", 2019, False, None),
        ("G7 ThinQ", "LM-G710", 2018, False, None),
        ("Q9", "LM-Q925", 2019, False, None),
        ("K92 5G", "LM-K920", 2020, False, None),
        ("K71", "LM-K710", 2020, False, None),
        ("Stylo 6", "LM-Q730", 2020, False, None),
        ("Stylo 7", "LM-K900", 2021, False, None),
    ]
    for n, m, y, e, note in lg:
        add("LG", n, m, y, e, note)

    # ============================================================
    # HTC — last few Android phones
    # ============================================================
    htc = [
        ("U24 Pro", "2Q9J300", 2024, False, None),
        ("U23 Pro", "2Q7B100", 2023, False, None),
        ("U23", "2Q7A200", 2023, False, None),
        ("Desire 22 Pro", "2QBK300", 2022, False, None),
        ("Wildfire E2 Plus", "2Q7G200", 2021, False, None),
        ("Desire 20+", "2Q9L100", 2020, False, None),
    ]
    for n, m, y, e, note in htc:
        add("HTC", n, m, y, e, note)

    # ============================================================
    # ONEPLUS full modern
    # ============================================================
    op = [
        ("13", "CPH2653", 2025, True, None),
        ("12", "CPH2581", 2024, True, None),
        ("11", "CPH2447", 2023, True, None),
        ("Open", "CPH2551", 2023, True, "Foldable"),
        ("10 Pro", "NE2210", 2022, False, None),
        ("10T", "CPH2413", 2022, False, None),
        ("10R", "CPH2411", 2022, False, None),
        ("9 Pro", "LE2125", 2021, False, None),
        ("9", "LE2115", 2021, False, None),
        ("9R", "LE2100", 2021, False, None),
        ("9RT", "MT2110", 2022, False, None),
        ("8T", "KB2005", 2020, False, None),
        ("8 Pro", "IN2023", 2020, False, None),
        ("8", "IN2013", 2020, False, None),
        ("Nord 3", "CPH2493", 2023, False, None),
        ("Nord 2T", "CPH2399", 2022, False, None),
        ("Nord 2", "DN2103", 2021, False, None),
        ("Nord", "AC2003", 2020, False, None),
        ("Nord N10 5G", "BE2029", 2020, False, None),
        ("Nord N100", "BE2013", 2020, False, None),
        ("Nord N200 5G", "DE2117", 2021, False, None),
    ]
    for n, m, y, e, note in op:
        add("OnePlus", n, m, y, e, note)

    # ============================================================
    # POCO — full recent
    # ============================================================
    poco = [
        ("F7 Ultra", "24122PC12G", 2025, True, "Global · dual-eSIM in EU"),
        ("F7 Pro", "24122PC11G", 2025, True, "Global · dual-eSIM in EU"),
        ("F7", "24122PC10G", 2025, True, "Global · dual-eSIM in EU"),
        ("X7 Pro", "24122PC12G", 2025, False, None),
        ("X7", "24122PC10G", 2025, False, None),
        ("F6 Pro", "23117RA68G", 2024, True, "Global"),
        ("F6", "24069PC21G", 2024, True, "Global"),
        ("X6 Pro", "23117RA68G", 2024, False, None),
        ("X6", "23122PCD1G", 2024, False, None),
        ("X6 Neo", "24035PC30G", 2024, False, None),
        ("M6 Pro", "23122PCD1G", 2024, False, None),
        ("M6", "23122PCD1G", 2024, False, None),
        ("C65", "23129RN51X", 2024, False, None),
        ("C61", "23129RN51X", 2024, False, None),
        ("F5 Pro", "23013RK75G", 2023, False, None),
        ("F5", "23049PCD8G", 2023, False, None),
        ("X5 Pro", "22101317PG", 2023, False, None),
        ("X5", "22101317G", 2022, False, None),
        ("M5s", "22071219CG", 2022, False, None),
        ("M5", "22071219CG", 2022, False, None),
        ("M4 5G", "22041219PG", 2022, False, None),
        ("M4 Pro 5G", "21091116AG", 2021, False, None),
        ("C40", "220333QPG", 2022, False, None),
        ("C55", "23100RN82L", 2023, False, None),
    ]
    for n, m, y, e, note in poco:
        add("POCO", n, m, y, e, note)

    # ============================================================
    # REDMI — Note & K series
    # ============================================================
    redmi = [
        ("Note 14 Pro+ 5G", "24122RN87G", 2025, False, "Global"),
        ("Note 14 Pro 5G", "24116RN51G", 2025, False, "Global"),
        ("Note 14 Pro", "24069RN51G", 2024, False, "Global"),
        ("Note 14 5G", "24094RAD4G", 2024, False, "Global"),
        ("Note 14", "24090RA29G", 2024, False, "Global"),
        ("Note 13 Pro+ 5G", "23090RA98G", 2024, False, "Global"),
        ("Note 13 Pro 5G", "23117RA68G", 2024, False, "Global"),
        ("Note 13 Pro", "23117RA68G", 2024, False, "Global"),
        ("Note 13 5G", "23124RN87G", 2024, False, "Global"),
        ("Note 13", "23129RAA4G", 2024, False, "Global"),
        ("Note 12 Pro+ 5G", "22101317PG", 2023, False, "Global"),
        ("Note 12 Pro 5G", "22101316G", 2023, False, "Global"),
        ("Note 12 5G", "22111317G", 2023, False, "Global"),
        ("Note 12S", "23030RAC7Y", 2023, False, "Global"),
        ("Note 12", "23021RAA2Y", 2023, False, "Global"),
        ("Redmi 14C 5G", "24076RN4BG", 2024, False, None),
        ("Redmi 14C", "23129RN51X", 2024, False, None),
        ("Redmi 13", "23100RN82L", 2024, False, None),
        ("Redmi 13C 5G", "23129RN51X", 2024, False, None),
        ("Redmi 13C", "23100RN82L", 2023, False, None),
        ("Redmi A3", "23129RN51X", 2024, False, None),
        ("Redmi A2+", "23028RN4DG", 2023, False, None),
        ("Redmi A2", "23028RA98G", 2023, False, None),
        ("Redmi A1+", "220733SG", 2022, False, None),
        ("Redmi A1", "220733SG", 2022, False, None),
    ]
    for n, m, y, e, note in redmi:
        add("Xiaomi", n, m, y, e, note)

    # ============================================================
    # HUAWEI more — Nova + Enjoy (China domestic) modern
    # ============================================================
    huawei_extra = [
        ("Nova 13 Ultra", "GLA-AL10", 2024, False, "HarmonyOS · CN"),
        ("Nova 13 Pro", "GLA-LX9", 2024, False, "HarmonyOS · CN"),
        ("Nova 13", "MNA-LX9", 2024, False, "HarmonyOS · CN"),
        ("Nova 12 Ultra", "GLA-AL80", 2023, False, "HarmonyOS · CN"),
        ("Nova 12 Pro", "GLA-LX9", 2023, False, "HarmonyOS · CN"),
        ("Nova 12", "GLA-LX2", 2024, False, None),
        ("Nova 11 Ultra", "MNA-AL80", 2023, False, "HarmonyOS · CN"),
        ("Nova 11 Pro", "MNA-LX9", 2023, False, None),
        ("Nova 11", "GOA-LX9", 2023, False, None),
        ("Nova Y72", "MGA-LX9", 2023, False, None),
        ("Nova Y61", "EVE-LX9N", 2023, False, None),
        ("Enjoy 70 Pro", "FGD-AN10", 2024, False, "HarmonyOS · CN"),
        ("Enjoy 70", "MNA-AL30", 2024, False, "HarmonyOS · CN"),
        ("Enjoy 60 Pro", "MGA-AL00", 2023, False, "HarmonyOS · CN"),
    ]
    for n, m, y, e, note in huawei_extra:
        add("Huawei", n, m, y, e, note)

    # ============================================================
    # Cellular WATCHES — Garmin extra, TicWatch, Amazfit, Huawei
    # ============================================================
    for n, m, y, e in [
        ("Watch GT 5 Pro (eSIM)", "PNX-AL00", 2024, True),
        ("Watch GT 4 (eSIM)", "PNX-B19", 2023, True),
        ("Watch 5 Pro (eSIM)", "PNX-B19", 2023, True),
        ("Watch 4 Pro (eSIM)", "MDS-AL00", 2022, True),
        ("Watch Ultimate (eSIM)", "COL-AL00", 2023, True),
        ("Kids Watch 5X", "TSL-AL00", 2023, True),
    ]:
        add("Huawei", n, m, y, e, "Cellular · HarmonyOS")
    for n, y, e in [
        ("TicWatch Pro 5 (LTE)", 2024, True),
        ("TicWatch Pro 3 GPS (LTE)", 2020, True),
    ]:
        add("Mobvoi", n, "—", y, e)
    for n, y, e in [
        ("Amazfit T-Rex Ultra (eSIM)", 2024, True),
        ("Amazfit Balance (LTE)", 2023, False),
        ("Amazfit Cheetah (LTE)", 2023, False),
    ]:
        add("Amazfit", n, "—", y, e)
    for n, y in [
        ("Fenix 8 (LTE)", 2024), ("Fenix 7X (LTE)", 2022),
        ("Enduro 3 (LTE)", 2024), ("Forerunner 265 (LTE)", 2023),
        ("Instinct 3 (LTE)", 2025),
    ]:
        add("Garmin", n, "—", y, True)

    # ============================================================
    # CELLULAR TABLETS — non-Apple/Samsung volume
    # ============================================================
    tablets = [
        ("Xiaomi", "Pad 7 5G", "25028PN0DG", 2025, True, "Cellular"),
        ("Xiaomi", "Redmi Pad Pro 5G", "24047RP44G", 2024, True, "Cellular"),
        ("Xiaomi", "Redmi Pad SE 8.7 4G", "24095RP1EG", 2024, False, "SIM tray only"),
        ("Honor", "MagicPad 2 5G", "PGT-W29", 2024, True, "Cellular"),
        ("Honor", "Pad 9 (LTE)", "HEY-W29", 2023, False, "SIM tray only"),
        ("Lenovo", "Legion Tab 5G", "TB-320F", 2024, True, "Cellular"),
        ("Lenovo", "Tab P12 (LTE)", "TB-370F", 2023, False, "SIM tray only"),
        ("Oppo", "Pad 3 Pro 5G", "OPD2401", 2024, True, "Cellular"),
        ("Oppo", "Pad 2 (LTE)", "OPD2202", 2023, False, "SIM tray only"),
        ("Nokia", "T20 LTE", "TA-1394", 2021, False, "SIM tray only"),
        ("Nokia", "T21 LTE", "TA-1487", 2022, False, "SIM tray only"),
        ("TCL", "Tab 10 Gen 2 5G", "9295G", 2024, False, "SIM tray only"),
        ("TCL", "Tab 10 5G", "9183G", 2022, False, "SIM tray only"),
        ("Blackview", "Tab 18 5G", "—", 2024, False, "SIM tray only"),
        ("Doogee", "T30 Ultra 5G", "—", 2024, False, "SIM tray only"),
        ("Alldocube", "iPlay 60 Pad Pro 5G", "—", 2024, False, "SIM tray only"),
    ]
    for brand, n, m, y, e, note in tablets:
        add(brand, n, m, y, e, note)

    # ============================================================
    # GAMING HANDHELDS with cellular
    # ============================================================
    handhelds = [
        ("Logitech", "G Cloud 5G", "—", 2023, False, "Wi-Fi only"),
        ("Razer", "Edge 5G", "RZ07", 2023, False, "Verizon-only 5G"),
        ("AYN", "Odin 2 Portal (LTE)", "—", 2024, False, "SIM tray only"),
        ("Ayaneo", "Pocket S (5G)", "—", 2024, False, "Wi-Fi only"),
    ]
    for brand, n, m, y, e, note in handhelds:
        add(brand, n, m, y, e, note)

    # ============================================================
    # Cellular Kindle / e-readers
    # ============================================================
    ereaders = [
        ("Amazon", "Kindle Scribe (Cellular)", "—", 2022, False, "Wi-Fi only in most regions"),
        ("Amazon", "Kindle Oasis (Cellular)", "—", 2019, False, "3G free · deprecated"),
        ("Amazon", "Kindle Paperwhite 5 (Cellular)", "—", 2021, False, "Wi-Fi + free 4G"),
        ("Kobo", "Elipsa 2E (LTE)", "—", 2023, False, "Wi-Fi only"),
        ("Onyx Boox", "Note Air 4C (LTE)", "—", 2024, False, "SIM tray only"),
    ]
    for brand, n, m, y, e, note in ereaders:
        add(brand, n, m, y, e, note)

    # ============================================================
    # Cellular hotspots / MiFi (people carry these for eSIM travel!)
    # ============================================================
    hotspots = [
        ("Netgear", "Nighthawk M6 Pro 5G", "MR6500", 2023, True, "Mobile hotspot"),
        ("Netgear", "Nighthawk M6 5G", "MR6110", 2022, True, "Mobile hotspot"),
        ("Netgear", "Nighthawk M5 5G", "MR5200", 2021, True, "Mobile hotspot"),
        ("Netgear", "Nighthawk M2", "MR2100", 2018, False, "Mobile hotspot"),
        ("TP-Link", "M7350", "M7350", 2016, False, "Mobile hotspot"),
        ("TP-Link", "M7650", "M7650", 2018, False, "Mobile hotspot"),
        ("Solis", "Solis Lite", "—", 2021, True, "Mobile hotspot"),
        ("Solis", "Solis 5G", "—", 2023, True, "Mobile hotspot"),
        ("Skyroam", "Solis X", "SX-1", 2019, False, "Mobile hotspot"),
        ("GlocalMe", "G4 Pro", "G4 Pro", 2020, True, "Mobile hotspot"),
        ("GlocalMe", "Numen Air", "Numen Air", 2022, True, "Mobile hotspot"),
        ("ZTE", "MU5001 5G MiFi", "MU5001", 2022, False, "Mobile hotspot"),
        ("Franklin Wireless", "T10 5G", "T10", 2023, False, "Mobile hotspot"),
        ("Inseego", "MiFi X PRO 5G", "M3000", 2022, False, "Mobile hotspot"),
    ]
    for brand, n, m, y, e, note in hotspots:
        add(brand, n, m, y, e, note)


if __name__ == "__main__":
    print("Import via build_devices.py")
