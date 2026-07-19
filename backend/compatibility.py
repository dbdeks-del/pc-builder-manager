"""
PC 부품 호환성 및 병목 분석 모듈
"""

CPU_SOCKET_MAP = {
    # Intel LGA1700 (12th~14th gen)
    "i3-12": "LGA1700", "i5-12": "LGA1700", "i7-12": "LGA1700", "i9-12": "LGA1700",
    "i3-13": "LGA1700", "i5-13": "LGA1700", "i7-13": "LGA1700", "i9-13": "LGA1700",
    "i3-14": "LGA1700", "i5-14": "LGA1700", "i7-14": "LGA1700", "i9-14": "LGA1700",
    # Intel LGA1200 (10th~11th gen)
    "i3-10": "LGA1200", "i5-10": "LGA1200", "i7-10": "LGA1200", "i9-10": "LGA1200",
    "i3-11": "LGA1200", "i5-11": "LGA1200", "i7-11": "LGA1200", "i9-11": "LGA1200",
    # Intel LGA1151v2 (8th~9th gen, Coffee Lake)
    "i3-8": "LGA1151v2", "i5-8": "LGA1151v2", "i7-8": "LGA1151v2",
    "i3-9": "LGA1151v2", "i5-9": "LGA1151v2", "i7-9": "LGA1151v2", "i9-9": "LGA1151v2",
    # Intel LGA1151 (6th~7th gen, Skylake/Kaby Lake)
    "i3-6": "LGA1151", "i5-6": "LGA1151", "i7-6": "LGA1151",
    "i3-7": "LGA1151", "i5-7": "LGA1151", "i7-7": "LGA1151",
    # Intel LGA1150 (4th~5th gen, Haswell/Broadwell)
    "i3-4": "LGA1150", "i5-4": "LGA1150", "i7-4": "LGA1150",
    "i3-5": "LGA1150", "i5-5": "LGA1150", "i7-5": "LGA1150",
    # Intel LGA2011-v3 (X99 HEDT)
    "i7-58": "LGA2011-v3", "i7-59": "LGA2011-v3",
    "i7-68": "LGA2011-v3", "i7-69": "LGA2011-v3",
    # AMD AM5 (Ryzen 7000/9000)
    "ryzen 3 7": "AM5", "ryzen 5 7": "AM5", "ryzen 7 7": "AM5", "ryzen 9 7": "AM5",
    "ryzen 3 9": "AM5", "ryzen 5 9": "AM5", "ryzen 7 9": "AM5", "ryzen 9 9": "AM5",
    # AMD AM4 (Ryzen 5000)
    "ryzen 3 5": "AM4", "ryzen 5 5": "AM4", "ryzen 7 5": "AM4", "ryzen 9 5": "AM4",
    # AMD AM4 (Ryzen 3000)
    "ryzen 3 3": "AM4", "ryzen 5 3": "AM4", "ryzen 7 3": "AM4", "ryzen 9 3": "AM4",
    # AMD AM4 (Ryzen 2000)
    "ryzen 3 2": "AM4", "ryzen 5 2": "AM4", "ryzen 7 2": "AM4",
    # AMD AM4 (Ryzen 1000)
    "ryzen 3 1": "AM4", "ryzen 5 1": "AM4", "ryzen 7 1": "AM4",
    # AMD AM3+ (FX 시리즈)
    "fx-4": "AM3+", "fx-6": "AM3+", "fx-8": "AM3+", "fx-9": "AM3+",
}

MOTHERBOARD_SOCKET_MAP = {
    # Intel LGA1700
    "z790": "LGA1700", "b760": "LGA1700", "h770": "LGA1700", "h610": "LGA1700",
    "z690": "LGA1700", "b660": "LGA1700", "h670": "LGA1700",
    # Intel LGA1200
    "z590": "LGA1200", "b560": "LGA1200", "h510": "LGA1200",
    "z490": "LGA1200", "b460": "LGA1200", "h410": "LGA1200",
    # Intel LGA1151v2 (Coffee Lake 8th/9th gen — Z370 전용)
    "z390": "LGA1151v2", "b365": "LGA1151v2", "b360": "LGA1151v2", "h370": "LGA1151v2",
    "h310": "LGA1151v2",
    "z370": "LGA1151v2",
    # Intel LGA1151 (6th/7th gen — Skylake/Kaby Lake)
    "z270": "LGA1151", "b250": "LGA1151", "h270": "LGA1151", "h110": "LGA1151",
    "z170": "LGA1151", "b150": "LGA1151", "h170": "LGA1151",
    # Intel LGA1150 (4th/5th gen — Haswell/Broadwell)
    "z97": "LGA1150", "h97": "LGA1150",
    "z87": "LGA1150", "h87": "LGA1150", "b85": "LGA1150", "h81": "LGA1150",
    # AMD AM5
    "x670": "AM5", "b650": "AM5", "a620": "AM5",
    # AMD AM4 (500 시리즈)
    "x570": "AM4", "b550": "AM4", "a520": "AM4",
    # AMD AM4 (400 시리즈)
    "x470": "AM4", "b450": "AM4", "a320": "AM4",
    # AMD AM4 (300 시리즈)
    "x370": "AM4", "b350": "AM4",
    # AMD AM3+
    "990fx": "AM3+", "990x": "AM3+", "970": "AM3+",
}

