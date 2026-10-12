import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

// Sunum bileseni. Arama kutusu artik calisiyor: yazip Enter'layinca
// /search?q=... sayfasina yonlendirir (useNavigate).
function Navbar() {
  const [q, setQ] = useState('')
  const navigate = useNavigate()

  function onSubmit(e) {
    e.preventDefault()                 // formun sayfayi yenilemesini engelle
    const term = q.trim()
    if (term) navigate(`/search?q=${encodeURIComponent(term)}`)
  }

  return (
    <header className="nav-bar">
      <div className="wrap">
        <nav className="nav-inner">
          <Link to="/" className="logo">
            <span className="mark" />
            Teknopanorama
          </Link>

          <div className="nav-links">
            <Link to="/" className="active">Gündem</Link>
            <Link to="/">Yapay Zeka</Link>
            <Link to="/">Güvenlik</Link>
            <Link to="/">Enerji</Link>
          </div>

          <form className="nav-search" onSubmit={onSubmit}>
            <span className="ic">⌕</span>
            <input
              type="text"
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="Haberlerde ara..."
            />
          </form>
        </nav>
      </div>
    </header>
  )
}

export default Navbar
