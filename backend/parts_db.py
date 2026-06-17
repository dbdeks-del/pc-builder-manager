"""
PC 부품 모델 데이터베이스
category, brand, model, specs 포함
"""

PARTS_DATABASE = [
    # ────────────────── CPU ──────────────────
    # Intel 14세대
    {"category": "cpu", "brand": "Intel", "model": "Core i9-14900K", "specs": {"socket": "LGA1700", "cores": 24, "threads": 32, "base_clock_ghz": 3.2, "boost_clock_ghz": 6.0, "tdp_w": 125, "architecture": "Raptor Lake Refresh"}},
    {"category": "cpu", "brand": "Intel", "model": "Core i9-14900KF", "specs": {"socket": "LGA1700", "cores": 24, "threads": 32, "base_clock_ghz": 3.2, "boost_clock_ghz": 6.0, "tdp_w": 125, "architecture": "Raptor Lake Refresh"}},
    {"category": "cpu", "brand": "Intel", "model": "Core i7-14700K", "specs": {"socket": "LGA1700", "cores": 20, "threads": 28, "base_clock_ghz": 3.4, "boost_clock_ghz": 5.6, "tdp_w": 125, "architecture": "Raptor Lake Refresh"}},
    {"category": "cpu", "brand": "Intel", "model": "Core i7-14700KF", "specs": {"socket": "LGA1700", "cores": 20, "threads": 28, "base_clock_ghz": 3.4, "boost_clock_ghz": 5.6, "tdp_w": 125, "architecture": "Raptor Lake Refresh"}},
    {"category": "cpu", "brand": "Intel", "model": "Core i5-14600K", "specs": {"socket": "LGA1700", "cores": 14, "threads": 20, "base_clock_ghz": 3.5, "boost_clock_ghz": 5.3, "tdp_w": 125, "architecture": "Raptor Lake Refresh"}},
    {"category": "cpu", "brand": "Intel", "model": "Core i5-14600KF", "specs": {"socket": "LGA1700", "cores": 14, "threads": 20, "base_clock_ghz": 3.5, "boost_clock_ghz": 5.3, "tdp_w": 125, "architecture": "Raptor Lake Refresh"}},
    {"category": "cpu", "brand": "Intel", "model": "Core i5-14400F", "specs": {"socket": "LGA1700", "cores": 10, "threads": 16, "base_clock_ghz": 2.5, "boost_clock_ghz": 4.7, "tdp_w": 65, "architecture": "Raptor Lake Refresh"}},
    {"category": "cpu", "brand": "Intel", "model": "Core i5-14400", "specs": {"socket": "LGA1700", "cores": 10, "threads": 16, "base_clock_ghz": 2.5, "boost_clock_ghz": 4.7, "tdp_w": 65, "architecture": "Raptor Lake Refresh"}},
    {"category": "cpu", "brand": "Intel", "model": "Core i3-14100F", "specs": {"socket": "LGA1700", "cores": 4, "threads": 8, "base_clock_ghz": 3.5, "boost_clock_ghz": 4.7, "tdp_w": 58, "architecture": "Raptor Lake Refresh"}},
    {"category": "cpu", "brand": "Intel", "model": "Core i3-14100", "specs": {"socket": "LGA1700", "cores": 4, "threads": 8, "base_clock_ghz": 3.5, "boost_clock_ghz": 4.7, "tdp_w": 60, "architecture": "Raptor Lake Refresh"}},
    # Intel 13세대
    {"category": "cpu", "brand": "Intel", "model": "Core i9-13900K", "specs": {"socket": "LGA1700", "cores": 24, "threads": 32, "base_clock_ghz": 3.0, "boost_clock_ghz": 5.8, "tdp_w": 125, "architecture": "Raptor Lake"}},
    {"category": "cpu", "brand": "Intel", "model": "Core i9-13900KF", "specs": {"socket": "LGA1700", "cores": 24, "threads": 32, "base_clock_ghz": 3.0, "boost_clock_ghz": 5.8, "tdp_w": 125, "architecture": "Raptor Lake"}},
    {"category": "cpu", "brand": "Intel", "model": "Core i7-13700K", "specs": {"socket": "LGA1700", "cores": 16, "threads": 24, "base_clock_ghz": 3.4, "boost_clock_ghz": 5.4, "tdp_w": 125, "architecture": "Raptor Lake"}},
    {"category": "cpu", "brand": "Intel", "model": "Core i7-13700KF", "specs": {"socket": "LGA1700", "cores": 16, "threads": 24, "base_clock_ghz": 3.4, "boost_clock_ghz": 5.4, "tdp_w": 125, "architecture": "Raptor Lake"}},
    {"category": "cpu", "brand": "Intel", "model": "Core i5-13600K", "specs": {"socket": "LGA1700", "cores": 14, "threads": 20, "base_clock_ghz": 3.5, "boost_clock_ghz": 5.1, "tdp_w": 125, "architecture": "Raptor Lake"}},
    {"category": "cpu", "brand": "Intel", "model": "Core i5-13600KF", "specs": {"socket": "LGA1700", "cores": 14, "threads": 20, "base_clock_ghz": 3.5, "boost_clock_ghz": 5.1, "tdp_w": 125, "architecture": "Raptor Lake"}},
    {"category": "cpu", "brand": "Intel", "model": "Core i5-13400F", "specs": {"socket": "LGA1700", "cores": 10, "threads": 16, "base_clock_ghz": 2.5, "boost_clock_ghz": 4.6, "tdp_w": 65, "architecture": "Raptor Lake"}},
    {"category": "cpu", "brand": "Intel", "model": "Core i5-13400", "specs": {"socket": "LGA1700", "cores": 10, "threads": 16, "base_clock_ghz": 2.5, "boost_clock_ghz": 4.6, "tdp_w": 65, "architecture": "Raptor Lake"}},
    {"category": "cpu", "brand": "Intel", "model": "Core i3-13100F", "specs": {"socket": "LGA1700", "cores": 4, "threads": 8, "base_clock_ghz": 3.4, "boost_clock_ghz": 4.5, "tdp_w": 58, "architecture": "Raptor Lake"}},
    {"category": "cpu", "brand": "Intel", "model": "Core i3-13100", "specs": {"socket": "LGA1700", "cores": 4, "threads": 8, "base_clock_ghz": 3.4, "boost_clock_ghz": 4.5, "tdp_w": 60, "architecture": "Raptor Lake"}},
    # Intel 12세대
    {"category": "cpu", "brand": "Intel", "model": "Core i9-12900K", "specs": {"socket": "LGA1700", "cores": 16, "threads": 24, "base_clock_ghz": 3.2, "boost_clock_ghz": 5.2, "tdp_w": 125, "architecture": "Alder Lake"}},
    {"category": "cpu", "brand": "Intel", "model": "Core i7-12700K", "specs": {"socket": "LGA1700", "cores": 12, "threads": 20, "base_clock_ghz": 3.6, "boost_clock_ghz": 5.0, "tdp_w": 125, "architecture": "Alder Lake"}},
    {"category": "cpu", "brand": "Intel", "model": "Core i5-12600K", "specs": {"socket": "LGA1700", "cores": 10, "threads": 16, "base_clock_ghz": 3.7, "boost_clock_ghz": 4.9, "tdp_w": 125, "architecture": "Alder Lake"}},
    {"category": "cpu", "brand": "Intel", "model": "Core i5-12400F", "specs": {"socket": "LGA1700", "cores": 6, "threads": 12, "base_clock_ghz": 2.5, "boost_clock_ghz": 4.4, "tdp_w": 65, "architecture": "Alder Lake"}},
    {"category": "cpu", "brand": "Intel", "model": "Core i5-12400", "specs": {"socket": "LGA1700", "cores": 6, "threads": 12, "base_clock_ghz": 2.5, "boost_clock_ghz": 4.4, "tdp_w": 65, "architecture": "Alder Lake"}},
    {"category": "cpu", "brand": "Intel", "model": "Core i3-12100F", "specs": {"socket": "LGA1700", "cores": 4, "threads": 8, "base_clock_ghz": 3.3, "boost_clock_ghz": 4.3, "tdp_w": 58, "architecture": "Alder Lake"}},
    # AMD Ryzen 7000 (AM5)
    {"category": "cpu", "brand": "AMD", "model": "Ryzen 9 7950X", "specs": {"socket": "AM5", "cores": 16, "threads": 32, "base_clock_ghz": 4.5, "boost_clock_ghz": 5.7, "tdp_w": 170, "architecture": "Zen 4"}},
    {"category": "cpu", "brand": "AMD", "model": "Ryzen 9 7900X", "specs": {"socket": "AM5", "cores": 12, "threads": 24, "base_clock_ghz": 4.7, "boost_clock_ghz": 5.6, "tdp_w": 170, "architecture": "Zen 4"}},
    {"category": "cpu", "brand": "AMD", "model": "Ryzen 9 7900X3D", "specs": {"socket": "AM5", "cores": 12, "threads": 24, "base_clock_ghz": 4.4, "boost_clock_ghz": 5.6, "tdp_w": 120, "architecture": "Zen 4 3D V-Cache"}},
    {"category": "cpu", "brand": "AMD", "model": "Ryzen 7 7800X3D", "specs": {"socket": "AM5", "cores": 8, "threads": 16, "base_clock_ghz": 4.5, "boost_clock_ghz": 5.0, "tdp_w": 120, "architecture": "Zen 4 3D V-Cache"}},
    {"category": "cpu", "brand": "AMD", "model": "Ryzen 7 7700X", "specs": {"socket": "AM5", "cores": 8, "threads": 16, "base_clock_ghz": 4.5, "boost_clock_ghz": 5.4, "tdp_w": 105, "architecture": "Zen 4"}},
    {"category": "cpu", "brand": "AMD", "model": "Ryzen 7 7700", "specs": {"socket": "AM5", "cores": 8, "threads": 16, "base_clock_ghz": 3.8, "boost_clock_ghz": 5.3, "tdp_w": 65, "architecture": "Zen 4"}},
    {"category": "cpu", "brand": "AMD", "model": "Ryzen 5 7600X", "specs": {"socket": "AM5", "cores": 6, "threads": 12, "base_clock_ghz": 4.7, "boost_clock_ghz": 5.3, "tdp_w": 105, "architecture": "Zen 4"}},
    {"category": "cpu", "brand": "AMD", "model": "Ryzen 5 7600", "specs": {"socket": "AM5", "cores": 6, "threads": 12, "base_clock_ghz": 3.8, "boost_clock_ghz": 5.1, "tdp_w": 65, "architecture": "Zen 4"}},
    # AMD Ryzen 5000 (AM4)
    {"category": "cpu", "brand": "AMD", "model": "Ryzen 9 5950X", "specs": {"socket": "AM4", "cores": 16, "threads": 32, "base_clock_ghz": 3.4, "boost_clock_ghz": 4.9, "tdp_w": 105, "architecture": "Zen 3"}},
    {"category": "cpu", "brand": "AMD", "model": "Ryzen 9 5900X", "specs": {"socket": "AM4", "cores": 12, "threads": 24, "base_clock_ghz": 3.7, "boost_clock_ghz": 4.8, "tdp_w": 105, "architecture": "Zen 3"}},
    {"category": "cpu", "brand": "AMD", "model": "Ryzen 7 5800X3D", "specs": {"socket": "AM4", "cores": 8, "threads": 16, "base_clock_ghz": 3.4, "boost_clock_ghz": 4.5, "tdp_w": 105, "architecture": "Zen 3 3D V-Cache"}},
    {"category": "cpu", "brand": "AMD", "model": "Ryzen 7 5800X", "specs": {"socket": "AM4", "cores": 8, "threads": 16, "base_clock_ghz": 3.8, "boost_clock_ghz": 4.7, "tdp_w": 105, "architecture": "Zen 3"}},
    {"category": "cpu", "brand": "AMD", "model": "Ryzen 5 5600X", "specs": {"socket": "AM4", "cores": 6, "threads": 12, "base_clock_ghz": 3.7, "boost_clock_ghz": 4.6, "tdp_w": 65, "architecture": "Zen 3"}},
    {"category": "cpu", "brand": "AMD", "model": "Ryzen 5 5600", "specs": {"socket": "AM4", "cores": 6, "threads": 12, "base_clock_ghz": 3.5, "boost_clock_ghz": 4.4, "tdp_w": 65, "architecture": "Zen 3"}},
    {"category": "cpu", "brand": "AMD", "model": "Ryzen 5 5500", "specs": {"socket": "AM4", "cores": 6, "threads": 12, "base_clock_ghz": 3.6, "boost_clock_ghz": 4.2, "tdp_w": 65, "architecture": "Zen 3"}},
    # AMD Ryzen 3000 (AM4)
    {"category": "cpu", "brand": "AMD", "model": "Ryzen 9 3900X", "specs": {"socket": "AM4", "cores": 12, "threads": 24, "base_clock_ghz": 3.8, "boost_clock_ghz": 4.6, "tdp_w": 105, "architecture": "Zen 2"}},
    {"category": "cpu", "brand": "AMD", "model": "Ryzen 7 3700X", "specs": {"socket": "AM4", "cores": 8, "threads": 16, "base_clock_ghz": 3.6, "boost_clock_ghz": 4.4, "tdp_w": 65, "architecture": "Zen 2"}},
    {"category": "cpu", "brand": "AMD", "model": "Ryzen 5 3600X", "specs": {"socket": "AM4", "cores": 6, "threads": 12, "base_clock_ghz": 3.8, "boost_clock_ghz": 4.4, "tdp_w": 95, "architecture": "Zen 2"}},
    {"category": "cpu", "brand": "AMD", "model": "Ryzen 5 3600", "specs": {"socket": "AM4", "cores": 6, "threads": 12, "base_clock_ghz": 3.6, "boost_clock_ghz": 4.2, "tdp_w": 65, "architecture": "Zen 2"}},

    # ────────────────── GPU ──────────────────
    # NVIDIA RTX 4000
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 4090", "specs": {"vram_gb": 24, "vram_type": "GDDR6X", "tdp_w": 450, "pcie": "PCIe 4.0 x16", "architecture": "Ada Lovelace", "cuda_cores": 16384}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 4080 Super", "specs": {"vram_gb": 16, "vram_type": "GDDR6X", "tdp_w": 320, "pcie": "PCIe 4.0 x16", "architecture": "Ada Lovelace", "cuda_cores": 10240}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 4080", "specs": {"vram_gb": 16, "vram_type": "GDDR6X", "tdp_w": 320, "pcie": "PCIe 4.0 x16", "architecture": "Ada Lovelace", "cuda_cores": 9728}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 4070 Ti Super", "specs": {"vram_gb": 16, "vram_type": "GDDR6X", "tdp_w": 285, "pcie": "PCIe 4.0 x16", "architecture": "Ada Lovelace", "cuda_cores": 8448}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 4070 Ti", "specs": {"vram_gb": 12, "vram_type": "GDDR6X", "tdp_w": 285, "pcie": "PCIe 4.0 x16", "architecture": "Ada Lovelace", "cuda_cores": 7680}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 4070 Super", "specs": {"vram_gb": 12, "vram_type": "GDDR6X", "tdp_w": 220, "pcie": "PCIe 4.0 x16", "architecture": "Ada Lovelace", "cuda_cores": 7168}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 4070", "specs": {"vram_gb": 12, "vram_type": "GDDR6X", "tdp_w": 200, "pcie": "PCIe 4.0 x16", "architecture": "Ada Lovelace", "cuda_cores": 5888}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 4060 Ti", "specs": {"vram_gb": 8, "vram_type": "GDDR6", "tdp_w": 165, "pcie": "PCIe 4.0 x16", "architecture": "Ada Lovelace", "cuda_cores": 4352}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 4060 Ti 16GB", "specs": {"vram_gb": 16, "vram_type": "GDDR6", "tdp_w": 165, "pcie": "PCIe 4.0 x16", "architecture": "Ada Lovelace", "cuda_cores": 4352}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 4060", "specs": {"vram_gb": 8, "vram_type": "GDDR6", "tdp_w": 115, "pcie": "PCIe 4.0 x16", "architecture": "Ada Lovelace", "cuda_cores": 3072}},
    # NVIDIA RTX 3000
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 3090 Ti", "specs": {"vram_gb": 24, "vram_type": "GDDR6X", "tdp_w": 450, "pcie": "PCIe 4.0 x16", "architecture": "Ampere", "cuda_cores": 10752}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 3090", "specs": {"vram_gb": 24, "vram_type": "GDDR6X", "tdp_w": 350, "pcie": "PCIe 4.0 x16", "architecture": "Ampere", "cuda_cores": 10496}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 3080 Ti", "specs": {"vram_gb": 12, "vram_type": "GDDR6X", "tdp_w": 350, "pcie": "PCIe 4.0 x16", "architecture": "Ampere", "cuda_cores": 10240}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 3080 12GB", "specs": {"vram_gb": 12, "vram_type": "GDDR6X", "tdp_w": 350, "pcie": "PCIe 4.0 x16", "architecture": "Ampere", "cuda_cores": 8960}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 3080", "specs": {"vram_gb": 10, "vram_type": "GDDR6X", "tdp_w": 320, "pcie": "PCIe 4.0 x16", "architecture": "Ampere", "cuda_cores": 8704}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 3070 Ti", "specs": {"vram_gb": 8, "vram_type": "GDDR6X", "tdp_w": 290, "pcie": "PCIe 4.0 x16", "architecture": "Ampere", "cuda_cores": 6144}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 3070", "specs": {"vram_gb": 8, "vram_type": "GDDR6", "tdp_w": 220, "pcie": "PCIe 4.0 x16", "architecture": "Ampere", "cuda_cores": 5888}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 3060 Ti", "specs": {"vram_gb": 8, "vram_type": "GDDR6", "tdp_w": 200, "pcie": "PCIe 4.0 x16", "architecture": "Ampere", "cuda_cores": 4864}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 3060 12GB", "specs": {"vram_gb": 12, "vram_type": "GDDR6", "tdp_w": 170, "pcie": "PCIe 4.0 x16", "architecture": "Ampere", "cuda_cores": 3584}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 3060", "specs": {"vram_gb": 8, "vram_type": "GDDR6", "tdp_w": 170, "pcie": "PCIe 4.0 x16", "architecture": "Ampere", "cuda_cores": 3584}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 3050", "specs": {"vram_gb": 8, "vram_type": "GDDR6", "tdp_w": 130, "pcie": "PCIe 4.0 x16", "architecture": "Ampere", "cuda_cores": 2560}},
    # NVIDIA RTX 2000 (Turing, 2018-2019)
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 2080 Ti", "specs": {"vram_gb": 11, "vram_type": "GDDR6", "tdp_w": 250, "pcie": "PCIe 3.0 x16", "architecture": "Turing", "cuda_cores": 4352}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 2080 Super", "specs": {"vram_gb": 8, "vram_type": "GDDR6", "tdp_w": 250, "pcie": "PCIe 3.0 x16", "architecture": "Turing", "cuda_cores": 3072}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 2080", "specs": {"vram_gb": 8, "vram_type": "GDDR6", "tdp_w": 215, "pcie": "PCIe 3.0 x16", "architecture": "Turing", "cuda_cores": 2944}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 2070 Super", "specs": {"vram_gb": 8, "vram_type": "GDDR6", "tdp_w": 215, "pcie": "PCIe 3.0 x16", "architecture": "Turing", "cuda_cores": 2560}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 2070", "specs": {"vram_gb": 8, "vram_type": "GDDR6", "tdp_w": 175, "pcie": "PCIe 3.0 x16", "architecture": "Turing", "cuda_cores": 2304}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 2060 Super", "specs": {"vram_gb": 8, "vram_type": "GDDR6", "tdp_w": 175, "pcie": "PCIe 3.0 x16", "architecture": "Turing", "cuda_cores": 2176}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce RTX 2060", "specs": {"vram_gb": 6, "vram_type": "GDDR6", "tdp_w": 160, "pcie": "PCIe 3.0 x16", "architecture": "Turing", "cuda_cores": 1920}},
    # NVIDIA GTX 1000 (Pascal, 2016-2017)
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce GTX 1080 Ti", "specs": {"vram_gb": 11, "vram_type": "GDDR5X", "tdp_w": 250, "pcie": "PCIe 3.0 x16", "architecture": "Pascal", "cuda_cores": 3584}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce GTX 1080", "specs": {"vram_gb": 8, "vram_type": "GDDR5X", "tdp_w": 180, "pcie": "PCIe 3.0 x16", "architecture": "Pascal", "cuda_cores": 2560}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce GTX 1070 Ti", "specs": {"vram_gb": 8, "vram_type": "GDDR5", "tdp_w": 180, "pcie": "PCIe 3.0 x16", "architecture": "Pascal", "cuda_cores": 2432}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce GTX 1070", "specs": {"vram_gb": 8, "vram_type": "GDDR5", "tdp_w": 150, "pcie": "PCIe 3.0 x16", "architecture": "Pascal", "cuda_cores": 1920}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce GTX 1060 6GB", "specs": {"vram_gb": 6, "vram_type": "GDDR5", "tdp_w": 120, "pcie": "PCIe 3.0 x16", "architecture": "Pascal", "cuda_cores": 1280}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce GTX 1060 3GB", "specs": {"vram_gb": 3, "vram_type": "GDDR5", "tdp_w": 120, "pcie": "PCIe 3.0 x16", "architecture": "Pascal", "cuda_cores": 1152}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce GTX 1050 Ti", "specs": {"vram_gb": 4, "vram_type": "GDDR5", "tdp_w": 75, "pcie": "PCIe 3.0 x16", "architecture": "Pascal", "cuda_cores": 768}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce GTX 1050", "specs": {"vram_gb": 2, "vram_type": "GDDR5", "tdp_w": 75, "pcie": "PCIe 3.0 x16", "architecture": "Pascal", "cuda_cores": 640}},
    # NVIDIA GTX 900 (Maxwell, 2014-2015)
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce GTX 980 Ti", "specs": {"vram_gb": 6, "vram_type": "GDDR5", "tdp_w": 250, "pcie": "PCIe 3.0 x16", "architecture": "Maxwell", "cuda_cores": 2816}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce GTX 980", "specs": {"vram_gb": 4, "vram_type": "GDDR5", "tdp_w": 165, "pcie": "PCIe 3.0 x16", "architecture": "Maxwell", "cuda_cores": 2048}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce GTX 970", "specs": {"vram_gb": 4, "vram_type": "GDDR5", "tdp_w": 145, "pcie": "PCIe 3.0 x16", "architecture": "Maxwell", "cuda_cores": 1664}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce GTX 960", "specs": {"vram_gb": 2, "vram_type": "GDDR5", "tdp_w": 120, "pcie": "PCIe 3.0 x16", "architecture": "Maxwell", "cuda_cores": 1024}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce GTX 950", "specs": {"vram_gb": 2, "vram_type": "GDDR5", "tdp_w": 90, "pcie": "PCIe 3.0 x16", "architecture": "Maxwell", "cuda_cores": 768}},
    # NVIDIA GTX 700 (Kepler, 2013-2014)
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce GTX 780 Ti", "specs": {"vram_gb": 3, "vram_type": "GDDR5", "tdp_w": 250, "pcie": "PCIe 3.0 x16", "architecture": "Kepler", "cuda_cores": 2880}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce GTX 780", "specs": {"vram_gb": 3, "vram_type": "GDDR5", "tdp_w": 250, "pcie": "PCIe 3.0 x16", "architecture": "Kepler", "cuda_cores": 2304}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce GTX 770", "specs": {"vram_gb": 2, "vram_type": "GDDR5", "tdp_w": 230, "pcie": "PCIe 3.0 x16", "architecture": "Kepler", "cuda_cores": 1536}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce GTX 760", "specs": {"vram_gb": 2, "vram_type": "GDDR5", "tdp_w": 170, "pcie": "PCIe 3.0 x16", "architecture": "Kepler", "cuda_cores": 1152}},
    {"category": "gpu", "brand": "NVIDIA", "model": "GeForce GTX 750 Ti", "specs": {"vram_gb": 2, "vram_type": "GDDR5", "tdp_w": 60, "pcie": "PCIe 3.0 x16", "architecture": "Maxwell", "cuda_cores": 640}},
    # AMD RX 7000
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 7900 XTX", "specs": {"vram_gb": 24, "vram_type": "GDDR6", "tdp_w": 355, "pcie": "PCIe 4.0 x16", "architecture": "RDNA 3", "stream_processors": 12288}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 7900 XT", "specs": {"vram_gb": 20, "vram_type": "GDDR6", "tdp_w": 315, "pcie": "PCIe 4.0 x16", "architecture": "RDNA 3", "stream_processors": 10752}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 7900 GRE", "specs": {"vram_gb": 16, "vram_type": "GDDR6", "tdp_w": 260, "pcie": "PCIe 4.0 x16", "architecture": "RDNA 3", "stream_processors": 9984}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 7800 XT", "specs": {"vram_gb": 16, "vram_type": "GDDR6", "tdp_w": 263, "pcie": "PCIe 4.0 x16", "architecture": "RDNA 3", "stream_processors": 3840}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 7700 XT", "specs": {"vram_gb": 12, "vram_type": "GDDR6", "tdp_w": 245, "pcie": "PCIe 4.0 x16", "architecture": "RDNA 3", "stream_processors": 3456}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 7600 XT", "specs": {"vram_gb": 16, "vram_type": "GDDR6", "tdp_w": 190, "pcie": "PCIe 4.0 x16", "architecture": "RDNA 3", "stream_processors": 2048}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 7600", "specs": {"vram_gb": 8, "vram_type": "GDDR6", "tdp_w": 165, "pcie": "PCIe 4.0 x16", "architecture": "RDNA 3", "stream_processors": 2048}},
    # AMD RX 6000
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 6950 XT", "specs": {"vram_gb": 16, "vram_type": "GDDR6", "tdp_w": 335, "pcie": "PCIe 4.0 x16", "architecture": "RDNA 2", "stream_processors": 5120}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 6900 XT", "specs": {"vram_gb": 16, "vram_type": "GDDR6", "tdp_w": 300, "pcie": "PCIe 4.0 x16", "architecture": "RDNA 2", "stream_processors": 5120}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 6800 XT", "specs": {"vram_gb": 16, "vram_type": "GDDR6", "tdp_w": 300, "pcie": "PCIe 4.0 x16", "architecture": "RDNA 2", "stream_processors": 4608}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 6800", "specs": {"vram_gb": 16, "vram_type": "GDDR6", "tdp_w": 250, "pcie": "PCIe 4.0 x16", "architecture": "RDNA 2", "stream_processors": 3840}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 6750 XT", "specs": {"vram_gb": 12, "vram_type": "GDDR6", "tdp_w": 250, "pcie": "PCIe 4.0 x16", "architecture": "RDNA 2", "stream_processors": 2560}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 6700 XT", "specs": {"vram_gb": 12, "vram_type": "GDDR6", "tdp_w": 230, "pcie": "PCIe 4.0 x16", "architecture": "RDNA 2", "stream_processors": 2560}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 6650 XT", "specs": {"vram_gb": 8, "vram_type": "GDDR6", "tdp_w": 180, "pcie": "PCIe 4.0 x16", "architecture": "RDNA 2", "stream_processors": 2048}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 6600 XT", "specs": {"vram_gb": 8, "vram_type": "GDDR6", "tdp_w": 160, "pcie": "PCIe 4.0 x16", "architecture": "RDNA 2", "stream_processors": 2048}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 6600", "specs": {"vram_gb": 8, "vram_type": "GDDR6", "tdp_w": 132, "pcie": "PCIe 4.0 x16", "architecture": "RDNA 2", "stream_processors": 1792}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 6500 XT", "specs": {"vram_gb": 4, "vram_type": "GDDR6", "tdp_w": 107, "pcie": "PCIe 4.0 x4", "architecture": "RDNA 2", "stream_processors": 1024}},
    # AMD RX 5000 (RDNA 1, 2019-2020)
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 5700 XT", "specs": {"vram_gb": 8, "vram_type": "GDDR6", "tdp_w": 225, "pcie": "PCIe 4.0 x16", "architecture": "RDNA 1", "stream_processors": 2560}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 5700", "specs": {"vram_gb": 8, "vram_type": "GDDR6", "tdp_w": 180, "pcie": "PCIe 4.0 x16", "architecture": "RDNA 1", "stream_processors": 2304}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 5600 XT", "specs": {"vram_gb": 6, "vram_type": "GDDR6", "tdp_w": 150, "pcie": "PCIe 4.0 x16", "architecture": "RDNA 1", "stream_processors": 2048}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 5500 XT 8GB", "specs": {"vram_gb": 8, "vram_type": "GDDR6", "tdp_w": 130, "pcie": "PCIe 4.0 x16", "architecture": "RDNA 1", "stream_processors": 1408}},
    # AMD RX 500 (Polaris, 2017-2018)
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 590", "specs": {"vram_gb": 8, "vram_type": "GDDR5", "tdp_w": 225, "pcie": "PCIe 3.0 x16", "architecture": "Polaris", "stream_processors": 2304}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 580 8GB", "specs": {"vram_gb": 8, "vram_type": "GDDR5", "tdp_w": 185, "pcie": "PCIe 3.0 x16", "architecture": "Polaris", "stream_processors": 2304}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 580 4GB", "specs": {"vram_gb": 4, "vram_type": "GDDR5", "tdp_w": 185, "pcie": "PCIe 3.0 x16", "architecture": "Polaris", "stream_processors": 2304}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 570 8GB", "specs": {"vram_gb": 8, "vram_type": "GDDR5", "tdp_w": 150, "pcie": "PCIe 3.0 x16", "architecture": "Polaris", "stream_processors": 2048}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 570 4GB", "specs": {"vram_gb": 4, "vram_type": "GDDR5", "tdp_w": 150, "pcie": "PCIe 3.0 x16", "architecture": "Polaris", "stream_processors": 2048}},
    # AMD RX 400 (Polaris, 2016)
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 480 8GB", "specs": {"vram_gb": 8, "vram_type": "GDDR5", "tdp_w": 150, "pcie": "PCIe 3.0 x16", "architecture": "Polaris", "stream_processors": 2304}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 480 4GB", "specs": {"vram_gb": 4, "vram_type": "GDDR5", "tdp_w": 150, "pcie": "PCIe 3.0 x16", "architecture": "Polaris", "stream_processors": 2304}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 470 8GB", "specs": {"vram_gb": 8, "vram_type": "GDDR5", "tdp_w": 120, "pcie": "PCIe 3.0 x16", "architecture": "Polaris", "stream_processors": 2048}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX 470 4GB", "specs": {"vram_gb": 4, "vram_type": "GDDR5", "tdp_w": 120, "pcie": "PCIe 3.0 x16", "architecture": "Polaris", "stream_processors": 2048}},
    # AMD RX Vega (2017-2018)
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX Vega 64", "specs": {"vram_gb": 8, "vram_type": "HBM2", "tdp_w": 295, "pcie": "PCIe 3.0 x16", "architecture": "Vega", "stream_processors": 4096}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon RX Vega 56", "specs": {"vram_gb": 8, "vram_type": "HBM2", "tdp_w": 210, "pcie": "PCIe 3.0 x16", "architecture": "Vega", "stream_processors": 3584}},
    # AMD R9 300 (2015)
    {"category": "gpu", "brand": "AMD", "model": "Radeon R9 Fury X", "specs": {"vram_gb": 4, "vram_type": "HBM", "tdp_w": 275, "pcie": "PCIe 3.0 x16", "architecture": "Fiji", "stream_processors": 4096}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon R9 390X", "specs": {"vram_gb": 8, "vram_type": "GDDR5", "tdp_w": 275, "pcie": "PCIe 3.0 x16", "architecture": "Hawaii", "stream_processors": 2816}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon R9 390", "specs": {"vram_gb": 8, "vram_type": "GDDR5", "tdp_w": 275, "pcie": "PCIe 3.0 x16", "architecture": "Hawaii", "stream_processors": 2560}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon R9 380X", "specs": {"vram_gb": 4, "vram_type": "GDDR5", "tdp_w": 190, "pcie": "PCIe 3.0 x16", "architecture": "Tonga", "stream_processors": 2048}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon R9 380", "specs": {"vram_gb": 4, "vram_type": "GDDR5", "tdp_w": 190, "pcie": "PCIe 3.0 x16", "architecture": "Tonga", "stream_processors": 1792}},
    # AMD R9 200 (2013-2014)
    {"category": "gpu", "brand": "AMD", "model": "Radeon R9 290X", "specs": {"vram_gb": 4, "vram_type": "GDDR5", "tdp_w": 290, "pcie": "PCIe 3.0 x16", "architecture": "Hawaii", "stream_processors": 2816}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon R9 290", "specs": {"vram_gb": 4, "vram_type": "GDDR5", "tdp_w": 250, "pcie": "PCIe 3.0 x16", "architecture": "Hawaii", "stream_processors": 2560}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon R9 280X", "specs": {"vram_gb": 3, "vram_type": "GDDR5", "tdp_w": 250, "pcie": "PCIe 3.0 x16", "architecture": "Tahiti", "stream_processors": 2048}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon R9 280", "specs": {"vram_gb": 3, "vram_type": "GDDR5", "tdp_w": 200, "pcie": "PCIe 3.0 x16", "architecture": "Tahiti", "stream_processors": 1792}},
    {"category": "gpu", "brand": "AMD", "model": "Radeon R9 270X", "specs": {"vram_gb": 2, "vram_type": "GDDR5", "tdp_w": 180, "pcie": "PCIe 3.0 x16", "architecture": "Pitcairn", "stream_processors": 1280}},

    # ────────────────── 메인보드 ──────────────────
    # Intel Z790
    {"category": "motherboard", "brand": "ASUS", "model": "ROG Maximus Z790 Hero", "specs": {"socket": "LGA1700", "chipset": "Z790", "ddr_type": "DDR5", "form_factor": "ATX", "pcie_slots": 3, "m2_slots": 5}},
    {"category": "motherboard", "brand": "ASUS", "model": "ROG Strix Z790-E Gaming WiFi", "specs": {"socket": "LGA1700", "chipset": "Z790", "ddr_type": "DDR5", "form_factor": "ATX", "pcie_slots": 2, "m2_slots": 5}},
    {"category": "motherboard", "brand": "ASUS", "model": "ROG Strix Z790-F Gaming WiFi", "specs": {"socket": "LGA1700", "chipset": "Z790", "ddr_type": "DDR5", "form_factor": "ATX", "pcie_slots": 2, "m2_slots": 5}},
    {"category": "motherboard", "brand": "ASUS", "model": "ProArt Z790-Creator WiFi", "specs": {"socket": "LGA1700", "chipset": "Z790", "ddr_type": "DDR5", "form_factor": "ATX", "pcie_slots": 2, "m2_slots": 4}},
    {"category": "motherboard", "brand": "MSI", "model": "MEG Z790 ACE", "specs": {"socket": "LGA1700", "chipset": "Z790", "ddr_type": "DDR5", "form_factor": "ATX", "pcie_slots": 3, "m2_slots": 5}},
    {"category": "motherboard", "brand": "MSI", "model": "MAG Z790 Tomahawk WiFi", "specs": {"socket": "LGA1700", "chipset": "Z790", "ddr_type": "DDR5", "form_factor": "ATX", "pcie_slots": 2, "m2_slots": 4}},
    {"category": "motherboard", "brand": "Gigabyte", "model": "Z790 AORUS Master", "specs": {"socket": "LGA1700", "chipset": "Z790", "ddr_type": "DDR5", "form_factor": "ATX", "pcie_slots": 2, "m2_slots": 4}},
    {"category": "motherboard", "brand": "Gigabyte", "model": "Z790 AORUS Elite AX", "specs": {"socket": "LGA1700", "chipset": "Z790", "ddr_type": "DDR5", "form_factor": "ATX", "pcie_slots": 2, "m2_slots": 4}},
    # Intel B760
    {"category": "motherboard", "brand": "ASUS", "model": "ROG Strix B760-G Gaming WiFi D4", "specs": {"socket": "LGA1700", "chipset": "B760", "ddr_type": "DDR4", "form_factor": "mATX", "m2_slots": 2}},
    {"category": "motherboard", "brand": "ASUS", "model": "PRIME B760M-A D4", "specs": {"socket": "LGA1700", "chipset": "B760", "ddr_type": "DDR4", "form_factor": "mATX", "m2_slots": 2}},
    {"category": "motherboard", "brand": "MSI", "model": "PRO B760M-A WiFi DDR4", "specs": {"socket": "LGA1700", "chipset": "B760", "ddr_type": "DDR4", "form_factor": "mATX", "m2_slots": 2}},
    {"category": "motherboard", "brand": "Gigabyte", "model": "B760M DS3H DDR4", "specs": {"socket": "LGA1700", "chipset": "B760", "ddr_type": "DDR4", "form_factor": "mATX", "m2_slots": 2}},
    # AMD X670/B650
    {"category": "motherboard", "brand": "ASUS", "model": "ROG Crosshair X670E Hero", "specs": {"socket": "AM5", "chipset": "X670E", "ddr_type": "DDR5", "form_factor": "ATX", "pcie_slots": 3, "m2_slots": 5}},
    {"category": "motherboard", "brand": "ASUS", "model": "ROG Strix X670E-E Gaming WiFi", "specs": {"socket": "AM5", "chipset": "X670E", "ddr_type": "DDR5", "form_factor": "ATX", "pcie_slots": 2, "m2_slots": 4}},
    {"category": "motherboard", "brand": "MSI", "model": "MEG X670E ACE", "specs": {"socket": "AM5", "chipset": "X670E", "ddr_type": "DDR5", "form_factor": "ATX", "pcie_slots": 3, "m2_slots": 5}},
    {"category": "motherboard", "brand": "MSI", "model": "MAG X670E Tomahawk WiFi", "specs": {"socket": "AM5", "chipset": "X670E", "ddr_type": "DDR5", "form_factor": "ATX", "pcie_slots": 2, "m2_slots": 4}},
    {"category": "motherboard", "brand": "Gigabyte", "model": "X670E AORUS Master", "specs": {"socket": "AM5", "chipset": "X670E", "ddr_type": "DDR5", "form_factor": "ATX", "m2_slots": 4}},
    {"category": "motherboard", "brand": "ASUS", "model": "ROG Strix B650E-F Gaming WiFi", "specs": {"socket": "AM5", "chipset": "B650E", "ddr_type": "DDR5", "form_factor": "ATX", "m2_slots": 4}},
    {"category": "motherboard", "brand": "MSI", "model": "MAG B650 Tomahawk WiFi", "specs": {"socket": "AM5", "chipset": "B650", "ddr_type": "DDR5", "form_factor": "ATX", "m2_slots": 3}},
    {"category": "motherboard", "brand": "Gigabyte", "model": "B650 AORUS Elite AX", "specs": {"socket": "AM5", "chipset": "B650", "ddr_type": "DDR5", "form_factor": "ATX", "m2_slots": 3}},
    # AMD X570/B550 (AM4)
    {"category": "motherboard", "brand": "ASUS", "model": "ROG Crosshair VIII Hero X570", "specs": {"socket": "AM4", "chipset": "X570", "ddr_type": "DDR4", "form_factor": "ATX", "m2_slots": 3}},
    {"category": "motherboard", "brand": "ASUS", "model": "ROG Strix X570-E Gaming WiFi", "specs": {"socket": "AM4", "chipset": "X570", "ddr_type": "DDR4", "form_factor": "ATX", "m2_slots": 3}},
    {"category": "motherboard", "brand": "MSI", "model": "MEG X570 ACE", "specs": {"socket": "AM4", "chipset": "X570", "ddr_type": "DDR4", "form_factor": "ATX", "m2_slots": 3}},
    {"category": "motherboard", "brand": "MSI", "model": "MAG B550 Tomahawk", "specs": {"socket": "AM4", "chipset": "B550", "ddr_type": "DDR4", "form_factor": "ATX", "m2_slots": 2}},
    {"category": "motherboard", "brand": "Gigabyte", "model": "B550 AORUS Pro AX", "specs": {"socket": "AM4", "chipset": "B550", "ddr_type": "DDR4", "form_factor": "ATX", "m2_slots": 2}},
    {"category": "motherboard", "brand": "ASUS", "model": "PRIME B550M-A", "specs": {"socket": "AM4", "chipset": "B550", "ddr_type": "DDR4", "form_factor": "mATX", "m2_slots": 2}},
    {"category": "motherboard", "brand": "MSI", "model": "MAG B450 Tomahawk MAX", "specs": {"socket": "AM4", "chipset": "B450", "ddr_type": "DDR4", "form_factor": "ATX", "m2_slots": 2}},
    {"category": "motherboard", "brand": "Gigabyte", "model": "B450M DS3H V2", "specs": {"socket": "AM4", "chipset": "B450", "ddr_type": "DDR4", "form_factor": "mATX", "m2_slots": 1}},

    # ────────────────── RAM ──────────────────
    {"category": "ram", "brand": "Samsung", "model": "DDR5-5600 16GB (8GB×2)", "specs": {"capacity_gb": 16, "speed_mhz": 5600, "ddr_type": "DDR5", "modules": 2, "latency": "CL36", "voltage_v": 1.1}},
    {"category": "ram", "brand": "Samsung", "model": "DDR5-5600 32GB (16GB×2)", "specs": {"capacity_gb": 32, "speed_mhz": 5600, "ddr_type": "DDR5", "modules": 2, "latency": "CL36", "voltage_v": 1.1}},
    {"category": "ram", "brand": "G.Skill", "model": "Trident Z5 DDR5-6000 32GB (16GB×2)", "specs": {"capacity_gb": 32, "speed_mhz": 6000, "ddr_type": "DDR5", "modules": 2, "latency": "CL30", "voltage_v": 1.35}},
    {"category": "ram", "brand": "G.Skill", "model": "Trident Z5 DDR5-6400 32GB (16GB×2)", "specs": {"capacity_gb": 32, "speed_mhz": 6400, "ddr_type": "DDR5", "modules": 2, "latency": "CL32", "voltage_v": 1.4}},
    {"category": "ram", "brand": "Corsair", "model": "Dominator Platinum DDR5-5600 32GB", "specs": {"capacity_gb": 32, "speed_mhz": 5600, "ddr_type": "DDR5", "modules": 2, "latency": "CL36", "voltage_v": 1.25}},
    {"category": "ram", "brand": "Kingston", "model": "Fury Beast DDR5-5200 16GB (8GB×2)", "specs": {"capacity_gb": 16, "speed_mhz": 5200, "ddr_type": "DDR5", "modules": 2, "latency": "CL40", "voltage_v": 1.1}},
    {"category": "ram", "brand": "G.Skill", "model": "Trident Z Neo DDR4-3600 32GB (16GB×2)", "specs": {"capacity_gb": 32, "speed_mhz": 3600, "ddr_type": "DDR4", "modules": 2, "latency": "CL16", "voltage_v": 1.35}},
    {"category": "ram", "brand": "G.Skill", "model": "Trident Z Neo DDR4-3600 16GB (8GB×2)", "specs": {"capacity_gb": 16, "speed_mhz": 3600, "ddr_type": "DDR4", "modules": 2, "latency": "CL16", "voltage_v": 1.35}},
    {"category": "ram", "brand": "Corsair", "model": "Vengeance DDR4-3200 16GB (8GB×2)", "specs": {"capacity_gb": 16, "speed_mhz": 3200, "ddr_type": "DDR4", "modules": 2, "latency": "CL16", "voltage_v": 1.35}},
    {"category": "ram", "brand": "Corsair", "model": "Vengeance DDR4-3200 32GB (16GB×2)", "specs": {"capacity_gb": 32, "speed_mhz": 3200, "ddr_type": "DDR4", "modules": 2, "latency": "CL16", "voltage_v": 1.35}},
    {"category": "ram", "brand": "Samsung", "model": "DDR4-3200 16GB (8GB×2)", "specs": {"capacity_gb": 16, "speed_mhz": 3200, "ddr_type": "DDR4", "modules": 2, "latency": "CL22", "voltage_v": 1.2}},
    {"category": "ram", "brand": "Crucial", "model": "Ballistix DDR4-3600 16GB (8GB×2)", "specs": {"capacity_gb": 16, "speed_mhz": 3600, "ddr_type": "DDR4", "modules": 2, "latency": "CL16", "voltage_v": 1.35}},
    {"category": "ram", "brand": "Kingston", "model": "Fury Beast DDR4-3200 16GB (8GB×2)", "specs": {"capacity_gb": 16, "speed_mhz": 3200, "ddr_type": "DDR4", "modules": 2, "latency": "CL16", "voltage_v": 1.35}},

    # ────────────────── SSD ──────────────────
    {"category": "ssd", "brand": "Samsung", "model": "980 Pro 1TB", "specs": {"capacity_gb": 1000, "interface": "NVMe PCIe 4.0 x4", "read_mbps": 7000, "write_mbps": 5000, "form_factor": "M.2 2280"}},
    {"category": "ssd", "brand": "Samsung", "model": "980 Pro 2TB", "specs": {"capacity_gb": 2000, "interface": "NVMe PCIe 4.0 x4", "read_mbps": 7000, "write_mbps": 5100, "form_factor": "M.2 2280"}},
    {"category": "ssd", "brand": "Samsung", "model": "990 Pro 1TB", "specs": {"capacity_gb": 1000, "interface": "NVMe PCIe 4.0 x4", "read_mbps": 7450, "write_mbps": 6900, "form_factor": "M.2 2280"}},
    {"category": "ssd", "brand": "Samsung", "model": "990 Pro 2TB", "specs": {"capacity_gb": 2000, "interface": "NVMe PCIe 4.0 x4", "read_mbps": 7450, "write_mbps": 6900, "form_factor": "M.2 2280"}},
    {"category": "ssd", "brand": "Samsung", "model": "870 EVO 500GB", "specs": {"capacity_gb": 500, "interface": "SATA", "read_mbps": 560, "write_mbps": 530, "form_factor": "2.5inch"}},
    {"category": "ssd", "brand": "Samsung", "model": "870 EVO 1TB", "specs": {"capacity_gb": 1000, "interface": "SATA", "read_mbps": 560, "write_mbps": 530, "form_factor": "2.5inch"}},
    {"category": "ssd", "brand": "Samsung", "model": "870 EVO 2TB", "specs": {"capacity_gb": 2000, "interface": "SATA", "read_mbps": 560, "write_mbps": 530, "form_factor": "2.5inch"}},
    {"category": "ssd", "brand": "WD", "model": "Black SN850X 1TB", "specs": {"capacity_gb": 1000, "interface": "NVMe PCIe 4.0 x4", "read_mbps": 7300, "write_mbps": 6300, "form_factor": "M.2 2280"}},
    {"category": "ssd", "brand": "WD", "model": "Black SN850X 2TB", "specs": {"capacity_gb": 2000, "interface": "NVMe PCIe 4.0 x4", "read_mbps": 7300, "write_mbps": 6600, "form_factor": "M.2 2280"}},
    {"category": "ssd", "brand": "SK Hynix", "model": "Platinum P41 1TB", "specs": {"capacity_gb": 1000, "interface": "NVMe PCIe 4.0 x4", "read_mbps": 7000, "write_mbps": 6500, "form_factor": "M.2 2280"}},
    {"category": "ssd", "brand": "Crucial", "model": "P3 Plus 1TB", "specs": {"capacity_gb": 1000, "interface": "NVMe PCIe 4.0 x4", "read_mbps": 5000, "write_mbps": 3600, "form_factor": "M.2 2280"}},
    {"category": "ssd", "brand": "Seagate", "model": "FireCuda 530 1TB", "specs": {"capacity_gb": 1000, "interface": "NVMe PCIe 4.0 x4", "read_mbps": 7300, "write_mbps": 6000, "form_factor": "M.2 2280"}},

    # ────────────────── HDD ──────────────────
    {"category": "hdd", "brand": "Seagate", "model": "Barracuda 2TB", "specs": {"capacity_gb": 2000, "rpm": 7200, "interface": "SATA 6Gb/s", "cache_mb": 256}},
    {"category": "hdd", "brand": "Seagate", "model": "Barracuda 4TB", "specs": {"capacity_gb": 4000, "rpm": 5400, "interface": "SATA 6Gb/s", "cache_mb": 256}},
    {"category": "hdd", "brand": "WD", "model": "Blue 2TB", "specs": {"capacity_gb": 2000, "rpm": 7200, "interface": "SATA 6Gb/s", "cache_mb": 256}},
    {"category": "hdd", "brand": "WD", "model": "Blue 4TB", "specs": {"capacity_gb": 4000, "rpm": 5400, "interface": "SATA 6Gb/s", "cache_mb": 256}},
    {"category": "hdd", "brand": "WD", "model": "Red Plus 4TB", "specs": {"capacity_gb": 4000, "rpm": 5400, "interface": "SATA 6Gb/s", "cache_mb": 256}},
    {"category": "hdd", "brand": "Toshiba", "model": "P300 2TB", "specs": {"capacity_gb": 2000, "rpm": 7200, "interface": "SATA 6Gb/s", "cache_mb": 64}},

    # ────────────────── PSU ──────────────────
    {"category": "psu", "brand": "Corsair", "model": "RM1000x 1000W", "specs": {"wattage": 1000, "rating": "Gold", "modular": "Full", "atx_version": "ATX 3.0"}},
    {"category": "psu", "brand": "Corsair", "model": "RM850x 850W", "specs": {"wattage": 850, "rating": "Gold", "modular": "Full", "atx_version": "ATX 3.0"}},
    {"category": "psu", "brand": "Corsair", "model": "RM750x 750W", "specs": {"wattage": 750, "rating": "Gold", "modular": "Full", "atx_version": "ATX 3.0"}},
    {"category": "psu", "brand": "Corsair", "model": "RM650x 650W", "specs": {"wattage": 650, "rating": "Gold", "modular": "Full", "atx_version": "ATX 3.0"}},
    {"category": "psu", "brand": "Seasonic", "model": "Focus GX-1000 1000W", "specs": {"wattage": 1000, "rating": "Gold", "modular": "Full", "atx_version": "ATX 3.0"}},
    {"category": "psu", "brand": "Seasonic", "model": "Focus GX-850 850W", "specs": {"wattage": 850, "rating": "Gold", "modular": "Full", "atx_version": "ATX 3.0"}},
    {"category": "psu", "brand": "Seasonic", "model": "Focus GX-750 750W", "specs": {"wattage": 750, "rating": "Gold", "modular": "Full", "atx_version": "ATX 3.0"}},
    {"category": "psu", "brand": "be quiet!", "model": "Dark Power 13 1000W", "specs": {"wattage": 1000, "rating": "Titanium", "modular": "Full", "atx_version": "ATX 3.0"}},
    {"category": "psu", "brand": "be quiet!", "model": "Straight Power 12 850W", "specs": {"wattage": 850, "rating": "Platinum", "modular": "Full", "atx_version": "ATX 3.0"}},
    {"category": "psu", "brand": "EVGA", "model": "SuperNOVA 850 G6 850W", "specs": {"wattage": 850, "rating": "Gold", "modular": "Full", "atx_version": "ATX 3.0"}},
    {"category": "psu", "brand": "MSI", "model": "MAG A850GL 850W", "specs": {"wattage": 850, "rating": "Gold", "modular": "Full", "atx_version": "ATX 3.0"}},
    {"category": "psu", "brand": "Thermalright", "model": "TRX-750W 750W", "specs": {"wattage": 750, "rating": "Gold", "modular": "Full", "atx_version": "ATX 2.0"}},
    {"category": "psu", "brand": "Thermalright", "model": "TRX-850W 850W", "specs": {"wattage": 850, "rating": "Gold", "modular": "Full", "atx_version": "ATX 3.0"}},

    # ────────────────── 케이스 ──────────────────
    {"category": "case", "brand": "Fractal Design", "model": "Torrent", "specs": {"form_factor": "ATX", "size": "Mid Tower", "max_gpu_mm": 461, "max_cooler_mm": 188, "fan_slots": 9}},
    {"category": "case", "brand": "Fractal Design", "model": "Define 7", "specs": {"form_factor": "ATX/E-ATX", "size": "Mid Tower", "max_gpu_mm": 491, "max_cooler_mm": 185, "fan_slots": 9}},
    {"category": "case", "brand": "Lian Li", "model": "PC-O11 Dynamic EVO", "specs": {"form_factor": "ATX/E-ATX", "size": "Mid Tower", "max_gpu_mm": 446, "max_cooler_mm": 167, "fan_slots": 10}},
    {"category": "case", "brand": "Lian Li", "model": "Lancool 216", "specs": {"form_factor": "ATX", "size": "Mid Tower", "max_gpu_mm": 400, "max_cooler_mm": 176, "fan_slots": 6}},
    {"category": "case", "brand": "NZXT", "model": "H9 Flow", "specs": {"form_factor": "ATX/E-ATX", "size": "Mid Tower", "max_gpu_mm": 435, "max_cooler_mm": 185, "fan_slots": 8}},
    {"category": "case", "brand": "NZXT", "model": "H7 Flow", "specs": {"form_factor": "ATX", "size": "Mid Tower", "max_gpu_mm": 400, "max_cooler_mm": 185, "fan_slots": 7}},
    {"category": "case", "brand": "be quiet!", "model": "Silent Base 802", "specs": {"form_factor": "ATX/E-ATX", "size": "Mid Tower", "max_gpu_mm": 435, "max_cooler_mm": 185, "fan_slots": 9}},
    {"category": "case", "brand": "Cooler Master", "model": "HAF 700 Evo", "specs": {"form_factor": "E-ATX", "size": "Full Tower", "max_gpu_mm": 490, "max_cooler_mm": 200, "fan_slots": 10}},

    # ────────────────── 쿨러 ──────────────────
    {"category": "cooler", "brand": "Noctua", "model": "NH-D15", "specs": {"type": "공랭", "height_mm": 165, "fan_size_mm": 150, "tdp_w": 250, "socket_support": "LGA1700/AM5/AM4"}},
    {"category": "cooler", "brand": "Noctua", "model": "NH-U12S Redux", "specs": {"type": "공랭", "height_mm": 158, "fan_size_mm": 120, "tdp_w": 150, "socket_support": "LGA1700/AM5/AM4"}},
    {"category": "cooler", "brand": "be quiet!", "model": "Dark Rock Pro 4", "specs": {"type": "공랭", "height_mm": 163, "fan_size_mm": 135, "tdp_w": 250, "socket_support": "LGA1700/AM5/AM4"}},
    {"category": "cooler", "brand": "Thermalright", "model": "Peerless Assassin 120 SE", "specs": {"type": "공랭", "height_mm": 157, "fan_size_mm": 120, "tdp_w": 260, "socket_support": "LGA1700/AM5/AM4"}},
    {"category": "cooler", "brand": "DeepCool", "model": "AK620", "specs": {"type": "공랭", "height_mm": 160, "fan_size_mm": 120, "tdp_w": 260, "socket_support": "LGA1700/AM5/AM4"}},
    {"category": "cooler", "brand": "Corsair", "model": "H150i Elite Capellix 360mm", "specs": {"type": "수냉 AIO", "radiator_mm": 360, "tdp_w": 350, "socket_support": "LGA1700/AM5/AM4"}},
    {"category": "cooler", "brand": "Corsair", "model": "H100i Elite Capellix 240mm", "specs": {"type": "수냉 AIO", "radiator_mm": 240, "tdp_w": 250, "socket_support": "LGA1700/AM5/AM4"}},
    {"category": "cooler", "brand": "NZXT", "model": "Kraken Elite 360", "specs": {"type": "수냉 AIO", "radiator_mm": 360, "tdp_w": 350, "socket_support": "LGA1700/AM5/AM4"}},
    {"category": "cooler", "brand": "NZXT", "model": "Kraken 240", "specs": {"type": "수냉 AIO", "radiator_mm": 240, "tdp_w": 250, "socket_support": "LGA1700/AM5/AM4"}},
    {"category": "cooler", "brand": "be quiet!", "model": "Pure Loop 2 360mm", "specs": {"type": "수냉 AIO", "radiator_mm": 360, "tdp_w": 300, "socket_support": "LGA1700/AM5/AM4"}},
    {"category": "cooler", "brand": "Lian Li", "model": "Galahad II Trinity 360", "specs": {"type": "수냉 AIO", "radiator_mm": 360, "tdp_w": 350, "socket_support": "LGA1700/AM5/AM4"}},
    {"category": "cooler", "brand": "DeepCool", "model": "LT720 360mm", "specs": {"type": "수냉 AIO", "radiator_mm": 360, "tdp_w": 350, "socket_support": "LGA1700/AM5/AM4"}},
]


def search_parts(query: str = "", category: str = "") -> list[dict]:
    query = query.lower().strip()
    results = PARTS_DATABASE

    if category:
        results = [p for p in results if p["category"] == category]

    if query:
        tokens = query.split()
        def matches(p):
            text = f"{p['brand']} {p['model']}".lower()
            return all(t in text for t in tokens)
        results = [p for p in results if matches(p)]

    return results[:30]


def get_categories() -> list[str]:
    return list({p["category"] for p in PARTS_DATABASE})
