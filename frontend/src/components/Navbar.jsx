import { Link, NavLink, useLocation } from 'react-router-dom'
import { TOPLAM, useIlerleme } from '../ilerleme'

// Menudeki kategoriler. posts.py'deki KATEGORILER ile ayni slug'lari kullanir.
const KATEGORILER = [
  { slug: 'yapay-zeka', ad: 'Yapay Zeka' },
  { slug: 'guvenlik', ad: 'Güvenlik' },
  { slug: 'enerji', ad: 'Enerji' },
]

function getOturum(){
  const m= document.cookie.match(/(?:^|;\s*)oturum=([^;]+)/)
  return m ? decodeURIComponent(m[1]):null
}


function Navbar() {
  const oturum =getOturum()
  const gorulen = useIlerleme()
  const konum = useLocation()
  // "Gundem" yalnizca ana sayfadayken isaretli olsun (NavLink'in "end"i gibi).
  const anaSayfada = konum.pathname === '/'
  return (
    <header className="nav-bar">
      <div className="wrap">
        <nav className="nav-inner">
          <Link to="/" className="logo">
            <span className="mark" />
            Teknopanorama
          </Link>

          <div className="nav-links">
            <Link to="/" className={anaSayfada ? 'active' : undefined}>Gündem</Link>
            {KATEGORILER.map((k) => (
              <NavLink
                key={k.slug}
                to={`/kategori/${k.slug}`}
                className={({ isActive }) => (isActive ? 'active' : undefined)}
              >
                {k.ad}
              </NavLink>
            ))}
            <Link to="/farkindalik" className="nav-fk">
              🛡 Farkındalık
              <span className="nav-fk-sayac">{gorulen.length}/{TOPLAM}</span>
            </Link>
          </div>

          {/* arama + hesap birlikte sagda dursun */}
          <div className="nav-right">
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
          </div>
        </nav>
      </div>
    </header>
  )
}

export default Navbar
