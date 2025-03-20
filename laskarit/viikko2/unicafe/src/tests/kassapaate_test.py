import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.kortti = Maksukortti(1000)

    def test_luodun_kassapaatteen_rahamäärä_ja_myytyjen_lounaiden_maara_on_oikea(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_kateisosto_toimii_edullisilla_kun_maksu_riittava(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(500), 260)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1002.40)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_kateisosto_toimii_maukkailla_kun_maksu_riittava(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(500), 100)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1004.00)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_kateisosto_edullisilla_kun_maksu_ei_riittava(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(200), 200)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_kateisosto_maukkailla_kun_maksu_ei_riittava(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(300), 300)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_korttiosto_toimii_edullisilla_kun_kortilla_tarpeeksi_rahaa(self):
        self.assertTrue(self.kassapaate.syo_edullisesti_kortilla(self.kortti))
        self.assertEqual(self.kortti.saldo_euroina(), 7.60)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)

    def test_korttiosto_toimii_maukkailla_kun_kortilla_tarpeeksi_rahaa(self):
        self.assertTrue(self.kassapaate.syo_maukkaasti_kortilla(self.kortti))
        self.assertEqual(self.kortti.saldo_euroina(), 6.00)
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)

    def test_korttiosto_edullisilla_kun_kortilla_ei_tarpeeksi_rahaa(self):
        kortti = Maksukortti(200)
        self.assertFalse(self.kassapaate.syo_edullisesti_kortilla(kortti))
        self.assertEqual(kortti.saldo_euroina(), 2.00)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)

    def test_korttiosto_maukkailla_kun_kortilla_ei_tarpeeksi_rahaa(self):
        kortti = Maksukortti(300)
        self.assertFalse(self.kassapaate.syo_maukkaasti_kortilla(kortti))
        self.assertEqual(kortti.saldo_euroina(), 3.00)
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)

    def test_kortille_rahaa_ladattaessa_kortin_saldo_muuttuu_ja_kassan_rahamäärä_kasvaa(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, 500)
        self.assertEqual(self.kortti.saldo_euroina(), 15.00)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1005.00)

    def test_kortille_negatiivista_summaa_ladattaessa_ei_muutoksia(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, -500)
        self.assertEqual(self.kortti.saldo_euroina(), 10.00)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.00)