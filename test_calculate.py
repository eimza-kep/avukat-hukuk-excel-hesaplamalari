import unittest
from calculate_legal import (
    calculate_aaut_fee,
    calculate_inkar_tazminati,
    calculate_icra_kapak,
    calculate_mediation_fee,
    calculate_yasal_faiz,
    calculate_appellate_limits,
    calculate_court_fees
)

class TestLegalCalculations(unittest.TestCase):
    def test_aaut_2026_vs_2024(self):
        # 400.000 TL alacak:
        # 2026/2027: İlk 400k %16 = 64.000 TL net
        res_2026 = calculate_aaut_fee(400000, year=2026)
        self.assertEqual(res_2026["net_vekalet_ucreti"], 64000.0)
        self.assertEqual(res_2026["kdv_tutari"], 12800.0)
        self.assertEqual(res_2026["toplam_ucret"], 76800.0)

        # 2024/2025: 100k*%16 + 100k*%15 + 200k*%14 = 16k + 15k + 28k = 59.000 TL net
        res_2024 = calculate_aaut_fee(400000, year=2024)
        self.assertEqual(res_2024["net_vekalet_ucreti"], 59000.0)

    def test_aaut_court_minimum_and_claim_cap(self):
        # AAÜT m. 13/2 Kuralı: Vekalet ücreti alacak tutarını geçemez!
        # Dava değeri 10.000 TL, Asliye Hukuk maktusu 30.000 TL -> 10.000 TL olmalı
        res_cap = calculate_aaut_fee(10000, year=2026, mahkeme="asliye_hukuk")
        self.assertEqual(res_cap["net_vekalet_ucreti"], 10000.0)
        self.assertTrue(res_cap["alacak_siniri_uygulandi"])

        # Dava değeri 50.000 TL, Asliye Hukuk maktusu 30.000 TL (Nispi: 50k*%16 = 8.000 TL)
        # Nispi < Maktu olduğu için maktu (30.000 TL) uygulanmalı
        res_maktu = calculate_aaut_fee(50000, year=2026, mahkeme="asliye_hukuk")
        self.assertEqual(res_maktu["net_vekalet_ucreti"], 30000.0)
        self.assertTrue(res_maktu["uygulanan_maktu"])

    def test_inkar_tazminati_full(self):
        # 100.000 TL asıl alacak, borçlu tamamına itiraz etti
        res = calculate_inkar_tazminati(100000, itiraz_edilen_tutar=100000, faiz=5000, masraf=1000)
        # %20 inkar tazminatı = 20.000 TL
        self.assertEqual(res["icra_inkar_tazminati"], 20000.0)
        self.assertEqual(res["kabul_edilen_tutar"], 0.0)
        self.assertGreater(res["vekalet_ucreti"], 0.0)
        self.assertGreater(res["toplam_borclu_yukumlulugu"], 126000.0)

    def test_inkar_tazminati_partial(self):
        # 200.000 TL asıl alacak, borçlu sadece 150.000 TL'sine itiraz etti (50.000 TL kabul)
        res = calculate_inkar_tazminati(200000, itiraz_edilen_tutar=150000)
        # %20 inkar tazminatı sadece itiraz edilen 150.000 TL üzerinden = 30.000 TL
        self.assertEqual(res["itiraz_edilen_tutar"], 150000.0)
        self.assertEqual(res["kabul_edilen_tutar"], 50000.0)
        self.assertEqual(res["icra_inkar_tazminati"], 30000.0)

    def test_icra_kapak(self):
        res = calculate_icra_kapak(100000, faiz=10000, masraf=2000, year=2026)
        self.assertEqual(res["asil_alacak"], 100000.0)
        self.assertGreater(res["dosya_kapak_bakiyesi"], 112000.0)

    def test_mediation_fee(self):
        res = calculate_mediation_fee(100000)
        self.assertEqual(res["net_arabuluculuk_ucreti"], 6000.0)
        self.assertEqual(res["toplam_ucret"], 7200.0)

    def test_yasal_faiz(self):
        # 365.000 TL, %24, 365 gün -> 87.600 TL faiz, toplam 452.600 TL
        res = calculate_yasal_faiz(365000, 365, 0.24)
        self.assertEqual(res["asil_alacak"], 365000.0)
        self.assertEqual(res["faiz_tutari"], 87600.0)
        self.assertEqual(res["toplam_alacak"], 452600.0)

    def test_appellate_limits_below_istinaf(self):
        # 2026 yılı HMK istinaf sınırı 58.520 TL; 40.000 TL alacak kesin olmalı
        res = calculate_appellate_limits(40000.0, karar_yili=2026, mahkeme="hmk")
        self.assertFalse(res["istinaf_acik"])
        self.assertFalse(res["temyiz_acik"])
        self.assertIn("KESİN", res["istinaf_durumu"])
        # Senetle ispat sınırı (48.580 TL) altında kaldığından tanık dinlenebilir
        self.assertFalse(res["senet_zorunlu"])

    def test_appellate_limits_between_istinaf_and_temyiz(self):
        # 2026 yılı 200.000 TL alacak: İstinafa AÇIK, fakat Temyize KAPALI (kesin), Senet Zorunlu
        res = calculate_appellate_limits(200000.0, karar_yili=2026, mahkeme="hmk")
        self.assertTrue(res["istinaf_acik"])
        self.assertFalse(res["temyiz_acik"])
        self.assertIn("AÇIK", res["istinaf_durumu"])
        self.assertIn("KESİN", res["temyiz_durumu"])
        self.assertTrue(res["senet_zorunlu"])

    def test_appellate_limits_above_temyiz(self):
        # 2026 yılı 1.000.000 TL alacak: İstinafa AÇIK ve Temyize AÇIK
        res = calculate_appellate_limits(1000000.0, karar_yili=2026, mahkeme="hmk")
        self.assertTrue(res["istinaf_acik"])
        self.assertTrue(res["temyiz_acik"])
        self.assertIn("AÇIK", res["temyiz_durumu"])

    def test_appellate_limits_iik(self):
        # 2026 yılı İİK İstinaf 136.930 TL, Temyiz 913.380 TL
        # 100.000 TL -> İİK İstinaf Kesin
        res_kesin = calculate_appellate_limits(100000.0, karar_yili=2026, mahkeme="iik")
        self.assertFalse(res_kesin["istinaf_acik"])
        self.assertEqual(res_kesin["istinaf_siniri"], 136930.0)

        # 500.000 TL -> İstinaf Açık, Temyiz Kesin
        res_istinaf = calculate_appellate_limits(500000.0, karar_yili=2026, mahkeme="iik")
        self.assertTrue(res_istinaf["istinaf_acik"])
        self.assertFalse(res_istinaf["temyiz_acik"])

    def test_court_fees_nispi_and_maktu(self):
        # 100.000 TL nispi dava, 2 taraf, 2026
        # Karar ilam harcı: 100.000 * 0.06831 = 6.831 TL
        # Peşin harç (1/4): 6.831 / 4 = 1.707,75 TL
        res_nispi = calculate_court_fees(100000.0, taraf_sayisi=2, dava_turu="nispi", year=2026)
        self.assertEqual(res_nispi["nispi_karar_ilam_harci"], 6831.0)
        self.assertEqual(res_nispi["pesin_nispi_harc"], 1707.75)
        self.assertGreater(res_nispi["gider_avansi"], 1000.0)
        self.assertGreater(res_nispi["toplam_dava_acilis_masrafi"], 3000.0)

        # Maktu dava
        res_maktu = calculate_court_fees(100000.0, taraf_sayisi=2, dava_turu="maktu", year=2026)
        self.assertEqual(res_maktu["nispi_karar_ilam_harci"], 0.0)
        self.assertEqual(res_maktu["pesin_nispi_harc"], 650.0)

if __name__ == "__main__":
    unittest.main()
