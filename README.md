# Hukuk ve Avukatlık Excel Hesaplama Araçları ⚖️🏛️

[![CI - Hukuk Excel Doğrulama](https://github.com/eimza-kep/avukat-hukuk-excel-hesaplamalari/actions/workflows/ci.yml/badge.svg)](https://github.com/eimza-kep/avukat-hukuk-excel-hesaplamalari/actions/workflows/ci.yml)
[![Şablon Sayısı](https://img.shields.io/badge/%C5%9Eablon_Say%C4%B1s%C4%B1-8_Excel_Arac%C4%B1-success.svg)](#-içerik-ve-şablon-listesi)
[![Mevzuat](https://img.shields.io/badge/Mevzuat-2026%2F2027_AA%C3%9CT_Uyumlu-blue.svg)](#)
[![Python Engine](https://img.shields.io/badge/Python-CLI_v2.0-brightgreen.svg)](calculate_legal.py)
[![Lisans](https://img.shields.io/badge/Lisans-MIT-orange.svg)](LICENSE)
[![Organizasyon](https://img.shields.io/badge/GitHub-eimza--kep-blue.svg)](https://github.com)

Avukatlar, stajyer avukatlar, hukuk büroları, icra müdürlükleri ve arabulucular için Türkiye Barolar Birliği (TBB) ve T.C. Adalet Bakanlığı mevzuatı (**2026/2027 Güncel AAÜT**, **İİK m. 67 & 68/a**, HMK, 3095 Sayılı Kanuni Faiz Kanunu, 4857 Sayılı İş Kanunu) esas alınarak hazırlanmış **8 adet formüllü profesyonel Excel (.xlsx) şablonu** ve **Python CLI hesaplama motoru**.

---

## 📑 İçerik ve Şablon Listesi

| No | Dosya Adı | Açıklama ve Kapsam | İlgili Mevzuat |
| :---: | :--- | :--- | :--- |
| **08** | [`08_aaut_vekalet_ucreti_hesaplayici.xlsx`](08_aaut_vekalet_ucreti_hesaplayici.xlsx) | Avukatlık Asgari Ücret Tarifesi (AAÜT) 2026/2027 kademeli nispi vekalet ücreti, mahkeme maktu sınırları ve %20 KDV hesabı. | Avukatlık Kanunu & AAÜT |
| **09** | [`09_icra_takip_ve_kapak_hesabi.xlsx`](09_icra_takip_ve_kapak_hesabi.xlsx) | İcra dairesi dosya kapak hesabı: asıl alacak, takip faizi, masraflar, icra vekalet ücreti, tahsil harcı (%9.10) ve cezaevi fonu (%2). | İcra ve İflas Kanunu (İİK) M.138 |
| **10** | [`10_yasal_faiz_ve_temerrut_faizi_hesaplayici.xlsx`](10_yasal_faiz_ve_temerrut_faizi_hesaplayici.xlsx) | 3095 Sayılı Kanun kapsamında yasal faiz (%24) ve ticari temerrüt faizi günlük kademeli hesaplama motoru. | 3095 Sayılı Kanun |
| **11** | [`11_dava_harc_ve_gider_avansi_hesaplayici.xlsx`](11_dava_harc_ve_gider_avansi_hesaplayici.xlsx) | Hukuk mahkemeleri dava açılışında peşin harç (binde 68.31'in 1/4'ü), başvurma harcı, vekâlet pulu ve HMK gider avansı. | Harçlar Kanunu (1) Sayılı Tarife & HMK M.120 |
| **12** | [`12_arabuluculuk_asgari_ucret_hesaplayici.xlsx`](12_arabuluculuk_asgari_ucret_hesaplayici.xlsx) | Dava şartı ve ihtiyari arabuluculuk kademeli ücret tarifesi (İlk 100 bin TL %6, sonraki 160 bin TL %5 vb.) ve tarafların %50 payı. | Arabuluculuk Asgari Ücret Tarifesi |
| **13** | [`13_avukat_dava_ve_is_takip_cizelgesi.xlsx`](13_avukat_dava_ve_is_takip_cizelgesi.xlsx) | Dava dosyaları, duruşma tarihleri, istinaf/temyiz süreleri, kalan gün hesabı (`=Tarih - BUGÜN()`) ve sorumlu avukat takip matrisi. | HMK & UYAP İş Akışları |
| **14** | [`14_ise_iade_ve_iscilik_alacaklari_hesaplayici.xlsx`](14_ise_iade_ve_iscilik_alacaklari_hesaplayici.xlsx) | Boşta geçen süre ücreti (en çok 4 ay), SGK/GV/DV kesintileri ve işe başlatmama tazminatı net alacak tablosu. | 4857 Sayılı İş Kanunu M.21 |
| **15** | [`15_itirazin_iptali_ve_icra_inkar_tazminati_hesaplayici.xlsx`](15_itirazin_iptali_ve_icra_inkar_tazminati_hesaplayici.xlsx) | İİK m. 67 ve 68/a uyarınca itirazın kaldırılması, kısmi itiraz ayrımı, **asgari %20 İcra İnkar Tazminatı** ve yargılama gideri hesabı. | İİK Madde 67, 68 ve 68/a |

---

## ⚡ CLI Hesaplama Motoru (Python `calculate_legal.py`)

Python motoru sıfır ek kütüphane bağımlılığıyla çalışır. Terminal üzerinden anlık hesaplamalar yapabilir, `--json` veya `--markdown` bayraklarıyla rapor üretebilirsiniz.

### 1. 2026/2027 AAÜT Vekalet Ücreti Hesaplama
```bash
# 2026/2027 Nispi Vekalet Ücreti (Varsayılan 2026)
python calculate_legal.py aaut 750000

# Belirli Mahkeme Türü ve Maktu Ücret / Alacak Sınırı Kontrolü (AAÜT m. 13/2)
python calculate_legal.py aaut 15000 --mahkeme sulh_hukuk
python calculate_legal.py aaut 50000 --mahkeme asliye_hukuk

# Geçmiş Yıl (2024/2025) Tarifesi ile Karşılaştırma
python calculate_legal.py aaut 400000 --year 2024
python calculate_legal.py aaut 400000 --year 2026
```

### 2. İİK Madde 67 & 68/a %20 İcra İnkar Tazminatı Hesabı
```bash
# 150.000 TL alacağın tamamına itiraz edilmişse:
python calculate_legal.py inkar 150000

# Kısmi İtiraz: 200.000 TL takibin 120.000 TL'sine itiraz edilmişse:
python calculate_legal.py inkar 200000 --itiraz 120000 --faiz 15000 --masraf 2000

# JSON ve Markdown Formatında Rapor Çıktısı Alma:
python calculate_legal.py inkar 100000 --markdown
python calculate_legal.py inkar 100000 --json
```

### 3. İcra Dosya Kapak Hesabı
```bash
# Asıl alacak, işlemiş faiz ve icra takip masrafları ile dosya kapak bakiyesi:
python calculate_legal.py icra 100000 --faiz 12000 --masraf 1800
```

### 4. 3095 Sayılı Kanun Yasal Faiz ve Ticari Temerrüt Faizi
```bash
# 250.000 TL asıl alacağın 180 günlük kanuni faizi (%24 yıllık oran):
python calculate_legal.py faiz 250000 180 --oran 0.24
```

### 5. Arabuluculuk Asgari Ücreti
```bash
# 500.000 TL anlaşma tutarı üzerinden kademeli arabulucu ücreti:
python calculate_legal.py arabuluculuk 500000
```

---

## 🛠️ Kurulum ve Test Kılavuzu

### Yerel Kurulum
1. Projeyi klonlayın:
   ```bash
   git clone https://github.com/eimza-kep/avukat-hukuk-excel-hesaplamalari.git
   cd avukat-hukuk-excel-hesaplamalari
   ```
2. (İsteğe Bağlı) Python sanal ortamı oluşturun:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```
3. Excel doğrulama bağımlılığını kurun:
   ```bash
   pip install openpyxl
   ```

### Birim Testleri Çalıştırma
Tüm hesaplama algoritmalarını ve Excel dosyalarını doğrulamak için:
```bash
# Hukuki hesaplama algoritmalarını test et (AAÜT, İİK 68/a, Faiz, Kapak):
python test_calculate.py

# 8 adet Excel şablonunun hücre, formül ve başlık yapısını test et:
python scripts/test_spreadsheets.py
```

---

## 🌐 E-Dönüşüm & LegalTech Ekosistemi

Bu depo, [@eimza-kep](https://github.com/eimza-kep) açık kaynak LegalTech ve e-dönüşüm ekosisteminin bir parçasıdır:

* ⚖️ **[e-fatura-itiraz-ve-iade-scripti](https://github.com/eimza-kep/e-fatura-itiraz-ve-iade-scripti):** TTK 18/3 uyarınca 8 günlük fatura itiraz süresi, KEP delil tespiti ve UBL ayrıştırma portalı.
* ⚖️ **[avukat-muvekkil-on-kayit-scripti](https://github.com/eimza-kep/avukat-muvekkil-on-kayit-scripti):** Avukatlar için müvekkil ön görüşme ve çıkar çatışması (conflict check) portalı.
* ⚖️ **[avukat-arabuluculuk-basvuru-scripti](https://github.com/eimza-kep/avukat-arabuluculuk-basvuru-scripti):** Arabuluculuk başvuru ve toplantı tutanağı portalı.
* 📝 **[udf2md](https://github.com/eimza-kep/udf2md):** UYAP UDF dosyalarını yapay zekanın (LLM/RAG) okuyabileceği Markdown ve JSON formatına dönüştürücü.
* 🛠️ **[uyap-editor-hizli-onarim](https://github.com/eimza-kep/uyap-editor-hizli-onarim):** UYAP Doküman Editörü açılmama ve Java bellek aşımı onarım aracı.
* 🇹🇷 **[awesome-turkiye-e-donusum](https://github.com/eimza-kep/awesome-turkiye-e-donusum):** Türkiye E-Dönüşüm ve LegalTech kütüphaneleri listesi.

---

## 📜 Lisans

Bu proje **MIT Lisansı** ile lisanslanmıştır. Serbestçe indirilebilir ve mesleki davalarda kullanılabilir.
