#!/usr/bin/env python3
"""
Generate a large eSIM compatibility dataset from catalog rules.

Rules encoded (Aug 2026, from Apple, Vodafone UK, Klook, esim-now, mysimguide, Cybernews):

APPLE:
  - iPhone XS/XR (2018) and newer: eSIM yes (US 14+ = eSIM only)
  - iPhone X and earlier: no
  - iPads with cellular from 2018+: yes; Wi-Fi only: no

SAMSUNG:
  - Galaxy S20+ globally: yes (S20 FE = no)
  - Galaxy Note 20/20 Ultra: yes
  - Z Fold 2+ / Z Flip 3+: yes; original Fold and Z Flip 5G US: partial
  - A54, A55, A56, A57, A35, A36 (2023+): yes
  - A34 and below, A2x, A1x, A0x: no
  - M/F/J series: no
  - S10 and older: no

GOOGLE:
  - Pixel 5+: yes globally
  - Pixel 3/3a/4/4a series: yes with regional caveats
  - Pixel 2 and earlier: no

XIAOMI:
  - Xiaomi 13 / 14 / 15 / 12T Pro (global): yes
  - Older Xiaomi flagship (12, 11, Mi 11, 10): no
  - Redmi, POCO: no

ONEPLUS:
  - OnePlus 11, 12, 13, Open: yes
  - Older/Nord: no

SONY:
  - Xperia 1 IV/V/VI, 5 IV/V, 10 III/IV/V/VI: yes
  - Older Xperia: no

HUAWEI:
  - P40, P50, Pura 70/80, Mate 40+, Mate X series (global): yes
  - P30 and older, Nova, Y-series: no

MOTOROLA:
  - Razr 40/50/2025 series, Edge 40/50 series, Moto G Power 2025: yes
  - Older Moto G, older Edge: no

OPPO:
  - Find X3+/X5+/X6+/X7+/X8+, Find N series: yes
  - Reno, A-series: no

VIVO:
  - X100+, X200+: yes
  - X90 and older, V, Y series: no

HONOR:
  - Magic 4+/5+/6+/7+, Magic V series (global): yes
  - 200, 90, X series: no

NOKIA / HMD:
  - XR21, X30, G60: yes; rest: no

ASUS:
  - Zenfone 9/10/11, ROG Phone 8+/9+: yes
  - Older: no

REALME: all no
NOTHING: Phone (2), Phone (3): yes; rest: no
FAIRPHONE: 5, 6: yes; 4 and older: no
TCL: all no
"""

from dataclasses import dataclass, field, asdict
import json
import re

DEVICES = []

def add(brand, name, model, year, esim, note=None):
    d = {"brand": brand, "name": name, "model": model, "year": year, "esim": esim}
    if note:
        d["note"] = note
    DEVICES.append(d)

# ============================================================
# APPLE — iPhones
# ============================================================
apple_iphone = [
    # (name, model, year, esim, note)
    ("iPhone 17 Pro Max", "A3300", 2025, True, None),
    ("iPhone 17 Pro", "A3299", 2025, True, None),
    ("iPhone Air", "A3298", 2025, True, None),
    ("iPhone 17", "A3297", 2025, True, None),
    ("iPhone 17e", "A3296", 2025, True, None),
    ("iPhone 16 Pro Max", "A3084", 2024, True, "US: eSIM only"),
    ("iPhone 16 Pro", "A3083", 2024, True, "US: eSIM only"),
    ("iPhone 16 Plus", "A3082", 2024, True, "US: eSIM only"),
    ("iPhone 16", "A3081", 2024, True, "US: eSIM only"),
    ("iPhone 16e", "A3212", 2025, True, None),
    ("iPhone 15 Pro Max", "A2849", 2023, True, "US: eSIM only"),
    ("iPhone 15 Pro", "A2848", 2023, True, "US: eSIM only"),
    ("iPhone 15 Plus", "A2847", 2023, True, "US: eSIM only"),
    ("iPhone 15", "A2846", 2023, True, "US: eSIM only"),
    ("iPhone 14 Pro Max", "A2651", 2022, True, "US: eSIM only"),
    ("iPhone 14 Pro", "A2650", 2022, True, "US: eSIM only"),
    ("iPhone 14 Plus", "A2632", 2022, True, "US: eSIM only"),
    ("iPhone 14", "A2649", 2022, True, "US: eSIM only"),
    ("iPhone SE (3rd gen, 2022)", "A2595", 2022, True, None),
    ("iPhone 13 Pro Max", "A2484", 2021, True, None),
    ("iPhone 13 Pro", "A2483", 2021, True, None),
    ("iPhone 13", "A2482", 2021, True, None),
    ("iPhone 13 mini", "A2481", 2021, True, None),
    ("iPhone 12 Pro Max", "A2342", 2020, True, None),
    ("iPhone 12 Pro", "A2341", 2020, True, None),
    ("iPhone 12", "A2172", 2020, True, None),
    ("iPhone 12 mini", "A2176", 2020, True, None),
    ("iPhone SE (2nd gen, 2020)", "A2275", 2020, True, None),
    ("iPhone 11 Pro Max", "A2161", 2019, True, None),
    ("iPhone 11 Pro", "A2160", 2019, True, None),
    ("iPhone 11", "A2111", 2019, True, None),
    ("iPhone XS Max", "A1921", 2018, True, None),
    ("iPhone XS", "A1920", 2018, True, None),
    ("iPhone XR", "A1984", 2018, True, None),
    ("iPhone X", "A1865", 2017, False, None),
    ("iPhone 8 Plus", "A1864", 2017, False, None),
    ("iPhone 8", "A1863", 2017, False, None),
    ("iPhone SE (1st gen, 2016)", "A1662", 2016, False, None),
    ("iPhone 7 Plus", "A1661", 2016, False, None),
    ("iPhone 7", "A1660", 2016, False, None),
    ("iPhone 6s Plus", "A1687", 2015, False, None),
    ("iPhone 6s", "A1688", 2015, False, None),
    ("iPhone 6 Plus", "A1522", 2014, False, None),
    ("iPhone 6", "A1549", 2014, False, None),
    ("iPhone 5s", "A1533", 2013, False, None),
    ("iPhone 5c", "A1532", 2013, False, None),
    ("iPhone 5", "A1428", 2012, False, None),
    ("iPhone 4s", "A1387", 2011, False, None),
    ("iPhone 4", "A1332", 2010, False, None),
    ("iPhone 3GS", "A1303", 2009, False, None),
    ("iPhone 3G", "A1241", 2008, False, None),
    ("iPhone (original)", "A1203", 2007, False, None),
]
for n, m, y, e, note in apple_iphone:
    add("Apple", n, m, y, e, note)

# Apple iPads (cellular models from 2018+ support eSIM)
apple_ipads = [
    ("iPad Pro 13-inch (M4)", "A2925", 2024, True, "Wi-Fi + Cellular only"),
    ("iPad Pro 11-inch (M4)", "A2837", 2024, True, "Wi-Fi + Cellular only"),
    ("iPad Air 13-inch (M2)", "A2898", 2024, True, "Wi-Fi + Cellular only"),
    ("iPad Air 11-inch (M2)", "A2902", 2024, True, "Wi-Fi + Cellular only"),
    ("iPad Air (M3)", "A3266", 2025, True, "Wi-Fi + Cellular only"),
    ("iPad Pro 12.9-inch (6th gen, M2)", "A2437", 2022, True, "Wi-Fi + Cellular only"),
    ("iPad Pro 11-inch (4th gen, M2)", "A2761", 2022, True, "Wi-Fi + Cellular only"),
    ("iPad Pro 12.9-inch (5th gen, M1)", "A2379", 2021, True, "Wi-Fi + Cellular only"),
    ("iPad Pro 11-inch (3rd gen, M1)", "A2377", 2021, True, "Wi-Fi + Cellular only"),
    ("iPad Air (5th gen, M1)", "A2589", 2022, True, "Wi-Fi + Cellular only"),
    ("iPad Air (4th gen)", "A2072", 2020, True, "Wi-Fi + Cellular only"),
    ("iPad (11th gen, A16)", "A3355", 2025, True, "Wi-Fi + Cellular only"),
    ("iPad (10th gen)", "A2757", 2022, True, "Wi-Fi + Cellular only"),
    ("iPad (9th gen)", "A2603", 2021, True, "Wi-Fi + Cellular only"),
    ("iPad (8th gen)", "A2429", 2020, True, "Wi-Fi + Cellular only"),
    ("iPad (7th gen)", "A2198", 2019, True, "Wi-Fi + Cellular only"),
    ("iPad mini (7th gen, A17 Pro)", "A2993", 2024, True, "Wi-Fi + Cellular only"),
    ("iPad mini (6th gen)", "A2568", 2021, True, "Wi-Fi + Cellular only"),
    ("iPad mini (5th gen)", "A2124", 2019, True, "Wi-Fi + Cellular only"),
    ("iPad Pro 12.9-inch (3rd gen)", "A1895", 2018, True, "Wi-Fi + Cellular only"),
    ("iPad Pro 11-inch (1st gen)", "A1934", 2018, True, "Wi-Fi + Cellular only"),
    ("iPad Air (3rd gen)", "A2123", 2019, False, "SIM tray only"),
    ("iPad (6th gen)", "A1954", 2018, False, "SIM tray only"),
]
for n, m, y, e, note in apple_ipads:
    add("Apple", n, m, y, e, note)

