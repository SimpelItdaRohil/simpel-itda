# Panduan untuk AI coding agent — repo portal SIMPEL-ITDA

## Arsitektur
- `docs/index.html` dirakit oleh `alat/rakit_portal.py` dari file Apps Script `portal_Index.html`, `portal_Css.html`, `portal_Js.html`, `sipeta_Logo.html`, `sipeta_LogoInsp.html`. Jangan menyunting index.html langsung bila perubahannya juga harus ada di portal lama; ubah sumbernya lalu rakit ulang.
- Semua panggilan server lewat fungsi `api(fn, ...args)` / `apiT(fn, ...args)` (token otomatis). Di versi web, `api()` memakai `fetch` POST ke `window.SIMPEL_API_URL` (docs/config.js).
- Backend: 16_ApiWeb.gs di proyek Apps Script; hanya fungsi di `API_WEB.FUNGSI` yang bisa dipanggil.

## Aturan wajib
- `fetch` ke API: `Content-Type: text/plain;charset=utf-8`, tanpa header lain (mencegah preflight CORS). Token dikirim di `args`, bukan header.
- Fungsi server baru yang dipanggil tampilan → tambahkan ke `API_WEB.FUNGSI` di 16_ApiWeb.gs.
- Data dari server ditampilkan lewat `esc()` / textContent, jangan langsung ke innerHTML.
- Jangan menaruh rahasia (ID spreadsheet, kunci, NIP admin, data pegawai) di repo ini — repo publik.
- Bahasa antarmuka: Bahasa Indonesia baku.
