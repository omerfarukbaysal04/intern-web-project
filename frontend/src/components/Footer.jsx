// Sunum bileseni (tasarim). Solda telif, sagda kisisel baglantilar.
// Baglantilar portfolyo sitesindeki footer'dan alindi.
const BAGLANTILAR = [
  {
    ad: "LinkedIn",
    url: "https://www.linkedin.com/in/baysal/",
    // Basit LinkedIn isareti
    yol: "M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3V9zm6 0h3.8v1.7h.05c.53-.95 1.82-1.95 3.75-1.95C20.4 8.75 22 10.9 22 14.1V21h-4v-6.1c0-1.45-.03-3.3-2.05-3.3-2.05 0-2.37 1.57-2.37 3.2V21H9V9z",
  },
  {
    ad: "GitHub",
    url: "https://github.com/omerfarukbaysal04",
    yol: "M12 2a10 10 0 0 0-3.16 19.49c.5.09.68-.22.68-.48l-.01-1.7c-2.78.6-3.37-1.34-3.37-1.34-.45-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.9 1.53 2.36 1.09 2.94.83.09-.65.35-1.09.63-1.34-2.22-.25-4.555-1.11-4.555-4.94 0-1.09.39-1.98 1.03-2.68-.1-.25-.45-1.27.1-2.65 0 0 .84-.27 2.75 1.02a9.5 9.5 0 0 1 5 0c1.91-1.29 2.75-1.02 2.75-1.02.55 1.38.2 2.4.1 2.65.64.7 1.03 1.59 1.03 2.68 0 3.84-2.34 4.69-4.57 4.93.36.31.68.92.68 1.85l-.01 2.75c0 .27.18.58.69.48A10 10 0 0 0 12 2z",
  },
  {
    ad: "Portfolyo",
    url: "https://omerfarukbaysal.netlify.app",
    // Kure (web) isareti
    yol: "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm0 2c1.3 0 2.73 2.2 3.24 5.5H8.76C9.27 6.2 10.7 4 12 4zM8.5 11.5h7a18 18 0 0 1 0 1 18 18 0 0 1-.09 1.5H8.59A18 18 0 0 1 8.5 12.5v-1zM6.6 14H4.26a8 8 0 0 1 0-4H6.6a20 20 0 0 0 0 4zm.37 2h1.9c.33 1.65.86 3.05 1.5 3.93A8.02 8.02 0 0 1 6.97 16zm7.16 3.93c.64-.88 1.17-2.28 1.5-3.93h1.9a8.02 8.02 0 0 1-3.4 3.93zM17.4 14a20 20 0 0 0 0-4h2.34a8 8 0 0 1 0 4H17.4zm-.47-6h-1.9c-.33-1.65-.86-3.05-1.5-3.93A8.02 8.02 0 0 1 16.93 8zM10.37 4.07c-.64.88-1.17 2.28-1.5 3.93h-1.9a8.02 8.02 0 0 1 3.4-3.93zM12 20c-1.3 0-2.73-2.2-3.24-5.5h6.48C14.73 17.8 13.3 20 12 20z",
  },
]

function Footer() {
  return (
    <footer className="site-footer">
      <div className="wrap">
        <div className="inner">
          <span>© 2026 Teknopanorama — Ömer Faruk BAYSAL</span>

          <div className="footer-link">
            {BAGLANTILAR.map((b) => (
              <a
                key={b.ad}
                href={b.url}
                target="_blank"
                rel="noopener noreferrer"
                aria-label={b.ad}
                title={b.ad}
              >
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true">
                  <path d={b.yol} />
                </svg>
              </a>
            ))}
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
