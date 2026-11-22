# SIMPEL-ITDA — Portal Web

Tampilan portal **SIMPEL-ITDA** (Sistem Informasi Terpadu Inspektorat Daerah Kabupaten Rokan Hilir) yang ditayangkan lewat GitHub Pages.

- **Frontend**: `docs/` (HTML + CSS + JavaScript statis, tanpa iframe)
- **Backend**: Google Apps Script SIMPEL-ITDA (tidak disimpan di repo ini), dipanggil lewat `docs/config.js` → `SIMPEL_API_URL`
- **Protokol**: `POST` teks JSON `{ "simpel": "1", "fn": "<nama fungsi>", "args": [...] }` → balasan `{ ok, data | error }`

## Memperbarui tampilan
Bila `portal_Index`, `portal_Css`, atau `portal_Js` di Apps Script berubah:

```bash
python3 alat/rakit_portal.py <folder-proyek-apps-script> docs
```

Lalu unggah `docs/index.html` yang baru.

## Keamanan
Repo ini publik. Jangan pernah menaruh kode backend (.gs), ID spreadsheet, kunci, atau data pegawai di sini.
