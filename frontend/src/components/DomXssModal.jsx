// DOM-based XSS farkindalik modali (tasarim). csrf-* stillerini paylasir.
function DomXssModal({ cookie, onClose }) {
  return (
    <>
      <div className="csrf-flash" />
      <div className="csrf-bg">
        <div className="csrf-card">
          <h2>⚠ DOM-based XSS saldırısına uğradın!</h2>
          <p>
            Tıkladığın "davet" linkinin içine gizlenmiş kod, senin tarayıcında —
            bu sitenin adına — çalıştı.
          </p>

          <h3>Reflected / Stored XSS'ten farkı ne?</h3>
          <p>
            Payload, linkin <code>#</code> (hash) kısmındaydı ve <b>sunucuya hiç
            gönderilmedi</b> — tamamen tarayıcıdaki JavaScript işledi. Sunucu
            logları bu saldırıyı hiç görmez; o yüzden tespiti de daha zordur.
          </p>

          <h3>Saldırgan ne elde etti?</h3>
          <p>Diğer XSS'lerde olduğu gibi oturum çerezini okuyabildi:</p>
          <p>
            <code style={{ wordBreak: "break-all" }}>
              {cookie || "(çerez bulunamadı)"}
            </code>
          </p>

          <h3>Nasıl korunulur?</h3>
          <p>
            URL'den (hash, query vb.) okunan veri <b>asla</b> doğrudan sayfaya
            yazılmamalı; <code>innerHTML</code>/<code>dangerouslySetInnerHTML</code>
            yerine güvenli yöntemler (React'te <code>{"{değer}"}</code>, ya da
            <code>textContent</code>) kullanılmalı. (Güvenli mod açıkken içerik
            escape edilerek basılıyor.)
          </p>

          <button onClick={onClose}>Anladım, kapat</button>
        </div>
      </div>
    </>
  )
}

export default DomXssModal
