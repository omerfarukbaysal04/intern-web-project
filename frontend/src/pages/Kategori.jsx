import { useEffect, useState } from "react"
import { Link, useParams } from "react-router-dom"
import HaberKarti from "../components/HaberKarti"

// Tek bir kategorinin yazilarini listeler: /kategori/<slug>
function Kategori() {
  const { slug } = useParams()
  const [veri, setVeri] = useState(null)

  // Gelen cevap hangi kategoriye aitse onu sakliyoruz; boylece kategori
  // degistirildiginde eski liste yanlislikla yeni basligin altinda gorunmuyor
  // ve gec donen bir istek yeni secimi ezmiyor.
  useEffect(() => {
    let iptal = false
    fetch(`/api/kategori/${slug}`)
      .then((res) => (res.ok ? res.json() : Promise.reject()))
      .then((data) => { if (!iptal) setVeri(data) })
      .catch(() => { if (!iptal) setVeri({ slug, hata: true }) })
    return () => { iptal = true }
  }, [slug])

  const hazir = veri && veri.slug === slug

  if (hazir && veri.hata) {
    return (
      <div className="wrap">
        <p className="state error">Böyle bir kategori yok.</p>
        <Link to="/" className="back">← Ana sayfa</Link>
      </div>
    )
  }
  if (!hazir) return <div className="wrap"><p className="state">Yükleniyor...</p></div>

  return (
    <div className="wrap">
      <section className="kat-hero">
        <div className="kicker">Kategori</div>
        <h1>{veri.ad}</h1>
        <p>{veri.items.length} yazı</p>
      </section>

      <div className="card-grid">
        {veri.items.map((post) => <HaberKarti key={post.slug} post={post} />)}
      </div>
    </div>
  )
}

export default Kategori
