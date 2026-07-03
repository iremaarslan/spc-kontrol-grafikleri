# 📉 İstatistiksel Süreç Kontrolü (SPC) — X-bar & R Kontrol Grafikleri


> **Alan:** Kalite Mühendisliği · İstatistiksel Süreç Kontrolü · Endüstri Mühendisliği
> **Araçlar:** Python · pandas · matplotlib

Bir imalat sürecinden alt gruplar halinde toplanan ölçümleri kullanarak
**Shewhart kontrol grafikleri** (X-bar ve R) oluşturan, kontrol limitlerini
hesaplayan ve **kontrol dışı (out-of-control) noktaları** otomatik tespit eden
bir kalite kontrol projesidir.

> 💡 Bu proje, CV'deki **"İstatistiksel Süreç Kontrolü"** yetkinliğinin doğrudan
> uygulamasıdır. SPC, endüstri mühendisliğinde bir sürecin zamanla kararlı kalıp
> kalmadığını izlemenin klasik yöntemidir.

---

## 🎯 Neyi Gösteriyor?

- Alt gruplama (subgroup) mantığıyla ölçüm verisi işleme
- **X-bar grafiği** (süreç ortalamasının izlenmesi)
- **R grafiği** (süreç değişkenliğinin izlenmesi)
- Standart Shewhart sabitleriyle (A2, D3, D4) kontrol limiti hesabı
- Kontrol dışı noktaların otomatik işaretlenmesi (Western Electric Kural 1)

## 🧠 Kontrol Limitleri

```
X-bar:  UCL = X̿ + A2 · R̄        LCL = X̿ − A2 · R̄
R    :  UCL = D4 · R̄            LCL = D3 · R̄
```

`A2`, `D3`, `D4` sabitleri alt grup boyutuna (n) göre standart SPC tablolarından
alınır (kod içinde `SPC_SABITLERI` sözlüğünde tanımlı, n = 2–7 destekli).

## 🧪 Test Senaryosu

Sentetik veriye bilerek iki bozulma enjekte edilir:
1. **20. alt gruptan sonra** süreç ortalaması yukarı kayar (mean shift)
2. **25. alt gruptan sonra** süreç değişkenliği artar

SPC grafiklerinin bu bozulmaları yakalaması beklenir — ve yakalar:

```
X-bar kontrol dışı: [29]
R     kontrol dışı: [27, 28, 29]
=> Süreçte istatistiksel olarak anlamlı bir bozulma tespit edildi.
```

## 🗂️ Klasör Yapısı

```
03-spc-kontrol-grafikleri/
├── veri/
│   └── olcum_verileri.csv       # Sentetik ölçümler (30 alt grup × 5 ölçüm)
├── src/
│   ├── veri_uret.py             # Sentetik ölçüm verisi üretir
│   └── spc.py                   # X-bar & R grafikleri + kontrol dışı tespiti
├── spc_defteri.ipynb            # 📓 İnteraktif Jupyter defteri (çıktılar gömülü)
├── cikti/                       # Grafik + alt grup özeti (script üretir)
├── requirements.txt
└── README.md
```

## 🚀 Nasıl Çalıştırılır?

```bash
pip install -r requirements.txt
python src/veri_uret.py    # (isteğe bağlı) veriyi yeniden üret
python src/spc.py          # kontrol grafikleri + rapor
jupyter notebook spc_defteri.ipynb   # interaktif defter (isteğe bağlı)
```

Çıktı: `cikti/spc_kontrol_grafikleri.png` (üstte X-bar, altta R grafiği).

## 🤔 Neden Bu Projede Makine Öğrenmesi Yok?

SPC, doğası gereği **istatistiksel** bir yöntemdir ve az veriyle bile güvenilir,
**yorumlanabilir** sonuç verir. 30 alt gruplu bir veri setinde ML modeli aşırı
öğrenmeye (overfitting) çok yatkın olur ve kontrol grafiklerinin sağladığı net
karar kurallarını sağlamaz.

**Doğru araç seçimi mühendisliğin bir parçasıdır** — her probleme ML uygulamak
yerine, kalite kontrolde kanıtlanmış Shewhart yöntemini kullanmak daha profesyonel
bir tercihtir. (ML'in doğal olarak oturduğu projeler için **Proje 1, 2 ve 4**'e bakın.)

---

### 🔧 Geliştirme Fikirleri
- Tüm Western Electric / Nelson kurallarını ekle (trend, 2/3 nokta 2σ dışı, vb.)
- Süreç yeterlilik indeksleri **Cp / Cpk** hesabı ekle
- Kontrol grafiğini gerçek zamanlı (streaming) veriyle güncelleyen bir sürüm yap
