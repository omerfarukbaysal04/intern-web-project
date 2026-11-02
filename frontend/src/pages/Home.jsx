import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import IntroModal from '../components/IntroModal'
import HaberKarti from '../components/HaberKarti'
import HaberSlider from '../components/HaberSlider'

// Navbar ile ayni kategori listesi (posts.py -> KATEGORILER).
const KATEGORILER = [
  { slug: 'yapay-zeka', ad: 'Yapay Zeka', ikon: '🤖' },
  { slug: 'guvenlik', ad: 'Güvenlik', ikon: '🛡' },
  { slug: 'enerji', ad: 'Enerji', ikon: '⚡' },
]

function Home(){
    const [posts, setPosts] = useState([])
    const [intro, setIntro] = useState(false)

    useEffect(() => {
        fetch("/api/posts")
        .then(res => res.json())
        .then(data => setPosts(data.items))
    }, [])

    // Ilk ziyarette karsilama penceresini goster (sonra hatirla).
    useEffect(() => {
        try { if (!localStorage.getItem("intro_goruldu")) setIntro(true) } catch {}
    }, [])

    function introKapat() {
        setIntro(false)
        try { localStorage.setItem("intro_goruldu", "1") } catch {}
    }

    // Kategori kartlarinda kac yazi oldugunu gosterebilmek icin.
    function sayi(slug) {
      return posts.filter((p) => p.kategori_slug === slug).length
    }

  return (
    <>
      {intro && <IntroModal onClose={introKapat} />}

      {/* Hero: solda tanitim, sagda one cikan haberler slaydi. Baska bir sey yok. */}
      <section className="hero">
        <div className="wrap">
          <div className="hero-grid">
            <div className="hero-metin">
              <div className="kicker">Teknoloji · Enerji · Güvenlik</div>
              <h1>Günün gelişmelerini sade bir dille okuyun.</h1>
              <p>Teknopanorama; yapay zeka, enerji ve siber güvenlik gündemini takip eden bağımsız bir haber köşesi.</p>
            </div>
            <HaberSlider posts={posts} />
          </div>
        </div>
      </section>

      <div className="wrap">
        {/* Bolum basligiyla ayni satirda kategori secenekleri: "Tumu" burada
            isaretli, digerleri kendi kategori sayfasina goturur. */}
        <div className="sec-label">
          <span>Son Yazılar</span>
          <div className="line"></div>
          <nav className="sec-kategori" aria-label="Kategoriler">
            <span className="aktif" aria-current="page">Tümü</span>
            {KATEGORILER.map((k) => (
              <Link key={k.slug} to={`/kategori/${k.slug}`} title={`${k.ad} — ${sayi(k.slug)} yazı`}>
                {k.ikon} {k.ad}
              </Link>
            ))}
          </nav>
        </div>

        <div className="card-grid">
          {posts.map((post) => <HaberKarti key={post.slug} post={post} />)}
        </div>
      </div>
    </>
  )
}

export default Home
