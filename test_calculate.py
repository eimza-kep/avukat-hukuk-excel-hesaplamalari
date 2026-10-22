import unittest
from calculate_legal import (
    calculate_aaut_fee,
    calculate_inkar_tazminati,
    calculate_icra_kapak,
    calculate_mediation_fee,
    calculate_yasal_faiz
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

if __name__ == "__main__":
    unittest.main()
