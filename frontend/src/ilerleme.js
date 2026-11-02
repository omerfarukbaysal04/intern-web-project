/* Ziyaretcinin hangi saldirilara dustugunu hatirlayan kucuk katman.
 *
 * Neden var: site sekiz saldiriyi rastgele sirayla sunuyor ve ziyaretci
 * hangilerini gordugunu takip edemiyordu. Burasi "8'de 3" diyebilmemizi
 * saglar; boylece demo, dagınık bir tuzak koleksiyonu olmaktan cikip
 * tamamlanabilir bir deneyime donusuyor.
 *
 * Veri tarayicida (localStorage) durur: sunucuya hic gitmez, kullanici
 * hakkinda hicbir sey toplamayiz. Gizli pencerede ya da depolama kapaliysa
 * her sey yine calisir, sadece hatirlanmaz -- bu yuzden tum okuma/yazmalar
 * try/catch icinde.
 *
 * DIKKAT: ANAHTAR ve id'ler sunucu-render'li ders sayfalariyla PAYLASILIR
 * (bkz. backend/app/templates/_ilerleme.html). Birini degistirirsen
 * digerini de degistir.
 */

import { useEffect, useState } from "react"

const ANAHTAR = "tp_gorulen_saldirilar"
const OLAY = "tp-ilerleme"   // ayni sekmedeki dinleyicileri uyandirmak icin

// Tek kaynak: hem farkindalik panosu hem ilerleme sayimi bunu kullanir.
export const SALDIRILAR = [
  {
    id: "reflected-xss",
    ikon: "🔍",
    ad: "Reflected XSS",
    tur: "XSS",
    kurban: "Hazırlanmış bir arama linkine tıklarsın; tarayıcında saldırganın kodu çalışır.",
    korunma: "Siteler kullanıcı girdisini ekrana basmadan önce escape etmeli.",
    nerede: "Arama kutusu",
  },
  {
    id: "stored-xss",
    ikon: "💬",
    ad: "Stored XSS",
    tur: "XSS",
    kurban: "Bir yorumu okursun; içine gizlenmiş kod oturum çerezini çalar.",
    korunma: "Kullanıcı içeriği gösterilmeden temizlenmeli/escape edilmeli.",
    nerede: "Haber yorumları",
  },
  {
    id: "dom-xss",
    ikon: "🔗",
    ad: "DOM-based XSS",
    tur: "XSS",
    kurban: "Bir davet linkine tıklarsın; kod tamamen tarayıcında çalışır, sunucu hiç görmez.",
    korunma: "URL'den okunan veri innerHTML'e değil, güvenli yöntemle basılmalı.",
    nerede: "Davet linki",
  },
  {
    id: "clickjacking",
    ikon: "🪤",
    ad: "Clickjacking",
    tur: "Arayüz tuzağı",
    kurban: "'Ödülü al' butonuna tıkladığını sanırsın; aslında görünmez bir butonla hesabını silersin.",
    korunma: "Sayfalar iframe'e girmekten men edilmeli (X-Frame-Options).",
    nerede: "Çekiliş reklamı",
  },
  {
    id: "csrf",
    ikon: "🎭",
    ad: "CSRF",
    tur: "İstek sahteciliği",
    kurban: "Sadece bir haberi okursun; haberin olmadan hesabının e-postası değişir.",
    korunma: "İşlemler CSRF token ile doğrulanmalı; GET ile durum değiştirilmemeli.",
    nerede: "Haber yorumları",
  },
  {
    id: "open-redirect",
    ikon: "↪️",
    ad: "Open Redirect",
    tur: "Phishing",
    kurban: "Güvenilir görünen bir linke tıklarsın; sahte bir siteye yönlendirilirsin.",
    korunma: "Yönlendirme hedefi doğrulanmalı (yalnızca site-içi adresler).",
    nerede: "Haber yorumları",
  },
  {
    id: "tabnabbing",
    ikon: "🗂️",
    ad: "Reverse Tabnabbing",
    tur: "Phishing",
    kurban: "Yeni sekmede bir şey açarsın; arkadaki sekmen sessizce sahte girişe dönüşür.",
    korunma: "Dış bağlantılara rel=\"noopener\" eklenmeli.",
    nerede: "Haber yorumları",
  },
  {
    id: "malvertising",
    ikon: "📢",
    ad: "Malvertising",
    tur: "Sosyal mühendislik",
    kurban: "İçerik sandığın bir 'reklama' tıklarsın; sahte ödeme sayfasında kartın çalınır.",
    korunma: "Reklamlar açıkça etiketlenmeli ve kaynakları denetlenmeli.",
    nerede: "Sayfa içi reklam",
  },
]

export const TOPLAM = SALDIRILAR.length

/** Gorulen saldirilarin id listesi (depolama yoksa bos dizi). */
export function gorulenler() {
  try {
    const ham = JSON.parse(localStorage.getItem(ANAHTAR) || "[]")
    if (!Array.isArray(ham)) return []
    // Bilinmeyen id'leri ele: liste degisirse eski kayit sayimi bozmasin.
    const idler = SALDIRILAR.map((s) => s.id)
    return ham.filter((id) => idler.includes(id))
  } catch {
    return []
  }
}

/** Bir saldiriyi "dustun" diye isaretler. Ayni id ikinci kez eklenmez. */
export function isaretle(id) {
  try {
    const liste = gorulenler()
    if (!liste.includes(id)) {
      localStorage.setItem(ANAHTAR, JSON.stringify([...liste, id]))
    }
  } catch {
    // depolama kapali: isaretleyemeyiz, akis yine de devam etsin
  }
  // Navbar ve farkindalik panosu ayni sekmede aninda guncellensin.
  try { window.dispatchEvent(new Event(OLAY)) } catch { /* yoksay */ }
}

/** Panoyu sifirlar (demoyu bastan anlatmak icin). */
export function sifirla() {
  try { localStorage.removeItem(ANAHTAR) } catch { /* yoksay */ }
  try { window.dispatchEvent(new Event(OLAY)) } catch { /* yoksay */ }
}

/** Gorulen listesini canli takip eden React hook'u.
 *  Ad 'use' ile baslamak ZORUNDA: React'in hook kurali (lint de bunu denetliyor). */
export function useIlerleme() {
  const [liste, setListe] = useState(gorulenler)

  useEffect(() => {
    const yenile = () => setListe(gorulenler())
    window.addEventListener(OLAY, yenile)      // ayni sekme
    window.addEventListener("storage", yenile) // baska sekme
    yenile()                                   // sunucu-render'li sayfadan donusler
    return () => {
      window.removeEventListener(OLAY, yenile)
      window.removeEventListener("storage", yenile)
    }
  }, [])

  return liste
}
