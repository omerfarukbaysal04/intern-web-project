import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import Home from './pages/Home'
import Post from './pages/Post'
import Search from './pages/Search'

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path='/post/:slug' element={<Post />}/>
        <Route path="/search" element={<Search />} />
      </Routes>
      <Footer />
    </>
  )
}

export default App