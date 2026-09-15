#!/usr/bin/env python3
"""
ARC 2 MASS 2: Even more archive volume.
- Japanese carrier-branded devices (NTT DoCoMo, au KDDI, SoftBank)
- Historical CDMA (US carriers: Verizon, Sprint, US Cellular)
- More Chinese OEMs (ZTE full historical, Coolpad, Gionee, Meizu, etc.)
- Feature phones (KaiOS, Symbian S40/S60)
- Amazon Kindle, e-readers, IoT/M2M
- More Indian OEMs (Lava, Karbonn, Intex, Micromax full catalog)
- African/LATAM brands
"""


def register(add):
    # ============================================================
    # ZTE — full historical catalog
    # ============================================================
    zte = [
        # Blade series (very extensive)
        ("Blade", "A315", 2011), ("Blade II", "V880+", 2012),
        ("Blade III", "V889M", 2012), ("Blade III Pro", "V889M", 2012),
        ("Blade Vec 4G", "V889M", 2014), ("Blade S6", "P839F50", 2015),
        ("Blade S6 Plus", "P839T20", 2015), ("Blade S7", "S7Q", 2015),
        ("Blade V6", "T660", 2015), ("Blade V6 Max", "V5 Max", 2015),
        ("Blade V6 Plus", "V6 Plus", 2015), ("Blade V7", "V7", 2016),
        ("Blade V7 Lite", "V7 Lite", 2016), ("Blade V7 Max", "V7 Max", 2016),
        ("Blade V7 Plus", "V7 Plus", 2016), ("Blade V8", "V0800", 2017),
        ("Blade V8 Lite", "V0800L", 2017), ("Blade V8 Mini", "V0800M", 2017),
        ("Blade V8 Pro", "Z978", 2017), ("Blade V9", "V1050", 2018),
        ("Blade V9 Vita", "V1050V", 2018), ("Blade V10", "V1000", 2019),
        ("Blade V10 Vita", "V1000V", 2019), ("Blade 10", "8010", 2019),
        ("Blade 10 Prime", "Z6410", 2019), ("Blade 20", "8010", 2020),
        ("Blade 20 5G", "V2050", 2020), ("Blade 20 Pro 5G", "V2050", 2020),
        ("Blade 20 Smart", "V2050", 2020), ("Blade A1", "C880A", 2015),
        ("Blade A2", "BA610C", 2016), ("Blade A2 Plus", "BA910", 2016),
        ("Blade A3 (2020)", "8010", 2019), ("Blade A31", "8012N", 2020),
        ("Blade A31 Lite", "8010", 2020), ("Blade A5 (2020)", "8010", 2020),
        ("Blade A51", "8010N", 2021), ("Blade A51 Lite", "8010", 2021),
        ("Blade A7 (2020)", "9000N", 2020), ("Blade A7 Prime", "9000N", 2020),
        ("Blade A71", "9000N", 2021), ("Blade A72", "9000N", 2022),
        ("Blade Apex", "P743T", 2013), ("Blade C", "V807", 2012),
        ("Blade C2", "V889D", 2013), ("Blade G", "V870", 2013),
        ("Blade G Lux", "V830", 2014), ("Blade G Pro", "V889D", 2013),
        ("Blade L2", "V815W", 2014), ("Blade L3", "L3", 2015),
        ("Blade L3 Plus", "L3 Plus", 2015), ("Blade L5", "L5", 2016),
        ("Blade L5 Plus", "L5 Plus", 2016), ("Blade L6", "L6", 2016),
        ("Blade L7", "A320", 2017), ("Blade L110", "L110", 2015),
        ("Blade L130", "L130", 2019), ("Blade Q", "Q", 2012),
        ("Blade Q Maxi", "Q Maxi", 2013), ("Blade Q Mini", "Q Mini", 2013),
        ("Blade Q Pro", "Q Pro", 2013), ("Blade Q Lux", "Q Lux", 2014),
        ("Blade Q Lux 3G", "Q Lux 3G", 2014), ("Blade Q Lux 4G", "Q Lux 4G", 2015),
        ("Blade X", "Z965", 2017), ("Blade X Max", "Z983", 2017),
        ("Blade Z Max", "Z982", 2017),
        # Axon (early)
        ("Axon", "A1P", 2015), ("Axon Elite", "A2015", 2015),
        ("Axon Lux", "S3003", 2015), ("Axon Max", "C2016", 2015),
        ("Axon Mini", "B2015", 2015), ("Axon Pro", "A1P", 2015),
        ("Axon 7", "A2017U", 2016), ("Axon 7 Max", "C2017", 2016),
        ("Axon 7 mini", "B2017G", 2016), ("Axon 7s", "A2018", 2017),
        ("Axon M", "Z999", 2017), ("Axon 9 Pro", "A2019", 2018),
        ("Axon 10 Pro", "A2020", 2019), ("Axon 10 Pro 5G", "A2020G", 2019),
        ("Axon 11", "A2021", 2020), ("Axon 11 5G", "A2021G", 2020),
        ("Axon 11 SE 5G", "A2022", 2020), ("Axon 20 5G", "A2022G", 2020),
        ("Axon 30", "A2023", 2021), ("Axon 30 Pro", "A2023P", 2021),
        ("Axon 30 5G", "A2022", 2021), ("Axon 30 Ultra", "A2321", 2021),
        # Grand series
        ("Grand X", "V970", 2012), ("Grand X2", "V967S", 2013),
        ("Grand X Max", "V987", 2014), ("Grand X Max+", "Z787", 2014),
        ("Grand Xtreme", "V987", 2014), ("Grand Memo", "N5", 2013),
        ("Grand Memo II", "N9520", 2014), ("Grand Memo II LTE", "N9521", 2014),
        ("Grand Era", "V985", 2013), ("Grand Era U985", "U985", 2013),
        ("Grand S", "S3", 2013), ("Grand S II", "S291", 2014),
        ("Grand SII LTE", "S291", 2014), ("Grand S Flex", "S291", 2014),
        ("Grand S Pro", "N9835", 2014),
        # Nubia (before ZTE spinoff took Nubia)
        ("Nubia Z5", "NX501", 2013), ("Nubia Z5 mini", "NX402", 2013),
        ("Nubia Z5S", "NX503A", 2013), ("Nubia Z5S mini", "NX403A", 2013),
        ("Nubia Z7", "NX506J", 2014), ("Nubia Z7 Max", "NX505J", 2014),
        ("Nubia Z7 mini", "NX507J", 2014), ("Nubia Z9", "NX508J", 2015),
        ("Nubia Z9 Max", "NX510J", 2015), ("Nubia Z9 mini", "NX511J", 2015),
        ("Nubia Z11", "NX531J", 2016), ("Nubia Z11 Max", "NX535J", 2016),
        ("Nubia Z11 mini", "NX529J", 2016), ("Nubia Z11 mini S", "NX549J", 2016),
        ("Nubia Z17", "NX563J", 2017), ("Nubia Z17 mini", "NX569J", 2017),
        ("Nubia Z17s", "NX595J", 2017), ("Nubia Z18", "NX606J", 2018),
        ("Nubia Z18 mini", "NX611J", 2018), ("Nubia Z20", "NX627J", 2019),
        ("Nubia N1", "NX541J", 2016), ("Nubia N2", "NX575J", 2017),
        ("Nubia N3", "NX608J", 2018), ("Nubia M2", "NX551J", 2017),
        ("Nubia M2 Play", "NX907J", 2017), ("Nubia M2 lite", "NX573J", 2017),
        # Nubia Red Magic (early)
        ("Red Magic", "NX609J", 2018), ("Red Magic Mars", "NX619J", 2018),
        ("Red Magic 3", "NX629J", 2019), ("Red Magic 3S", "NX629J", 2019),
        ("Red Magic 5G", "NX659J", 2020), ("Red Magic 5S", "NX669J", 2020),
        ("Red Magic 6", "NX669J", 2021), ("Red Magic 6 Pro", "NX669J", 2021),
        ("Red Magic 6R", "NX666J", 2021), ("Red Magic 6S Pro", "NX669J", 2021),
        # Legacy phones
        ("Kis", "V788D", 2013), ("Kis 3", "V790", 2013), ("Kis 3 Max", "V815W", 2014),
        ("N799D", "N799D", 2013), ("N880F", "N880F", 2013), ("N880S", "N880S", 2013),
        ("Nova 2S", "P945A20", 2014), ("Nova 3.2", "P743T", 2013),
        ("Nova 3.5", "V870", 2013), ("Open", "Open", 2013), ("Open 2", "Open C", 2014),
        ("Open C", "Open C", 2014), ("Open L", "Open L", 2015), ("Optik", "V55", 2012),
        ("Orbit", "A1", 2012), ("Overture", "Z995", 2013), ("Overture 2", "Z855", 2015),
        ("Overture 3", "Z851", 2016), ("Prelude", "Z998", 2013),
        ("Prelude 2", "Z667", 2014), ("Prelude+", "Z853", 2014),
        ("Racer", "X850", 2010), ("Racer II", "X8", 2011), ("Radiant", "Z740", 2013),
        ("Reef", "N810", 2011), ("Rhapsody", "T18", 2012), ("Roamer", "R11", 2010),
        ("Salute", "F327", 2013), ("Score", "X500", 2012), ("Score M", "X501", 2013),
        ("Sonata", "Z750C", 2012), ("Sonata 2", "Z755", 2014), ("Sonata 3", "Z832", 2016),
        ("Sonata 4G", "Z755", 2015), ("Speed", "N9130", 2014), ("Spro Plus", "MF97G", 2016),
        ("Star", "MW01", 2014), ("Star 2", "MW04", 2015), ("Style Pro", "V861", 2014),
        ("Tania", "V8306", 2012), ("Tempo Go", "N9137", 2018),
        ("Trek 2 HD", "K88", 2015), ("Twist", "V4", 2013), ("V6", "V6", 2015),
        ("V6 Plus", "V6 Plus", 2015), ("V7", "V7", 2016), ("V7 Lite", "V7 Lite", 2016),
        ("V860", "V860", 2011), ("V889", "V889", 2012), ("V96", "V96", 2010),
        ("Warp", "N860", 2011), ("Warp 2", "N861", 2012), ("Warp 3", "N860S", 2012),
        ("Warp 4G", "N9510", 2013), ("Warp 7", "N9519", 2016), ("Warp Elite", "N9518", 2015),
        ("Warp LTE", "N9510", 2013), ("Warp Sequent", "N861", 2012),
        ("Warp Sync", "N9515", 2014), ("Whirl 2", "Z667T", 2014),
        ("Zephyr", "Z752C", 2013), ("Zephyr Plus", "Z753", 2014), ("Zinger", "Z667", 2014),
        # Home tablets/hotspots
        ("V71C", "V71C", 2011), ("V72C", "V72C", 2012), ("V81", "V81", 2011),
        ("V9", "V9", 2010), ("V9+", "V9+", 2011), ("V9A", "V9A", 2011),
        ("V96A", "V96A", 2011),
    ]
    for n, m, y in zte:
        add("ZTE", n, m, y, False, None)

    # ============================================================
    # COOLPAD / GIONEE / MEIZU / SMARTISAN / LEEcO / ZUK
    # ============================================================
    coolpad = [
        ("Cool Play 6", "C107", 2017), ("Cool Play 7", "C107", 2018),
        ("Cool 1 Dual", "C103", 2016), ("Cool 2", "C105", 2017),
        ("Cool Changer 1C", "C105-6", 2017), ("Cool Dazen X7", "8720", 2015),
        ("Cool M7", "M7", 2016), ("Cool S1", "C105-6", 2016),
        ("Note 3", "8676-A01", 2015), ("Note 3 Lite", "8298-A01", 2015),
        ("Note 3 Plus", "8676-M01", 2015), ("Note 5", "C103", 2016),
        ("Note 5 Lite", "3600i", 2017), ("Note 5 Lite C", "3705AS", 2017),
        ("Note 6 Lite", "N2M", 2018), ("Note 8", "8300", 2018),
        ("Torino R108", "R108", 2015), ("Torino S", "E561", 2015),
        ("TipTop 2 T2-00", "T2-00", 2014), ("TipTop 3", "T3-01", 2015),
        ("Modena 2", "E502", 2015), ("Porto", "E560", 2015),
        ("Roar Plus", "8722V", 2015), ("Roar A110", "A110", 2015),
        ("Sky 3", "E502", 2015), ("Legacy S", "3705A", 2018),
        ("Legacy", "3705AS", 2018), ("Cool 6", "1873", 2020),
        ("Cool 12", "2318", 2022), ("Cool 20 5G", "2265", 2021),
        ("Cool 20 Pro", "2266", 2021), ("Cool 30", "2318", 2022),
        ("Cool 30 Pro", "2318", 2022),
    ]
    for n, m, y in coolpad:
        add("Coolpad", n, m, y, False, None)

    gionee = [
        ("Elife E7", "E7", 2013), ("Elife E7 Mini", "E7 Mini", 2013),
        ("Elife E8", "E8", 2015), ("Elife S5.5", "S5.5", 2014),
        ("Elife S5.5L", "S5.5L", 2014), ("Elife S6", "GN9010", 2016),
        ("Elife S6 Pro", "GN9012", 2016), ("Elife S6s", "S6s", 2016),
        ("Elife S7", "GN9006", 2015), ("Elife S8", "S8", 2016),
        ("Elife S Plus", "GN9011", 2015),
        ("Marathon M2", "M2", 2014), ("Marathon M3", "M3", 2015),
        ("Marathon M4", "M4", 2015), ("Marathon M5", "M5", 2015),
        ("Marathon M5 Enjoy", "M5", 2015), ("Marathon M5 Lite", "M5 Lite", 2016),
        ("Marathon M5 Mini", "M5 Mini", 2016), ("Marathon M5 Plus", "M5 Plus", 2016),
        ("Marathon M6", "M6", 2016), ("Marathon M6 Plus", "M6 Plus", 2016),
        ("Marathon M7", "M7", 2017), ("Marathon M7 Plus", "M7 Plus", 2017),
        ("Marathon M7 Power", "M7 Power", 2017),
        ("A1", "GN5003", 2017), ("A1 Lite", "GN5003L", 2017),
        ("A1 Plus", "GN5005", 2017),
        ("F103", "F103", 2015), ("F103 Pro", "F103 Pro", 2016),
        ("F109", "F109", 2016), ("F205", "F205", 2018),
        ("F5", "F5", 2015), ("F6", "F6", 2018), ("F6 (2019)", "F6", 2019),
        ("F8", "F8", 2019), ("F9", "F9", 2019), ("F9 Plus", "F9 Plus", 2019),
        ("F11", "F11", 2020), ("F103S", "F103S", 2016), ("F205 Pro", "F205 Pro", 2018),
        ("K3", "K3", 2019), ("K30 Pro", "K30 Pro", 2019),
        ("M15", "M15", 2020), ("M17", "M17", 2020),
        ("M30", "M30", 2020), ("M30 Pro", "M30 Pro", 2020),
        ("P8W", "P8W", 2016), ("P8 Max", "P8 Max", 2015),
        ("P4", "P4", 2015), ("P5 Mini", "P5 Mini", 2015),
        ("P5W", "P5W", 2016), ("P5L CDMA", "P5L", 2015),
        ("P7", "P7", 2016), ("P7 Max", "P7 Max", 2016),
        ("Pioneer P1", "P1", 2013), ("Pioneer P2", "P2", 2013),
        ("Pioneer P3", "P3", 2013), ("Pioneer P3S", "P3S", 2014),
        ("Pioneer P4", "P4", 2014), ("Pioneer P5W", "P5W", 2015),
        ("Pioneer P6", "P6", 2015), ("Pioneer P8W", "P8W", 2015),
        ("Steel", "GN5001", 2015), ("Steel 2", "GN5005", 2017),
    ]
    for n, m, y in gionee:
        add("Gionee", n, m, y, False, None)

    for n, m, y in [
        ("M3", "M081", 2014), ("M3 Note", "L681H", 2015),
        ("M3 Note (S)", "M681Q", 2016), ("M3 Max", "M3 Max", 2016),
        ("M3s", "Y685H", 2016), ("M5", "M5", 2015), ("M5s", "M5s", 2016),
        ("M5c", "M710M", 2017), ("M5 Note", "M621H", 2016),
        ("M6", "M711H", 2016), ("M6 Note", "M721H", 2017),
        ("M6s", "M712H", 2017), ("M6T", "M811Q", 2018), ("M8", "M813H", 2018),
        ("M8c", "M810L", 2018), ("M8 Lite", "M816H", 2018),
        ("M9", "M9", 2015), ("M9 Note", "M9 Note", 2017),
        ("Note 8", "M822H", 2018), ("Note 9", "M923H", 2019),
        ("15", "M881H", 2018), ("15 Lite", "M871H", 2018),
        ("15 Plus", "M891Q", 2018), ("16", "M872H", 2018),
        ("16 Plus", "M892Q", 2018), ("16s", "M971H", 2019),
        ("16s Pro", "M972H", 2019), ("16T", "M928Q", 2019),
        ("16Xs", "M926H", 2019), ("16th", "M872H", 2018),
        ("17", "M081Q", 2020), ("17 Pro", "M092Q", 2020),
        ("18", "M181Q", 2021), ("18 Pro", "M182Q", 2021), ("18s", "M181S", 2021),
        ("18X", "M181X", 2021), ("Pro 5", "PRO 5", 2015),
        ("Pro 6", "PRO 6", 2016), ("Pro 6 Plus", "PRO 6 Plus", 2016),
        ("Pro 6s", "PRO 6s", 2016), ("Pro 7", "M792Q", 2017),
        ("Pro 7 Plus", "M793Q", 2017),
        ("MX2", "M045", 2012), ("MX3", "M351", 2013), ("MX4", "M460", 2014),
        ("MX4 Pro", "M462U", 2014), ("MX5", "M575M", 2015), ("MX6", "M685Q", 2016),
        ("MX 6th", "M685Q", 2016),
    ]:
        add("Meizu", n, m, y, False, None)

    for n, y in [
        ("T1", 2015), ("T2 Pro", 2016), ("U1", 2016), ("Nut", 2016),
        ("Nut Pro", 2017), ("Nut Pro 2", 2018), ("Nut Pro 2S", 2018),
        ("Nut 3", 2018), ("Nut R1", 2018), ("Nut Pro 3", 2020),
        ("R2", 2019), ("Nut Air 2020", 2020), ("Jianguo 3", 2019),
        ("Jianguo Pro 3", 2020),
    ]:
        add("Smartisan", n, "—", y, False, None)

    for n, m, y in [
        ("Le 1", "Le 1", 2015), ("Le 1s", "Le 1s", 2015),
        ("Le 1 Pro", "Le 1 Pro", 2015), ("Le 2", "Le 2", 2016),
        ("Le 2 Pro", "Le 2 Pro", 2016), ("Le Max", "Le Max", 2015),
        ("Le Max 2", "Le Max 2", 2016), ("Le Max Pro", "Le Max Pro", 2015),
        ("Le Pro 3", "Le Pro 3", 2016), ("Le Pro 3 AI Edition", "Le Pro 3 AI", 2017),
        ("Le S3", "Le S3", 2016), ("Cool 1 Dual", "Cool 1 Dual", 2016),
    ]:
        add("LeEco / LeTV", n, m, y, False, None)

    for n, m, y in [
        ("Z1", "Z1221", 2015), ("Z2", "Z2131", 2016), ("Z2 Pro", "Z2121", 2016),
        ("Edge", "Z2151", 2017), ("Edge 32", "Z2151", 2017),
    ]:
        add("ZUK", n, m, y, False, None)

    # ============================================================
    # LARGE INDIAN/EMERGING MARKET catalogs
    # ============================================================
    lava = [
        ("Iris 300", 2011), ("Iris 302 Style", 2013), ("Iris 349+", 2013),
        ("Iris 349i", 2013), ("Iris 356", 2013), ("Iris 360 Music", 2013),
        ("Iris 400 Colour", 2012), ("Iris 400 Q", 2013), ("Iris 401e", 2013),
        ("Iris 402", 2013), ("Iris 402+", 2013), ("Iris 404 Flair", 2014),
        ("Iris 405", 2013), ("Iris 405+", 2014), ("Iris 406Q", 2014),
        ("Iris 410", 2013), ("Iris 411", 2013), ("Iris 412", 2014),
        ("Iris 414", 2014), ("Iris 415", 2015), ("Iris 456", 2013),
        ("Iris 458Q", 2014), ("Iris 465", 2015), ("Iris 501", 2012),
        ("Iris 502", 2013), ("Iris 503", 2013), ("Iris 504q", 2014),
        ("Iris 505", 2013), ("Iris 550Q", 2014), ("Iris 600", 2011),
        ("Iris 700", 2011), ("Iris 702", 2013), ("Iris 758", 2015),
        ("Iris 810", 2013), ("Iris 870", 2015), ("Iris Alfa", 2015),
        ("Iris Alfa L", 2015), ("Iris Atom", 2016), ("Iris Atom 2X", 2016),
        ("Iris Fuel 25", 2015), ("Iris Fuel 50", 2015), ("Iris Fuel 60", 2015),
        ("Iris Fuel F1", 2015), ("Iris Fuel F2", 2015), ("Iris N400", 2013),
        ("Iris Pro 20", 2013), ("Iris Pro 30", 2013), ("Iris Pro 30+", 2014),
        ("Iris Pro 30i", 2015), ("Iris Pro 30i (2)", 2015), ("Iris Selfie 50", 2015),
        ("Iris X1", 2014), ("Iris X1 Beats", 2015), ("Iris X1 Grand", 2014),
        ("Iris X1 Mini", 2015), ("Iris X1 Selfie", 2015), ("Iris X10", 2014),
        ("Iris X5", 2014), ("Iris X8", 2015), ("Iris X9", 2015),
        ("Xolo Q800", 2013), ("Z Series Z25", 2020), ("Z Series Z40", 2020),
        ("Z Series Z50", 2020), ("Z Series Z60", 2020), ("Z Series Z61", 2020),
        ("Z Series Z62", 2020), ("Z Series Z66", 2020), ("Z Series Z81", 2020),
        ("Z Series Z90", 2020), ("Z Series Z91", 2020),
        ("Be U", 2020), ("Blaze", 2022),
    ]
    for entry in lava:
        if len(entry) == 2:
            n, y = entry; m = "—"
        else:
            n, m, y = entry
        add("Lava", n, m, y, False, None)

    micromax = [
        ("A25", 2012), ("A27 Ninja", 2012), ("A34 Bolt", 2013), ("A35 Bolt", 2013),
        ("A36 Bolt", 2013), ("A37 Bolt", 2013), ("A46", 2013), ("A47 Bolt", 2013),
        ("A54 Ninja 3.5", 2013), ("A56 Ninja 3", 2012), ("A58 Ninja 3", 2013),
        ("A61 Bolt", 2013), ("A65 Smarty 4.3", 2013), ("A66 Canvas Fun", 2013),
        ("A67 Bolt", 2013), ("A68 Smarty 4.5", 2013), ("A69 Ninja", 2013),
        ("A71 Bolt", 2013), ("A72 Canvas Viva", 2013), ("A74 Canvas Fun", 2013),
        ("A75 Canvas Nitro", 2013), ("A76", 2012), ("A77 Canvas Juice", 2014),
        ("A79 Canvas Fire 3", 2014), ("A82 Superfone", 2013),
        ("A84 Superfone Elite", 2014), ("A88 Canvas Music", 2014),
        ("A89 Ninja", 2013), ("A90S", 2012), ("A091 Canvas Engage", 2013),
        ("A092 Unite", 2013), ("A093 Canvas Fire", 2014), ("A094 Canvas Mad", 2014),
        ("A096 Canvas Fire 3", 2014), ("A099 Canvas Xpress", 2014),
        ("A100 Canvas HD", 2013), ("A101 Canvas Doodle 3", 2014),
        ("A102 Canvas Doodle 3", 2014), ("A104 Canvas Fire 2", 2014),
        ("A105 Canvas Entice", 2014), ("A106 Unite 2", 2014),
        ("A108 Canvas L", 2014), ("A109 Canvas XL2", 2014), ("A110 Canvas 2", 2013),
        ("A111 Canvas Doodle", 2013), ("A114 Canvas 2.2", 2013),
        ("A116 Canvas HD", 2013), ("A117 Canvas Magnus", 2014),
        ("A119 Canvas XL", 2014), ("A120 Canvas 2 Colours", 2014),
        ("A177 Canvas Juice", 2015), ("A200 Canvas Turbo", 2013),
        ("A210 Canvas 4 Plus", 2014), ("A215 Canvas Elanza 2", 2014),
        ("A240 Canvas Doodle 2", 2013), ("A250 Canvas Turbo", 2013),
        ("A290 Canvas Knight Cameo", 2014), ("A300 Canvas Gold", 2014),
        ("A310 Canvas Nitro", 2014), ("A311 Canvas Nitro 2", 2015),
        ("A315 Canvas 4 Turbo", 2014), ("A350 Canvas Knight", 2014),
        ("A355 Canvas Blaze 4G", 2015), ("Bolt A24", 2013), ("Bolt A26", 2013),
        ("Bolt A28", 2013), ("Bolt A46", 2014), ("Bolt A47", 2013),
        ("Bolt A61+", 2013), ("Bolt A62", 2013), ("Bolt A66", 2014),
        ("Bolt A67", 2013), ("Bolt A71", 2013), ("Bolt A82", 2013),
        ("Bolt AD3520", 2013), ("Bolt AD4500", 2014), ("Bolt D200", 2014),
        ("Bolt D303", 2014), ("Bolt D304", 2014), ("Bolt D320", 2013),
        ("Bolt Q301", 2014), ("Bolt Q324", 2015), ("Bolt Q325", 2015),
        ("Bolt Q326", 2015), ("Bolt Q327", 2015), ("Bolt Q331", 2015),
        ("Bolt Q332", 2015), ("Bolt Q333", 2015), ("Bolt Q335", 2015),
        ("Bolt Q336", 2015), ("Bolt Q338", 2015), ("Bolt Q339", 2015),
        ("Bolt Q346", 2016), ("Bolt Q381", 2015), ("Bolt Q393", 2016),
        ("Bolt Q400", 2016), ("Bolt S300", 2015), ("Canvas 4 A210", 2013),
        ("Canvas 5 E481", 2015), ("Canvas 6", 2016), ("Canvas 6 Pro", 2016),
        ("Canvas Alpha A114", 2016), ("Canvas Amaze 2", 2016),
        ("Canvas Amaze 4G", 2016), ("Canvas Amaze Q391", 2015),
        ("Canvas Blaze 4G Plus", 2015), ("Canvas Blaze 4G+ Q414", 2015),
        ("Canvas Blaze HD EG116", 2013), ("Canvas Blaze MT500", 2014),
        ("Canvas Doodle A111", 2013), ("Canvas Duet II", 2013),
        ("Canvas Elanza A121", 2013), ("Canvas Evok", 2016),
        ("Canvas Fire 5", 2016), ("Canvas Fire 6", 2016),
        ("Canvas Gold A300", 2014), ("Canvas Hue AQ5000", 2015),
        ("Canvas Hue 2 AQ5000L", 2015), ("Canvas Infinity", 2017),
        ("Canvas Infinity Life", 2018), ("Canvas Infinity Pro", 2017),
        ("Canvas Juice 3 Q392", 2015), ("Canvas Juice 3+ Q394", 2015),
        ("Canvas Juice 4 Q465", 2015), ("Canvas Knight 2", 2015),
        ("Canvas Knight 2 4G", 2015), ("Canvas Lapbook L1160", 2014),
        ("Canvas Laptab LT666", 2014), ("Canvas Laptab II LT777", 2015),
        ("Canvas Magnus HD Q422", 2015), ("Canvas Mega 4G Q417", 2015),
        ("Canvas Mega 2 Q426", 2016), ("Canvas Nitro 2 E311", 2015),
        ("Canvas Nitro 3 E352", 2015), ("Canvas Nitro 4G E455", 2015),
        ("Canvas Play Q355", 2015), ("Canvas Play 4G", 2016),
        ("Canvas Plex Tab", 2020), ("Canvas Pulse 4G E451", 2015),
        ("Canvas Selfie 2 Q4311", 2015), ("Canvas Selfie 3 E460", 2015),
        ("Canvas Selfie 4 Q349", 2015), ("Canvas Selfie AQ4501", 2015),
        ("Canvas Selfie Lens Q345", 2016), ("Canvas Sliver 5", 2015),
        ("Canvas Spark 2 Plus Q350", 2015), ("Canvas Spark 3 Q385", 2015),
        ("Canvas Spark 4G Q4201", 2016), ("Canvas Spark Q380", 2015),
        ("Canvas Turbo A250", 2013), ("Canvas Turbo Mini A200", 2014),
        ("Canvas Unite 3 Q372", 2015), ("Canvas Unite 4 Q427", 2016),
        ("Canvas Unite 4 Plus Q351+", 2016), ("Canvas Xpress 4G Q413", 2016),
        ("Canvas Xpress 4G Q414", 2016), ("Canvas Xpress Q413S", 2016),
        ("Canvas Yuphoria E4816", 2016), ("Canvas 6 E484", 2016),
        ("Canvas 6 Pro E484", 2016), ("Canvas Fire 4G Q412", 2016),
        ("Canvas Fire 4G+ Q412+", 2016), ("Canvas Nitro 4G E455", 2015),
        ("Canvas Spark 3 Q385", 2015), ("Canvas 1", 2017), ("Canvas 2", 2017),
        ("Vdeo 1", 2016), ("Vdeo 2", 2016), ("Vdeo 3", 2016),
        ("Vdeo 4", 2017), ("Vdeo 5", 2017), ("Yu Ace", 2018),
        ("Yu Yunicorn", 2016), ("Yu Yureka", 2015), ("Yu Yureka 2", 2015),
        ("Yu Yureka Black", 2016), ("Yu Yureka Note", 2015), ("Yu Yureka Plus", 2015),
        ("Yu Yureka S", 2015), ("Yu Yuphoria", 2015), ("Yu Yunique", 2015),
        ("Yu Yunique 2", 2016), ("Yu Yutopia", 2015),
    ]
    for entry in micromax:
        if len(entry) == 2:
            n, y = entry; m = "—"
        else:
            n, m, y = entry
        add("Micromax", n, m, y, False, None)

    # Karbonn / Intex
    for n, y in [
        ("A11 Star", 2013), ("A11+", 2013), ("A12+", 2013), ("A14", 2013),
        ("A15", 2013), ("A16", 2013), ("A18", 2013), ("A19+", 2013),
        ("A2+", 2013), ("A21", 2013), ("A25", 2013), ("A3", 2013),
        ("A34", 2013), ("A50s", 2014), ("A51+", 2015), ("A6 Turbo", 2014),
        ("A7 Star", 2013), ("A9+", 2013), ("A9 Star", 2013),
        ("Aura 1", 2016), ("Aura 9", 2016), ("Aura Note", 2015),
        ("K9 Music", 2018), ("Machone Titanium S310", 2014),
        ("Platinum P9", 2015), ("Q100", 2015), ("Sparkle V", 2014),
        ("Titanium Delight S1", 2015), ("Titanium Frames S7", 2015),
        ("Titanium Hexa", 2015), ("Titanium Mach Five", 2014),
        ("Titanium Mach Six", 2015), ("Titanium Machfive Turbo", 2014),
        ("Titanium Octane", 2013), ("Titanium Octane Plus", 2014),
        ("Titanium S1 Plus", 2014), ("Titanium S12 Delite", 2014),
        ("Titanium S15 Ultra", 2015), ("Titanium S19", 2014),
        ("Titanium S200 HD", 2014), ("Titanium S200", 2014),
        ("Titanium S205", 2014), ("Titanium S25 Klick", 2014),
        ("Titanium S2 Plus", 2014), ("Titanium S3 Plus", 2015),
        ("Titanium S5+", 2014), ("Titanium S5 Plus", 2014),
        ("Titanium S9 Lite", 2014), ("Titanium S9 Plus", 2014),
        ("Titanium S99", 2014), ("Titanium Vindaas S1", 2014),
    ]:
        add("Karbonn", n, "—", y, False, None)
    for n, y in [
        ("Aqua Ace", 2016), ("Aqua Ace Mini", 2016), ("Aqua Amaze", 2015),
        ("Aqua Amaze+", 2015), ("Aqua Craze II", 2016), ("Aqua Curve", 2015),
        ("Aqua Curve Mini", 2015), ("Aqua Fish", 2016), ("Aqua Freedom", 2015),
        ("Aqua Glory", 2015), ("Aqua HD 5.0", 2015), ("Aqua i-5 3G", 2015),
        ("Aqua i-6", 2016), ("Aqua Life II", 2015), ("Aqua Life III", 2015),
        ("Aqua Life IV", 2016), ("Aqua Lions 4G", 2017), ("Aqua Lions 3", 2017),
        ("Aqua Lions T1 Lite", 2018), ("Aqua Lions X1", 2017),
        ("Aqua Lions X1+", 2017), ("Aqua N11", 2016), ("Aqua N15", 2015),
        ("Aqua N17", 2015), ("Aqua N4", 2015), ("Aqua N7", 2015),
        ("Aqua Power+", 2015), ("Aqua Power 4G", 2016), ("Aqua Power HD", 2015),
        ("Aqua Power II", 2015), ("Aqua Power M", 2015), ("Aqua Prime 4G", 2016),
        ("Aqua Q7", 2015), ("Aqua Q7 Pro", 2015), ("Aqua Q7N", 2015),
        ("Aqua Ring", 2015), ("Aqua Secure", 2016), ("Aqua Sense 5.0", 2015),
        ("Aqua Sense", 2015), ("Aqua Shine 4G", 2016), ("Aqua Shine+", 2015),
        ("Aqua Slice 2", 2015), ("Aqua Speed", 2014), ("Aqua Speed HD", 2015),
        ("Aqua Star 2", 2014), ("Aqua Star HD 5.0", 2015), ("Aqua Star II", 2014),
        ("Aqua Star L", 2014), ("Aqua Style Pro", 2014), ("Aqua Style X", 2015),
        ("Aqua Style", 2014), ("Aqua Supreme", 2015), ("Aqua Trend", 2015),
        ("Aqua Trend Lite", 2015), ("Aqua Twist", 2015), ("Aqua Xtreme", 2014),
        ("Aqua Xtreme II", 2015), ("Aqua Xtreme V", 2015), ("Aqua Y2", 2016),
        ("Aqua Y4", 2016), ("Aqua Young", 2016), ("Aqua Zenith", 2015),
        ("Cloud 3G Gem", 2015), ("Cloud Breeze", 2016), ("Cloud Champ", 2015),
        ("Cloud Crystal 2.5D", 2016), ("Cloud Cube", 2015), ("Cloud Fame", 2016),
        ("Cloud Flash", 2016), ("Cloud Force", 2016), ("Cloud FX", 2014),
        ("Cloud Glory 4G", 2016), ("Cloud Gem+", 2015), ("Cloud Gem 4G", 2016),
        ("Cloud Jewel", 2015), ("Cloud M6", 2015), ("Cloud N4", 2015),
        ("Cloud N-II", 2015), ("Cloud Power", 2015), ("Cloud Q11", 2015),
        ("Cloud Q11 4G", 2016), ("Cloud String", 2015), ("Cloud String 2", 2015),
        ("Cloud Style", 2015), ("Cloud Style 4G", 2016), ("Cloud Swift", 2015),
        ("Cloud X1+", 2015), ("Cloud X2", 2015), ("Cloud X4", 2015),
        ("Cloud X5", 2015), ("Cloud Y11", 2015), ("Cloud Y2", 2015),
        ("Cloud Y3", 2015), ("Cloud Y4+", 2015), ("Cloud Y5", 2015),
        ("Cloud Y7", 2016), ("Cloud Zest 4G", 2016), ("Cloud Zest", 2015),
        ("Elyt Dual", 2016), ("Elyt e1", 2017), ("Elyt e6", 2018),
        ("Elyt e7", 2018), ("Indie 5", 2018), ("Indie 5G", 2019),
        ("Staari 9", 2018), ("Staari 10", 2018), ("Staari 11", 2018),
        ("Staari 12", 2018), ("Uday", 2018),
    ]:
        add("Intex", n, "—", y, False, None)

    # ============================================================
    # WINDOWS PHONE catalog (non-Lumia)
    # ============================================================
    for brand, models in [
        ("Acer", [("Allegro", 2011), ("W4", 2013), ("Liquid M220", 2015), ("Jade Primo", 2015)]),
        ("Alcatel", [("OneTouch VIEW", 2013), ("OneTouch Pixi 3 (4)", 2015),
                     ("Fierce XL Windows", 2016), ("Idol 4S Windows", 2016)]),
        ("Dell", [("Venue Pro", 2010)]),
        ("Fujitsu", [("IS12T", 2011)]),
        ("Kazam", [("Thunder Q4.5", 2014)]),
        ("Karbonn", [("Wind W4", 2015)]),
        ("MicroMax", [("Canvas Win W092", 2015), ("Canvas Win W121", 2015)]),
        ("LG", [("Optimus 7", 2010), ("Optimus 7Q", 2010), ("Quantum", 2010),
                 ("Jil Sander", 2012), ("Lancet", 2015)]),
        ("Prestigio", [("MultiPhone 8500 DUO", 2014)]),
        ("Yezz", [("Billy 4", 2015), ("Billy 4.7", 2015)]),
        ("Wiko", [("Wiko WP4.7", 2013)]),
        ("BLU", [("Win HD", 2014), ("Win HD LTE", 2015), ("Win JR", 2014),
                  ("Win JR LTE", 2015)]),
        ("Cherry Mobile", [("Alpha Luxe", 2014), ("Alpha Prime 4", 2015),
                            ("Alpha Prime 5", 2015), ("Alpha Style", 2014)]),
        ("Prestigio", [("MultiPhone 8500 DUO", 2014)]),
        ("Highscreen", [("WinWin", 2015), ("WinJoy", 2015)]),
        ("Xolo", [("Win Q900s", 2014)]),
    ]:
        for entry in models:
            if len(entry) == 2:
                n, y = entry; m = "—"
            else:
                n, m, y = entry
            add(brand, n, m, y, False, "Windows Phone")

    # ============================================================
    # AFRICAN/LATAM long-tail brands
    # ============================================================
    # Tecno legacy
    tecno_all = [
        ("T351", 2015), ("T401", 2016), ("T402", 2016), ("T462", 2017),
        ("T473", 2017), ("T528", 2017), ("Boom J7", 2015), ("Boom J8", 2016),
        ("Camon C5", 2015), ("Camon C7", 2015), ("Camon C8", 2015),
        ("Camon C9", 2016), ("Camon CX", 2017), ("Camon CX Air", 2017),
        ("Camon i", 2018), ("Camon i Air", 2018), ("Camon i Ace", 2018),
        ("Camon i Twin", 2018), ("Camon i2", 2018), ("Camon i2X", 2018),
        ("Camon i4", 2019), ("Camon 11", 2018), ("Camon 11 Pro", 2018),
        ("Camon 12", 2019), ("Camon 12 Air", 2019), ("Camon 12 Pro", 2019),
        ("Camon 15", 2020), ("Camon 15 Air", 2020), ("Camon 15 Pro", 2020),
        ("Camon 16", 2020), ("Camon 16 Premier", 2020), ("Camon 16 Pro", 2020),
        ("Camon 17", 2021), ("Camon 17 Premier", 2021), ("Camon 17 Pro", 2021),
        ("Camon 18", 2021), ("Camon 18 P", 2021), ("Camon 18 Premier", 2021),
        ("Camon 18 Pro", 2021), ("Camon 19", 2022), ("Camon 19 Neo", 2022),
        ("Camon 19 Pro", 2022), ("Camon 19 Pro 5G", 2022), ("Pop 1", 2018),
        ("Pop 1 Pro", 2018), ("Pop 1s", 2018), ("Pop 1s Pro", 2018),
        ("Pop 2 Air", 2018), ("Pop 2 F", 2018), ("Pop 2 Plus", 2018),
        ("Pop 2 Power", 2018), ("Pop 2 Pro", 2018), ("Pop 2S", 2018),
        ("Pop 2s Pro", 2019), ("Pop 3", 2019), ("Pop 3 Plus", 2019),
        ("Pop 3 Pro", 2019), ("Pop 4", 2020), ("Pop 4 Air", 2020),
        ("Pop 4 Pro", 2020), ("Pop 5", 2021), ("Pop 5 LTE", 2021),
        ("Pop 5C", 2021), ("Pop 5 Pro", 2021), ("Pop 6", 2022),
        ("Spark 1", 2017), ("Spark 2", 2018), ("Spark 3", 2019),
        ("Spark 3 Pro", 2019), ("Spark 4", 2019), ("Spark 4 Air", 2019),
        ("Spark 4 Lite", 2019), ("Spark 5", 2020), ("Spark 5 Air", 2020),
        ("Spark 5 Pro", 2020), ("Spark 6", 2020), ("Spark 6 Air", 2020),
        ("Spark 6 Go", 2020), ("Spark 7", 2021), ("Spark 7 P", 2021),
        ("Spark 7 Pro", 2021), ("Spark 7T", 2021), ("Spark 8", 2021),
        ("Spark 8 P", 2022), ("Spark 8 Pro", 2022), ("Spark 8C", 2022),
        ("Spark 8T", 2022), ("Spark 9", 2022), ("Spark 9 Pro", 2022),
        ("Spark 9T", 2022), ("Spark Go 2022", 2022),
    ]
    for entry in tecno_all:
        if len(entry) == 2:
            n, y = entry; m = "—"
        else:
            n, m, y = entry
        add("Tecno", n, m, y, False, None)

    # Infinix legacy
    infinix_all = [
        ("Hot 2", "X510", 2015), ("Hot 3", "X553", 2016), ("Hot 4", "X557", 2016),
        ("Hot 4 Pro", "X556", 2016), ("Hot 5", "X559", 2017),
        ("Hot 5 Lite", "X559C", 2017), ("Hot 6", "X606", 2018),
        ("Hot 6 Pro", "X608", 2018), ("Hot 6X", "X623", 2018),
        ("Hot 7", "X624", 2019), ("Hot 7 Pro", "X625", 2019),
        ("Hot 8", "X650", 2019), ("Hot 8 Lite", "X650B", 2019),
        ("Hot 9", "X655", 2020), ("Hot 9 Play", "X680B", 2020),
        ("Hot 9 Pro", "X655F", 2020), ("Hot 10", "X682", 2020),
        ("Hot 10 Lite", "X657", 2020), ("Hot 10 Play", "X688", 2021),
        ("Hot 10i", "X658E", 2021), ("Hot 10s", "X689D", 2021),
        ("Hot 10T", "X689F", 2021), ("Hot 11", "X662", 2021),
        ("Hot 11 2022", "X6812", 2022), ("Hot 11 Play", "X688D", 2021),
        ("Hot 11S", "X6812B", 2021), ("Hot 11S NFC", "X6812C", 2021),
        ("Hot 12", "X6816", 2022), ("Hot 12 Play", "X6816D", 2022),
        ("Hot 12 Pro", "X6816B", 2022), ("Hot 12i", "X665B", 2022),
        ("Hot 20", "X6826", 2022), ("Hot 20 5G", "X6826B", 2022),
        ("Hot 20 Play", "X6826D", 2022), ("Hot 20 Pro", "X6826A", 2022),
        ("Hot 20i", "X665E", 2022), ("Hot 20S", "X6827", 2022),
        # Note
        ("Note 2", "X600", 2015), ("Note 3", "X601", 2016),
        ("Note 3 Pro", "X601", 2016), ("Note 4", "X572", 2017),
        ("Note 4 Pro", "X571", 2017), ("Note 5", "X604", 2018),
        ("Note 5 Stylus", "X605", 2018), ("Note 6", "X610", 2019),
        ("Note 7", "X690", 2019), ("Note 7 Lite", "X656", 2019),
        ("Note 8", "X692", 2020), ("Note 8i", "X683", 2020),
        ("Note 10", "X693", 2021), ("Note 10 Pro", "X695", 2021),
        ("Note 10 Pro NFC", "X695C", 2021), ("Note 11", "X663", 2021),
        ("Note 11 Pro", "X697", 2021), ("Note 11i", "X664", 2022),
        ("Note 11S", "X6812B", 2022), ("Note 12", "X670", 2022),
        ("Note 12 5G", "X670B", 2022), ("Note 12 G96", "X670C", 2022),
        ("Note 12 Pro", "X676B", 2022), ("Note 12 Pro 5G", "X671B", 2022),
        ("Note 12i", "X664C", 2022), ("Note 12S", "X670N", 2022),
        # S / Smart / Zero
        ("Smart", "X5010", 2017), ("Smart 2", "X5515", 2018),
        ("Smart 2 HD", "X609", 2018), ("Smart 2 Pro", "X5514D", 2018),
        ("Smart 3", "X5516", 2019), ("Smart 3 Plus", "X627", 2019),
        ("Smart 4", "X653C", 2020), ("Smart 4 Plus", "X653D", 2020),
        ("Smart 5", "X657", 2020), ("Smart 5A", "X657C", 2020),
        ("Smart 6", "X6511", 2021), ("Smart 6 HD", "X6512", 2021),
        ("Smart 6 Plus", "X6511B", 2022), ("Smart 7", "X6515", 2022),
        ("Smart 7 HD", "X6515C", 2022), ("Smart 7 Plus", "X6517", 2023),
        ("S2", "X522", 2017), ("S2 Pro", "X603", 2017), ("S3", "X573", 2018),
        ("S3X", "X622", 2018), ("S4", "X626", 2019), ("S5", "X652", 2019),
        ("S5 Lite", "X652B", 2019), ("S5 Pro", "X660", 2020),
        ("Zero 3", "X552", 2015), ("Zero 4", "X555", 2016),
        ("Zero 4 Plus", "X602", 2016), ("Zero 5", "X603", 2017),
        ("Zero 5 Pro", "X603B", 2017), ("Zero 6", "X620", 2018),
        ("Zero 6 Pro", "X620B", 2018), ("Zero 8", "X687", 2020),
        ("Zero 8i", "X687B", 2020), ("Zero X", "X6811", 2021),
        ("Zero X Neo", "X6810", 2021), ("Zero X Pro", "X6811B", 2021),
        ("Zero 5G", "X6815", 2022), ("Zero Ultra", "X6820", 2022),
    ]
    for n, m, y in infinix_all:
        add("Infinix", n, m, y, False, None)

    # Itel
    for n, y in [
        ("Alpha", 2020), ("A11", 2015), ("A14", 2015), ("A14 Plus", 2015),
        ("A15", 2015), ("A16", 2015), ("A18", 2016), ("A20", 2016), ("A21", 2016),
        ("A22", 2017), ("A22 Pro", 2017), ("A23", 2017), ("A24", 2017),
        ("A25", 2018), ("A26", 2018), ("A32F", 2018), ("A33", 2019),
        ("A44", 2019), ("A44 Pro", 2019), ("A45", 2019), ("A46", 2019),
        ("A47", 2020), ("A48", 2020), ("A49", 2020), ("A55", 2020),
        ("A55 Lite", 2020), ("A56", 2020), ("A57", 2020), ("A58", 2021),
        ("A58 Lite", 2021), ("A58 Pro", 2021), ("Muse", 2017), ("Prime 4", 2017),
        ("Prime 4 GB", 2018), ("S11", 2017), ("S11 Plus", 2018), ("S12", 2018),
        ("S13", 2019), ("S13 Plus", 2019), ("S14", 2019), ("S15", 2020),
        ("S15 Pro", 2020), ("S16", 2020), ("S16 Pro", 2020), ("S17", 2021),
        ("S18 Pro", 2022), ("Vision 1", 2019), ("Vision 1 Plus", 2019),
        ("Vision 1 Pro", 2019), ("Vision 2", 2020), ("Vision 2 Plus", 2020),
        ("Vision 2S", 2020), ("Vision 3", 2021), ("Vision 3 Plus", 2021),
        ("P11", 2015), ("P12", 2016), ("P13", 2017), ("P32", 2018), ("P33", 2019),
        ("P36", 2020), ("P36 Pro", 2020), ("P37", 2020), ("P37 Pro", 2020),
        ("P38", 2020), ("P38 Pro", 2021),
    ]:
        add("Itel", n, "—", y, False, None)

    # ============================================================
    # KAIOS feature phones (JioPhone, Nokia 8110 4G, etc.)
    # ============================================================
    for brand, models in [
        ("Jio", [("JioPhone F30C", 2017), ("JioPhone F81E", 2017),
                  ("JioPhone 2 F221B", 2018), ("JioPhone 3 F350L", 2019),
                  ("JioPhone Next", 2021), ("JioPhone Prima 4G", 2023)]),
        ("Reliance", [("KaiOS 2.5.4 Prime", 2018)]),
        ("Doro", [("7060", 2018), ("7080", 2019)]),
        ("Cat", [("B35", 2018)]),
        ("Alcatel", [("Go Flip", 2017), ("Cingular Flip 2", 2018),
                      ("Cingular Flip 3", 2019), ("SmartFlip", 2017)]),
    ]:
        for entry in models:
            if len(entry) == 2:
                n, y = entry; m = "—"
            else:
                n, m, y = entry
            add(brand, n, m, y, False, "KaiOS feature phone")

    # ============================================================
    # PALM WEBOS / MEEGO / SAILFISH / SYMBIAN S60 phones (misc)
    # ============================================================
    # Nokia N9 already in Nokia; other MeeGo
    for brand, models in [
        ("Neo900", [("Neo900", 2015)]),
        ("Jolla", [("Jolla Phone", 2013), ("Jolla Tablet", 2015),
                    ("Jolla C", 2016), ("Jolla C2", 2024)]),
        ("YotaPhone", [("YotaPhone", 2013), ("YotaPhone 2", 2014),
                        ("YotaPhone 3", 2017)]),
        ("Turing", [("Phone", 2016), ("Cadenza", 2017)]),
        ("Silent Circle", [("Blackphone", 2014), ("Blackphone 2", 2015)]),
        ("Geeksphone", [("Peak+", 2013), ("Revolution", 2014), ("Blackphone", 2014)]),
        ("Nextbit", [("Robin", 2016)]),
    ]:
        for entry in models:
            if len(entry) == 2:
                n, y = entry; m = "—"
            else:
                n, m, y = entry
            add(brand, n, m, y, False, None)

    # ============================================================
    # AMAZON KINDLE 3G/4G (historical)
    # ============================================================
    for n, y in [
        ("Kindle 2 3G", 2009), ("Kindle DX", 2009), ("Kindle DX 2nd gen", 2010),
        ("Kindle Keyboard 3G", 2010), ("Kindle Touch 3G", 2011),
        ("Kindle Paperwhite 1st gen 3G", 2012), ("Kindle Paperwhite 2nd gen 3G", 2013),
        ("Kindle Paperwhite 3rd gen 3G", 2015), ("Kindle Voyage 3G", 2014),
        ("Kindle Oasis 1st gen 3G", 2016), ("Kindle Oasis 2nd gen Cellular", 2017),
        ("Kindle Oasis 3rd gen Cellular", 2019), ("Kindle Paperwhite Signature Edition", 2021),
        ("Fire HD 8 4G (2015)", 2015), ("Fire HDX 8.9 LTE (2013)", 2013),
        ("Fire HDX 8.9 LTE (2014)", 2014),
    ]:
        add("Amazon", n, "—", y, False, "Cellular · 3G/4G · sunset")

    # ============================================================
    # NOOK, SONY READER, KOBO cellular
    # ============================================================
    for brand, models in [
        ("Barnes & Noble", [("Nook 3G", 2009), ("Nook Simple Touch", 2011)]),
        ("Sony", [("Reader Daily Edition", 2009), ("Reader T3", 2013)]),
        ("Kobo", [("Aura HD", 2013), ("Aura One", 2016)]),
    ]:
        for entry in models:
            if len(entry) == 2:
                n, y = entry; m = "—"
            else:
                n, m, y = entry
            add(brand, n, m, y, False, "E-reader · Wi-Fi/3G")

    # ============================================================
    # GPS TRACKERS / M2M devices
    # ============================================================
    for brand, models in [
        ("Garmin", [("Alpha 200i (LTE)", 2020), ("inReach Mini 2", 2022),
                      ("inReach Explorer+", 2016), ("inReach SE+", 2017),
                      ("inReach Messenger", 2022)]),
        ("SPOT", [("Gen4", 2019), ("Trace", 2020), ("X", 2020)]),
        ("Zoleo", [("Zoleo (LTE)", 2020)]),
        ("Motorola", [("Defy Satellite Link", 2023)]),
        ("Bullitt", [("Motorola Defy Satellite Link", 2023)]),
        ("Iridium", [("GO! exec", 2022), ("Extreme 9575", 2011)]),
    ]:
        for entry in models:
            if len(entry) == 2:
                n, y = entry; m = "—"
            else:
                n, m, y = entry
            add(brand, n, m, y, False, "GPS/satellite tracker")

    # ============================================================
    # MEDICAL ALERT / PERS
    # ============================================================
    for brand, models in [
        ("Lively", [("Mobile Plus", 2018), ("Wearable 2", 2020)]),
        ("Life Alert", [("Mobile+", 2019)]),
        ("Medical Guardian", [("MGMove", 2021), ("Mini Guardian", 2020)]),
        ("Bay Alarm Medical", [("SOS Mobile", 2019), ("SOS Smartwatch", 2021)]),
        ("GreatCall", [("Lively Wearable", 2018)]),
    ]:
        for entry in models:
            if len(entry) == 2:
                n, y = entry; m = "—"
            else:
                n, m, y = entry
            add(brand, n, m, y, False, "Medical alert · Cellular")


if __name__ == "__main__":
    print("Import via build_devices.py")