MOTHERBOARD_DDR_MAP = {
    # LGA1700 DDR5/DDR4
    "z790": "DDR5", "b760": "DDR4/DDR5", "h770": "DDR4/DDR5", "h610": "DDR4",
    "z690": "DDR4/DDR5", "b660": "DDR4/DDR5",
    # LGA1200 DDR4
    "z590": "DDR4", "b560": "DDR4", "h510": "DDR4",
    "z490": "DDR4", "b460": "DDR4", "h410": "DDR4",
    # LGA1151v2 DDR4
    "z390": "DDR4", "b365": "DDR4", "b360": "DDR4", "h370": "DDR4", "h310": "DDR4",
    "z370": "DDR4",
    # LGA1151 DDR4
    "z270": "DDR4", "b250": "DDR4", "h270": "DDR4", "h110": "DDR4",
    "z170": "DDR4", "b150": "DDR4", "h170": "DDR4",
    # LGA1150 DDR3
    "z97": "DDR3", "h97": "DDR3",
    "z87": "DDR3", "h87": "DDR3", "b85": "DDR3", "h81": "DDR3",
    # AM5 DDR5
    "x670": "DDR5", "b650": "DDR4/DDR5", "a620": "DDR4",
    # AM4 DDR4
    "x570": "DDR4", "b550": "DDR4", "a520": "DDR4",
    "x470": "DDR4", "b450": "DDR4", "a320": "DDR4",
    "x370": "DDR4", "b350": "DDR4",
    # AM3+ DDR3
    "990fx": "DDR3", "990x": "DDR3", "970": "DDR3",
}

