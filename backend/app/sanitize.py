"""Yorum HTML'i icin beyaz-liste temizleyicisi (SAFE_MODE savunmasi).

Neden escape yerine temizleme?
  Ilk surumde SAFE_MODE yorumlari bastan sona `html.escape()` ediyordu. Bu stored
  XSS'i gerceklen durduruyordu, ama yan etkisi vardi: yorum icine gomulu TUM HTML
  olduyordu -- open redirect, reverse tabnabbing ve DOM XSS tuzaklarinin tasiyicisi
  olan <a> linkleri de dahil. Yani o uc saldirinin kendi savunmasi (yonlendirme
  dogrulamasi, rel=noopener, guvenli DOM yazimi) hic devreye girmiyor, saldiri
  sadece "linki gostermeyerek" sonuyordu.

  Gercek siteler de boyle yapmaz: yorumda kalin yazi ve link'e izin verip tehlikeli
  olani ayiklarlar. Bu modul tam olarak onu yapiyor; boylece SAFE_MODE'da her
  saldiri KENDI savunmasiyla cokuyor.

Kural:
  - Sadece IZINLI_ETIKETLER gecer; digerleri (ornegin <img>, <script>, <svg>)
    tamamen dusurulur.
  - Sadece IZINLI_NITELIKLER gecer; bu yuzden onerror/onload gibi olay
    nitelikleri daha kurala bakilmadan elenir.
  - href yalnizca site-ici (/...) ya da http(s) olabilir; javascript: reddedilir.
  - target="_blank" olan her linke rel="noopener noreferrer" ZORLA eklenir
    (reverse tabnabbing savunmasi).
  - Etiket disindaki tum metin escape edilir.
"""

import html
from html.parser import HTMLParser

IZINLI_ETIKETLER = {"b", "strong", "i", "em", "u", "code", "br", "a"}
IZINLI_NITELIKLER = {"a": {"href", "title", "target"}}
BOS_ETIKETLER = {"br"}


def _href_guvenli(deger: str) -> bool:
    """Sadece site-ici ya da http(s) adreslere izin ver (javascript:, data: hayir)."""
    d = (deger or "").strip().lower()
    if d.startswith("//"):          # protokol-bagimsiz dis adres
        return False
    return d.startswith("/") or d.startswith("http://") or d.startswith("https://")


class _Temizleyici(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parcalar = []
        self._acik = []   # dusurulmeyen, kapatilmasi gereken etiketler

    # --- acilis etiketi ---
    def handle_starttag(self, tag, attrs):
        if tag not in IZINLI_ETIKETLER:
            return  # etiketi dusur (icerigi metin olarak yine gelecek)

        nitelikler = dict(attrs)
        izinli = IZINLI_NITELIKLER.get(tag, set())
        temiz = {}
        for ad, deger in nitelikler.items():
            if ad not in izinli or deger is None:
                continue
            if ad == "href" and not _href_guvenli(deger):
                continue
            temiz[ad] = deger

        if tag == "a":
            if "href" not in temiz:
                return  # hedefi olmayan/gecersiz link: etiketi dusur
            # REVERSE TABNABBING SAVUNMASI: yeni sekmede acilan her link
            # kendisini acan sekmeye erisemesin.
            if temiz.get("target") == "_blank":
                temiz["rel"] = "noopener noreferrer"

        yazi = "".join(
            ' {}="{}"'.format(ad, html.escape(str(deger), quote=True))
            for ad, deger in temiz.items()
        )
        self.parcalar.append("<{}{}>".format(tag, yazi))
        if tag not in BOS_ETIKETLER:
            self._acik.append(tag)

    def handle_startendtag(self, tag, attrs):
        if tag in BOS_ETIKETLER:
            self.parcalar.append("<{}>".format(tag))

    # --- kapanis etiketi ---
    def handle_endtag(self, tag):
        if tag in self._acik:
            # en son acilan ayni etikete kadar kapat (bozuk ic ice yazimi toparlar)
            while self._acik:
                acik = self._acik.pop()
                self.parcalar.append("</{}>".format(acik))
                if acik == tag:
                    break

    # --- metin ---
    def handle_data(self, veri):
        self.parcalar.append(html.escape(veri))

    def sonuc(self) -> str:
        while self._acik:
            self.parcalar.append("</{}>".format(self._acik.pop()))
        return "".join(self.parcalar)


def temizle(metin: str) -> str:
    """Yorum metnini beyaz-listeye gore temizler ve guvenli HTML dondurur."""
    t = _Temizleyici()
    t.feed(metin or "")
    t.close()
    return t.sonuc()
