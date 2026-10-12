import { useState, useEffect } from 'react'
import { useSearchParams, Link } from 'react-router-dom'

function Search() {
  const [params] = useSearchParams()      
  const q = params.get('q') || ''
  const [results, setResults] = useState([])

  useEffect(() => {
    fetch(`/api/search?q=${encodeURIComponent(q)}`)
    .then(res=>res.json())
    .then(data=>setResults(data.items))
  }, [q])

  return (
    <div className="wrap">
      <div className="sec-label" style={{ marginTop: '32px' }}>
        <span>"{q}" için sonuçlar</span>
        <div className="line"></div>
      </div>

      {results.length === 0 && <p className="state">Sonuç bulunamadı.</p>}

      <div className="card-grid">
        {results.map((post =>
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
  )
}

export default Search