# CPU PassMark 벤치마크 점수 (대략값)
CPU_SCORES = {
    # Intel 14th gen LGA1700
    "i9-14900k": 62000, "i9-14900": 56000,
    "i7-14700k": 52000, "i7-14700": 45000,
    "i5-14600k": 38000, "i5-14600": 33000,
    "i5-14400": 27000, "i3-14100": 14000,
    # Intel 13th gen LGA1700
    "i9-13900k": 60000, "i9-13900": 54000,
    "i7-13700k": 48000, "i7-13700": 42000,
    "i5-13600k": 36000, "i5-13600": 30000,
    "i5-13400": 27000, "i3-13100": 14000,
    # Intel 12th gen LGA1700
    "i9-12900k": 40000, "i9-12900": 36000,
    "i7-12700k": 34000, "i7-12700": 30000,
    "i5-12600k": 28000, "i5-12600": 24000,
    "i5-12400": 24000, "i3-12100": 12000,
    # Intel 11th gen LGA1200
    "i9-11900k": 25000, "i9-11900": 22000,
    "i7-11700k": 22000, "i7-11700": 19000,
    "i5-11600k": 16000, "i5-11600": 14000,
    "i5-11400": 14000, "i3-11100": 8500,
    # Intel 10th gen LGA1200
    "i9-10900k": 22000, "i9-10900": 20000,
    "i7-10700k": 19000, "i7-10700": 17000,
    "i5-10600k": 13000, "i5-10600": 12000,
    "i5-10400": 11000, "i3-10100": 8500,
    "i3-10300": 9000,
    # Intel 9th gen LGA1151v2
    "i9-9900k": 20000, "i9-9900": 18000,
    "i7-9700k": 15000, "i7-9700": 13000,
    "i5-9600k": 12000, "i5-9600": 10000,
    "i5-9400f": 9500, "i5-9400": 9500,
    "i3-9100": 7000,
    # Intel 8th gen LGA1151v2
    "i7-8700k": 14000, "i7-8700": 12000,
    "i5-8600k": 10000, "i5-8600": 9000,
    "i5-8400": 9000, "i3-8100": 7000,
    "i3-8350k": 7500,
    # Intel 7th gen LGA1151
    "i7-7700k": 10000, "i7-7700": 8500,
    "i5-7600k": 8000, "i5-7600": 7000,
    "i5-7500": 7000, "i5-7400": 6000,
    "i3-7100": 5000, "i3-7350k": 5500,
    # Intel 6th gen LGA1151
    "i7-6700k": 9000, "i7-6700": 7500,
    "i5-6600k": 7500, "i5-6600": 6500,
    "i5-6500": 6500, "i5-6400": 5500,
    "i3-6100": 4500, "i3-6300": 5000,
    # Intel 4th/5th gen LGA1150
    "i7-4790k": 8000, "i7-4790": 7000,
    "i7-4770k": 7500, "i7-4770": 7000,
    "i5-4690k": 6000, "i5-4690": 5500,
    "i5-4670k": 6000, "i5-4460": 5000,
    "i3-4170": 4000, "i3-4160": 3800, "i3-4130": 3500,
    # AMD Ryzen 9000 AM5
    "ryzen 9 9950x": 65000, "ryzen 7 9700x": 42000,
    "ryzen 5 9600x": 32000,
    # AMD Ryzen 7000 AM5
    "ryzen 9 7950x": 65000, "ryzen 9 7900x": 55000,
    "ryzen 7 7700x": 42000, "ryzen 7 7700": 36000,
    "ryzen 5 7600x": 32000, "ryzen 5 7600": 28000,
    # AMD Ryzen 5000 AM4
    "ryzen 9 5950x": 50000, "ryzen 9 5900x": 45000,
    "ryzen 7 5800x3d": 40000, "ryzen 7 5800x": 35000, "ryzen 7 5800": 32000,
    "ryzen 5 5600x": 25000, "ryzen 5 5600": 22000,
    "ryzen 5 5500": 18000, "ryzen 3 5300g": 12000,
    # AMD Ryzen 3000 AM4
    "ryzen 9 3950x": 36000, "ryzen 9 3900x": 36000, "ryzen 9 3900xt": 38000,
    "ryzen 7 3800xt": 27000, "ryzen 7 3800x": 25000,
    "ryzen 7 3700x": 24000,
    "ryzen 5 3600x": 18000, "ryzen 5 3600": 15000,
    "ryzen 3 3300x": 10000, "ryzen 3 3100": 8500,
    # AMD Ryzen 2000 AM4
    "ryzen 7 2700x": 15000, "ryzen 7 2700": 13000,
    "ryzen 5 2600x": 12000, "ryzen 5 2600": 11000,
    "ryzen 3 2300x": 7000, "ryzen 3 2200g": 5500,
    # AMD Ryzen 1000 AM4
    "ryzen 7 1800x": 12000, "ryzen 7 1700x": 12000, "ryzen 7 1700": 11000,
    "ryzen 5 1600x": 10000, "ryzen 5 1600": 9000,
    "ryzen 5 1500x": 7500, "ryzen 5 1400": 6500,
    "ryzen 3 1300x": 5500, "ryzen 3 1200": 4500,
    # AMD FX AM3+
    "fx-9590": 7500, "fx-9370": 6500,
    "fx-8370": 7000, "fx-8350": 7000, "fx-8320": 6000, "fx-8300": 5500,
    "fx-6350": 5500, "fx-6300": 5000,
    "fx-4350": 3500, "fx-4300": 3000,
}

