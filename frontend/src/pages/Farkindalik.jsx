import { Link } from "react-router-dom"

const ZAFIYETLER = [
  { ikon: "🔍", ad: "Reflected XSS", tur: "XSS", kurban: "Hazırlanmış bir arama linkine tıklarsın; tarayıcında saldırganın kodu çalışır.", korunma: "Siteler kullanıcı girdisini ekrana basmadan önce escape etmeli." },
  { ikon: "💬", ad: "Stored XSS", tur: "XSS", kurban: "Bir yorumu okursun; içine gizlenmiş kod oturum çerezini çalar.", korunma: "Kullanıcı içeriği gösterilmeden temizlenmeli/escape edilmeli." },
  { ikon: "🔗", ad: "DOM-based XSS", tur: "XSS", kurban: "Bir davet linkine tıklarsın; kod tamamen tarayıcında çalışır, sunucu hiç görmez.", korunma: "URL'den okunan veri innerHTML'e değil, güvenli yöntemle basılmalı." },
  { ikon: "🪤", ad: "Clickjacking", tur: "Arayüz tuzağı", kurban: "'Ödülü al' butonuna tıkladığını sanırsın; aslında görünmez bir butonla hesabını silersin.", korunma: "Sayfalar iframe'e girmekten men edilmeli (X-Frame-Options)." },
  { ikon: "🎭", ad: "CSRF", tur: "İstek sahteciliği", kurban: "Sadece bir haberi okursun; haberin olmadan hesabının e-postası değişir.", korunma: "İşlemler CSRF token ile doğrulanmalı; GET ile durum değiştirilmemeli." },
  { ikon: "↪️", ad: "Open Redirect", tur: "Phishing", kurban: "Güvenilir görünen bir linke tıklarsın; sahte bir siteye yönlendirilirsin.", korunma: "Yönlendirme hedefi doğrulanmalı (yalnızca site-içi adresler)." },
  { ikon: "🗂️", ad: "Reverse Tabnabbing", tur: "Phishing", kurban: "Yeni sekmede bir şey açarsın; arkadaki sekmen sessizce sahte girişe dönüşür.", korunma: "Dış bağlantılara rel=\"noopener\" eklenmeli." },
  { ikon: "📢", ad: "Malvertising", tur: "Sosyal mühendislik", kurban: "İçerik sandığın bir 'reklama' tıklarsın; sahte ödeme sayfasında kartın çalınır.", korunma: "Reklamlar açıkça etiketlenmeli ve kaynakları denetlenmeli." },
]

function Farkindalik() {
  return (
    <div className="wrap">
      <section className="fk-hero">
        <div className="kicker">Güvenlik Farkındalığı</div>
        <h1>Sıradan bir gün, sıradan bir site... ve bir tıklama.</h1>
        <p>
          Teknopanorama, güvenli bir deneme ortamıdır. Burada gerçek web saldırılarına
          <b> zararsızca </b> maruz kalır, "az önce ne oldu ve nasıl korunurum" diye
          anında öğrenirsin. Çünkü çoğu saldırıya düşmek için teknik bilgiye değil,
          yalnızca bir linke tıklamaya ya da bir sayfayı açmaya gerek var.
        </p>
      </section>

      <div className="sec-label"><span>Kurban Olabileceğin 8 Saldırı</span><div className="line"></div></div>

      <div className="fk-grid">
        {ZAFIYETLER.map((z) => (
          <div className="fk-card" key={z.ad}>
            <div className="fk-top">
              <span className="fk-ikon">{z.ikon}</span>
              <div>
                <h3>{z.ad}</h3>
                <span className="fk-tur">{z.tur}</span>
              </div>
            </div>
            <p className="fk-kurban"><b>Nasıl kurban olursun:</b> {z.kurban}</p>
            <p className="fk-korunma"><b>Nasıl korunursun:</b> {z.korunma}</p>
          </div>
        ))}
      </div>

      <p className="fk-not">
        Tüm saldırılar bu sitede <b>izole ve zararsızdır</b>; yalnızca farkındalık amaçlıdır.
        Sitede gezinmeye <Link to="/">buradan başlayabilirsin</Link>.
      </p>
    </div>
  )
}

export default Farkindalik
