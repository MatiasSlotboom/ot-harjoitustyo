import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_kortin_saldo_alussa_oikein(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.00)

    def test_rahan_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(500)
        self.assertEqual(self.maksukortti.saldo_euroina(), 15.00)

    def test_kortilta_rahan_ottaminen_vahentaa_saldoa_oikein(self):
        self.maksukortti.ota_rahaa(500)
        self.assertEqual(self.maksukortti.saldo_euroina(), 5.00)

    def test_kortilta_rahan_ottaminen_ei_vahenna_saldoa_jos_ei_riittavasti(self):
        self.maksukortti.ota_rahaa(2000)
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

    def test_kortilta_rahan_ottaminen_palauttaa_true_jos_riittaa(self):
        self.assertEqual(self.maksukortti.ota_rahaa(500), True)

    def test_kortilta_rahan_ottaminen_palauttaa_false_jos_riittaa(self):
        self.assertEqual(self.maksukortti.ota_rahaa(100000), False)

    def test_str_metodi_palauttaa_oikean_merkkijonon(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")