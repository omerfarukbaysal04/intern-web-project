# Teknopanorama — Güvenlik Farkındalık Demosu

Sıradan bir teknoloji-haber sitesi gibi görünen, aslında bir **güvenlik farkındalık aracı.**
Ziyaretçi siteyi normal kullanırken (haber okurken, arama yaparken, bir linke tıklarken)
gerçek web saldırılarına **zararsızca** maruz kalır; her saldırıdan hemen sonra
*"az önce ne oldu ve nasıl korunurum"* diye bir **farkındalık ekranı** gösterilir.

Proje **kurban odaklıdır**: amaç, teknik bilgisi olmayan normal bir kullanıcının bile
yalnızca gezinirken nasıl kurban olabileceğini göstermek ve öğretmek.

> ⚠️ Tüm zafiyetler **bilerek, izole ve zararsız** biçimde, yalnızca eğitim/farkındalık
> amacıyla eklenmiştir. Hiçbir gerçek veri çalınmaz veya dışarı gönderilmez.

## İçerdiği 8 Saldırı

| # | Saldırı | Kurban nasıl düşer | Tuzağın yeri |
|---|---------|--------------------|--------------|
| 1 | **Reflected XSS** | Hazırlanmış bir arama linkine tıklar; kod tarayıcıda çalışır | `/search?q=...` |
| 2 | **Stored XSS** | Bir yorumu okur; içindeki gizli kod çerezini çalar | yorum metni |
| 3 | **DOM-based XSS** | Bir davet linkine tıklar; kod tamamen tarayıcıda çalışır (sunucu görmez) | yorumdaki `/davet#...` linki |
| 4 | **Clickjacking** | "Ödül" butonuna tıkladığını sanır; görünmez iframe'le hesabını siler | reklam → `/saldirgan` |
| 5 | **CSRF** | Sadece bir haberi okur; haberi olmadan e-postası değişir | yorumun "resim" alanı |
| 6 | **Open Redirect** | Güvenilir görünen bir linke tıklar; sahte siteye yönlendirilir | yorumdaki `/git?url=...` linki |
| 7 | **Reverse Tabnabbing** | Yeni sekmede bir şey açar; eski sekmesi sahte girişe dönüşür | yorumdaki `target="_blank"` linki |
| 8 | **Malvertising** | İçerik sandığı bir "reklama" tıklar; sahte ödemede kartı çalınır | etiketsiz reklam kutusu |

Tuzakların çoğu `backend/app/data/comments.py` içine **önceden ekilmiş yorumlar**
olarak duruyor; yani saldırılar kullanıcı hiçbir şey yazmadan, sadece haberi okurken
kendiliğinden tetikleniyor.

## İçerik ve Kategoriler

Site dokuz haber taşıyor; **Yapay Zeka**, **Güvenlik** ve **Enerji** kategorilerinin
her birinde üçer yazı var. Navbar'daki kategori bağlantıları artık çalışıyor ve
`/kategori/<slug>` adresine gidiyor; bulunulan kategori menüde işaretli kalıyor.

İçerik uydurma değil: yazılar Ekim–Kasım 2026 tarihli **gerçek haberlerden**
derlendi. Metinler kopyalanmadı, kendi cümlelerimizle özetlendi ve her yazının
altında alındığı yayın kaynak bağlantısıyla birlikte duruyor
(`posts.py` → `kaynak` alanı). Kaynaklar arasında FBI'ın siber uyarısı, Wood
Mackenzie'nin maliyet analizi, The Hacker News, Macworld, DonanımHaber ve EPDK
düzenlemesini aktaran haberler var. Bir haber sitesi kılığındaki demonun
inandırıcı olması, içeriğinin de gerçek olmasına bağlı.

Her yazının bir **kapak görseli** var (`posts.py` → `gorsel`). Görseller
Wikimedia Commons'tan alındı; hepsi **kamu malı ya da CC0** olduğu için atıf
zorunlu değil, yine de her haberin altında künyesi yazılı. Dosyalar
`frontend/public/haber/` içinde yerel duruyor — dışarıya bağlantı yok, site
internetsiz de aynı görünüyor. Görseli olmayan bir yazı eklenirse kart, eski
davranışa düşüp kategori rengini gösterir.

