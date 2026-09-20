# Hukuk ve Avukatlık Excel Hesaplama Araçları ⚖️🏛️

[![CI - Hukuk Excel Doğrulama](https://github.com/eimza-kep/avukat-hukuk-excel-hesaplamalari/actions/workflows/ci.yml/badge.svg)](https://github.com/eimza-kep/avukat-hukuk-excel-hesaplamalari/actions/workflows/ci.yml)
[![Şablon Sayısı](https://img.shields.io/badge/%C5%9Eablon_Say%C4%B1s%C4%B1-7_Excel_Arac%C4%B1-success.svg)](#-içerik-ve-şablon-listesi)
[![Mevzuat](https://img.shields.io/badge/Mevzuat-2026_Uyumlu-blue.svg)](#)
[![Lisans](https://img.shields.io/badge/Lisans-MIT-orange.svg)](LICENSE)
[![Organizasyon](https://img.shields.io/badge/GitHub-eimza--kep-blue.svg)](https://github.com/eimza-kep)

Avukatlar, stajyer avukatlar, hukuk büroları ve arabulucular için Türkiye Cumhuriyeti Adalet Bakanlığı ve Barolar Birliği mevzuatı (AAÜT, İİK, HMK, 3095 Sayılı Kanun, 4857 Sayılı İş Kanunu) esas alınarak hazırlanmış **7 adet formüllü ve profesyonel Excel (.xlsx) hesaplama şablonu**.

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

## 💡 Öne Çıkan Özellikler

* **Kademeli Dilim Mantığı:** AAÜT ve Arabuluculuk tablolarında tek bir yeknesak oran yerine Resmi Gazete'deki kademeli baremler (`MIN`, `MAX` fonksiyonları ile) otomatik hesaplanır.
* **Kapak Hesabı Güvenliği:** İcra dosyası kapatılırken borçludan talep edilecek tahsil harcı ve cezaevi harcı kuruşu kuruşuna denetlenir.
* **Görsel Tasarım:** Ağır kurumsal bordo ve lacivert renk teması, okunabilir büyük puntolar ve anlaşılır açıklama sütunları.
* **Sıfır Makro:** Tamamen saf `.xlsx` formatındadır; UYAP bilgisayarlarında veya mobil cihazlarda sorunsuz çalışır.

---

## 🧪 Test ve Doğrulama

Tüm hukuk tabloları CI test betiği ile denetlenir:

```bash
pip install openpyxl
python scripts/test_spreadsheets.py
```

---

## 🌐 E-Dönüşüm Ekosistemi

Bu depo, [@eimza-kep](https://github.com/eimza-kep) açık kaynak ekosisteminin bir parçasıdır:
* 📖 [e-donusum-rehberleri](https://github.com/eimza-kep/e-donusum-rehberleri) - 24 adet rehber ve UYAP/E-İmza tıkla-çalıştır araçları.
* 📊 [muhasebe-excel-sablonlari](https://github.com/eimza-kep/muhasebe-excel-sablonlari) - e-SMM, Tevkifat, Kıdem ve Bordro hesaplayıcıları.
* 🏢 [kobi-finans-yonetim-excel-sablonlari](https://github.com/eimza-kep/kobi-finans-yonetim-excel-sablonlari) - KOBİ nakit akış, başabaş ve stok tabloları.

---

## 📜 Lisans

Bu proje **MIT Lisansı** ile lisanslanmıştır. Serbestçe indirilebilir ve mesleki davalarda kullanılabilir.