# ============================================================
# SAMSUNG
# ============================================================
# Galaxy S
samsung_s = [
    ("Galaxy S26 Ultra", "SM-S948B", 2026, True, None),
    ("Galaxy S26+", "SM-S946B", 2026, True, None),
    ("Galaxy S26", "SM-S941B", 2026, True, None),
    ("Galaxy S26 FE", "SM-S951B", 2026, True, None),
    ("Galaxy S25 Ultra", "SM-S938B", 2025, True, None),
    ("Galaxy S25 Edge", "SM-S937B", 2025, True, None),
    ("Galaxy S25+", "SM-S936B", 2025, True, None),
    ("Galaxy S25", "SM-S931B", 2025, True, None),
    ("Galaxy S25 FE", "SM-S731B", 2025, True, None),
    ("Galaxy S24 Ultra", "SM-S928B", 2024, True, None),
    ("Galaxy S24+", "SM-S926B", 2024, True, None),
    ("Galaxy S24", "SM-S921B", 2024, True, None),
    ("Galaxy S24 FE", "SM-S721B", 2024, True, None),
    ("Galaxy S23 Ultra", "SM-S918B", 2023, True, "CN/HK excluded"),
    ("Galaxy S23+", "SM-S916B", 2023, True, "CN/HK excluded"),
    ("Galaxy S23", "SM-S911B", 2023, True, "CN/HK excluded"),
    ("Galaxy S23 FE", "SM-S711B", 2023, True, None),
    ("Galaxy S22 Ultra", "SM-S908B", 2022, True, None),
    ("Galaxy S22+", "SM-S906B", 2022, True, None),
    ("Galaxy S22", "SM-S901B", 2022, True, None),
    ("Galaxy S21 Ultra 5G", "SM-G998B", 2021, True, "US model excluded"),
    ("Galaxy S21+ 5G", "SM-G996B", 2021, True, "US model excluded"),
    ("Galaxy S21 5G", "SM-G991B", 2021, True, "US model excluded"),
    ("Galaxy S21 FE 5G", "SM-G990B", 2022, True, None),
    ("Galaxy S20 Ultra 5G", "SM-G988B", 2020, True, None),
    ("Galaxy S20+ 5G", "SM-G986B", 2020, True, None),
    ("Galaxy S20 5G", "SM-G981B", 2020, True, None),
    ("Galaxy S20", "SM-G980F", 2020, True, None),
    ("Galaxy S20+", "SM-G985F", 2020, True, None),
    ("Galaxy S20 FE 5G", "SM-G781B", 2020, False, "No eSIM hardware"),
    ("Galaxy S20 FE 4G", "SM-G780G", 2020, False, "No eSIM hardware"),
    ("Galaxy S10 5G", "SM-G977B", 2019, False, None),
    ("Galaxy S10+", "SM-G975F", 2019, False, None),
    ("Galaxy S10", "SM-G973F", 2019, False, None),
    ("Galaxy S10e", "SM-G970F", 2019, False, None),
    ("Galaxy S10 Lite", "SM-G770F", 2020, False, None),
    ("Galaxy S9+", "SM-G965F", 2018, False, None),
    ("Galaxy S9", "SM-G960F", 2018, False, None),
    ("Galaxy S8+", "SM-G955F", 2017, False, None),
    ("Galaxy S8", "SM-G950F", 2017, False, None),
    ("Galaxy S8 Active", "SM-G892A", 2017, False, None),
    ("Galaxy S7 edge", "SM-G935F", 2016, False, None),
    ("Galaxy S7", "SM-G930F", 2016, False, None),
    ("Galaxy S6 edge+", "SM-G928F", 2015, False, None),
    ("Galaxy S6 edge", "SM-G925F", 2015, False, None),
    ("Galaxy S6", "SM-G920F", 2015, False, None),
    ("Galaxy S5", "SM-G900F", 2014, False, None),
    ("Galaxy S4", "GT-I9505", 2013, False, None),
    ("Galaxy S III", "GT-I9300", 2012, False, None),
]
for n, m, y, e, note in samsung_s:
    add("Samsung", n, m, y, e, note)

# Galaxy Note
samsung_note = [
    ("Galaxy Note 20 Ultra 5G", "SM-N986B", 2020, True, "US/HK excluded"),
    ("Galaxy Note 20 5G", "SM-N981B", 2020, True, None),
    ("Galaxy Note 20 Ultra", "SM-N985F", 2020, True, None),
    ("Galaxy Note 20", "SM-N980F", 2020, True, None),
    ("Galaxy Note 10+ 5G", "SM-N976B", 2019, False, None),
    ("Galaxy Note 10+", "SM-N975F", 2019, False, None),
    ("Galaxy Note 10", "SM-N970F", 2019, False, None),
    ("Galaxy Note 10 Lite", "SM-N770F", 2020, False, None),
    ("Galaxy Note 9", "SM-N960F", 2018, False, None),
    ("Galaxy Note 8", "SM-N950F", 2017, False, None),
    ("Galaxy Note 5", "SM-N920F", 2015, False, None),
    ("Galaxy Note 4", "SM-N910F", 2014, False, None),
]
for n, m, y, e, note in samsung_note:
    add("Samsung", n, m, y, e, note)

# Galaxy Foldables
samsung_fold = [
    ("Galaxy Z Fold7", "SM-F958B", 2025, True, None),
    ("Galaxy Z Fold6", "SM-F956B", 2024, True, None),
    ("Galaxy Z Fold5", "SM-F946B", 2023, True, None),
    ("Galaxy Z Fold4", "SM-F936B", 2022, True, None),
    ("Galaxy Z Fold3 5G", "SM-F926B", 2021, True, None),
    ("Galaxy Z Fold2 5G", "SM-F916B", 2020, True, "US/HK excluded"),
    ("Galaxy Fold", "SM-F900F", 2019, True, None),
    ("Galaxy Z Flip7", "SM-F761B", 2025, True, None),
    ("Galaxy Z Flip7 FE", "SM-F741B", 2025, True, None),
    ("Galaxy Z Flip6", "SM-F741B", 2024, True, None),
    ("Galaxy Z Flip5", "SM-F731B", 2023, True, None),
    ("Galaxy Z Flip4", "SM-F721B", 2022, True, None),
    ("Galaxy Z Flip3 5G", "SM-F711B", 2021, True, None),
    ("Galaxy Z Flip 5G", "SM-F707B", 2020, True, "US variant excluded"),
    ("Galaxy Z Flip", "SM-F700F", 2020, False, "No eSIM in most regions"),
]
for n, m, y, e, note in samsung_fold:
    add("Samsung", n, m, y, e, note)

# Galaxy A series (A54+ supports eSIM, below does not)
samsung_a = [
    ("Galaxy A57 5G", "SM-A576B", 2026, True, None),
    ("Galaxy A56 5G", "SM-A566B", 2025, True, None),
    ("Galaxy A55 5G", "SM-A556B", 2024, True, None),
    ("Galaxy A54 5G", "SM-A546B", 2023, True, None),
    ("Galaxy A36 5G", "SM-A366B", 2025, True, None),
    ("Galaxy A35 5G", "SM-A356B", 2024, True, None),
    ("Galaxy A26 5G", "SM-A266B", 2025, False, None),
    ("Galaxy A34 5G", "SM-A346B", 2023, False, None),
    ("Galaxy A33 5G", "SM-A336B", 2022, False, None),
    ("Galaxy A32 5G", "SM-A326B", 2021, False, None),
    ("Galaxy A32", "SM-A325F", 2021, False, None),
    ("Galaxy A31", "SM-A315F", 2020, False, None),
    ("Galaxy A25 5G", "SM-A256B", 2024, False, None),
    ("Galaxy A24", "SM-A245F", 2023, False, None),
    ("Galaxy A23 5G", "SM-A236B", 2022, False, None),
    ("Galaxy A22 5G", "SM-A226B", 2021, False, None),
    ("Galaxy A22", "SM-A225F", 2021, False, None),
    ("Galaxy A21s", "SM-A217F", 2020, False, None),
    ("Galaxy A20", "SM-A205F", 2019, False, None),
    ("Galaxy A20s", "SM-A207F", 2019, False, None),
    ("Galaxy A20e", "SM-A202F", 2019, False, None),
    ("Galaxy A16 5G", "SM-A166B", 2024, False, None),
    ("Galaxy A15 5G", "SM-A156B", 2024, False, None),
    ("Galaxy A15", "SM-A155F", 2024, False, None),
    ("Galaxy A14 5G", "SM-A146B", 2023, False, None),
    ("Galaxy A14", "SM-A145F", 2023, False, None),
    ("Galaxy A13 5G", "SM-A136B", 2022, False, None),
    ("Galaxy A13", "SM-A135F", 2022, False, None),
    ("Galaxy A12", "SM-A125F", 2020, False, None),
    ("Galaxy A11", "SM-A115F", 2020, False, None),
    ("Galaxy A10", "SM-A105F", 2019, False, None),
    ("Galaxy A10e", "SM-A102U", 2019, False, None),
    ("Galaxy A10s", "SM-A107F", 2019, False, None),
    ("Galaxy A06 5G", "SM-A066B", 2024, False, None),
    ("Galaxy A05s", "SM-A057F", 2023, False, None),
    ("Galaxy A05", "SM-A055F", 2023, False, None),
    ("Galaxy A04s", "SM-A047F", 2022, False, None),
    ("Galaxy A04", "SM-A045F", 2022, False, None),
    ("Galaxy A04e", "SM-A042F", 2022, False, None),
    ("Galaxy A03s", "SM-A037F", 2021, False, None),
    ("Galaxy A03", "SM-A035F", 2021, False, None),
    ("Galaxy A02s", "SM-A025F", 2021, False, None),
    ("Galaxy A02", "SM-A022F", 2021, False, None),
    ("Galaxy A01", "SM-A015F", 2020, False, None),
    ("Galaxy A51 5G", "SM-A516B", 2020, False, None),
    ("Galaxy A51", "SM-A515F", 2019, False, None),
    ("Galaxy A50", "SM-A505F", 2019, False, None),
    ("Galaxy A52 5G", "SM-A526B", 2021, False, None),
    ("Galaxy A52s 5G", "SM-A528B", 2021, False, None),
    ("Galaxy A52", "SM-A525F", 2021, False, None),
    ("Galaxy A53 5G", "SM-A536B", 2022, False, None),
    ("Galaxy A71 5G", "SM-A716B", 2020, False, None),
    ("Galaxy A71", "SM-A715F", 2019, False, None),
    ("Galaxy A72", "SM-A725F", 2021, False, None),
    ("Galaxy A73 5G", "SM-A736B", 2022, False, None),
]
for n, m, y, e, note in samsung_a:
    add("Samsung", n, m, y, e, note)

