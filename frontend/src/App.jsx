import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import Home from './pages/Home'
import Post from './pages/Post'
import Davet from './pages/Davet'
import AdPopup from './components/AdPopup'
import ReklamKutusu from './components/ReklamKutusu'

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path='/post/:slug' element={<Post />}/>
        <Route path="/davet" element={<Davet />} />
      </Routes>
      <ReklamKutusu />
      <Footer />
      <AdPopup></AdPopup>
    </>
  )
}

export default App