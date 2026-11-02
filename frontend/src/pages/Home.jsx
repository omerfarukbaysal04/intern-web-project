import { useState, useEffect } from 'react'
import IntroModal from '../components/IntroModal'
import HaberKarti from '../components/HaberKarti'

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

  return (
    <>
      {intro && <IntroModal onClose={introKapat} />}

      <section className="hero">
        <div className="wrap">
          <div className="kicker">Teknoloji · Enerji · Güvenlik</div>
          <h1>Günün gelişmelerini sade bir dille okuyun.</h1>
          <p>Teknopanorama; yapay zeka, enerji ve siber güvenlik gündemini takip eden bağımsız bir haber köşesi.</p>
        </div>
      </section>

      <div className="wrap">
        <div className="sec-label"><span>Son Yazılar</span><div className="line"></div></div>

        <div className="card-grid">
          {posts.map((post) => <HaberKarti key={post.slug} post={post} />)}
        </div>
      </div>
    </>
  )
}

export default Home