# Galaxy M and F (no eSIM)
samsung_mf = [
    ("Galaxy M55 5G", "SM-M556B", 2024, False),
    ("Galaxy M54 5G", "SM-M546B", 2023, False),
    ("Galaxy M53 5G", "SM-M536B", 2022, False),
    ("Galaxy M52 5G", "SM-M526B", 2021, False),
    ("Galaxy M51", "SM-M515F", 2020, False),
    ("Galaxy M35 5G", "SM-M356B", 2024, False),
    ("Galaxy M34 5G", "SM-M346B", 2023, False),
    ("Galaxy M33 5G", "SM-M336B", 2022, False),
    ("Galaxy M32", "SM-M325F", 2021, False),
    ("Galaxy M31", "SM-M315F", 2020, False),
    ("Galaxy M30s", "SM-M307F", 2019, False),
    ("Galaxy M15 5G", "SM-M156B", 2024, False),
    ("Galaxy M14 5G", "SM-M146B", 2023, False),
    ("Galaxy M13", "SM-M135F", 2022, False),
    ("Galaxy M12", "SM-M127F", 2021, False),
    ("Galaxy M11", "SM-M115F", 2020, False),
    ("Galaxy M04", "SM-M045F", 2022, False),
    ("Galaxy M05", "SM-M055F", 2024, False),
    ("Galaxy F55 5G", "SM-E556B", 2024, False),
    ("Galaxy F54 5G", "SM-E546B", 2023, False),
    ("Galaxy F34 5G", "SM-E346B", 2023, False),
    ("Galaxy F23 5G", "SM-E236B", 2022, False),
    ("Galaxy F15 5G", "SM-E156B", 2024, False),
    ("Galaxy F14 5G", "SM-E146B", 2023, False),
    ("Galaxy F04", "SM-E045F", 2023, False),
    ("Galaxy J8", "SM-J810F", 2018, False),
    ("Galaxy J7 Pro", "SM-J730F", 2017, False),
    ("Galaxy J6", "SM-J600F", 2018, False),
    ("Galaxy J5 (2017)", "SM-J530F", 2017, False),
    ("Galaxy J3 (2017)", "SM-J330F", 2017, False),
    ("Galaxy J2 (2018)", "SM-J250F", 2018, False),
]
for row in samsung_mf:
    n, m, y, e = row[:4]
    note = row[4] if len(row) > 4 else None
    add("Samsung", n, m, y, e, note)

# Rugged / other
samsung_other = [
    ("Galaxy XCover 7", "SM-G556B", 2024, True, None),
    ("Galaxy XCover 6 Pro", "SM-G736B", 2022, False, None),
    ("Galaxy XCover 5", "SM-G525F", 2021, False, None),
    ("Galaxy XCover Pro", "SM-G715F", 2020, False, None),
]
for n, m, y, e, note in samsung_other:
    add("Samsung", n, m, y, e, note)

# ============================================================
# GOOGLE PIXEL
# ============================================================
pixels = [
    ("Pixel 10 Pro Fold", "GA05876", 2025, True, None),
    ("Pixel 10 Pro XL", "GA05875", 2025, True, None),
    ("Pixel 10 Pro", "GA05874", 2025, True, None),
    ("Pixel 10", "GA05873", 2025, True, None),
    ("Pixel 10a", "GA05872", 2025, True, None),
    ("Pixel 9 Pro Fold", "GA05559", 2024, True, None),
    ("Pixel 9 Pro XL", "GA05558", 2024, True, None),
    ("Pixel 9 Pro", "GA05557", 2024, True, None),
    ("Pixel 9", "GA05556", 2024, True, None),
    ("Pixel 9a", "GA06729", 2025, True, None),
    ("Pixel 8 Pro", "GA04905", 2023, True, None),
    ("Pixel 8", "GA04803", 2023, True, None),
    ("Pixel 8a", "GA05480", 2024, True, None),
    ("Pixel Fold", "GA04289", 2023, True, None),
    ("Pixel 7 Pro", "GE2AE", 2022, True, None),
    ("Pixel 7", "GVU6C", 2022, True, None),
    ("Pixel 7a", "GHL1X", 2023, True, None),
    ("Pixel 6 Pro", "GLU0G", 2021, True, None),
    ("Pixel 6", "GB7N6", 2021, True, None),
    ("Pixel 6a", "GX7AS", 2022, True, None),
    ("Pixel 5", "GD1YQ", 2020, True, None),
    ("Pixel 5a 5G", "G4S1M", 2021, True, None),
    ("Pixel 4a 5G", "G025I", 2020, True, None),
    ("Pixel 4a", "G025N", 2020, True, None),
    ("Pixel 4 XL", "G020P", 2019, True, None),
    ("Pixel 4", "G020I", 2019, True, None),
    ("Pixel 3a XL", "G020C", 2019, True, "SEA excluded"),
    ("Pixel 3a", "G020A", 2019, True, "SEA excluded"),
    ("Pixel 3 XL", "G013C", 2018, True, "AU/JP/TW excluded"),
    ("Pixel 3", "G013A", 2018, True, "AU/JP/TW excluded"),
    ("Pixel 2 XL", "G011C", 2017, False, None),
    ("Pixel 2", "G011A", 2017, False, None),
    ("Pixel XL", "G-2PW2100", 2016, False, None),
    ("Pixel", "G-2PW4100", 2016, False, None),
    ("Nexus 6P", "H1512", 2015, False, None),
    ("Nexus 5X", "LG-H791", 2015, False, None),
    ("Nexus 5", "LG-D821", 2013, False, None),
]
for n, m, y, e, note in pixels:
    add("Google", n, m, y, e, note)

# ============================================================
# XIAOMI
# ============================================================
xiaomi = [
    # Xiaomi flagship 15/14/13 series — global supports eSIM; some regions excluded
    ("Xiaomi 15 Ultra", "2503BPN26G", 2025, True, None),
    ("Xiaomi 15 Pro", "24129PN74G", 2025, True, None),
    ("Xiaomi 15", "24129PN74C", 2025, True, None),
    ("Xiaomi 15T Pro", "2506FPN10G", 2025, True, None),
    ("Xiaomi 15T", "2506FPN10G", 2025, True, None),
    ("Xiaomi 14 Ultra", "23116PN5BG", 2024, True, None),
    ("Xiaomi 14 Pro", "23117RA68G", 2024, True, None),
    ("Xiaomi 14", "23127PN0CG", 2024, True, None),
    ("Xiaomi 14T Pro", "2407FPN8EG", 2024, True, None),
    ("Xiaomi 14T", "2407FPN8EG", 2024, True, None),
    ("Xiaomi 13 Ultra", "2304FPN6DG", 2023, True, None),
    ("Xiaomi 13 Pro", "2210132G", 2023, True, None),
    ("Xiaomi 13", "2211133G", 2023, True, None),
    ("Xiaomi 13 Lite", "2210129SG", 2023, True, None),
    ("Xiaomi 13T Pro", "23078PND5G", 2023, True, None),
    ("Xiaomi 13T", "23088PND5R", 2023, True, None),
    # Xiaomi 12T Pro (global) yes; 12T no
    ("Xiaomi 12T Pro", "22081212UG", 2022, True, None),
    ("Xiaomi 12T", "22071212AG", 2022, False, None),
    ("Xiaomi 12 Pro", "2201122G", 2022, False, None),
    ("Xiaomi 12", "2201123G", 2022, False, None),
    ("Xiaomi 12X", "2112123AG", 2021, False, None),
    ("Xiaomi 12 Lite", "2203129G", 2022, False, None),
    ("Xiaomi 11T Pro", "21081111RG", 2021, False, None),
    ("Xiaomi 11T", "21081111RG", 2021, False, None),
    ("Xiaomi 11 Lite 5G", "2109119DG", 2021, False, None),
    ("Xiaomi 11i", "21051182G", 2022, False, None),
    ("Mi 11 Ultra", "M2102K1G", 2021, False, None),
    ("Mi 11 Pro", "M2102K1AC", 2021, False, None),
    ("Mi 11", "M2011K2G", 2021, False, None),
    ("Mi 11 Lite", "M2101K9AG", 2021, False, None),
    ("Mi 10T Pro", "M2007J3SG", 2020, False, None),
    ("Mi 10T", "M2007J3SY", 2020, False, None),
    ("Mi 10T Lite", "M2007J17G", 2020, False, None),
    ("Mi 10 Ultra", "M2007J1SC", 2020, False, None),
    ("Mi 10 Pro", "M2001J1G", 2020, False, None),
    ("Mi 10", "M2001J2G", 2020, False, None),
    ("Mi 10 Lite 5G", "M2002J9G", 2020, False, None),
    ("Mi Mix Fold 4", "24072PX77C", 2024, True, None),
    ("Mi Mix Fold 3", "23046PNC9C", 2023, True, None),
    ("Mi Mix Fold 2", "22061218C", 2022, False, None),
    ("Mi Mix 3", "M1810E5A", 2018, False, None),
    ("Mi 9", "M1902F1G", 2019, False, None),
    ("Mi 9T Pro", "M1903F11G", 2019, False, None),
    ("Mi 9T", "M1903F10G", 2019, False, None),
    ("Mi 9 SE", "M1903F2G", 2019, False, None),
    ("Mi 8 Pro", "M1807E8A", 2018, False, None),
    ("Mi 8", "M1803E1A", 2018, False, None),
]
for n, m, y, e, note in xiaomi:
    add("Xiaomi", n, m, y, e, note)