# GPU 3DMark TimeSpy 벤치마크 점수 (대략값)
GPU_SCORES = {
    # RTX 4000 시리즈
    "rtx 4090": 22000, "rtx 4080 super": 18000, "rtx 4080": 17000,
    "rtx 4070 ti super": 15500, "rtx 4070 ti": 14000,
    "rtx 4070 super": 12500, "rtx 4070": 11000,
    "rtx 4060 ti": 9000, "rtx 4060": 7500,
    "rtx 4050": 5500,
    # RTX 3000 시리즈
    "rtx 3090 ti": 17000, "rtx 3090": 16000,
    "rtx 3080 ti": 15000, "rtx 3080 12gb": 14500, "rtx 3080": 14000,
    "rtx 3070 ti": 11500, "rtx 3070": 10000,
    "rtx 3060 ti": 9000, "rtx 3060": 7000,
    "rtx 3050": 4500,
    # RTX 2000 시리즈
    "rtx 2080 ti": 9000, "rtx 2080 super": 8500, "rtx 2080": 7500,
    "rtx 2070 super": 7000, "rtx 2070": 6000,
    "rtx 2060 super": 5800, "rtx 2060": 5000,
    # GTX 1600 시리즈
    "gtx 1660 super": 4500, "gtx 1660 ti": 4200, "gtx 1660": 3700,
    "gtx 1650 super": 3000, "gtx 1650": 2200,
    # GTX 1000 시리즈
    "gtx 1080 ti": 5000, "gtx 1080": 4000,
    "gtx 1070 ti": 4000, "gtx 1070": 3500,
    "gtx 1060 6gb": 2500, "gtx 1060 3gb": 2000,
    "gtx 1060": 2400,
    "gtx 1050 ti": 1500, "gtx 1050": 1100,
    # GTX 900 시리즈
    "gtx 980 ti": 3000, "gtx 980": 2500,
    "gtx 970": 2200, "gtx 960": 1300,
    "gtx 950": 1000,
    # GTX 700 시리즈
    "gtx 780 ti": 2000, "gtx 780": 1700,
    "gtx 770": 1300, "gtx 760": 1000,
    # RX 7000 시리즈
    "rx 7900 xtx": 20000, "rx 7900 xt": 17000, "rx 7900 gre": 14500,
    "rx 7800 xt": 12000, "rx 7700 xt": 10000,
    "rx 7600 xt": 8000, "rx 7600": 7000,
    # RX 6000 시리즈
    "rx 6950 xt": 17000, "rx 6900 xt": 16000,
    "rx 6800 xt": 14000, "rx 6800": 12000,
    "rx 6750 xt": 11000, "rx 6700 xt": 10000, "rx 6700": 8500,
    "rx 6650 xt": 8500, "rx 6600 xt": 8000, "rx 6600": 6500,
    "rx 6500 xt": 3500, "rx 6400": 2200,
    # RX 5000 시리즈
    "rx 5700 xt": 7000, "rx 5700": 6000,
    "rx 5600 xt": 5000, "rx 5500 xt": 2800,
    # Vega
    "radeon vii": 8000, "vega 64": 4500, "vega 56": 3800,
    # RX 400/500 시리즈
    "rx 590": 3200, "rx 580 8gb": 2800, "rx 580": 2600,
    "rx 570": 2100, "rx 560": 1400,
    "rx 480 8gb": 2500, "rx 480": 2300,
    "rx 470": 2000, "rx 460": 1100,
    # R9 시리즈
    "r9 390x": 2200, "r9 390": 1900,
    "r9 380x": 1500, "r9 380": 1300,
    "r9 290x": 1800, "r9 290": 1600,
    "r9 280x": 1200, "r9 280": 1000,
    "r9 270x": 900, "r9 270": 800,
}

GPU_TDP = {
    # RTX 4000
    "rtx 4090": 450, "rtx 4080 super": 320, "rtx 4080": 320,
    "rtx 4070 ti super": 285, "rtx 4070 ti": 285,
    "rtx 4070 super": 220, "rtx 4070": 200,
    "rtx 4060 ti": 165, "rtx 4060": 115, "rtx 4050": 90,
    # RTX 3000
    "rtx 3090 ti": 450, "rtx 3090": 350,
    "rtx 3080 ti": 350, "rtx 3080": 320,
    "rtx 3070 ti": 290, "rtx 3070": 220,
    "rtx 3060 ti": 200, "rtx 3060": 170, "rtx 3050": 130,
    # RTX 2000
    "rtx 2080 ti": 250, "rtx 2080 super": 250, "rtx 2080": 215,
    "rtx 2070 super": 215, "rtx 2070": 175,
    "rtx 2060 super": 175, "rtx 2060": 160,
    # GTX 1600
    "gtx 1660 super": 125, "gtx 1660 ti": 120, "gtx 1660": 120,
    "gtx 1650 super": 100, "gtx 1650": 75,
    # GTX 1000
    "gtx 1080 ti": 250, "gtx 1080": 180,
    "gtx 1070 ti": 180, "gtx 1070": 150,
    "gtx 1060 6gb": 120, "gtx 1060 3gb": 120, "gtx 1060": 120,
    "gtx 1050 ti": 75, "gtx 1050": 75,
    # GTX 900
    "gtx 980 ti": 250, "gtx 980": 165,
    "gtx 970": 145, "gtx 960": 120, "gtx 950": 90,
    # GTX 700
    "gtx 780 ti": 250, "gtx 780": 250,
    "gtx 770": 230, "gtx 760": 170,
    # RX 7000
    "rx 7900 xtx": 355, "rx 7900 xt": 315,
    "rx 7800 xt": 263, "rx 7700 xt": 245,
    "rx 7600": 165,
    # RX 6000
    "rx 6950 xt": 335, "rx 6900 xt": 300,
    "rx 6800 xt": 300, "rx 6800": 250,
    "rx 6700 xt": 230, "rx 6700": 175,
    "rx 6600 xt": 160, "rx 6600": 132,
    # RX 5000
    "rx 5700 xt": 225, "rx 5700": 180,
    "rx 5600 xt": 150, "rx 5500 xt": 130,
    # Vega
    "radeon vii": 295, "vega 64": 295, "vega 56": 210,
    # RX 400/500
    "rx 590": 225, "rx 580 8gb": 185, "rx 580": 185,
    "rx 570": 150, "rx 480 8gb": 150, "rx 480": 150,
    "rx 470": 120, "rx 460": 75,
    # R9
    "r9 390x": 275, "r9 390": 275,
    "r9 380x": 190, "r9 380": 190,
    "r9 290x": 290, "r9 290": 250,
    "r9 280x": 250, "r9 280": 200,
}

