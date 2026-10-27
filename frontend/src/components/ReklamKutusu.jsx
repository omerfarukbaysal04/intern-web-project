import { useState, useEffect } from "react"

// Reklamlar. "kotu" olan, native icerik gibi gorunup sahte odeme sayfasina goturur.
const REKLAMLAR = [
  { emoji: "📱", baslik: "2026'nın en iyi 10 akıllı telefonu", alt: "Teknoloji editörlerimizden seçki", href: "#", kotu: false },
  { emoji: "⚡", baslik: "İnternet hızını 2 katına çıkaran 5 ayar", alt: "Çoğu kişi 3'üncüyü bilmiyor", href: "#", kotu: false },
  { emoji: "🎁", baslik: "Teknopanorama Premium — ilk ay ücretsiz!", alt: "Reklamsız oku, hemen etkinleştir", href: "/premium-odeme", kotu: true },
]

function ReklamKutusu() {
  const [safe, setSafe] = useState(null)
  const [i, setI] = useState(0)

  useEffect(() => {
    fetch("/api/safe-mode").then((r) => r.json()).then((d) => setSafe(d.safe_mode))
  }, [])

  // Guvenli modda kotu reklam elenir (site reklamlarini denetlemis gibi).
  const liste = safe ? REKLAMLAR.filter((r) => !r.kotu) : REKLAMLAR

  // Slaytlar birkac saniyede bir donuyor.
  useEffect(() => {
    if (liste.length <= 1) return
    const t = setInterval(() => setI((x) => (x + 1) % liste.length), 4000)
    return () => clearInterval(t)
  }, [liste.length])

  if (safe === null || liste.length === 0) return null
  const r = liste[i % liste.length]

  return (
    <div className="wrap">
      {/* Guvenli modda "Reklam" etiketi gorunur; zafiyetli modda hic etiket yok -> ayirt edilemez */}
      <a className={`reklam ${safe ? "reklam-labelli" : ""}`} href={r.href}>
        {safe && <span className="reklam-etiket">Reklam</span>}
        <span className="reklam-emoji">{r.emoji}</span>
        <span className="reklam-metin">
          <strong>{r.baslik}</strong>
          <span>{r.alt}</span>
        </span>
        <span className="reklam-ok">→</span>
      </a>
    </div>
  )
}

export default ReklamKutusu
