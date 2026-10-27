import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
import DomXssModal from "../components/DomXssModal"

function Davet() {
  const [safe, setSafe] = useState(null)
  const [dom, setDom] = useState(false)

  // Davet edenin adi URL'nin hash (#) kismindan gelir.
  // DIKKAT: hash sunucuya GONDERILMEZ -> bu DOM-based XSS'in kaynagi.
  let davetEden = ""
  try {
    davetEden = decodeURIComponent(window.location.hash.slice(1))
  } catch {
    davetEden = window.location.hash.slice(1)
  }

  // Enjekte edilen kodun cagiracagi global tetikleyici (modali acar).
  useEffect(() => {
    window.xssDom = () => setDom(true)
    return () => { delete window.xssDom }
  }, [])

  // Savunma client tarafinda oldugu icin React SAFE_MODE'u sunucudan ogreniyor.
  useEffect(() => {
    fetch("/api/safe-mode")
      .then((r) => r.json())
      .then((d) => setSafe(d.safe_mode))
  }, [])

  if (safe === null) return <div className="wrap"><p className="state">Yükleniyor...</p></div>

  const isim = davetEden || "Bir arkadaşın"
  const mesaj = `🎉 <b>${isim}</b> seni Teknopanorama'ya davet etti!`

  return (
    <div className="wrap" style={{ maxWidth: 640, margin: "56px auto" }}>
      {safe ? (
        // GUVENLI: React {} ile basar -> escape edilir, kod calismaz
        <h1 style={{ fontSize: "26px", fontWeight: 700 }}>
          🎉 {isim} seni Teknopanorama'ya davet etti!
        </h1>
      ) : (
        // ZAFIYETLI: ham HTML olarak basar -> hash'teki kod calisir (DOM XSS)
        <h1
          style={{ fontSize: "26px", fontWeight: 700 }}
          dangerouslySetInnerHTML={{ __html: mesaj }}
        />
      )}

      <p className="state">Katılmak için kaydol ve günlük haberleri takip etmeye başla.</p>
      <Link to="/" className="back">← Ana sayfa</Link>

      {dom && <DomXssModal cookie={document.cookie} onClose={() => setDom(false)} />}
    </div>
  )
}

export default Davet