CPU_TDP = {
    # Intel 14th gen
    "i9-14900k": 253, "i9-14900": 65,
    "i7-14700k": 253, "i7-14700": 65,
    "i5-14600k": 181, "i5-14600": 65, "i5-14400": 65, "i3-14100": 60,
    # Intel 13th gen
    "i9-13900k": 253, "i9-13900": 65,
    "i7-13700k": 253, "i7-13700": 65,
    "i5-13600k": 181, "i5-13600": 65,
    "i5-13400": 65, "i3-13100": 60,
    # Intel 12th gen
    "i9-12900k": 241, "i9-12900": 65,
    "i7-12700k": 190, "i7-12700": 65,
    "i5-12600k": 125, "i5-12600": 65,
    "i5-12400": 65, "i3-12100": 60,
    # Intel 11th gen
    "i9-11900k": 125, "i7-11700k": 125, "i5-11600k": 125,
    "i5-11400": 65, "i3-11100": 65,
    # Intel 10th gen
    "i9-10900k": 125, "i7-10700k": 125, "i5-10600k": 125,
    "i5-10400": 65, "i3-10100": 65,
    # Intel 9th gen
    "i9-9900k": 95, "i7-9700k": 95, "i5-9600k": 95,
    "i5-9400f": 65, "i3-9100": 65,
    # Intel 8th gen
    "i7-8700k": 95, "i7-8700": 65, "i5-8600k": 95,
    "i5-8400": 65, "i3-8100": 65,
    # Intel 7th gen
    "i7-7700k": 91, "i7-7700": 65, "i5-7600k": 91, "i5-7600": 65,
    "i5-7500": 65, "i3-7100": 51,
    # Intel 6th gen
    "i7-6700k": 91, "i7-6700": 65, "i5-6600k": 91, "i5-6600": 65,
    "i5-6500": 65, "i3-6100": 51,
    # Intel 4th/5th gen
    "i7-4790k": 88, "i7-4790": 84, "i7-4770k": 84,
    "i5-4690k": 88, "i5-4460": 84, "i3-4130": 54,
    # AMD Ryzen 9000
    "ryzen 9 9950x": 170, "ryzen 7 9700x": 65, "ryzen 5 9600x": 65,
    # AMD Ryzen 7000
    "ryzen 9 7950x": 170, "ryzen 9 7900x": 170,
    "ryzen 7 7700x": 105, "ryzen 7 7700": 65,
    "ryzen 5 7600x": 105, "ryzen 5 7600": 65,
    # AMD Ryzen 5000
    "ryzen 9 5950x": 105, "ryzen 9 5900x": 105,
    "ryzen 7 5800x3d": 105, "ryzen 7 5800x": 105,
    "ryzen 5 5600x": 65, "ryzen 5 5600": 65,
    # AMD Ryzen 3000
    "ryzen 9 3950x": 105, "ryzen 9 3900x": 105,
    "ryzen 7 3700x": 65, "ryzen 5 3600": 65,
    # AMD Ryzen 2000
    "ryzen 7 2700x": 105, "ryzen 7 2700": 65,
    "ryzen 5 2600x": 95, "ryzen 5 2600": 65,
    # AMD Ryzen 1000
    "ryzen 7 1800x": 95, "ryzen 7 1700x": 95, "ryzen 7 1700": 65,
    "ryzen 5 1600x": 95, "ryzen 5 1600": 65,
    # AMD FX
    "fx-9590": 220, "fx-8350": 125, "fx-8300": 95,
    "fx-6350": 125, "fx-6300": 95, "fx-4300": 95,
}

# 각 스케일의 최댓값 (정규화 기준)
_CPU_SCORE_MAX = 65000
_GPU_SCORE_MAX = 22000


import re


# 한글 표기 → 영문 (매칭 전 치환)
KOREAN_ALIASES = [
    ("쓰레드리퍼", "threadripper"), ("스레드리퍼", "threadripper"),
    ("라이젠", "ryzen"), ("인텔", "intel"), ("코어", "core"),
    ("지포스", "geforce"), ("라데온", "radeon"),
    ("펜티엄", "pentium"), ("셀러론", "celeron"), ("제온", "xeon"),
]