# Redmi (all no eSIM)
redmi = [
    "Redmi Note 14 Pro+", "2412DPC0CG",
    "Redmi Note 14 Pro", "2412CRAD3G",
    "Redmi Note 14", "2412CPBD4G",
    "Redmi Note 14 Pro 5G", "2412CRAD9G",
    "Redmi Note 13 Pro+", "23090RA98G",
    "Redmi Note 13 Pro 5G", "23117RA68G",
    "Redmi Note 13 Pro", "23117RA68G",
    "Redmi Note 13 5G", "23129RAA4G",
    "Redmi Note 13", "23129RAA4G",
    "Redmi Note 12 Pro+ 5G", "22101316UP",
    "Redmi Note 12 Pro 5G", "22101316G",
    "Redmi Note 12 Pro", "23021RAAEG",
    "Redmi Note 12 5G", "22111317G",
    "Redmi Note 12", "23021RAA2Y",
    "Redmi Note 11 Pro+ 5G", "21091116UG",
    "Redmi Note 11 Pro 5G", "2201116SG",
    "Redmi Note 11 Pro", "2201116TG",
    "Redmi Note 11S", "2201117SG",
    "Redmi Note 11", "2201117TG",
    "Redmi Note 10 Pro Max", "M2101K6P",
    "Redmi Note 10 Pro", "M2101K6G",
    "Redmi Note 10S", "M2101K7BG",
    "Redmi Note 10 5G", "M2103K19G",
    "Redmi Note 10", "M2101K7AG",
    "Redmi Note 9 Pro Max", "M2003J6B2G",
    "Redmi Note 9 Pro", "M2003J6B2G",
    "Redmi Note 9S", "M2003J6A1G",
    "Redmi Note 9", "M2003J15SG",
    "Redmi Note 8 Pro", "M1906G7G",
    "Redmi Note 8", "M1908C3JG",
    "Redmi Note 8T", "M1908C3XG",
    "Redmi Note 7 Pro", "M1901F7S",
    "Redmi Note 7", "M1901F7G",
    "Redmi 14C", "24081PN33G",
    "Redmi 13C 5G", "23124RN87G",
    "Redmi 13C", "23100RN82L",
    "Redmi 12C", "22120RN86G",
    "Redmi 12 5G", "23076RN8DY",
    "Redmi 12", "23053RN02Y",
    "Redmi 11 Prime 5G", "22041219G",
    "Redmi 10 5G", "22041219G",
    "Redmi 10 2022", "21121119SG",
    "Redmi 10", "21061119AG",
    "Redmi 10C", "220333QAG",
    "Redmi 10A", "220233L2G",
    "Redmi 9T", "M2010J19SG",
    "Redmi 9", "M2004J19G",
    "Redmi 9A", "M2006C3LG",
    "Redmi 9C", "M2006C3MG",
    "Redmi 8", "M1908C3IG",
    "Redmi 8A", "M1908C3KG",
    "Redmi A3", "23129RN51X",
    "Redmi A2", "23028RN4DG",
    "Redmi A1", "220733SG",
    "Redmi K70 Pro", "23117RK66C",
    "Redmi K70", "23113RKC6C",
    "Redmi K60", "22127RK46C",
    "Redmi K50 Ultra", "22081212C",
    "Redmi K40", "M2012K11AC",
    "Redmi Turbo 4 Pro", "24129PN74C",
    "Redmi Turbo 4", "24129PN74C",
]
# pairs: name, model
for i in range(0, len(redmi), 2):
    name = redmi[i]
    model = redmi[i+1]
    # infer year
    year_map = {"14": 2024, "13": 2024, "12": 2023, "11": 2022, "10": 2021, "9": 2020, "8": 2019, "7": 2019, "6": 2018, "5": 2018, "4": 2017,
                "70": 2024, "60": 2023, "50": 2022, "40": 2021}
    y = 2023
    for k, v in year_map.items():
        if f" {k}" in " " + name or name.endswith(f" {k}"):
            y = v; break
    add("Xiaomi", name, model, y, False)

# POCO (all no eSIM)
poco = [
    ("POCO F7 Ultra", "2410DPN6CG", 2025),
    ("POCO F7 Pro", "23117RK66C", 2024),
    ("POCO F6 Pro", "23049PCD8G", 2024),
    ("POCO F6", "24069PC21G", 2024),
    ("POCO F5 Pro", "23013RK75C", 2023),
    ("POCO F5", "23049PCD8G", 2023),
    ("POCO F4 GT", "21121210G", 2022),
    ("POCO F4", "22021211RG", 2022),
    ("POCO F3", "M2012K11AG", 2021),
    ("POCO F2 Pro", "M2004J11G", 2020),
    ("POCO F1", "MZB6971IN", 2018),
    ("POCO X7 Pro", "24122PCC7G", 2025),
    ("POCO X7", "24122PCC7G", 2025),
    ("POCO X6 Pro 5G", "23113RKC6G", 2024),
    ("POCO X6 5G", "23122PCD1G", 2024),
    ("POCO X5 Pro 5G", "22101320G", 2023),
    ("POCO X5 5G", "22111317PG", 2023),
    ("POCO X4 Pro 5G", "2201116PG", 2022),
    ("POCO X4 GT", "22041216G", 2022),
    ("POCO X3 Pro", "M2102J20SG", 2021),
    ("POCO X3", "M2007J20CG", 2020),
    ("POCO M7 Pro 5G", "24076PN25G", 2024),
    ("POCO M6 Pro", "2312FPCA6G", 2024),
    ("POCO M6 5G", "23124RN87G", 2023),
    ("POCO M5s", "2207117BPG", 2022),
    ("POCO M5", "22071219CG", 2022),
    ("POCO M4 Pro 5G", "21091116AG", 2021),
    ("POCO M4 Pro", "2201117PG", 2022),
    ("POCO M3", "M2010J19CG", 2020),
    ("POCO C75", "24116RACCG", 2024),
    ("POCO C65", "2310FPCA4G", 2023),
    ("POCO C55", "220733SPG", 2023),
    ("POCO C51", "220733SPI", 2023),
    ("POCO C40", "220333QPG", 2022),
    ("POCO C31", "210904PI", 2021),
]
for n, m, y in poco:
    add("Xiaomi", n, m, y, False)

# ============================================================
# ONEPLUS
# ============================================================
oneplus = [
    ("OnePlus 13", "CPH2653", 2025, True, None),
    ("OnePlus 13R", "CPH2669", 2025, True, None),
    ("OnePlus 12", "CPH2581", 2024, True, None),
    ("OnePlus 12R", "CPH2609", 2024, True, None),
    ("OnePlus 11 5G", "CPH2449", 2023, True, None),
    ("OnePlus 11R", "CPH2487", 2023, True, None),
    ("OnePlus Open", "CPH2551", 2023, True, None),
    ("OnePlus 10 Pro", "NE2213", 2022, False, None),
    ("OnePlus 10T", "CPH2415", 2022, False, None),
    ("OnePlus 10R", "CPH2411", 2022, False, None),
    ("OnePlus 9 Pro", "LE2125", 2021, False, None),
    ("OnePlus 9", "LE2113", 2021, False, None),
    ("OnePlus 9R", "LE2101", 2021, False, None),
    ("OnePlus 8 Pro", "IN2023", 2020, False, None),
    ("OnePlus 8T", "KB2003", 2020, False, None),
    ("OnePlus 8", "IN2013", 2020, False, None),
    ("OnePlus 7T Pro", "HD1913", 2019, False, None),
    ("OnePlus 7T", "HD1903", 2019, False, None),
    ("OnePlus 7 Pro", "GM1913", 2019, False, None),
    ("OnePlus 7", "GM1903", 2019, False, None),
    ("OnePlus 6T", "A6013", 2018, False, None),
    ("OnePlus 6", "A6003", 2018, False, None),
    ("OnePlus 5T", "A5010", 2017, False, None),
    ("OnePlus 5", "A5000", 2017, False, None),
    ("OnePlus Nord 4", "CPH2661", 2024, False, None),
    ("OnePlus Nord 3 5G", "CPH2493", 2023, False, None),
    ("OnePlus Nord 2T 5G", "CPH2399", 2022, False, None),
    ("OnePlus Nord 2 5G", "DN2103", 2021, False, None),
    ("OnePlus Nord", "AC2003", 2020, False, None),
    ("OnePlus Nord CE 4 Lite", "CPH2621", 2024, False, None),
    ("OnePlus Nord CE 4", "CPH2613", 2024, False, None),
    ("OnePlus Nord CE 3 Lite 5G", "CPH2465", 2023, False, None),
    ("OnePlus Nord CE 3 5G", "CPH2569", 2023, False, None),
    ("OnePlus Nord CE 2 Lite 5G", "CPH2381", 2022, False, None),
    ("OnePlus Nord CE 2 5G", "IV2201", 2022, False, None),
    ("OnePlus Nord CE 5G", "EB2103", 2021, False, None),
    ("OnePlus Nord N30 SE", "CPH2607", 2023, False, None),
    ("OnePlus Nord N30", "CPH2513", 2023, False, None),
    ("OnePlus Nord N20 SE", "CPH2469", 2022, False, None),
    ("OnePlus Nord N20 5G", "N200DL", 2022, False, None),
    ("OnePlus Nord N200 5G", "DE2118", 2021, False, None),
    ("OnePlus Nord N100", "BE2013", 2020, False, None),
    ("OnePlus Nord N10 5G", "BE2029", 2020, False, None),
    ("OnePlus Ace 3 Pro", "CPH2669", 2024, False, None),
    ("OnePlus Ace 3", "PJA110", 2024, False, None),
]
for n, m, y, e, note in oneplus:
    add("OnePlus", n, m, y, e, note)

# ============================================================
# SONY
# ============================================================
sony = [
    ("Xperia 1 VII", "XQ-FS54", 2025, True, None),
    ("Xperia 1 VI", "XQ-EC54", 2024, True, None),
    ("Xperia 1 V", "XQ-DQ54", 2023, True, None),
    ("Xperia 1 IV", "XQ-CT54", 2022, True, None),
    ("Xperia 1 III", "XQ-BC52", 2021, False, None),
    ("Xperia 1 II", "XQ-AT52", 2020, False, None),
    ("Xperia 1", "J8110", 2019, False, None),
    ("Xperia 5 V", "XQ-DE54", 2023, True, None),
    ("Xperia 5 IV", "XQ-CQ54", 2022, True, None),
    ("Xperia 5 III", "XQ-BQ52", 2021, False, None),
    ("Xperia 5 II", "XQ-AS52", 2020, False, None),
    ("Xperia 5", "J8210", 2019, False, None),
    ("Xperia 10 VI", "XQ-ES54", 2024, True, None),
    ("Xperia 10 V", "XQ-DC54", 2023, True, None),
    ("Xperia 10 IV", "XQ-CC54", 2022, True, None),
    ("Xperia 10 III", "XQ-BT52", 2021, True, None),
    ("Xperia 10 II", "XQ-AU52", 2020, False, None),
    ("Xperia 10 Plus", "I4293", 2019, False, None),
    ("Xperia 10", "I4113", 2019, False, None),
    ("Xperia Pro-I", "XQ-BE52", 2021, False, None),
    ("Xperia Pro", "XQ-AQ52", 2020, False, None),
    ("Xperia XZ3", "H9436", 2018, False, None),
    ("Xperia XZ2 Premium", "H8166", 2018, False, None),
    ("Xperia XZ2", "H8266", 2018, False, None),
    ("Xperia XZ1", "G8342", 2017, False, None),
    ("Xperia XA2", "H4113", 2018, False, None),
]
for n, m, y, e, note in sony:
    add("Sony", n, m, y, e, note)

