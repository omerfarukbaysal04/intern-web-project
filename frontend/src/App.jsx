import { useState, useEffect } from 'react'

function App() {
  const [health, setHealth] = useState(null)

  //bileşen ilk geldiğinde çalışır ~useEffect()
  useEffect(() => {
    fetch("/api/health") //api dan bilgiyi aldık
    .then(response => response.json())
    .then(data => setHealth(data.status))
  }, [])

  return (
    <div>
      <h1>Teknopanorama</h1>
      {health ? <p>Sunucu durumu: {health}</p> : <p>Yükleniyor...</p>}
    </div>
  )
}

export default App