def _normalize(s: str) -> str:
    """공백/기호 제거 소문자화 + 한글 별칭 치환 — '라이젠5 3600'과 'ryzen 5 3600' 매칭용"""
    s = s.lower()
    for ko, en in KOREAN_ALIASES:
        s = s.replace(ko, en)
    return re.sub(r"[^a-z0-9가-힣]", "", s)


def longest_match(name_norm: str, normalized_map: dict):
    """정규화된 이름에서, 정규화된 키들 중 가장 긴 부분일치 키의 값을 반환.
    호출부는 각자의 방식으로 정규화를 마친 맵을 넘긴다 (scoring.py도 이 함수를 재사용)."""
    best_val, best_len = None, 0
    for key_norm, val in normalized_map.items():
        if key_norm in name_norm and len(key_norm) > best_len:
            best_val, best_len = val, len(key_norm)
    return best_val


# 정적 맵(소켓/점수/TDP 테이블)의 정규화 결과 캐시 — 맵은 모듈 로드 시 한 번만 만들어지는
# 전역 상수이므로 id() 기반 캐시로 충분하고, 매 조회마다 모든 키를 재정규화하지 않아도 된다.
_norm_map_cache: dict[int, dict[str, object]] = {}


def _normalized_map(mapping: dict) -> dict:
    cached = _norm_map_cache.get(id(mapping))
    if cached is None:
        cached = {_normalize(k): v for k, v in mapping.items()}
        _norm_map_cache[id(mapping)] = cached
    return cached


def find_score(name: str, score_map: dict) -> float:
    """이름으로 점수를 찾음 (가장 긴 키 우선으로 매칭)"""
    val = longest_match(_normalize(name), _normalized_map(score_map))
    return val if val is not None else 0


def find_socket(name: str, socket_map: dict) -> str | None:
    """이름으로 소켓/슬롯 정보를 찾음 (가장 긴 키 우선)"""
    return longest_match(_normalize(name), _normalized_map(socket_map))


def check_compatibility(parts: list[dict]) -> dict:
    """부품 목록을 받아 호환성 체크 결과 반환"""
    issues = []
    warnings = []

    cpu = next((p for p in parts if p["category"] == "cpu"), None)
    motherboard = next((p for p in parts if p["category"] == "motherboard"), None)
    ram = next((p for p in parts if p["category"] == "ram"), None)
    psu = next((p for p in parts if p["category"] == "psu"), None)
    gpu = next((p for p in parts if p["category"] == "gpu"), None)

    # CPU - 메인보드 소켓 호환성
    if cpu and motherboard:
        cpu_name = f"{cpu['brand']} {cpu['model']}".lower()
        mb_name = f"{motherboard['brand']} {motherboard['model']}".lower()

        # specs에 직접 소켓 정보가 있으면 우선 사용
        cpu_socket = cpu.get("specs", {}).get("socket") or find_socket(cpu_name, CPU_SOCKET_MAP)
        mb_socket = motherboard.get("specs", {}).get("socket") or find_socket(mb_name, MOTHERBOARD_SOCKET_MAP)

        # LGA1151 vs LGA1151v2: Z370 이하 보드는 8/9세대 CPU와 호환
        # (실제로는 바이오스 업데이트 필요하지만 Z390/B360 등 네이티브 지원)
        compatible_pairs = {
            ("LGA1151", "LGA1151v2"): True,
            ("LGA1151v2", "LGA1151"): True,
        }

        if cpu_socket and mb_socket:
            if cpu_socket != mb_socket and (cpu_socket, mb_socket) not in compatible_pairs:
                issues.append({
                    "type": "socket_mismatch",
                    "severity": "error",
                    "message": f"CPU 소켓({cpu_socket})과 메인보드 소켓({mb_socket})이 호환되지 않습니다.",
                    "parts": ["cpu", "motherboard"]
                })
            elif (cpu_socket, mb_socket) in compatible_pairs:
                warnings.append({
                    "type": "socket_warning",
                    "message": f"CPU({cpu_socket})와 메인보드({mb_socket})는 일부 호환되나 바이오스 업데이트가 필요할 수 있습니다."
                })
        elif not cpu_socket:
            warnings.append({
                "type": "unknown_cpu_socket",
                "message": f"CPU 소켓 정보를 확인할 수 없습니다: {cpu['model']}"
            })

    # RAM DDR 세대 호환성
    if ram and motherboard:
        ram_specs = ram.get("specs", {})
        ram_ddr = ram_specs.get("ddr_type", "")
        mb_name = f"{motherboard['brand']} {motherboard['model']}".lower()
        mb_ddr = motherboard.get("specs", {}).get("ddr_type") or find_socket(mb_name, MOTHERBOARD_DDR_MAP) or ""

        if ram_ddr and mb_ddr:
            if ram_ddr not in mb_ddr:
                issues.append({
                    "type": "ram_incompatible",
                    "severity": "error",
                    "message": f"RAM 규격({ram_ddr})이 메인보드({mb_ddr})와 호환되지 않습니다.",
                    "parts": ["ram", "motherboard"]
                })

    # PSU 와트수 적합성
    if psu and (cpu or gpu):
        psu_specs = psu.get("specs", {})
        psu_watt = psu_specs.get("wattage", 0)

        cpu_power = find_score(f"{cpu['brand']} {cpu['model']}" if cpu else "", CPU_TDP) or 65
        gpu_power = find_score(f"{gpu['brand']} {gpu['model']}" if gpu else "", GPU_TDP) or 0
        base_power = 80  # 기타 부품 (M/B, RAM, 스토리지, 쿨러 등)
        recommended_watt = int((cpu_power + gpu_power + base_power) * 1.2)

        if psu_watt > 0 and psu_watt < recommended_watt:
            issues.append({
                "type": "psu_insufficient",
                "severity": "error",
                "message": f"파워 용량({psu_watt}W)이 부족합니다. 권장: {recommended_watt}W 이상",
                "parts": ["psu"],
                "recommended_watt": recommended_watt
            })
        elif psu_watt > 0:
            warnings.append({
                "type": "psu_info",
                "message": f"파워 {psu_watt}W (권장 최소: {recommended_watt}W) — 적합합니다."
            })

    return {
        "compatible": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
    }


