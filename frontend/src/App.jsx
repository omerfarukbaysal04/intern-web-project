import { useEffect } from 'react'
import { Routes, Route, useLocation, useNavigate } from 'react-router-dom'
import { isaretle, SALDIRILAR } from './ilerleme'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import Home from './pages/Home'
import Post from './pages/Post'
import Davet from './pages/Davet'
import Farkindalik from './pages/Farkindalik'
import AdPopup from './components/AdPopup'
import ReklamKutusu from './components/ReklamKutusu'

/* Baska bir origin'de yasanan bir saldiridan donus: isaret ?gorulen=... ile
 * gelir (bkz. templates/sahte_giris.html). Isaretleyip adresi temizliyoruz ki
 * sayfa yenilenince tekrar islenmesin ve URL'de izi kalmasin. */
function DonusIsareti() {
  const konum = useLocation()
  const yonlendir = useNavigate()

  useEffect(() => {
    const id = new URLSearchParams(konum.search).get("gorulen")
    if (!id) return
    if (SALDIRILAR.some((s) => s.id === id)) isaretle(id)
    yonlendir(konum.pathname, { replace: true })
  }, [konum.search, konum.pathname, yonlendir])

  return null
}

function App() {
  return (
    <>
      <DonusIsareti />
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path='/post/:slug' element={<Post />}/>
        <Route path="/davet" element={<Davet />} />
        <Route path="/farkindalik" element={<Farkindalik />} />
      </Routes>
      <ReklamKutusu />
      <Footer />
      <AdPopup></AdPopup>
    </>
  )
}

export default App