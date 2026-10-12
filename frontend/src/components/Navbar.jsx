// Sunum bileseni (tasarim). Arama kutusu ve linkler simdilik gorsel;
// yonlendirme (routing) ekledigimizde <a> yerine <Link> baglayacagiz.
function Navbar() {
  return (
    <header className="nav-bar">
      <div className="wrap">
        <nav className="nav-inner">
          <a href="/" className="logo">
            <span className="mark" />
            Teknopanorama
          </a>

          <div className="nav-links">
            <a href="/" className="active">Gündem</a>
            <a href="/">Yapay Zeka</a>
            <a href="/">Güvenlik</a>
            <a href="/">Enerji</a>
          </div>

          <div className="nav-search">
            <span className="ic">⌕</span>
            <input type="text" placeholder="Haberlerde ara..." />
          </div>
        </nav>
      </div>
    </header>
  )
}

export default Navbar
