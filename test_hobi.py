import unittest
import json
import os

# Test edeceğimiz fonksiyonu içeren mantığı buraya basitçe simüle ediyoruz
def bütçe_kontrolü(fiyat, limit):
    return fiyat <= limit

class HobiTesti(unittest.TestCase):

    # 1. TEST: Dosya var mı?
    def test_dosya_var_mi(self):
        self.assertTrue(os.path.exists('activity.json'), "HATA: activity.json dosyası yerinde değil!")

    # 2. TEST: Bütçe filtresi doğru çalışıyor mu?
    def test_butce_limit(self):
        # 0.5 bütçe sınırı varken 0.2'lik hobi uygun mu? (Evet olmalı)
        self.assertEqual(bütçe_kontrolü(0.2, 0.5), True)
        # 0.5 bütçe sınırı varken 0.8'lik hobi uygun mu? (Hayır olmalı)
        self.assertEqual(bütçe_kontrolü(0.8, 0.5), False)

    # 3. TEST: Veri setindeki alanlar doğru mu?
    def test_veri_yapisi(self):
        with open('activity.json', 'r', encoding='utf-8') as f:
            veri = json.load(f)
            ilk_hobi = veri[0]
            self.assertIn('activity', ilk_hobi)
            self.assertIn('price', ilk_hobi)

if __name__ == '__main__':
    unittest.main()