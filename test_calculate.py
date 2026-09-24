import unittest
from calculate_legal import calculate_aaut_fee, calculate_icra_kapak

class TestCalculateLegal(unittest.TestCase):
    def test_aaut_first_tier(self):
        # 50.000 TL için %16 = 8.000 TL net, %20 KDV = 1.600 TL, toplam = 9.600 TL
        res = calculate_aaut_fee(50000)
        self.assertEqual(res["net_vekalet_ucreti"], 8000.0)
        self.assertEqual(res["kdv_tutari"], 1600.0)
        self.assertEqual(res["toplam_ucret"], 9600.0)

    def test_aaut_second_tier(self):
        # 150.000 TL: ilk 100k %16 (16k) + sonraki 50k %15 (7.5k) = 23.500 TL net
        res = calculate_aaut_fee(150000)
        self.assertEqual(res["net_vekalet_ucreti"], 23500.0)

    def test_icra_kapak_calculation(self):
        res = calculate_icra_kapak(100000, faiz=10000, masraf=2000)
        self.assertEqual(res["asil_alacak"], 100000.0)
        self.assertEqual(res["faiz"], 10000.0)
        self.assertEqual(res["masraf"], 2000.0)
        self.assertGreater(res["dosya_kapak_bakiyesi"], 112000.0)

if __name__ == "__main__":
    unittest.main()