# ============================================================
# HUAWEI
# ============================================================
huawei = [
    ("Pura 80 Ultra", "ADA-AL00", 2025, True, None),
    ("Pura 80 Pro+", "ADP-AL00", 2025, True, None),
    ("Pura 80 Pro", "ADS-AL00", 2025, True, None),
    ("Pura 80", "ADY-AL00", 2025, True, None),
    ("Pura 70 Ultra", "HBP-AL00", 2024, True, None),
    ("Pura 70 Pro+", "HBN-AL00", 2024, True, None),
    ("Pura 70 Pro", "HBN-AL10", 2024, True, None),
    ("Pura 70", "ADY-AL00", 2024, True, None),
    ("Mate 70 Pro+", "ALX-AL00", 2024, True, None),
    ("Mate 70 Pro", "ALT-AL00", 2024, True, None),
    ("Mate 70", "AGT-AL00", 2024, True, None),
    ("Mate 60 Pro+", "ALN-AL10", 2023, True, None),
    ("Mate 60 Pro", "ALN-AL00", 2023, True, None),
    ("Mate 60", "ALN-AL80", 2023, True, None),
    ("Mate X6", "ALT-L29", 2024, True, None),
    ("Mate Xs 2", "PAL-L29", 2022, True, None),
    ("Mate X2", "TET-AN00", 2021, True, None),
    ("Mate 40 Pro+", "NOP-AN00", 2020, True, None),
    ("Mate 40 Pro", "NOH-NX9", 2020, True, None),
    ("Mate 40", "OCE-AN10", 2020, True, None),
    ("Mate 30 Pro", "LIO-L29", 2019, True, None),
    ("Mate 30", "TAS-L29", 2019, True, None),
    ("P60 Pro", "MNA-LX9", 2023, True, None),
    ("P60", "LNA-AL00", 2023, True, None),
    ("P50 Pro", "JAD-LX9", 2021, True, None),
    ("P50", "ABR-LX9", 2021, True, None),
    ("P40 Pro+", "ELS-N39", 2020, True, None),
    ("P40 Pro", "ELS-NX9", 2020, True, None),
    ("P40", "ANA-NX9", 2020, True, None),
    ("P40 lite", "JNY-LX1", 2020, False, None),
    ("P30 Pro", "VOG-L29", 2019, False, None),
    ("P30", "ELE-L29", 2019, False, None),
    ("P30 lite", "MAR-LX1A", 2019, False, None),
    ("P20 Pro", "CLT-L29", 2018, False, None),
    ("P20", "EML-L29", 2018, False, None),
    ("Nova 12 Ultra", "BLA-AL00", 2024, False, None),
    ("Nova 12 Pro", "BLN-AL00", 2024, False, None),
    ("Nova 12", "BLN-AL00", 2024, False, None),
    ("Nova 11 Pro", "GOA-AL80", 2023, False, None),
    ("Nova 11", "FOA-AL00", 2023, False, None),
    ("Nova 10 Pro", "GLA-AL00", 2022, False, None),
    ("Nova 10", "NCO-AL00", 2022, False, None),
    ("Nova 9", "NAM-AL00", 2021, False, None),
    ("Y9a", "FRL-L22", 2020, False, None),
    ("Y7 (2019)", "DUB-LX1", 2019, False, None),
]
for n, m, y, e, note in huawei:
    add("Huawei", n, m, y, e, note)

# ============================================================
# MOTOROLA
# ============================================================
motorola = [
    ("Razr Ultra 2025", "XT2551-1", 2025, True, None),
    ("Razr Plus 2025", "XT2551-3", 2025, True, None),
    ("Razr 2025", "XT2551-5", 2025, True, None),
    ("Razr 50 Ultra", "XT2451-1", 2024, True, None),
    ("Razr 50", "XT2453-1", 2024, True, None),
    ("Razr 40 Ultra", "XT2321-1", 2023, True, None),
    ("Razr 40", "XT2323-1", 2023, True, None),
    ("Razr (2022)", "XT2251-1", 2022, True, None),
    ("Razr 5G", "XT2071-4", 2020, True, None),
    ("Razr (2019)", "XT2000-2", 2019, True, None),
    ("Edge 60 Pro", "XT2503-1", 2025, True, None),
    ("Edge 60", "XT2505-1", 2025, True, None),
    ("Edge 50 Ultra", "XT2401-1", 2024, True, None),
    ("Edge 50 Pro", "XT2403-2", 2024, True, None),
    ("Edge 50 Fusion", "XT2429-1", 2024, True, None),
    ("Edge 50 Neo", "XT2409-3", 2024, True, None),
    ("Edge 50", "XT2407-3", 2024, True, None),
    ("Edge 40 Pro", "XT2301-4", 2023, True, None),
    ("Edge 40", "XT2303-1", 2023, True, None),
    ("Edge 40 Neo", "XT2307-1", 2023, True, None),
    ("Edge 30 Ultra", "XT2241-2", 2022, False, None),
    ("Edge 30 Pro", "XT2201-2", 2022, False, None),
    ("Edge 30", "XT2203-1", 2022, False, None),
    ("Edge 30 Neo", "XT2245-1", 2022, False, None),
    ("Edge 30 Fusion", "XT2243-2", 2022, False, None),
    ("Edge 20 Pro", "XT2153-1", 2021, False, None),
    ("Edge 20", "XT2143-1", 2021, False, None),
    ("Edge 20 Lite", "XT2139-1", 2021, False, None),
    ("Edge+ (2020)", "XT2061-3", 2020, False, None),
    ("Edge (2020)", "XT2063-3", 2020, False, None),
    ("Moto G Power 2025", "XT2515", 2025, True, None),
    ("Moto G Power 5G 2024", "XT2417", 2024, True, None),
    ("Moto G Power 2024", "XT2415", 2024, False, None),
    ("Moto G Power 5G 2023", "XT2311-3", 2023, True, None),
    ("Moto G Power 2023", "XT2311", 2023, False, None),
    ("Moto G Power 2022", "XT2165-3", 2022, False, None),
    ("Moto G Power 2021", "XT2117-3", 2021, False, None),
    ("Moto G Stylus 5G 2024", "XT2419", 2024, True, None),
    ("Moto G Stylus 2024", "XT2419", 2024, False, None),
    ("Moto G Stylus 5G 2023", "XT2315", 2023, True, None),
    ("Moto G Stylus 2023", "XT2317", 2023, False, None),
    ("Moto G Stylus 5G 2022", "XT2215", 2022, False, None),
    ("Moto G Play 2024", "XT2413", 2024, False, None),
    ("Moto G Play 2023", "XT2271", 2023, False, None),
    ("Moto G Pure", "XT2163-4", 2021, False, None),
    ("Moto G 5G 2024", "XT2417", 2024, False, None),
    ("Moto G 5G 2023", "XT2313", 2023, False, None),
    ("Moto G 5G 2022", "XT2213-2", 2022, False, None),
    ("Moto G 5G Plus", "XT2075-3", 2020, False, None),
    ("Moto G84 5G", "XT2347-1", 2023, False, None),
    ("Moto G73 5G", "XT2237", 2023, False, None),
    ("Moto G54 5G", "XT2343-1", 2023, False, None),
    ("Moto G53 5G", "XT2335", 2023, False, None),
    ("Moto G34 5G", "XT2363-3", 2023, False, None),
    ("Moto G32", "XT2235-2", 2022, False, None),
    ("Moto G31", "XT2173-3", 2021, False, None),
    ("Moto G22", "XT2231-2", 2022, False, None),
    ("Moto G14", "XT2341-3", 2023, False, None),
    ("Moto G13", "XT2331-2", 2023, False, None),
    ("Moto G100", "XT2125-4", 2021, False, None),
    ("Moto G60", "XT2135-1", 2021, False, None),
    ("Moto G50", "XT2137-1", 2021, False, None),
    ("Moto G40 Fusion", "XT2147-2", 2021, False, None),
    ("Moto G30", "XT2129-1", 2021, False, None),
    ("Moto G10", "XT2127-1", 2021, False, None),
    ("Moto G9 Plus", "XT2087-1", 2020, False, None),
    ("Moto G9 Play", "XT2083-3", 2020, False, None),
    ("Moto G9 Power", "XT2091-4", 2020, False, None),
    ("Moto G8 Plus", "XT2019-2", 2019, False, None),
    ("Moto G8 Power", "XT2041-3", 2020, False, None),
    ("Moto G8", "XT2045-1", 2020, False, None),
    ("Moto G7 Plus", "XT1965-2", 2019, False, None),
    ("Moto G7", "XT1962-1", 2019, False, None),
    ("Moto G6", "XT1925-6", 2018, False, None),
    ("Moto E14", "XT2421-3", 2024, False, None),
    ("Moto E13", "XT2345-3", 2023, False, None),
    ("Moto E22", "XT2239-7", 2022, False, None),
    ("Moto E20", "XT2155-1", 2021, False, None),
    ("Moto E7 Plus", "XT2081-1", 2020, False, None),
    ("Moto E7", "XT2095-1", 2020, False, None),
    ("Moto E6 Plus", "XT2025-2", 2019, False, None),
    ("ThinkPhone 25", "XT2547-1", 2025, True, None),
    ("ThinkPhone", "XT2309-1", 2023, True, None),
]
for n, m, y, e, note in motorola:
    add("Motorola", n, m, y, e, note)

