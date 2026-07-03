"""
Istatistiksel Surec Kontrolu (SPC) - X-bar ve R Kontrol Grafikleri
------------------------------------------------------------------
Alt gruplar halinde toplanmis olcum verisinden X-bar (ortalama) ve R (deger
araligi) kontrol grafiklerini olusturur, kontrol limitlerini hesaplar ve
kontrol disi (out-of-control) noktalari isaretler.

Kontrol limitleri (Shewhart, standart sabitlerle):
    X-bar:  UCL = X_ortalama + A2 * R_ortalama
            LCL = X_ortalama - A2 * R_ortalama
    R    :  UCL = D4 * R_ortalama
            LCL = D3 * R_ortalama

Ek olarak Western Electric Kural 1 uygulanir: 3-sigma limitleri disindaki
her nokta kontrol disi kabul edilir.

Calistirma:
    python src/spc.py
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

VERI_YOLU = "veri/olcum_verileri.csv"
CIKTI_KLASORU = "cikti"

# Alt grup boyutuna gore SPC sabitleri (Shewhart tablolari)
SPC_SABITLERI = {
    2: {"A2": 1.880, "D3": 0.000, "D4": 3.267},
    3: {"A2": 1.023, "D3": 0.000, "D4": 2.574},
    4: {"A2": 0.729, "D3": 0.000, "D4": 2.282},
    5: {"A2": 0.577, "D3": 0.000, "D4": 2.114},
    6: {"A2": 0.483, "D3": 0.000, "D4": 2.004},
    7: {"A2": 0.419, "D3": 0.076, "D4": 1.924},
}


def veri_yukle(yol: str) -> pd.DataFrame:
    return pd.read_csv(yol)


def alt_grup_istatistikleri(df: pd.DataFrame) -> pd.DataFrame:
    """Her alt grup icin ortalama (X-bar) ve deger araligini (R) hesaplar."""
    ozet = df.groupby("alt_grup")["olcum_mm"].agg(
        x_bar="mean",
        r_deger=lambda s: s.max() - s.min(),
    )
    return ozet.reset_index()


def kontrol_limitleri(ozet: pd.DataFrame, n: int) -> dict:
    """X-bar ve R grafikleri icin merkez cizgi ve kontrol limitlerini hesaplar."""
    if n not in SPC_SABITLERI:
        raise ValueError(f"n={n} icin SPC sabiti tanimli degil (2-7 destekleniyor).")
    sabit = SPC_SABITLERI[n]

    x_ort = ozet["x_bar"].mean()   # X çift bar (genel ortalama)
    r_ort = ozet["r_deger"].mean()  # R bar

    return {
        "x_merkez": x_ort,
        "x_ucl": x_ort + sabit["A2"] * r_ort,
        "x_lcl": x_ort - sabit["A2"] * r_ort,
        "r_merkez": r_ort,
        "r_ucl": sabit["D4"] * r_ort,
        "r_lcl": sabit["D3"] * r_ort,
    }


def kontrol_disi_isaretle(ozet: pd.DataFrame, lim: dict) -> pd.DataFrame:
    """Kontrol limitleri disindaki alt gruplari isaretler."""
    ozet = ozet.copy()
    ozet["x_kontrol_disi"] = (ozet["x_bar"] > lim["x_ucl"]) | (ozet["x_bar"] < lim["x_lcl"])
    ozet["r_kontrol_disi"] = (ozet["r_deger"] > lim["r_ucl"]) | (ozet["r_deger"] < lim["r_lcl"])
    return ozet


def rapor_yazdir(ozet: pd.DataFrame, lim: dict) -> None:
    print("=" * 55)
    print("KONTROL LIMITLERI")
    print("=" * 55)
    print(f"X-bar  Merkez: {lim['x_merkez']:.4f} | UCL: {lim['x_ucl']:.4f} | LCL: {lim['x_lcl']:.4f}")
    print(f"R      Merkez: {lim['r_merkez']:.4f} | UCL: {lim['r_ucl']:.4f} | LCL: {lim['r_lcl']:.4f}")
    print()

    x_disi = ozet.loc[ozet["x_kontrol_disi"], "alt_grup"].tolist()
    r_disi = ozet.loc[ozet["r_kontrol_disi"], "alt_grup"].tolist()
    print("=" * 55)
    print("KONTROL DISI NOKTALAR")
    print("=" * 55)
    print(f"X-bar grafiginde kontrol disi alt gruplar: {x_disi if x_disi else 'Yok'}")
    print(f"R grafiginde kontrol disi alt gruplar    : {r_disi if r_disi else 'Yok'}")
    print()
    if x_disi or r_disi:
        print("=> Surecte istatistiksel olarak anlamli bir bozulma tespit edildi.")
    else:
        print("=> Surec kontrol altinda gorunuyor.")
    print()


def grafik_ciz(ozet: pd.DataFrame, lim: dict) -> None:
    os.makedirs(CIKTI_KLASORU, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8), sharex=True)

    # --- X-bar grafigi ---
    ax1.plot(ozet["alt_grup"], ozet["x_bar"], marker="o", color="#2b6cb0")
    ax1.axhline(lim["x_merkez"], color="green", label="Merkez (X̿)")
    ax1.axhline(lim["x_ucl"], color="red", linestyle="--", label="UCL / LCL")
    ax1.axhline(lim["x_lcl"], color="red", linestyle="--")
    disi = ozet[ozet["x_kontrol_disi"]]
    ax1.scatter(disi["alt_grup"], disi["x_bar"], color="red", s=90, zorder=5, label="Kontrol dışı")
    ax1.set_title("X-bar Kontrol Grafiği (Alt Grup Ortalamaları)")
    ax1.set_ylabel("Ortalama ölçü (mm)")
    ax1.legend(loc="upper left", fontsize=8)
    ax1.grid(alpha=0.3)

    # --- R grafigi ---
    ax2.plot(ozet["alt_grup"], ozet["r_deger"], marker="o", color="#805ad5")
    ax2.axhline(lim["r_merkez"], color="green", label="Merkez (R̄)")
    ax2.axhline(lim["r_ucl"], color="red", linestyle="--", label="UCL / LCL")
    ax2.axhline(lim["r_lcl"], color="red", linestyle="--")
    disi_r = ozet[ozet["r_kontrol_disi"]]
    ax2.scatter(disi_r["alt_grup"], disi_r["r_deger"], color="red", s=90, zorder=5, label="Kontrol dışı")
    ax2.set_title("R Kontrol Grafiği (Alt Grup Değer Aralıkları)")
    ax2.set_xlabel("Alt grup no")
    ax2.set_ylabel("Değer aralığı R (mm)")
    ax2.legend(loc="upper left", fontsize=8)
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{CIKTI_KLASORU}/spc_kontrol_grafikleri.png", dpi=120)
    plt.close()
    print(f"Kontrol grafikleri '{CIKTI_KLASORU}/spc_kontrol_grafikleri.png' olarak kaydedildi.")


def main() -> None:
    df = veri_yukle(VERI_YOLU)
    n = int(df.groupby("alt_grup").size().mode()[0])  # alt grup boyutu
    print(f"Alt grup boyutu (n): {n}\n")

    ozet = alt_grup_istatistikleri(df)
    lim = kontrol_limitleri(ozet, n)
    ozet = kontrol_disi_isaretle(ozet, lim)

    rapor_yazdir(ozet, lim)
    grafik_ciz(ozet, lim)

    os.makedirs(CIKTI_KLASORU, exist_ok=True)
    ozet.to_csv(f"{CIKTI_KLASORU}/alt_grup_ozeti.csv", index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    main()
