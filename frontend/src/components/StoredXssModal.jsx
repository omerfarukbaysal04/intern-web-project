// Stored XSS farkindalik modali (tasarim). Kurban bir yorumdaki gizli kod
// calisinca gosterilir; saldirganin okudugu oturum cerezini ekranda gosterir.
// Not: csrf-* stillerini paylasiyor (ayni kirmizi ders-modali gorunumu).
function StoredXssModal({ cookie, kotuYorum, onClose }) {
  return (
    <>
      <div className="csrf-flash" />
      <div className="csrf-bg">
        <div className="csrf-card">
          <h2>⚠ Stored XSS saldırısına uğradın!</h2>

          <div className="aflow">
            <div className="step"><span className="ic">💬</span><span>Bir yorumu okursun</span></div>
            <span className="ok">→</span>
            <div className="step"><span className="ic">🧬</span><span>İçindeki gizli kod çalışır</span></div>
            <span className="ok">→</span>
            <div className="step"><span className="ic">🍪</span><span>Oturum çerezin çalınır</span></div>
          </div>
          <p>
            Bu haberdeki bir <b>yorum</b>, içine gizlenmiş kodu senin tarayıcında —
            bu sitenin adına — çalıştırdı. Sen sadece haberi okudun.
          </p>

          <h3>Saldırgan ne elde etti?</h3>
          <p>O kod az önce senin <b>oturum çerezini</b> okudu:</p>
          <p>
            <code style={{ wordBreak: "break-all" }}>
              {cookie || "(çerez bulunamadı)"}
            </code>
          </p>
          <p style={{ marginTop: "8px" }}>
            Bu çerezle saldırgan, parolanı hiç bilmeden <b>senin hesabına girebilir.</b>
          </p>

          <h3>Tuzak hangi yorumdaydı?</h3>
          <p>Masum görünen şu yorumun içine gizlenmişti:</p>
          <p>
            <code style={{ whiteSpace: "pre-wrap", wordBreak: "break-all" }}>
              {kotuYorum ? kotuYorum.metin : "(bulunamadı)"}
            </code>
          </p>
          <p style={{ marginTop: "6px" }}>
            Görünen kısım masumdu; sondaki gizli{" "}
            <code>&lt;img onerror=...&gt;</code> kodu arka planda çalıştı.
          </p>

          <h3>Neden bu kadar tehlikeli?</h3>
          <p>
            Reflected XSS'ten farklı olarak bu <b>kalıcı</b>: zararlı yorum sitede
            duruyor, o haberi açan <b>herkes</b> aynı şekilde vuruluyor.
          </p>

          <h3>Nasıl korunulur?</h3>
          <p>
            Kullanıcı içeriği ekrana basılmadan önce <b>temizlenmeli/escape
            edilmeli</b>; güvenli olmayan girdiyi ham HTML olarak basmak
            (<code>dangerouslySetInnerHTML</code>) için kullanmak çok tehlikelidir.
            Ayrıca oturum çerezleri <code>HttpOnly</code> olsaydı JavaScript onları
            hiç okuyamazdı. (Güvenli mod açıkken içerik escape ediliyor.)
          </p>

          <button onClick={onClose}>Anladım, kapat</button>
        </div>
      </div>
    </>
  )
}

export default StoredXssModal
