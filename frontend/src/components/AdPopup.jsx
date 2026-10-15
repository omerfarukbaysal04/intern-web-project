import { useState, useEffect } from "react";

function getOturum(){
  const m = document.cookie.match(/(?:^|;\s*)oturum=([^;]+)/)
  return m ? decodeURIComponent(m[1]) : null
}

function AdPopup(){
    const [visible,setVisible]=useState(false)

    useEffect(()=>{
        if(getOturum()){
            const t= setTimeout(()=>setVisible(true),8000)
            return () => clearTimeout(t)
        }
    },[])

    if(!visible) return null

      return (
    <div className="ad-popup">
      <button className="ad-close" onClick={() => setVisible(false)}>×</button>
      <div className="ad-emoji">🎉</div>
      <div className="ad-text">
        <strong>Bugünün şanslısı sizsiniz!</strong>
        <span>iPhone 16 çekilişine katılmak için son saatler.</span>
        <a className="ad-cta" href="/saldirgan">Hemen Katıl →</a>
      </div>
    </div>
    )
}

export default AdPopup