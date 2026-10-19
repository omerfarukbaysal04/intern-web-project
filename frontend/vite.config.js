import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:8000', //cors
      '/search': 'http://127.0.0.1:8000', // sunucu-render'li arama sayfasi (zafiyetli)
      '/giris': 'http://127.0.0.1:8000',  // giris sayfasi (backend)
      '/hesap': 'http://127.0.0.1:8000',  // hesap + /hesap/email + /hesap/sil
      '/cikis': 'http://127.0.0.1:8000',  // cikis
      '/saldirgan': 'http://127.0.0.1:8000', // clickjacking demo saldirgan sayfasi
      '/clickjack-ders': 'http://127.0.0.1:8000', // clickjacking farkindalik dersi
      '/csrf-saldirgan': 'http://127.0.0.1:8000', // csrf demo saldirgan sayfasi
    },
  },
})