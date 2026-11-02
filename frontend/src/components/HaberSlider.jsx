import { useEffect, useRef, useState } from "react"
import { Link } from "react-router-dom"

// Hero'nun sag tarafindaki haber slaytI: one cikan yazilari sirayla gosterir.
// Kendi kendine doner; fareyle uzerine gelince ya da sekme arka plandayken durur.
const SURE = 5000

function HaberSlider({ posts }) {
  const [i, setI] = useState(0)
  const [durdu, setDurdu] = useState(false)
  const kapsayici = useRef(null)

  const liste = posts.slice(0, 5)
  const adet = liste.length

  useEffect(() => {
    if (adet <= 1 || durdu) return
    const t = setInterval(() => setI((x) => (x + 1) % adet), SURE)
    return () => clearInterval(t)
  }, [adet, durdu])

  if (adet === 0) return null
  // Liste kisalirsa gecersiz indekste kalmayalim: indeksi render sirasinda
  // kirpiyoruz, effect icinde setState etmeye gerek yok.
  const indeks = i % adet
  const aktif = liste[indeks]

  function git(yon) {
    setI((x) => (x + yon + adet) % adet)
  }

  // Sol/sag ok tuslariyla da gezilebilsin.
  function tus(e) {
    if (e.key === "ArrowRight") { e.preventDefault(); git(1) }
    if (e.key === "ArrowLeft") { e.preventDefault(); git(-1) }
  }

  return (
    <div
      className="slider"
      ref={kapsayici}
      onMouseEnter={() => setDurdu(true)}
      onMouseLeave={() => setDurdu(false)}
      onFocus={() => setDurdu(true)}
      onBlur={() => setDurdu(false)}
      onKeyDown={tus}
      tabIndex={0}
      role="group"
      aria-roledescription="slayt gösterisi"
      aria-label="Öne çıkan haberler"
    >
      <Link to={`/post/${aktif.slug}`} className="slider-kart">
        {aktif.gorsel && (
          <img src={aktif.gorsel.dosya} alt={aktif.gorsel.alt} />
        )}
        <div className="slider-icerik">
          <span className="chip">{aktif.category}</span>
          <h2>{aktif.title}</h2>
          <p>{aktif.excerpt}</p>
          <div className="slider-meta">
            <span>{aktif.author}</span>
            <span>·</span>
            <span className="mono">{aktif.date}</span>
          </div>
        </div>
      </Link>

      <div className="slider-kontrol">
        <button type="button" className="slider-ok" onClick={() => git(-1)} aria-label="Önceki haber">‹</button>
        <div className="slider-nokta">
          {liste.map((p, n) => (
            <button
              key={p.slug}
              type="button"
              className={n === indeks ? "aktif" : undefined}
              onClick={() => setI(n)}
              aria-label={`${n + 1}. haber`}
              aria-current={n === indeks ? "true" : undefined}
            />
          ))}
        </div>
        <button type="button" className="slider-ok" onClick={() => git(1)} aria-label="Sonraki haber">›</button>
      </div>
    </div>
  )
}

export default HaberSlider
