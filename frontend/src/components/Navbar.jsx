import { Link } from 'react-router-dom'

function getOturum(){
  const m= document.cookie.match(/(?:^|;\s*)oturum=([^;]+)/)
  return m ? decodeURIComponent(m[1]):null  
}


function Navbar() {
  const oturum =getOturum()
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
            <Link to="/farkindalik" className="nav-fk">🛡 Farkındalık</Link>
          </div>

          <form className="nav-search" method="get" action="/search">
            <span className="ic">⌕</span>
            <input type="text" name="q" placeholder="Haberlerde ara..." />
          </form>
          <div className="nav-auth">
            {oturum ? (
              <>
                <span className="hi">Merhaba, {oturum}</span>
                <a href="/hesap">Hesabım</a>
                <a href="/cikis">Çıkış</a>
              </>
            ) : (
              <a href="/giris">Giriş Yap</a>
            )}
          </div>
        </nav>
      </div>
    </header>
  )
}

export default Navbar
