import { Link } from "react-router-dom"

// Ana sayfa ilk acilista gosterilen ozet karsilama penceresi.
function IntroModal({ onClose }) {
  return (
    <div className="intro-bg" onClick={onClose}>
      <div className="intro-card" onClick={(e) => e.stopPropagation()}>
        <button className="intro-close" onClick={onClose} aria-label="Kapat">×</button>
        <div className="intro-ikon">🛡️</div>
        <h2>Teknopanorama'ya hoş geldin</h2>
        <p>
          Burası sıradan bir haber sitesi gibi görünüyor — ama aynı zamanda bir{" "}
          <b>güvenlik farkındalık demosu.</b> Sitede gezinirken gerçek web
          saldırılarına <b>zararsızca</b> maruz kalabilir, her birinde "az önce ne
          oldu ve nasıl korunurum" diye anında öğrenirsin.
        </p>
        <p className="intro-alt">
          Çoğu saldırıya düşmek için teknik bilgiye değil, yalnızca bir linke
          tıklamaya ya da bir sayfayı açmaya gerek var.
        </p>
        <div className="intro-btns">
          <button className="intro-devam" onClick={onClose}>Anladım, keşfetmeye başla</button>
          <Link className="intro-detay" to="/farkindalik" onClick={onClose}>
            Kurban olabileceğin 8 saldırıyı gör →
          </Link>
        </div>
      </div>
    </div>
  )
}

export default IntroModal