def analyze_bottleneck(parts: list[dict]) -> dict:
    """CPU-GPU 병목 및 기타 병목 분석"""
    results = []

    cpu = next((p for p in parts if p["category"] == "cpu"), None)
    gpu = next((p for p in parts if p["category"] == "gpu"), None)
    ram = next((p for p in parts if p["category"] == "ram"), None)

    # CPU-GPU 병목 분석
    if cpu and gpu:
        cpu_score = find_score(f"{cpu['brand']} {cpu['model']}", CPU_SCORES)
        gpu_score = find_score(f"{gpu['brand']} {gpu['model']}", GPU_SCORES)

        if cpu_score > 0 and gpu_score > 0:
            # 동일 스케일(0~100)로 정규화
            cpu_norm = min(cpu_score / _CPU_SCORE_MAX * 100, 100)
            gpu_norm = min(gpu_score / _GPU_SCORE_MAX * 100, 100)

            ratio = cpu_norm / gpu_norm if gpu_norm > 0 else 1

            if ratio < 0.65:
                bottleneck_pct = int((1 - ratio) * 100)
                results.append({
                    "type": "cpu_bottleneck",
                    "severity": "high",
                    "message": f"CPU 병목 발생! CPU가 GPU 성능을 {bottleneck_pct}% 제한하고 있습니다.",
                    "detail": f"CPU 성능 지수: {cpu_norm:.0f} / GPU 성능 지수: {gpu_norm:.0f}",
                    "recommendation": f"CPU 업그레이드를 권장합니다. 현재 GPU({gpu['model']})에 맞는 CPU를 선택하세요."
                })
            elif ratio > 1.55:
                bottleneck_pct = int((1 - 1 / ratio) * 100)
                results.append({
                    "type": "gpu_bottleneck",
                    "severity": "high",
                    "message": f"GPU 병목 발생! GPU가 CPU 성능을 {bottleneck_pct}% 제한하고 있습니다.",
                    "detail": f"CPU 성능 지수: {cpu_norm:.0f} / GPU 성능 지수: {gpu_norm:.0f}",
                    "recommendation": f"GPU 업그레이드를 권장합니다. 현재 CPU({cpu['model']})에 맞는 GPU를 선택하세요."
                })
            else:
                balance_score = 100 - abs(cpu_norm - gpu_norm)
                results.append({
                    "type": "balanced",
                    "severity": "ok",
                    "message": f"CPU-GPU 균형이 잘 맞습니다. (균형도: {balance_score:.0f}%)",
                    "detail": f"CPU 성능 지수: {cpu_norm:.0f} / GPU 성능 지수: {gpu_norm:.0f}",
                })
        elif cpu_score == 0 and gpu_score == 0:
            results.append({
                "type": "unknown",
                "severity": "info",
                "message": f"CPU({cpu['model']})와 GPU({gpu['model']}) 벤치마크 데이터가 없습니다.",
            })
        elif cpu_score == 0:
            results.append({
                "type": "unknown_cpu",
                "severity": "info",
                "message": f"CPU({cpu['model']}) 벤치마크 데이터가 없습니다. GPU만 분석합니다.",
            })
        elif gpu_score == 0:
            results.append({
                "type": "unknown_gpu",
                "severity": "info",
                "message": f"GPU({gpu['model']}) 벤치마크 데이터가 없습니다. CPU만 분석합니다.",
            })

    # RAM 용량 분석
    if ram:
        ram_specs = ram.get("specs", {})
        ram_gb = ram_specs.get("capacity_gb", 0)
        if ram_gb > 0:
            if ram_gb < 8:
                results.append({
                    "type": "ram_low",
                    "severity": "high",
                    "message": f"RAM {ram_gb}GB는 현대 작업에 부족합니다. 최소 16GB 권장.",
                    "recommendation": "RAM을 16GB 이상으로 업그레이드하세요."
                })
            elif ram_gb < 16:
                results.append({
                    "type": "ram_warning",
                    "severity": "medium",
                    "message": f"RAM {ram_gb}GB — 가벼운 작업에는 충분하지만 게임/멀티태스킹에 16GB 권장.",
                })
            else:
                results.append({
                    "type": "ram_ok",
                    "severity": "ok",
                    "message": f"RAM {ram_gb}GB — 충분합니다.",
                })

    # RAM 속도 분석
    if ram:
        ram_specs = ram.get("specs", {})
        ram_speed = ram_specs.get("speed_mhz", 0)
        ram_ddr = ram_specs.get("ddr_type", "")
        if ram_speed > 0:
            if ram_ddr == "DDR5" and ram_speed < 4800:
                results.append({
                    "type": "ram_slow",
                    "severity": "medium",
                    "message": f"DDR5 {ram_speed}MHz — 느립니다. 5600MHz 이상 권장.",
                })
            elif ram_ddr != "DDR5" and ram_speed < 3200:
                results.append({
                    "type": "ram_slow",
                    "severity": "medium",
                    "message": f"RAM 속도 {ram_speed}MHz — 느립니다. DDR4 3200MHz 이상 권장.",
                    "recommendation": "더 빠른 RAM으로 교체하면 성능이 향상됩니다."
                })

    return {"bottlenecks": results}