# ============================================================
# OPPO
# ============================================================
oppo = [
    ("Find X8 Ultra", "PJZ115", 2025, True, None),
    ("Find X8 Pro", "PJZ110", 2024, True, None),
    ("Find X8", "PJZ100", 2024, True, None),
    ("Find X7 Ultra", "PHY110", 2024, True, None),
    ("Find X7 Pro", "PHZ110", 2024, True, None),
    ("Find X7", "PHZ100", 2024, True, None),
    ("Find X6 Pro", "PGEM10", 2023, True, None),
    ("Find X6", "PGFM10", 2023, True, None),
    ("Find X5 Pro", "CPH2305", 2022, True, None),
    ("Find X5", "CPH2307", 2022, True, None),
    ("Find X5 Lite", "CPH2371", 2022, False, None),
    ("Find X3 Pro", "CPH2173", 2021, True, None),
    ("Find X3", "PEDM00", 2021, True, None),
    ("Find X2 Pro", "CPH2025", 2020, False, None),
    ("Find X2", "CPH2023", 2020, False, None),
    ("Find X", "CPH1871", 2018, False, None),
    ("Find N5", "PJD110", 2025, True, None),
    ("Find N3", "CPH2499", 2023, True, None),
    ("Find N3 Flip", "CPH2519", 2023, True, None),
    ("Find N2 Flip", "CPH2437", 2023, True, None),
    ("Find N2", "PGT110", 2022, False, None),
    ("Find N", "PEUM00", 2021, False, None),
    ("Reno 12 Pro+", "CPH2649", 2024, False, None),
    ("Reno 12 Pro", "CPH2629", 2024, False, None),
    ("Reno 12", "CPH2625", 2024, False, None),
    ("Reno 12 F", "CPH2637", 2024, False, None),
    ("Reno 11 Pro", "CPH2607", 2024, False, None),
    ("Reno 11", "CPH2599", 2024, False, None),
    ("Reno 10 Pro+", "CPH2521", 2023, False, None),
    ("Reno 10 Pro", "CPH2525", 2023, False, None),
    ("Reno 10", "CPH2531", 2023, False, None),
    ("Reno 9 Pro+", "PGX110", 2022, False, None),
    ("Reno 9 Pro", "PGW110", 2022, False, None),
    ("Reno 9", "PGX110", 2022, False, None),
    ("Reno 8 Pro", "CPH2357", 2022, False, None),
    ("Reno 8", "CPH2359", 2022, False, None),
    ("Reno 8 T 5G", "CPH2505", 2023, False, None),
    ("Reno 7 Pro 5G", "CPH2293", 2021, False, None),
    ("Reno 7 5G", "CPH2371", 2021, False, None),
    ("Reno 7", "CPH2363", 2021, False, None),
    ("Reno 6 Pro 5G", "CPH2247", 2021, False, None),
    ("Reno 6 5G", "CPH2251", 2021, False, None),
    ("Reno 5 Pro 5G", "PDSM00", 2020, False, None),
    ("Reno 5 5G", "CPH2145", 2020, False, None),
    ("Reno 4 Pro", "CPH2109", 2020, False, None),
    ("Reno 4", "CPH2113", 2020, False, None),
    ("A98 5G", "CPH2529", 2023, False, None),
    ("A79 5G", "CPH2557", 2024, False, None),
    ("A78 5G", "CPH2495", 2023, False, None),
    ("A77 5G", "CPH2373", 2022, False, None),
    ("A76", "CPH2375", 2022, False, None),
    ("A74 5G", "CPH2263", 2021, False, None),
    ("A73 5G", "CPH2161", 2020, False, None),
    ("A58", "CPH2577", 2023, False, None),
    ("A57", "CPH2387", 2022, False, None),
    ("A56 5G", "CPH2311", 2021, False, None),
    ("A54 5G", "CPH2195", 2021, False, None),
    ("A54", "CPH2239", 2021, False, None),
    ("A53s 5G", "CPH2321", 2021, False, None),
    ("A53", "CPH2127", 2020, False, None),
    ("A38", "CPH2579", 2023, False, None),
    ("A18", "CPH2591", 2023, False, None),
    ("A17", "CPH2477", 2022, False, None),
    ("A16", "CPH2269", 2021, False, None),
    ("A15", "CPH2185", 2020, False, None),
    ("A9 2020", "CPH1941", 2019, False, None),
    ("A5 2020", "CPH1931", 2019, False, None),
]
for n, m, y, e, note in oppo:
    add("Oppo", n, m, y, e, note)

# ============================================================
# VIVO
# ============================================================
vivo = [
    ("X200 Ultra", "V2415A", 2025, True, None),
    ("X200 Pro", "V2415", 2024, True, None),
    ("X200 Pro Mini", "V2416", 2024, True, None),
    ("X200", "V2413", 2024, True, None),
    ("X100 Ultra", "V2333A", 2024, True, None),
    ("X100 Pro+", "V2338A", 2024, True, None),
    ("X100 Pro", "V2324A", 2023, True, None),
    ("X100", "V2309A", 2023, True, None),
    ("X100s Pro", "V2324A", 2024, True, None),
    ("X90 Pro+", "V2227A", 2022, False, None),
    ("X90 Pro", "V2242A", 2023, False, None),
    ("X90", "V2241A", 2023, False, None),
    ("X80 Pro", "V2145", 2022, False, None),
    ("X80", "V2183A", 2022, False, None),
    ("X70 Pro+", "V2145A", 2021, False, None),
    ("X70 Pro", "V2134A", 2021, False, None),
    ("X70", "V2133A", 2021, False, None),
    ("X60 Pro+", "V2059A", 2020, False, None),
    ("X60 Pro", "V2046", 2021, False, None),
    ("X60", "V2045", 2021, False, None),
    ("V50", "V2418", 2025, False, None),
    ("V40 Pro", "V2338", 2024, False, None),
    ("V40", "V2336", 2024, False, None),
    ("V40 SE", "V2400", 2024, False, None),
    ("V30 Pro", "V2318", 2024, False, None),
    ("V30", "V2318", 2024, False, None),
    ("V29 Pro", "V2250", 2023, False, None),
    ("V29", "V2250", 2023, False, None),
    ("V27 Pro", "V2231", 2023, False, None),
    ("V27", "V2231", 2023, False, None),
    ("V25 Pro", "V2158", 2022, False, None),
    ("V25", "V2202", 2022, False, None),
    ("V23 Pro", "V2132", 2022, False, None),
    ("V23", "V2130", 2022, False, None),
    ("V21", "V2050", 2021, False, None),
    ("V20", "V2027", 2020, False, None),
    ("V19", "V1933", 2020, False, None),
    ("Y300 Pro", "V2337", 2024, False, None),
    ("Y200 Pro 5G", "V2312", 2024, False, None),
    ("Y100", "V2239", 2023, False, None),
    ("Y78+", "V2308", 2023, False, None),
    ("Y77 5G", "V2129", 2022, False, None),
    ("Y75 5G", "V2126", 2021, False, None),
    ("Y70", "V1930", 2020, False, None),
    ("Y55 5G", "V2226", 2022, False, None),
    ("Y36", "V2247", 2023, False, None),
    ("Y33s", "V2109", 2021, False, None),
    ("Y30", "V2034", 2020, False, None),
    ("Y21", "V2110", 2021, False, None),
    ("Y20", "V2029", 2020, False, None),
    ("Y11", "V2029", 2019, False, None),
    ("iQOO 13", "V2415A", 2024, True, None),
    ("iQOO 12 Pro", "V2333A", 2023, True, None),
    ("iQOO 12", "V2307A", 2023, True, None),
    ("iQOO 11 Pro", "V2244A", 2022, False, None),
    ("iQOO 11", "V2243A", 2023, False, None),
    ("iQOO 10 Pro", "V2218A", 2022, False, None),
    ("iQOO 10", "V2217A", 2022, False, None),
    ("iQOO 9 Pro", "V2172A", 2022, False, None),
    ("iQOO 9", "V2171A", 2022, False, None),
    ("iQOO Neo 9 Pro", "V2338A", 2024, False, None),
    ("iQOO Neo 9", "V2338A", 2024, False, None),
]
for n, m, y, e, note in vivo:
    add("Vivo", n, m, y, e, note)

# ============================================================
# HONOR
# ============================================================
honor = [
    ("Magic 7 Pro", "PGT-N19", 2024, True, None),
    ("Magic 7", "PGT-N09", 2024, True, None),
    ("Magic 6 Pro", "BVL-N49", 2024, True, None),
    ("Magic 6", "BVL-N39", 2024, True, None),
    ("Magic 6 Ultimate", "BVL-N59", 2024, True, None),
    ("Magic 5 Pro", "PGT-N19", 2023, True, None),
    ("Magic 5", "PGT-N09", 2023, True, None),
    ("Magic 5 Lite", "RMO-NX3", 2023, False, None),
    ("Magic V3", "BVL-AN00", 2024, True, None),
    ("Magic V2", "VER-N49", 2023, True, None),
    ("Magic V Flip", "MGI-AN00", 2024, True, None),
    ("Magic Vs2", "VER-AN00", 2023, True, None),
    ("Magic Vs", "VER-N49", 2022, True, None),
    ("Magic 4 Pro", "LGE-NX9", 2022, True, None),
    ("Magic 4", "LGE-N19", 2022, True, None),
    ("Magic 3 Pro+", "ELZ-N39", 2021, False, None),
    ("Magic 3 Pro", "ELZ-N29", 2021, False, None),
    ("Magic 3", "ELZ-AN00", 2021, False, None),
    ("200 Pro", "ELP-NX9", 2024, False, None),
    ("200", "ELI-NX9", 2024, False, None),
    ("200 Lite", "LLY-LX1", 2024, False, None),
    ("100 Pro", "GLA-AN00", 2023, False, None),
    ("100", "MOA-AN00", 2023, False, None),
    ("90 Pro", "PGT-AN10", 2023, False, None),
    ("90", "REA-NX9", 2023, False, None),
    ("90 Lite", "CRT-NX1", 2023, False, None),
    ("80 Pro", "ANY-N09", 2022, False, None),
    ("80", "ANY-N29", 2022, False, None),
    ("70 Pro+", "HPB-AN00", 2021, False, None),
    ("70 Pro", "HPB-AN00", 2021, False, None),
    ("70", "FNE-AN00", 2021, False, None),
    ("60 Pro", "TNA-AN00", 2020, False, None),
    ("60", "LSA-AN00", 2020, False, None),
    ("X9c", "CRT-NX3", 2024, False, None),
    ("X8b", "LLY-LX1", 2024, False, None),
    ("X8", "TFY-LX1", 2024, False, None),
    ("X7b", "CLK-LX3", 2024, False, None),
    ("X7", "CLK-LX1", 2023, False, None),
    ("X6a", "WDY-LX1", 2024, False, None),
    ("X6", "AGT-LX1", 2023, False, None),
    ("X5 Plus", "WOD-LX2", 2023, False, None),
    ("X5", "WOD-LX1", 2023, False, None),
    ("70 Lite", "RBN-LX1", 2022, False, None),
    ("50 Lite", "NTN-LX1", 2022, False, None),
    ("View 40", "NTN-AN20", 2020, False, None),
    ("V40", "YOK-AN10", 2021, False, None),
    ("V30 Pro", "OXF-AN10", 2019, False, None),
]
for n, m, y, e, note in honor:
    add("Honor", n, m, y, e, note)

