// Farkindalik modali (tasarim). Kurban CSRF'e ugrayinca gosterilir:
// kirmizi flas + "ne oldu / nasil korunursun".
function CsrfModal({ onClose }) {
  return (
    <>
      <div className="csrf-flash" />
      <div className="csrf-bg">
        <div className="csrf-card">
          <h2>⚠ Az önce CSRF saldırısına uğradın!</h2>
          <p>
            Sadece bu haberi okudun — ama hesabının e-postası, senin haberin
            olmadan <b>saldırganınkiyle değiştirildi.</b>
          </p>

          <h3>Ne oldu?</h3>
          <p>
            Yorumlardan birindeki "görsel" aslında görsel değildi; adresi gizlice
            bir <b>işlem komutuydu</b> (<code>/hesap/email-degistir?email=...</code>).
            Tarayıcın o "görseli" yüklerken giriş çerezini otomatik ekledi, site de
            isteği "sen yaptın" sandı.
          </p>

          <h3>Nasıl korunulur?</h3>
          <p>
            Siteler durum değiştiren işlemleri basit bir <code>GET</code> ile
            yaptırmamalı ve her işlemde saldırganın bilemeyeceği bir{" "}
            <b>CSRF token</b> istemeli. Bu sitede "güvenli mod" açıkken tam da bu
            devrededir.
          </p>

          <h3>Sen ne yapabilirsin?</h3>
          <p>
            Önemli hesaplarında işin bitince <b>çıkış yap</b>; bir sitede
            girişliyken tanımadığın içeriklere dikkat et.
          </p>

          <button onClick={onClose}>Anladım, kapat</button>
        </div>
      </div>
    </>
  )
}

export default CsrfModal
