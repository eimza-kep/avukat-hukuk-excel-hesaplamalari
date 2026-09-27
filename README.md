# Hukuk ve Avukatlık Excel Hesaplama Araçları ⚖️🏛️

[![CI - Hukuk Excel Doğrulama](https://github.com/eimza-kep/avukat-hukuk-excel-hesaplamalari/actions/workflows/ci.yml/badge.svg)](https://github.com/eimza-kep/avukat-hukuk-excel-hesaplamalari/actions/workflows/ci.yml)
[![Şablon Sayısı](https://img.shields.io/badge/%C5%9Eablon_Say%C4%B1s%C4%B1-7_Excel_Arac%C4%B1-success.svg)](#-içerik-ve-şablon-listesi)
[![Mevzuat](https://img.shields.io/badge/Mevzuat-2026_Uyumlu-blue.svg)](#)
[![Lisans](https://img.shields.io/badge/Lisans-MIT-orange.svg)](LICENSE)
[![Organizasyon](https://img.shields.io/badge/GitHub-eimza--kep-blue.svg)](https://github.com)

Avukatlar, stajyer avukatlar, hukuk büroları ve arabulucular için Türkiye Cumhuriyeti Adalet Bakanlığı ve Barolar Birliği mevzuatı (AAÜT, İİK, HMK, 3095 Sayılı Kanun, 4857 Sayılı İş Kanunu) esas alınarak hazırlanmış **7 adet formüllü profesyonel Excel (.xlsx) şablonu** ve **Python CLI hesaplama motoru**.

---

## 📑 İçerik ve Şablon Listesi

| No | Dosya Adı | Açıklama ve Kapsam | İlgili Mevzuat |
| :---: | :--- | :--- | :--- |
| **08** | [`08_aaut_vekalet_ucreti_hesaplayici.xlsx`](08_aaut_vekalet_ucreti_hesaplayici.xlsx) | Avukatlık Asgari Ücret Tarifesi (AAÜT) 5 kademeli nispi vekalet ücreti, maktu sınır ve %20 KDV hesabı. | Avukatlık Kanunu & AAÜT |
| **09** | [`09_icra_takip_ve_kapak_hesabi.xlsx`](09_icra_takip_ve_kapak_hesabi.xlsx) | İcra dairesi dosya kapak hesabı: asıl alacak, takip faizi, masraflar, icra vekalet ücreti, tahsil harcı (%9.10) ve cezaevi fonu (%2). | İcra ve İflas Kanunu (İİK) M.138 |
| **10** | [`10_yasal_faiz_ve_temerrut_faizi_hesaplayici.xlsx`](10_yasal_faiz_ve_temerrut_faizi_hesaplayici.xlsx) | 3095 Sayılı Kanun kapsamında %9 ve %24 güncel kademeli yasal faiz ve ticari temerrüt faizi günlük faiz formülü. | 3095 Sayılı Kanun |
| **11** | [`11_dava_harc_ve_gider_avansi_hesaplayici.xlsx`](11_dava_harc_ve_gider_avansi_hesaplayici.xlsx) | Hukuk mahkemeleri dava açılışında peşin harç (binde 68.31'in 1/4'ü), başvurma harcı, vekâlet pulu ve HMK gider avansı. | Harçlar Kanunu (1) Sayılı Tarife & HMK M.120 |
| **12** | [`12_arabuluculuk_asgari_ucret_hesaplayici.xlsx`](12_arabuluculuk_asgari_ucret_hesaplayici.xlsx) | Dava şartı ve ihtiyari arabuluculuk kademeli ücret tarifesi (İlk 100 bin TL %6, sonraki 160 bin TL %5 vb.) ve tarafların %50 payı. | Arabuluculuk Asgari Ücret Tarifesi |
| **13** | [`13_avukat_dava_ve_is_takip_cizelgesi.xlsx`](13_avukat_dava_ve_is_takip_cizelgesi.xlsx) | Dava dosyaları, duruşma tarihleri, istinaf/temyiz süreleri, kalan gün hesabı (`=Tarih - BUGÜN()`) ve sorumlu avukat takip matrisi. | HMK & UYAP İş Akışları |
| **14** | [`14_ise_iade_ve_iscilik_alacaklari_hesaplayici.xlsx`](14_ise_iade_ve_iscilik_alacaklari_hesaplayici.xlsx) | Boşta geçen süre ücreti (en çok 4 ay), SGK/GV/DV kesintileri ve işe başlatmama tazminatı (yalnızca DV kesintili) net alacak tablosu. | 4857 Sayılı İş Kanunu M.21 |

---

## ⚡ CLI Hesaplama Motoru (Python)

Excel açmadan terminalden saniyeler içinde hesaplama yapabilirsiniz:

```bash
# AAÜT Nispi Vekalet Ücreti
python calculate_legal.py aaut 250000

# İcra Dosya Kapak Hesabı (Asıl alacak + faiz + masraf)
python calculate_legal.py icra 100000 --faiz 12000 --masraf 1500

# Arabuluculuk Ücreti
python calculate_legal.py arabuluculuk 150000
```

---

## 🌐 E-Dönüşüm & LegalTech Ekosistemi

Bu depo, [@eimza-kep](https://github.com/eimza-kep) açık kaynak LegalTech ve e-dönüşüm ekosisteminin bir parçasıdır:

* ⚖️ **[avukat-muvekkil-on-kayit-scripti](https://github.com/eimza-kep/avukat-muvekkil-on-kayit-scripti):** Avukatlar için müvekkil ön görüşme ve çıkar çatışması (conflict check) portalı.
* ⚖️ **[avukat-arabuluculuk-basvuru-scripti](https://github.com/eimza-kep/avukat-arabuluculuk-basvuru-scripti):** Arabuluculuk başvuru ve toplantı tutanağı portalı.
* 📝 **[udf2md](https://github.com/eimza-kep/udf2md):** UYAP UDF dosyalarını yapay zekanın (LLM/RAG) okuyabileceği Markdown ve JSON formatına dönüştürücü.
* 🛠️ **[uyap-editor-hizli-onarim](https://github.com/eimza-kep/uyap-editor-hizli-onarim):** UYAP Doküman Editörü açılmama ve Java bellek aşımı onarım aracı.
* 🇹🇷 **[awesome-turkiye-e-donusum](https://github.com/eimza-kep/awesome-turkiye-e-donusum):** Türkiye E-Dönüşüm ve LegalTech kütüphaneleri listesi.

---

## 📜 Lisans

Bu proje **MIT Lisansı** ile lisanslanmıştır. Serbestçe indirilebilir ve mesleki davalarda kullanılabilir.