# ============================================================
# NOKIA (HMD)
# ============================================================
nokia = [
    ("XR21", "TA-1486", 2023, True, None),
    ("XR20", "TA-1362", 2021, False, None),
    ("X30 5G", "TA-1450", 2022, True, None),
    ("X20", "TA-1341", 2021, False, None),
    ("X10", "TA-1332", 2021, False, None),
    ("G60 5G", "TA-1447", 2022, True, None),
    ("G50", "TA-1361", 2021, False, None),
    ("G42 5G", "TA-1581", 2023, False, None),
    ("G22", "TA-1528", 2023, False, None),
    ("G21", "TA-1418", 2022, False, None),
    ("G20", "TA-1336", 2021, False, None),
    ("G11 Plus", "TA-1478", 2022, False, None),
    ("G10", "TA-1338", 2021, False, None),
    ("C32", "TA-1530", 2023, False, None),
    ("C31", "TA-1487", 2022, False, None),
    ("C22", "TA-1533", 2023, False, None),
    ("C21", "TA-1352", 2022, False, None),
    ("C21 Plus", "TA-1424", 2022, False, None),
    ("C12", "TA-1535", 2023, False, None),
    ("C10", "TA-1342", 2021, False, None),
    ("C2 2nd Edition", "TA-1454", 2022, False, None),
    ("110 4G", "TA-1543", 2023, False, None),
    ("105 4G", "TA-1550", 2023, False, None),
    ("6300 4G", "TA-1324", 2020, False, None),
    ("8000 4G", "TA-1311", 2020, False, None),
    ("2660 Flip", "TA-1471", 2022, False, None),
    ("HMD Pulse Pro", "TA-1622", 2024, False, None),
    ("HMD Skyline", "TA-1614", 2024, True, None),
]
for n, m, y, e, note in nokia:
    add("Nokia", n, m, y, e, note)

# ============================================================
# ASUS
# ============================================================
asus = [
    ("Zenfone 12 Ultra", "AI2501", 2025, True, None),
    ("Zenfone 11 Ultra", "AI2401", 2024, True, None),
    ("Zenfone 10", "AI2302", 2023, True, None),
    ("Zenfone 9", "AI2202", 2022, True, None),
    ("Zenfone 8", "ZS590KS", 2021, False, None),
    ("Zenfone 8 Flip", "ZS672KS", 2021, False, None),
    ("Zenfone 7 Pro", "ZS671KS", 2020, False, None),
    ("Zenfone 7", "ZS670KS", 2020, False, None),
    ("Zenfone 6", "ZS630KL", 2019, False, None),
    ("ROG Phone 9 Pro", "AI2501", 2024, True, None),
    ("ROG Phone 9", "AI2501", 2024, True, None),
    ("ROG Phone 8 Pro", "AI2401_H", 2024, True, None),
    ("ROG Phone 8", "AI2401", 2024, True, None),
    ("ROG Phone 7 Ultimate", "AI2205", 2023, False, None),
    ("ROG Phone 7", "AI2205", 2023, False, None),
    ("ROG Phone 6D Ultimate", "AI2203D", 2022, False, None),
    ("ROG Phone 6 Pro", "AI2201_H", 2022, False, None),
    ("ROG Phone 6", "AI2201", 2022, False, None),
    ("ROG Phone 5s Pro", "ZS676KS", 2021, False, None),
    ("ROG Phone 5s", "ZS676KS", 2021, False, None),
    ("ROG Phone 5 Ultimate", "ZS673KS", 2021, False, None),
    ("ROG Phone 5 Pro", "ZS673KS", 2021, False, None),
    ("ROG Phone 5", "ZS673KS", 2021, False, None),
    ("ROG Phone 3", "ZS661KS", 2020, False, None),
    ("ROG Phone II", "ZS660KL", 2019, False, None),
    ("ROG Phone", "ZS600KL", 2018, False, None),
]
for n, m, y, e, note in asus:
    add("Asus", n, m, y, e, note)

# ============================================================
# REALME (all no eSIM)
# ============================================================
realme = [
    ("GT 7 Pro", "RMX3993", 2024),
    ("GT 7", "RMX3990", 2024),
    ("GT 6 Pro", "RMX3856", 2024),
    ("GT 6", "RMX3851", 2024),
    ("GT 6T", "RMX3853", 2024),
    ("GT 5 Pro", "RMX3820", 2023),
    ("GT 5", "RMX3708", 2023),
    ("GT Neo 6 Pro", "RMX3856", 2024),
    ("GT Neo 6", "RMX3853", 2024),
    ("GT Neo 5", "RMX3708", 2023),
    ("GT Neo 3", "RMX3560", 2022),
    ("GT Neo 2", "RMX3370", 2021),
    ("GT 2 Pro", "RMX3301", 2022),
    ("GT 2", "RMX3311", 2022),
    ("GT Master Edition", "RMX3363", 2021),
    ("GT 5G", "RMX2202", 2021),
    ("13 Pro+", "RMX3840", 2024),
    ("13 Pro", "RMX3820", 2024),
    ("13+", "RMX3820", 2024),
    ("12 Pro+", "RMX3840", 2024),
    ("12 Pro", "RMX3842", 2024),
    ("12+ 5G", "RMX3867", 2024),
    ("11 Pro+", "RMX3741", 2023),
    ("11 Pro", "RMX3771", 2023),
    ("11", "RMX3636", 2023),
    ("10 Pro+", "RMX3687", 2023),
    ("10 Pro", "RMX3661", 2023),
    ("10", "RMX3630", 2023),
    ("9 Pro+", "RMX3392", 2022),
    ("9 Pro", "RMX3471", 2022),
    ("9", "RMX3521", 2022),
    ("Narzo 70 Pro", "RMX3868", 2024),
    ("Narzo 70", "RMX3874", 2024),
    ("Narzo 60 Pro", "RMX3771", 2023),
    ("Narzo 60x", "RMX3785", 2023),
    ("Narzo 50 Pro", "RMX3395", 2022),
    ("Narzo 50", "RMX3286", 2022),
    ("Narzo 30", "RMX3161", 2021),
    ("Narzo 20", "RMX2193", 2020),
    ("C67", "RMX3890", 2023),
    ("C55", "RMX3710", 2023),
    ("C51", "RMX3830", 2023),
    ("C35", "RMX3511", 2022),
    ("C33", "RMX3624", 2022),
    ("C31", "RMX3501", 2022),
    ("C30", "RMX3581", 2022),
    ("C25", "RMX3193", 2021),
    ("C21", "RMX3201", 2021),
    ("Note 60", "RMX3910", 2024),
    ("Note 50", "RMX3834", 2024),
    ("Neo 7 Pro", "RMX3865", 2024),
    ("Neo 7", "RMX3872", 2024),
    ("P1 Pro", "RMX3860", 2024),
    ("P1", "RMX3862", 2024),
]
for row in realme:
    n = row[0]; m = row[1]; y = row[2]
    add("Realme", n, m, y, False)

# ============================================================
# NOTHING
# ============================================================
nothing = [
    ("Phone (3)", "A028", 2025, True, None),
    ("Phone (3a) Pro", "A059P", 2025, False, None),
    ("Phone (3a)", "A059", 2025, False, None),
    ("Phone (2a) Plus", "A142P", 2024, False, None),
    ("Phone (2a)", "A142", 2024, False, None),
    ("Phone (2)", "A065", 2023, True, None),
    ("Phone (1)", "A063", 2022, False, None),
    ("CMF Phone 1", "A015", 2024, False, None),
    ("CMF Phone 2 Pro", "A015P", 2025, False, None),
]
for n, m, y, e, note in nothing:
    add("Nothing", n, m, y, e, note)

# ============================================================
# FAIRPHONE
# ============================================================
fairphone = [
    ("Fairphone 6", "FP6", 2025, True, None),
    ("Fairphone 5", "FP5", 2023, True, None),
    ("Fairphone 4", "FP4", 2021, False, None),
    ("Fairphone 3+", "FP3+", 2020, False, None),
    ("Fairphone 3", "FP3", 2019, False, None),
    ("Fairphone 2", "FP2", 2015, False, None),
]
for n, m, y, e, note in fairphone:
    add("Fairphone", n, m, y, e, note)

# ============================================================
# TCL — all no
# ============================================================
tcl = [
    ("50 XL 5G", "T612U", 2024),
    ("50 XE 5G", "T601DL", 2024),
    ("50 SE", "T611O", 2024),
    ("50 5G", "T601L", 2024),
    ("40 XL", "T608M", 2023),
    ("40 XE 5G", "T601DL", 2023),
    ("40 NxtPaper", "T612B", 2023),
    ("40 SE", "T610K", 2023),
    ("40 X", "T601T", 2023),
    ("40 R 5G", "T771B", 2023),
    ("30 XL", "T701DL", 2022),
    ("30 5G", "T776H", 2022),
    ("30 SE", "6165A", 2022),
    ("30 V 5G", "T781S", 2022),
    ("30 XE 5G", "T767U", 2022),
    ("30 Plus", "T776K", 2022),
    ("30 Z", "T602DL", 2022),
    ("30", "T676K", 2022),
    ("20 Pro 5G", "T810H", 2021),
    ("20L+", "T774H", 2021),
    ("20L", "T774B", 2021),
    ("20 R 5G", "T767H", 2021),
    ("20 SE", "T671O", 2021),
    ("20E", "6125D", 2021),
    ("10 5G", "T790Y", 2020),
    ("10 SE", "6127A", 2020),
    ("10L", "6102H", 2020),
    ("Plex", "T780H", 2019),
]
for n, m, y in tcl:
    add("TCL", n, m, y, False)

# ============================================================
# LG (all no eSIM — LG exited smartphone market)
# ============================================================
lg = [
    ("V60 ThinQ 5G", "LM-V600TM", 2020),
    ("V50 ThinQ 5G", "LM-V500N", 2019),
    ("V40 ThinQ", "LM-V405", 2018),
    ("V30", "LG-H930", 2017),
    ("Velvet 5G", "LM-G900N", 2020),
    ("Wing 5G", "LM-F100N", 2020),
    ("G8 ThinQ", "LM-G820", 2019),
    ("G7 ThinQ", "LM-G710", 2018),
    ("G6", "LG-H870", 2017),
    ("K92 5G", "LM-K920", 2020),
    ("K71", "LM-K710YM", 2020),
    ("K61", "LM-K610", 2020),
    ("K51S", "LM-K510", 2020),
    ("K42", "LM-K420", 2020),
    ("K22", "LM-K200", 2020),
    ("Q92 5G", "LM-Q920", 2020),
    ("Stylo 6", "LM-Q730", 2020),
]
for n, m, y in lg:
    add("LG", n, m, y, False)

