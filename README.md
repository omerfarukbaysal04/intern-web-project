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

### Demo gezinti sırası

1. `omerfaruk / 1234` ile giriş yap.
2. Ana sayfadaki haberleri sırayla aç — her birinde ekili bir tuzak var.
3. Arama kutusuna bir XSS payload'ı yaz (örn. `<script>caught()</script>`).
4. 8 saniye sonra çıkan çekiliş reklamına tıkla (clickjacking).
5. Farkındalık sayfasından ilerlemene bak; kalanlar için oradaki ipucunu takip et.
6. `SAFE_MODE = True` yap ve aynı adımları tekrarla: hiçbiri çalışmayacak.

> İlerleme panosunu baştan anlatmak için Farkındalık sayfasındaki
> **"Panoyu sıfırla"** butonunu kullan.

## Dizin Yapısı

```
backend/app/
  main.py                   FastAPI uygulaması, tüm endpoint'ler
  config.py                 SAFE_MODE bayrağı
  sanitize.py               yorum HTML'i için beyaz-liste temizleyicisi (SAFE_MODE)
  data/                     posts.py, users.py, comments.py (bellekte veri + ekili tuzaklar)
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
frontend/src/
  ilerleme.js               saldırı listesi + ilerleme panosu (localStorage)
  pages/                    Home, Post, Davet, Farkindalik
  components/               Navbar, Footer, reklam/popup ve farkındalık modalları
  index.css                 tema (koyu yeşil)
```

## Not

Bu proje bir staj kapsamında, güvenlik farkındalığı oluşturmak amacıyla hazırlanmıştır.
Zafiyetler bilinçli olarak eklenmiştir; **üretim ortamında kullanılmamalıdır.**

Bilerek bırakılmış, "düzeltilmemesi gereken" noktalar: parolalar düz metin tutulur,
oturum çerezi imzasız ve `HttpOnly` değildir, yorumlar `dangerouslySetInnerHTML` ile
basılır. Bunlar demonun kendisidir — XSS ile çerez çalmayı gösterebilmek için gereklidir.
