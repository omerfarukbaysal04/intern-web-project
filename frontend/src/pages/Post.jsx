import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Link } from 'react-router-dom'


function Post(){

    const {slug}=useParams()
    const [post,setPost]=useState(null)

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
    </article>
  )
}

export default Post