Kart kapak renkleri (`tone`) kategoriye göre sabit: görselin yüklenemediği
durumda bile aynı kategorinin yazıları birbirini tutuyor.

**Tuzaklar konularıyla eşleşiyor.** Kripto hırsızlığı haberinin altında sahte bir
"güvenlik rehberi" bağlantısı (open redirect), hesap güvenliği haberinde hesap
ayarıyla oynayan bir "görsel" (CSRF), performans haberinde "hız testi" bağlantısı
(tabnabbing) duruyor. Gerçek kimlik avı da böyle çalışır: bağlam ne kadar doğalsa
tuzak o kadar görünmez olur.

## İlerleme Panosu

Ziyaretçi saldırılara rastgele sırayla düştüğü için hangilerini gördüğünü takip
edemiyordu. Artık her farkındalık ekranı o saldırıyı "düştün" diye işaretliyor;
Farkındalık sayfası **"8'de 3"** diye ilerleme gösteriyor, navbar'da canlı bir sayaç
duruyor ve kalan saldırılardan biri için ipucu veriliyor. Böylece demo, dağınık bir
tuzak koleksiyonu olmaktan çıkıp tamamlanabilir bir deneyime dönüşüyor.

Kartların içeriği hiçbir zaman kilitlenmez — bir farkındalık aracında korunma
bilgisini saklamak ters teper. Düşülen saldırılar kırmızı kenarlık ve "✓ düştün"
rozetiyle öne çıkar, kalanlar soluk durur.

Nasıl çalışıyor:

- Tek kaynak [`frontend/src/ilerleme.js`](frontend/src/ilerleme.js): sekiz saldırının
  listesi, `localStorage` okuma/yazma ve canlı takip için `kullanIlerleme()` hook'u.
- React modalleri (stored XSS, DOM XSS, CSRF) açıldıkları an `isaretle(id)` çağırır.
- Sunucu-render'lı ders sayfaları aynı anahtara, ortak
  [`templates/_ilerleme.html`](backend/app/templates/_ilerleme.html) parçasıyla yazar
  (`{% with saldiri_id = "..." %}{% include %}`). Vite backend'i de `:5173`'e
  proxy'lediği için iki taraf **aynı origin'de**, dolayısıyla aynı depolamayı paylaşır.
- Tek istisna open redirect: kurban oraya bilerek **başka bir origin'de**
  (`127.0.0.1:8000`) düşer, yani farklı bir `localStorage`. İşaret o sayfadaki "gerçek
  siteye dön" linkine `?gorulen=open-redirect` olarak eklenir; React (`App.jsx` →
  `DonusIsareti`) işaretleyip adresi temizler.

İlerleme **yalnızca ziyaretçinin tarayıcısında** tutulur, sunucuya hiç gitmez. Gizli
pencerede veya depolama kapalıyken site normal çalışır, sadece hatırlamaz — bütün
okuma/yazmalar `try/catch` içinde.

## Güvenli Mod (SAFE_MODE)

`backend/app/config.py` içindeki `SAFE_MODE` bayrağı `True` yapıldığında her saldırının
**kendi savunması** devreye girer ve saldırı çöker. Böylece aynı giriş için
**yamasız / yamalı** hali yan yana gösterilebilir.

