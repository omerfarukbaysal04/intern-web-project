import { useState, useEffect } from 'react'
import Navbar from './components/Navbar'
import Footer from './components/Footer'

function App() {
  const [posts, setPosts] = useState([])   // haberler burada; başta boş liste

  useEffect(() => {
    fetch("/api/posts")
    .then(res => res.json())
    .then(data => setPosts(data.items))
  }, [])

  return (
    <>
      <Navbar />

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
            <a key={post.slug} href={`/post/${post.slug}`} className="card">
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
            </a>
           ))}
        </div>
      </div>

      <Footer />
    </>
  )
}

export default App