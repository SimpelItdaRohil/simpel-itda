#!/usr/bin/env python3
"""
Rakit portal SIMPEL-ITDA (HtmlService) menjadi halaman statis untuk GitHub Pages.

Pemakaian:
    python3 rakit_portal.py <folder_proyek_apps_script> <folder_docs_keluaran>

Yang dilakukan:
  1. portal_Index.html  → kerangka halaman
  2. <?!= PT_include('portal_Css') ?> / portal_Js → isi file ditempel langsung
  3. Logo (sipeta_Logo, sipeta_LogoInsp) ditempel sebagai data URI
  4. URL_DASAR diambil dari config.js (SIMPEL_API_URL)
  5. Fungsi api() (google.script.run) diganti fetch() ke pintu API (16_ApiWeb.gs)
File sumber tidak diubah.
"""
import json, os, re, sys

API_BARU = r"""function api(fn) {
  /* Versi GitHub Pages: memanggil pintu API (16_ApiWeb.gs) lewat fetch().
     Content-Type text/plain WAJIB agar browser tidak mengirim preflight (penyebab error CORS). */
  var args = Array.prototype.slice.call(arguments, 1);
  if (!window.SIMPEL_API_URL || /GANTI_/.test(window.SIMPEL_API_URL)) {
    return Promise.reject(new Error('Alamat API belum diatur. Isi SIMPEL_API_URL di file config.js.'));
  }
  return fetch(window.SIMPEL_API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain;charset=utf-8' },
    body: JSON.stringify({ simpel: '1', fn: fn, args: args }),
    redirect: 'follow'
  }).then(function (r) {
    return r.text();
  }, function () {
    throw new Error('Tidak dapat terhubung ke server. Periksa koneksi internet Anda.');
  }).then(function (teks) {
    var j;
    try { j = JSON.parse(teks); } catch (e) {
      throw new Error('Server tidak membalas JSON. Pastikan deployment Apps Script versi terbaru sudah diterapkan dan aksesnya "Siapa saja".');
    }
    if (j && j.ok) return j.data;
    var m = String((j && j.error) || 'Terjadi kesalahan di server.');
    if (/SESI_HABIS/.test(m)) { keluarLokal(/dinonaktifkan|ditutup/i.test(m) ? m.replace(/^.*SESI_HABIS:\s*/, '') : 'Sesi berakhir, silakan masuk kembali.'); }
    else if (/GANTI_SANDI/.test(m)) { dialogSandi(true); }
    else if (/AKTIFKAN_OTP/.test(m)) { dialogOtpDaftar(true); }
    var er = new Error(m.replace(/^(Error|Exception):\s*/, '').replace(/^(SESI_HABIS|GANTI_SANDI|AKTIFKAN_OTP):\s*/, ''));
    er.kode = (m.match(/(SESI_HABIS|GANTI_SANDI|AKTIFKAN_OTP)/) || [])[1] || '';
    throw er;
  });
}
"""


def baca(folder, nama):
    with open(os.path.join(folder, nama + '.html'), encoding='utf-8') as f:
        return f.read()


def rakit(src, out):
    index = baca(src, 'portal_Index')
    css = baca(src, 'portal_Css')
    js = baca(src, 'portal_Js')
    logo_rohil = baca(src, 'sipeta_Logo').strip()
    logo_insp = baca(src, 'sipeta_LogoInsp').strip()

    # Ganti fungsi api() lama (dari "function api(fn) {" sampai sebelum "function apiT(")
    awal = js.index('function api(fn) {')
    akhir = js.index('function apiT(')
    js = js[:awal] + API_BARU + js[akhir:]
    if 'google.script.run' in js:
        raise SystemExit('Masih ada google.script.run di portal_Js — periksa manual.')

    ganti = {
        "</head>": '<script src="config.js"></script>\n</head>',
        "<?!= PT_include('portal_Css') ?>": css,
        "<?!= JSON.stringify(PT_include('sipeta_Logo').trim()) ?>": json.dumps(logo_rohil),
        "<?!= JSON.stringify(PT_include('sipeta_LogoInsp').trim()) ?>": json.dumps(logo_insp),
        "<?!= JSON.stringify(urlDasar || '') ?>": "window.SIMPEL_API_URL",
        "<?!= PT_include('portal_Js') ?>": js,
    }
    for lama, baru in ganti.items():
        if index.count(lama) != 1:
            raise SystemExit('Penanda tidak ditemukan tepat satu kali: ' + lama)
        index = index.replace(lama, baru)
    if '<?' in index:
        raise SystemExit('Masih ada tag template <? ?> yang belum diganti.')

    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index)
    print('OK →', os.path.join(out, 'index.html'), len(index), 'byte')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    rakit(sys.argv[1], sys.argv[2])
