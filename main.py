import pandas as pd
import json
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. DOSYADAN VERİ OKUMA
try:
    # Senin activity.json dosyanı açar
    with open('activity.json', 'r', encoding='utf-8') as f:
        veri = json.load(f)
    df = pd.DataFrame(veri)
    # Eğer aynı aktivite varsa temizler (Hata payını düşürür)
    df = df.drop_duplicates(subset=['activity']).reset_index(drop=True)
except FileNotFoundError:
    print("HATA: 'activity.json' dosyası bulunamadı! Dosyanın main.py ile aynı klasörde olduğundan emin ol.")
    exit()

# 2. YAPAY ZEKA MODELİ (Senin veri setine özel)
# Algoritmanın daha iyi çalışması için tür ve ismi birleştiriyoruz
df['ozellikler'] = df['type'] + " " + df['activity']

vektorlestirici = TfidfVectorizer(stop_words='english')
tfidf_matrisi = vektorlestirici.fit_transform(df['ozellikler'])
benzerlik_matrisi = cosine_similarity(tfidf_matrisi)

# 3. ÖNERİ SİSTEMİ
def onerileri_goster(secilen_hobi, max_butce=1.0):
    if secilen_hobi not in df['activity'].values:
        print(f"\n'{secilen_hobi}' listede yok!")
        return

    # Seçilen hobinin index'ini bul
    idx = df[df['activity'] == secilen_hobi].index[0]
    
    # Benzerlik skorlarını hesapla
    puanlar = list(enumerate(benzerlik_matrisi[idx]))
    sirali_puanlar = sorted(puanlar, key=lambda x: x[1], reverse=True)

    print(f"\n>>> SEÇİLEN: '{secilen_hobi}' (Tür: {df.iloc[idx]['type']})")
    print("-" * 50)
    
    sayac = 0
    # Listeyi tara ve benzerleri getir
    for i, puan in sirali_puanlar[1:]:
        onerilen = df.iloc[i]
        # BÜTÇE VE KATILIMCI KONTROLÜ (Senin verine uygun filtre)
        if onerilen['price'] <= max_butce:
            print(f"Öneri {sayac+1}: {onerilen['activity']}")
            print(f"   [Tür: {onerilen['type']} | Fiyat: {onerilen['price']} | Katılımcı: {onerilen['participants']}]")
            print("-" * 50)
            sayac += 1
        
        if sayac == 3: break # En iyi 3 sonucu göster

# 4. DOSYADAN RASTGELE BİR HOBİ ÇEKİP TEST EDELİM
rastgele_secim = random.choice(df['activity'].tolist())
onerileri_goster(rastgele_secim, max_butce=0.5)