def recommend_build(parts: list[dict], purpose: str = "gaming") -> dict:
    """보유 부품 기반 최적 빌드 추천"""
    owned_parts = [p for p in parts if p.get("owned", True)]
    categories = {p["category"]: p for p in owned_parts}

    missing = []
    upgrade_suggestions = []

    required = ["cpu", "motherboard", "ram", "gpu", "psu", "case"]
    for cat in required:
        if cat not in categories:
            missing.append(cat)

    # 병목 분석 기반 업그레이드 추천
    bottleneck_result = analyze_bottleneck(owned_parts)
    for b in bottleneck_result["bottlenecks"]:
        if b["severity"] in ("high", "medium") and b["type"] not in ("balanced", "ram_ok"):
            upgrade_suggestions.append({
                "category": b["type"].replace("_bottleneck", "").replace("_low", "").replace("_warning", "").replace("_slow", ""),
                "reason": b["message"],
                "recommendation": b.get("recommendation", ""),
            })

    # 목적별 가중치 (cpu_weight + gpu_weight = 1.0)
    weights = {
        "gaming": {"cpu": 0.35, "gpu": 0.65},      # 게임은 GPU 비중 높음
        "work": {"cpu": 0.65, "gpu": 0.35},         # 작업(영상편집, 렌더링)은 CPU 비중
        "streaming": {"cpu": 0.55, "gpu": 0.45},   # 스트리밍은 CPU 인코딩 중요
        "office": {"cpu": 0.70, "gpu": 0.30},       # 사무용은 CPU 위주
    }
    w = weights.get(purpose, weights["gaming"])

    cpu_score = 0
    gpu_score = 0
    if "cpu" in categories:
        raw = find_score(f"{categories['cpu']['brand']} {categories['cpu']['model']}", CPU_SCORES)
        cpu_score = min(raw / _CPU_SCORE_MAX * 100, 100)
    if "gpu" in categories:
        raw = find_score(f"{categories['gpu']['brand']} {categories['gpu']['model']}", GPU_SCORES)
        gpu_score = min(raw / _GPU_SCORE_MAX * 100, 100)

    # 0~100 단일 점수
    score = round(cpu_score * w["cpu"] + gpu_score * w["gpu"])

    purpose_labels = {
        "gaming": "게임",
        "work": "작업(영상편집/렌더링)",
        "streaming": "스트리밍",
        "office": "사무/일반 작업",
    }
    label = purpose_labels.get(purpose, purpose)

    return {
        "purpose": purpose,
        "purpose_label": label,
        "estimated_score": score,
        "cpu_score": round(cpu_score),
        "gpu_score": round(gpu_score),
        "missing_parts": missing,
        "upgrade_suggestions": upgrade_suggestions,
        "build_summary": f"[{label}] 빌드 점수: {score} / 100",
    }
