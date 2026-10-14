import { Link } from 'react-router-dom'

// Arama kutusu klasik bir GET formu: Enter'layinca tarayici /search?q=...
// adresine tam sayfa gider. Bu adres Vite proxy ile backend'e (sunucu-render'li
// arama sayfasi) yonlendirilir. Siradan bir sitede aramanin calismasi aynen boyledir.
function Navbar() {
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

          <form className="nav-search" method="get" action="/search">
            <span className="ic">⌕</span>
            <input type="text" name="q" placeholder="Haberlerde ara..." />
          </form>
        </nav>
      </div>
    </header>
  )
}

export default Navbar
