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

| # | Saldırı | Kurban nasıl düşer |
|---|---------|--------------------|
| 1 | **Reflected XSS** | Hazırlanmış bir arama linkine tıklar; kod tarayıcıda çalışır |
| 2 | **Stored XSS** | Bir yorumu okur; içindeki gizli kod çerezini çalar |
| 3 | **DOM-based XSS** | Bir davet linkine tıklar; kod tamamen tarayıcıda çalışır (sunucu görmez) |
| 4 | **Clickjacking** | "Ödül" butonuna tıkladığını sanır; görünmez iframe'le hesabını siler |
| 5 | **CSRF** | Sadece bir haberi okur; haberi olmadan e-postası değişir |
| 6 | **Open Redirect** | Güvenilir görünen bir linke tıklar; sahte siteye yönlendirilir |
| 7 | **Reverse Tabnabbing** | Yeni sekmede bir şey açar; eski sekmesi sahte girişe dönüşür |
| 8 | **Malvertising** | İçerik sandığı bir "reklama" tıklar; sahte ödemede kartı çalınır |

Her saldırının **savunulmuş hali** de vardır: `backend/app/config.py` içindeki
`SAFE_MODE` bayrağı `True` yapıldığında ilgili savunma devreye girer
(çıktı escape'i, `X-Frame-Options`, CSRF token, yönlendirme doğrulaması vb.) ve saldırı çöker.
Böylece aynı giriş için **yamasız / yamalı** hali yan yana gösterilebilir.

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

### Demo hesabı
`omerfaruk / 1234` (diğerleri: `deniz / deniz123`, `selin / selin123`)

### Savunmayı açmak/kapatmak
`backend/app/config.py` → `SAFE_MODE = True` / `False` (kaydedince otomatik yeniden yüklenir).

## Dizin Yapısı

```
backend/app/
  main.py            FastAPI uygulaması, tüm endpoint'ler
  config.py          SAFE_MODE bayrağı
  data/              posts.py, users.py, comments.py (bellekte veri)
  templates/         sunucu-render'lı sayfalar + farkındalık ekranları (Jinja2)
frontend/src/
  pages/             Home, Post, Davet, Farkindalik
  components/        Navbar, Footer, reklam/popup ve farkındalık modalları
  index.css          tema (koyu yeşil)
```

## Not

Bu proje bir staj kapsamında, güvenlik farkındalığı oluşturmak amacıyla hazırlanmıştır.
Zafiyetler bilinçli olarak eklenmiştir; **üretim ortamında kullanılmamalıdır.**