| Saldırı | SAFE_MODE açıkken devreye giren savunma | Nerede |
|---------|------------------------------------------|--------|
| Reflected XSS | Girdi ekrana basılmadan `html.escape()` ile kaçışlanır | `main.py` → `/search` |
| Stored XSS | Yorumlar **beyaz-liste** ile temizlenir (`<img>`, `<script>`, `on*` düşer) | `sanitize.py` |
| DOM-based XSS | URL hash'i `innerHTML` yerine React'in `{}` ifadesiyle basılır | `pages/Davet.jsx` |
| Clickjacking | `X-Frame-Options: DENY` + `Content-Security-Policy: frame-ancestors 'none'` | `main.py` → `/hesap` |
| CSRF | (1) GET ile durum değişimi reddedilir, (2) formlar **CSRF token** ister | `main.py` |
| Open Redirect | Yönlendirme hedefi doğrulanır; yalnızca site-içi adresler kabul edilir | `main.py` → `/git` |
| Reverse Tabnabbing | `target="_blank"` linklere `rel="noopener noreferrer"` zorla eklenir | `sanitize.py` |
| Malvertising | Reklamlar "Reklam" etiketiyle gösterilir, tuzak reklam hiç basılmaz | `components/ReklamKutusu.jsx` |

### Neden escape değil, temizleme (sanitize)?

İlk sürümde güvenli mod yorumları baştan sona `html.escape()` ediyordu. Bu stored XSS'i
durduruyordu, ama yan etkisi vardı: yorumdaki **tüm** HTML ölüyordu — open redirect,
reverse tabnabbing ve DOM XSS tuzaklarının taşıyıcısı olan `<a>` linkleri de dahil.
Yani o üç saldırının kendi savunması hiç çalışmıyor, saldırı sadece "linki
göstermeyerek" sönüyordu.

`backend/app/sanitize.py` bunun yerine gerçek sitelerin yaptığını yapıyor: zararsız bir
etiket kümesine (`<b>`, `<i>`, `<code>`, `<a href>`) izin verip tehlikeli olanı ayıklıyor
ve her yeni-sekme linkine `rel="noopener noreferrer"` ekliyor. Böylece güvenli modda
**her saldırı kendi savunmasıyla** çöküyor.

### Clickjacking demosunda origin notu

Gerçek bir clickjacking saldırısında tuzak sayfa **başka bir alan adında** durur. Bu
demoda saldırgan sayfası (`/saldirgan`) Teknopanorama ile **aynı origin'de** servis
ediliyor: oturum çerezi `SameSite=Lax` olduğu için tarayıcı onu farklı bir siteden
açılan iframe'e göndermez; göndermesi için `SameSite=None; Secure`, yani HTTPS gerekir.
Bu kısıt kendi başına bir ders — **modern çerez varsayılanları bu saldırıyı zaten
kısmen zorlaştırıyor.** Savunmanın gösterimi yine gerçek: `X-Frame-Options: DENY`
sayfayı aynı origin'deki iframe'lere bile kapatır.

## Teknoloji

- **Frontend:** React (Vite) — güvenli/modern gezinme kabuğu (ana sayfa, haber detayı, davet, farkındalık panosu)
- **Backend:** FastAPI + Jinja2 — zafiyetlerin ve savunmaların yaşadığı sunucu-render'lı sayfalar
- **Veri:** Bellekte Python sözlükleri (haberler, kullanıcılar, yorumlar) — veritabanı yok

React güvenli tarafı, sunucu-render'lı sayfalar ise zafiyet/savunma tarafını temsil eder.
Vite, `/api` ve backend sayfalarını `:8000`'e proxy'ler; tarayıcı için her şey tek origin'dendir.

## Çalıştırma

İki ayrı terminal gerekir.

**Backend** (port 8000):

