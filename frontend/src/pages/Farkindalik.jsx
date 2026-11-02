import { Link } from "react-router-dom"
import { SALDIRILAR, TOPLAM, useIlerleme, sifirla } from "../ilerleme"

function Farkindalik() {
  const gorulen = useIlerleme()
  const sayi = gorulen.length
  const yuzde = Math.round((sayi / TOPLAM) * 100)
  const bitti = sayi === TOPLAM

  // Henuz dusmedigi saldirilardan birine yon gostermek icin.
  const kalanlar = SALDIRILAR.filter((z) => !gorulen.includes(z.id))

  return (
    <div className="wrap">
      <section className="fk-hero">
        <div className="kicker">Güvenlik Farkındalığı</div>
        <h1>Sıradan bir gün, sıradan bir site... ve bir tıklama.</h1>
        <p>
          Teknopanorama, güvenli bir deneme ortamıdır. Burada gerçek web saldırılarına
          <b> zararsızca </b> maruz kalır, "az önce ne oldu ve nasıl korunurum" diye
          anında öğrenirsin. Çünkü çoğu saldırıya düşmek için teknik bilgiye değil,
          yalnızca bir linke tıklamaya ya da bir sayfayı açmaya gerek var.
        </p>
      </section>

      {/* ---- ilerleme panosu ---- */}
      <section className="fk-pano">
        <div className="fk-pano-ust">
          <div>
            <div className="fk-sayi">
              <strong>{sayi}</strong> / {TOPLAM}
            </div>
            <p className="fk-pano-alt">
              {sayi === 0
                ? "Henüz hiçbir saldırıya düşmedin. Sitede gezinmeye başla."
                : bitti
                  ? "Sekizinin de kurbanı oldun — artık hepsini içeriden biliyorsun."
                  : `${sayi} saldırının kurbanı oldun, ${TOPLAM - sayi} tanesi seni bekliyor.`}
            </p>
          </div>
          {sayi > 0 && (
            <button className="fk-sifirla" onClick={sifirla}>
              Panoyu sıfırla
            </button>
          )}
        </div>

        <div className="fk-bar" role="progressbar" aria-valuenow={sayi} aria-valuemin={0} aria-valuemax={TOPLAM}>
          <div className="fk-bar-dolu" style={{ width: `${yuzde}%` }} />
        </div>

        {!bitti && kalanlar.length > 0 && (
          <p className="fk-ipucu">
            Sıradaki ipucu: <b>{kalanlar[0].ad}</b> tuzağı <b>{kalanlar[0].nerede.toLowerCase()}</b> tarafında saklı.
          </p>
        )}
      </section>

      <div className="sec-label">
        <span>Kurban Olabileceğin {TOPLAM} Saldırı</span>
        <div className="line"></div>
      </div>

      <div className="fk-grid">
        {SALDIRILAR.map((z) => {
          const dustu = gorulen.includes(z.id)
          return (
            <div className={`fk-card ${dustu ? "fk-dustu" : "fk-bekliyor"}`} key={z.id}>
              <div className="fk-top">
                <span className="fk-ikon">{z.ikon}</span>
                <div>
                  <h3>{z.ad}</h3>
                  <span className="fk-tur">{z.tur}</span>
                </div>
                <span className={`fk-rozet ${dustu ? "var" : "yok"}`}>
                  {dustu ? "✓ düştün" : "karşılaşmadın"}
                </span>
              </div>
              <p className="fk-kurban"><b>Nasıl kurban olursun:</b> {z.kurban}</p>
              <p className="fk-korunma"><b>Nasıl korunursun:</b> {z.korunma}</p>
              <p className="fk-nerede">Tuzağın yeri: {z.nerede}</p>
            </div>
          )
        })}
      </div>

      <p className="fk-not">
        Tüm saldırılar bu sitede <b>izole ve zararsızdır</b>; yalnızca farkındalık amaçlıdır.
        İlerlemen yalnızca kendi tarayıcında tutulur, sunucuya gönderilmez.
        Sitede gezinmeye <Link to="/">buradan başlayabilirsin</Link>.
      </p>
    </div>
  )
}

export default Farkindalik
