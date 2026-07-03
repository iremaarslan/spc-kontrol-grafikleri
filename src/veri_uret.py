"""
Sentetik olcum verisi ureticisi (SPC icin).
-------------------------------------------
Bir imalat surecinde uretilen parcalara ait kritik bir olcuyu (ornek: parca capi,
mm) simule eder. Veri "alt gruplar" (subgroup) halinde toplanir: her alt grup,
belirli bir zamanda olculen n adet parcadan olusur.

Surece bilerek iki tur bozulma enjekte edilir:
    1) Ortalama kaymasi (process shift) - belirli bir noktadan sonra ortalama artar
    2) Degiskenlik artisi - surecin sonlarina dogru dagilim genisler

Bu sayede SPC kontrol grafiklerinin bu bozulmalari yakalayip yakalamadigi test edilir.

Calistirma:
    python src/veri_uret.py
"""

import numpy as np
import pandas as pd

rng = np.random.default_rng(2024)

HEDEF = 25.00      # nominal olcu (mm)
STD = 0.05         # normal surec standart sapmasi
ALT_GRUP_SAYISI = 30
ALT_GRUP_BOYUTU = 5   # her alt grupta 5 olcum

kayitlar = []
for grup_no in range(1, ALT_GRUP_SAYISI + 1):
    ortalama = HEDEF
    std = STD

    # 20. alt gruptan sonra ortalama yukari kayar (surec kaymasi)
    if grup_no > 20:
        ortalama = HEDEF + 0.06
    # 25. alt gruptan sonra degiskenlik artar
    if grup_no > 25:
        std = STD * 2.2

    olcumler = rng.normal(ortalama, std, ALT_GRUP_BOYUTU)
    for olcum_no, deger in enumerate(olcumler, start=1):
        kayitlar.append(
            {
                "alt_grup": grup_no,
                "olcum_no": olcum_no,
                "olcum_mm": round(float(deger), 4),
            }
        )

df = pd.DataFrame(kayitlar)
cikti_yolu = "veri/olcum_verileri.csv"
df.to_csv(cikti_yolu, index=False, encoding="utf-8-sig")
print(f"{len(df)} olcum uretildi ({ALT_GRUP_SAYISI} alt grup) -> {cikti_yolu}")
print(df.head(10))