```bash
cd backend
py -m venv .venv
.venv\Scripts\activate        # PowerShell: .venv\Scripts\Activate.ps1  |  bash: source .venv/Scripts/activate
pip install fastapi "uvicorn[standard]" jinja2 python-multipart
.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

**Frontend** (port 5173):

```bash
cd frontend
npm install
npm run dev
```

Tarayıcı: <http://localhost:5173>

> `backend/.venv/` sürüm kontrolüne dahil değildir; projeyi ilk kez açan herkesin
> yukarıdaki `py -m venv .venv` adımını kendi makinesinde çalıştırması gerekir.

### Demo hesabı

`omerfaruk / 1234` (diğerleri: `deniz / deniz123`, `selin / selin123`)

### Savunmayı açmak/kapatmak

`backend/app/config.py` → `SAFE_MODE = True` / `False` (kaydedince otomatik yeniden yüklenir).

## Sekiz Saldırı Nasıl Test Edilir

Aşağıdaki adımlar `SAFE_MODE = False` iken geçerlidir. Her saldırıdan sonra
farkındalık ekranı açılır ve sayaç bir artar; sırayla gidersen 8/8'e ulaşırsın.

**Önce:** `omerfaruk / 1234` ile giriş yap. Dört saldırı (Stored XSS, Clickjacking,
CSRF, Reverse Tabnabbing) giriş yapılmış bir oturum gerektirir.

### 1. Reflected XSS — arama kutusu

Üstteki arama kutusuna `<script>caught()</script>` yazıp Enter'a bas.
Sonuç sayfası açılır açılmaz kırmızı flaş ve *"Az önce hacklendin!"* ekranı gelir.
Girdin sunucu tarafından hiç temizlenmeden sayfaya basıldığı için çalıştı.
`2 < 3` gibi masum bir arama ekranı **açmaz**.

### 2. Stored XSS — *"Chainalysis, Yapay Zekâ Ajanlarıyla Yapılan Sızmayı Doğruladı"*

Haberi aç ve bekle. Yorumlardan biri masum görünür ama sonunda gizli bir
`<img onerror=...>` taşır; yaklaşık 2,5 saniye sonra modal açılır ve **senin
oturum çerezini** ekranda gösterir. Hiçbir şeye tıklamadın, sadece okudun.

### 3. DOM-based XSS — *"Açık Kaynak Dünya Modeli Tek Ekran Kartında Çalışıyor"*

Haberi aç, yorumlardaki **"davet linkin hazır 🎉"** bağlantısına tıkla.
`/davet` sayfasında modal açılır. Buradaki fark: zararlı kod linkin `#` kısmındaydı,
yani **sunucuya hiç gitmedi** — saldırı tamamen tarayıcıda oldu, sunucu logları görmez.

### 4. Clickjacking — çekiliş reklamı

Giriş yaptıktan sonra ~8 saniye bekle; sağ altta *"Bugünün şanslısı sizsiniz"*
kutusu çıkar. **"Hemen Katıl"**a, açılan sayfada da **"Ödülümü Al 🎁"**a tıkla.
Butonun üstünde görünmez bir iframe vardır: aslında kendi hesap sayfandaki
*"Hesabımı Sil"* butonuna basmış olursun ve hesabın silinir.

> Hesabın gerçekten silinir (veri bellekte tutulur). Geri getirmek için
> backend'i yeniden başlatman yeterli.

### 5. CSRF — *"Parolasız Döneme Geçiş: Passkey Varsayılan Oluyor"*

Giriş yapmışken haberi aç ve bekle. Yorumlardan birindeki "görsel" aslında görsel
değil, bir **işlem adresidir**; tarayıcın onu yüklerken giriş çerezini otomatik
ekler. ~1,5 saniye sonra modal açılır. Doğrulamak için **Hesabım** sayfasına git:
e-postan `saldirgan@evil.com` olmuştur.

### 6. Open Redirect — *"FBI: Binance'ten Çalınan 6 Milyar Dolar..."*

Haberi aç, yorumdaki **"teknopanorama.com/guvenlik-rehberi"** bağlantısına tıkla.
Link metni güvenilir görünür ama adresi `/git?url=...` üzerinden seni başka bir
siteye atar. Sahte giriş sayfasına düşersin — **adres çubuğuna bak**, artık
`127.0.0.1:8000` üzerindesin. "Gerçek siteye dön" bağlantısı seni geri getirir.

### 7. Reverse Tabnabbing — *"Apple, M6'lı iMac ile Cihaz Üstü Yapay Zekâda İddialı"*

Haberi aç, yorumdaki **"speedtest-pro.com"** bağlantısına tıkla; yeni sekmede bir
"hız testi" açılır. Beş saniye sonra ipucu çıkar. **Eski sekmene geri dön:**
Teknopanorama sekmesi sessizce *"Oturumunuz sona erdi, tekrar giriş yapın"*
ekranına dönüşmüştür. Yeni sekme, `window.opener` ile eski sekmeyi ele geçirdi.

