import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import IntroModal from '../components/IntroModal'

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
          {posts.map((post =>
            <Link key={post.slug}  to={`/post/${post.slug}`}  className="card">
              <div className={`thumb ${post.tone}`}>
                <span className="chip">{post.category}</span>
              </div>
              <div className="cbody">
                <h3>{post.title}</h3>   
                <p>{post.excerpt}</p>
                <div className="meta">
                  <span>{post.author}</span>
                  <span>·</span>
                  <span className="mono">{post.date}</span>
                  <span>·</span>
                  <span className="mono">{post.read_minutes} dk</span>
                </div>
              </div>
            </Link>
           ))}
        </div>
      </div>
    </>
  )
}

export default Home