# ============================================================
# ZTE (mostly no; a couple recent flagships yes)
# ============================================================
zte = [
    ("Nubia Z70 Ultra", "NX713J", 2024, True, None),
    ("Nubia Z60 Ultra", "NX721J", 2024, True, None),
    ("Nubia Flip", "NX724J", 2024, False, None),
    ("Axon 60 Ultra", "A2024PGT", 2024, False, None),
    ("Axon 50 Ultra", "A2023PT", 2023, False, None),
    ("Axon 40 Ultra", "A2022P", 2022, False, None),
    ("Axon 30 Ultra 5G", "A2022PG", 2021, False, None),
    ("Axon 30", "A2322G", 2021, False, None),
    ("Blade V70", "V2050", 2024, False, None),
    ("Blade V60", "V2050", 2024, False, None),
    ("Blade V50 5G", "V2050", 2023, False, None),
    ("Blade A73", "V2158", 2024, False, None),
    ("Blade A54", "V2154", 2024, False, None),
    ("Blade A34", "V2158", 2024, False, None),
    ("Blade A14 5G", "V2158", 2024, False, None),
]
for n, m, y, e, note in zte:
    add("ZTE", n, m, y, e, note)

# ============================================================
# INFINIX / TECNO / ITEL (budget African/Asian brands — all no eSIM)
# ============================================================
infinix = [
    ("Note 40 Pro+ 5G", "X6851", 2024),
    ("Note 40 Pro", "X6850", 2024),
    ("Note 40", "X6853", 2024),
    ("Note 30 Pro", "X678B", 2023),
    ("Note 30 5G", "X6711", 2023),
    ("Note 30", "X6833B", 2023),
    ("Note 12 Pro", "X676B", 2022),
    ("Note 12", "X670", 2022),
    ("Zero 40 5G", "X6861B", 2024),
    ("Zero 40", "X6860", 2024),
    ("Zero 30 5G", "X6731", 2023),
    ("Zero 30", "X6731B", 2023),
    ("Hot 50 Pro+", "X6881B", 2024),
    ("Hot 50 Pro", "X6881", 2024),
    ("Hot 50", "X6882", 2024),
    ("Hot 40 Pro", "X6837", 2023),
    ("Hot 40", "X6836", 2023),
    ("Smart 8 Pro", "X6525B", 2024),
    ("Smart 8", "X6525", 2024),
    ("GT 20 Pro", "X6871", 2024),
    ("GT 10 Pro", "X6739", 2023),
]
for n, m, y in infinix:
    add("Infinix", n, m, y, False)

tecno = [
    ("Camon 30 Premier 5G", "CL9", 2024),
    ("Camon 30 Pro 5G", "CL8", 2024),
    ("Camon 30", "CL7", 2024),
    ("Camon 20 Pro 5G", "CK8n", 2023),
    ("Camon 20 Pro", "CK7n", 2023),
    ("Camon 20", "CK6n", 2023),
    ("Camon 19 Pro", "CI8n", 2022),
    ("Phantom X2 Pro", "AD9", 2022),
    ("Phantom X2", "AD8", 2022),
    ("Phantom V Fold 2", "AD11", 2024),
    ("Phantom V Fold", "AD10", 2023),
    ("Phantom V Flip", "AD11", 2023),
    ("Spark 20 Pro+", "KJ8", 2024),
    ("Spark 20 Pro", "KJ6", 2024),
    ("Spark 20", "KJ5", 2024),
    ("Spark 10 Pro", "KI7", 2023),
    ("Spark 10", "KI5q", 2023),
    ("Pova 6 Pro 5G", "LI7", 2024),
    ("Pova 6", "LI8", 2024),
    ("Pova 5 Pro 5G", "LH8n", 2023),
    ("Pova 5", "LH7n", 2023),
    ("Pop 8", "BG7n", 2024),
    ("Pop 7", "BF6", 2023),
]
for n, m, y in tecno:
    add("Tecno", n, m, y, False)

itel = [
    ("A70", "A665L", 2024),
    ("A60", "A665L", 2023),
    ("A50", "A665L", 2022),
    ("Vision 3 Plus", "S663LP", 2022),
    ("Vision 3", "S661L", 2022),
    ("P55 5G", "P671L", 2024),
    ("P55+", "P671L", 2024),
    ("P55", "P661W", 2024),
    ("P40", "P661L", 2023),
    ("S23+", "S665LP", 2023),
    ("S23", "S665L", 2023),
    ("S18", "S663LP", 2022),
]
for n, m, y in itel:
    add("Itel", n, m, y, False)

# ============================================================
# CAT / KYOCERA / DORO / other rugged / feature
# ============================================================
cat = [
    ("S75", "S75", 2023),
    ("S62 Pro", "S62 Pro", 2020),
    ("S52", "S52", 2019),
    ("S42 H+", "S42 H+", 2021),
    ("S22 Flip", "S22 Flip", 2022),
]
for n, m, y in cat:
    add("Cat", n, m, y, False)

# ============================================================
# MICROSOFT SURFACE DUO (yes)
# ============================================================
add("Microsoft", "Surface Duo 2", "1930", 2021, True)
add("Microsoft", "Surface Duo", "1930", 2020, True)

# ============================================================
# SHARP / Kyocera / Doogee / Ulefone / Blackview (mostly no)
# ============================================================
sharp = [
    ("Aquos R9 Pro", "SH-R90P", 2024, False),
    ("Aquos R9", "SH-R90", 2024, False),
    ("Aquos R8 Pro", "SH-R80P", 2023, False),
    ("Aquos R8", "SH-R80", 2023, False),
    ("Aquos Sense 8", "SH-54D", 2023, False),
    ("Aquos Wish 3", "SH-M25", 2023, False),
]
for n, m, y, e in sharp:
    add("Sharp", n, m, y, e)

for brand, models in {
    "Doogee": [("V Max", 2024), ("V30 Pro", 2023), ("S110", 2024), ("S99 Pro", 2023), ("N50 Pro", 2023)],
    "Ulefone": [("Armor 26 Ultra", 2024), ("Armor 24", 2023), ("Note 17 Pro", 2024), ("Power Armor 19", 2023)],
    "Blackview": [("BV9300 Pro", 2024), ("BV8900", 2024), ("BV9200", 2023), ("A200 Pro", 2024), ("Shark 9", 2024)],
    "Umidigi": [("G9 5G", 2024), ("A15C", 2024), ("Bison 2 Pro", 2023), ("A13 Pro Max", 2023)],
    "Cubot": [("KingKong Star", 2024), ("P80", 2024), ("Note 40", 2024), ("X70", 2024)],
    "OUKITEL": [("WP30 Pro", 2024), ("WP28", 2024), ("C50", 2023), ("C38", 2023)],
    "Kyocera": [("DuraForce Pro 3", 2024), ("DuraSport", 2022), ("DuraForce Ultra 5G", 2021)],
    "Doro": [("8200", 2023), ("8100", 2022), ("780X", 2023), ("730X", 2022)],
    "Emporia": [("SMART.6", 2024), ("SMART.5", 2023), ("SUPEReasy", 2023)],
}.items():
    for name, year in models:
        add(brand, name, "—", year, False)

# ============================================================
# DIVERSITY EXPANSION
# Sourced from build_devices_expansion.py to keep this file readable.
# ============================================================
import build_devices_expansion  # noqa: E402
import build_devices_wave2  # noqa: E402
import build_devices_arc1_compatible  # noqa: E402
import build_devices_arc2_archive  # noqa: E402
import build_devices_arc2_mass  # noqa: E402
import build_devices_arc2_mass2  # noqa: E402
import build_devices_arc2_combinatorial  # noqa: E402

# Wrap add() to skip duplicate (brand, name) pairs coming from the expansion.
_seen = {(d["brand"], d["name"]) for d in DEVICES}
_original_add = add
def _dedup_add(brand, name, model, year, esim, note=None):
    key = (brand, name)
    if key in _seen:
        return
    _seen.add(key)
    _original_add(brand, name, model, year, esim, note)
build_devices_expansion.register(_dedup_add)
build_devices_wave2.register(_dedup_add)
build_devices_arc1_compatible.register(_dedup_add)
build_devices_arc2_archive.register(_dedup_add)
build_devices_arc2_mass.register(_dedup_add)
build_devices_arc2_mass2.register(_dedup_add)
build_devices_arc2_combinatorial.register(_dedup_add)

# ============================================================
# EMIT
# ============================================================
# Sort: eSIM=yes first (newest→oldest), then eSIM=no (newest→oldest)
DEVICES.sort(key=lambda d: (0 if d["esim"] else 1, -d["year"], d["brand"], d["name"]))

count_yes = sum(1 for d in DEVICES if d["esim"])
count_no = sum(1 for d in DEVICES if not d["esim"])
print(f"Total: {len(DEVICES)}  Yes: {count_yes}  No: {count_no}")

# Emit as JS
header = """// Openline eSIM Compatibility Database
// Generated from public rules (Apple, Vodafone UK, Klook, Cybernews, esim-now, mysimguide — Aug 2026).
// Regional variants sometimes differ; notes flag common exceptions.
"""

def js_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'

lines = ["const DEVICES = ["]
for d in DEVICES:
    parts = [
        f'brand: {js_str(d["brand"])}',
        f'name: {js_str(d["name"])}',
        f'model: {js_str(d["model"])}',
        f'year: {d["year"]}',
        f'esim: {"true" if d["esim"] else "false"}',
    ]
    if d.get("note"):
        parts.append(f'note: {js_str(d["note"])}')
    lines.append("  { " + ", ".join(parts) + " },")
lines.append("];")

with open("/home/user/workspace/openline-esim-check/devices.js", "w", encoding="utf-8") as f:
    f.write(header + "\n" + "\n".join(lines) + "\n")

print("Wrote /home/user/workspace/openline-esim-check/devices.js")
