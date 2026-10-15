import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import Home from './pages/Home'
import Post from './pages/Post'
import AdPopup from './components/AdPopup'

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path='/post/:slug' element={<Post />}/>
      </Routes>
      <Footer />
      <AdPopup></AdPopup>
    </>
  )
}

export default App