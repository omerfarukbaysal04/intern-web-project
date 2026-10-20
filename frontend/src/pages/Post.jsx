import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Link } from 'react-router-dom'
import CsrfModal from "../components/CsrfModal"
import StoredXssModal from "../components/StoredXssModal"


function Post(){

    const {slug}=useParams()
    const [post,setPost]=useState(null)
    const [yorumlar, setYorumlar]=useState([])
    const [metin, setMetin]=useState("")
    const [resim, setResim]=useState("")
    const [csrf, setCsrf] = useState(false)
    const [xss, setXss] = useState(false)
    const [calinanCerez, setCalinanCerez] = useState("")

      useEffect(() => {
        const t = setTimeout(() => {
          fetch("/api/csrf-uyari")
            .then(res => res.json())
            .then(data => { if (data.uyari) setCsrf(true) })
        }, 1500)
        return () => clearTimeout(t)
      }, [slug])

      useEffect(()=>{
        window.xssYakala = (cerez) => {
          setCalinanCerez(cerez)
          setTimeout(()=> setXss(true),2500)
        }
        return () => {delete window.xssYakala}
      },[])

          function loadYorumlar(){
        fetch(`/api/yorumlar/${slug}`)
        .then(res=>res.json())
        .then(data=>setYorumlar(data.items))
      }

      useEffect(()=>{loadYorumlar()},[slug])

      function yorumGonder(e){
        e.preventDefault()
        fetch(`/api/yorum`, {
          method: "POST",
          body: new URLSearchParams({slug,metin,resim})    
        }).then(()=>{
          setMetin("")
          setResim("")
          loadYorumlar()
        })
      }

    useEffect(()=> {
        fetch(`/api/posts/${slug}`)
        .then(res=> res.ok ? res.json() :Promise.reject() )
        .then(data=>setPost(data))
        .catch(()=>setPost("notFound"))
    },[slug])

     if (post === "notfound") return <div className="wrap"><p className="state error">Yazı bulunamadı.</p></div>
  if (!post) return <div className="wrap"><p className="state">Yükleniyor...</p></div>

  return (
    <article className="article">
      <Link to="/" className="back">← Ana sayfa</Link>
      <h1>{post.title}</h1>
      <div className="byline">
        <span className="chip">{post.category}</span>
        <span>{post.author}</span>
        <span>·</span>
        <span className="mono">{post.date}</span>
        <span>·</span>
        <span className="mono">{post.read_minutes} dk</span>
      </div>
      <div className="content">
        {post.body.map((p, i) => <p key={i}>{p}</p>)}
      </div>
          <section className="comments">
      <h2>Yorumlar ({yorumlar.length})</h2>

      {yorumlar.map((c, i) => (
        <div key={i} className="comment">
          <div className="comment-head">{c.yazar}</div>
          <p dangerouslySetInnerHTML={{__html: c.metin}}></p>
          {c.resim && <img className="comment-img" src={c.resim} alt="" />}
        </div>
      ))}

      <form className="comment-form" onSubmit={yorumGonder}>
        <textarea placeholder="Yorumunuz..." value={metin} onChange={e => setMetin(e.target.value)} required />
        <input placeholder="Resim URL (opsiyonel)" value={resim} onChange={e => setResim(e.target.value)} />
        <button type="submit">Gönder</button>
      </form>
    </section>
    {csrf && <CsrfModal onClose={() => setCsrf(false)} />}
    {xss && (
      <StoredXssModal
        cookie={calinanCerez}
        kotuYorum={yorumlar.find(c => /<img|onerror|<script|<svg/i.test(c.metin))}
        onClose={() => setXss(false)}
      />
    )}
    </article>
    
  )
}

export default Post