### 8. Malvertising — sayfa içi reklam kutusu

Ana sayfada aşağı in; içerik kartlarının arasındaki kutu birkaç saniyede bir döner.
**"Teknopanorama Premium — ilk ay ücretsiz!"** öğesine tıkla. Sahte bir ödeme
sayfasına düşersin. Dikkat et: güvensiz modda o kutuda **"Reklam" etiketi yoktur**,
yani sitenin kendi içeriğinden ayırt edilemez.

### Savunmaları görmek

`backend/app/config.py` → `SAFE_MODE = True` yap (`--reload` ile çalışıyorsa
kendi kendine yeniden başlar) ve **tarayıcıda sayfayı yenile** — React güvenli mod
durumunu açılışta bir kez sorar. Sonra aynı sekiz adımı tekrarla:

| Adım | Güvenli modda ne olur |
|------|------------------------|
| 1 | Payload metin olarak görünür, çalışmaz |
| 2 | Yorumdaki `<img onerror>` temizlenir, modal hiç açılmaz |
| 3 | Davet linki durur ama isim escape edilerek basılır |
| 4 | `/hesap` iframe'e girmeyi reddeder, buton hiçbir şey yapmaz |
| 5 | GET ile e-posta değişmez; sahte form 403 + ders sayfası alır |
| 6 | `/git` dış adresi reddeder, seni ana sayfaya götürür |
| 7 | Linke `rel="noopener"` eklenir, eski sekme ele geçirilemez |
| 8 | Tuzak reklam hiç gösterilmez, kalanlar "Reklam" etiketi alır |

> İlerleme panosunu baştan anlatmak için Farkındalık sayfasındaki
> **"Panoyu sıfırla"** butonunu kullan.

## Dizin Yapısı

```
backend/app/
  main.py                   FastAPI uygulaması, tüm endpoint'ler
  config.py                 SAFE_MODE bayrağı
  sanitize.py               yorum HTML'i için beyaz-liste temizleyicisi (SAFE_MODE)
  data/                     posts.py (9 haber + kategoriler), users.py,
                            comments.py (yorumlar + ekili tuzaklar)
  templates/                sunucu-render'lı sayfalar + farkındalık ekranları (Jinja2)
    _ilerleme.html          ilerleme panosuna işaret bırakan ortak parça
    search.html             zafiyetli arama sayfası (reflected XSS)
    hesap.html, giris.html  oturum ve hesap yönetimi
    saldirgan.html          clickjacking tuzağı
    csrf_saldirgan.html     CSRF tuzağı
    tab_saldirgan.html      reverse tabnabbing tuzağı
    sahte_giris.html        open redirect kurbanının düştüğü sahte giriş
    tab_sahte_giris.html    tabnabbing sonrası ele geçirilmiş sekme
    sahte_odeme.html        malvertising sahte ödeme sayfası
    clickjack_ders.html     clickjacking farkındalık ekranı
    csrf_engellendi.html    CSRF token doğrulaması patladığında (SAFE_MODE)
frontend/public/
  haber/                    haber kapak görselleri (kamu malı / CC0)
frontend/src/
  ilerleme.js               saldırı listesi + ilerleme panosu (localStorage)
  pages/                    Home, Post, Kategori, Davet, Farkindalik
  components/               Navbar, Footer, HaberKarti, reklam/popup ve
                            farkındalık modalları
  index.css                 tema (koyu yeşil)
```

## Not

Bu proje bir staj kapsamında, güvenlik farkındalığı oluşturmak amacıyla hazırlanmıştır.
Zafiyetler bilinçli olarak eklenmiştir; **üretim ortamında kullanılmamalıdır.**

Bilerek bırakılmış, "düzeltilmemesi gereken" noktalar: parolalar düz metin tutulur,
oturum çerezi imzasız ve `HttpOnly` değildir, yorumlar `dangerouslySetInnerHTML` ile
basılır. Bunlar demonun kendisidir — XSS ile çerez çalmayı gösterebilmek için gereklidir.
