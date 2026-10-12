import unittest
from calculate_legal import calculate_aaut_fee, calculate_icra_kapak, calculate_mediation_fee, calculate_yasal_faiz

class TestLegalCalculations(unittest.TestCase):
    def test_aaut_small(self):
        res = calculate_aaut_fee(50000)
        self.assertEqual(res["net_vekalet_ucreti"], 8000.0)
        self.assertEqual(res["kdv_tutari"], 1600.0)
        self.assertEqual(res["toplam_ucret"], 9600.0)

    def test_aaut_brackets(self):
        res = calculate_aaut_fee(250000)
        # 100k * 0.16 = 16k
        # 100k * 0.15 = 15k
        # 50k * 0.14 = 7k -> total net 38k
        self.assertEqual(res["net_vekalet_ucreti"], 38000.0)

    def test_icra_kapak(self):
        res = calculate_icra_kapak(100000, faiz=10000, masraf=2000)
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
