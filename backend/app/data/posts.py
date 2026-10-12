"""Statik blog icerigi (sahte haberler).

Veritabani yok: demo icin gereksiz. Ileride (SQLi dersi gelince) burasi
SQLite'a tasinabilir, endpoint sozlesmesi ayni kalir.

Alanlar:
  slug          -> URL'de kullanilacak benzersiz kimlik
  title         -> baslik
  excerpt       -> kisa ozet (kartta gorunur)
  author, date  -> yazar ve tarih
  read_minutes  -> tahmini okuma suresi
  category      -> kart cipinde gorunen tek kategori
  tone          -> kart kapaginin rengi (frontend'de stil icin)
  body          -> paragraf listesi (detay sayfasinda gorunur)
"""

POSTS = [
    {
        "slug": "yapay-zeka-telefonlara-tasiniyor",
        "title": "Yapay Zeka Modelleri Telefonlara Tasiniyor",
        "excerpt": "Buyuk dil modellerinin kucultulmus surumleri artik bulut baglantisi olmadan cihaz uzerinde calisiyor.",
        "author": "Deniz Aydin",
        "date": "2026-10-09",
        "read_minutes": 6,
        "category": "Yapay Zeka",
        "tone": "t1",
        "body": [
            "Gecen hafta duyurulan uc yeni model, ayni isi bulut sunucularina hic veri gondermeden yapmayi vaat ediyor.",
            "Cihaz uzerinde calisan bir model, kullanici verisinin agdan hic cikmamasi anlamina geliyor. Teoride bu bir gizlilik kazanimi.",
            "Alanin uzerinde uzlastigi tek nokta su: saldiri yuzeyi yer degistirdi, kuculmedi.",
        ],
    },
    {
        "slug": "parola-yoneticisi-sekiz-neden",
        "title": "Parola Yoneticisi Kullanmanin Sekiz Nedeni",
        "excerpt": "Akilda tutulabilen bir parola, kirilabilen bir paroladir. Neden bu isi bir yazilima devretmeliyiz?",
        "author": "Selin Korkmaz",
        "date": "2026-10-07",
        "read_minutes": 4,
        "category": "Guvenlik",
        "tone": "t2",
        "body": [
            "Ortalama bir internet kullanicisinin yuzden fazla hesabi var. Hepsine ayri ve guclu parola atamak insan hafizasinin isi degil.",
            "Sonuc tahmin edilebilir: ayni parola her yerde kullaniliyor. Tek bir sizinti, o parolayla girilebilen her hesabi riske atiyor.",
            "Parola yoneticisi bu zinciri kiriyor: her site icin rastgele uzun parola uretir, siz tek bir ana parolayi hatirlarsiniz.",
        ],
    },
    {
        "slug": "sarj-agi-standartlar",
        "title": "Sarj Agi Buyuyor, Standartlar Geride Kaliyor",
        "excerpt": "Sarj istasyonu sayisi bir yilda ikiye katlandi. Ancak odeme ve dogrulama ayni hizda ilerlemiyor.",
        "author": "Mert Ozkan",
        "date": "2026-10-04",
        "read_minutes": 5,
        "category": "Enerji",
        "tone": "t3",
        "body": [
            "Yeni rapor, hizli sarj noktasi sayisinin bir yilda iki kat arttigini gosteriyor. Kullanici memnuniyeti ayni egriyi izlemiyor.",
            "Sikayetlerin cogu sarjin kendisiyle degil, oncesindeki adimlarla ilgili: calismayan uygulamalar, dogrulanamayan kartlar.",
            "Ortak bir dogrulama standardina gecmek hem deneyim hem guvenlik acisindan en mantikli adim gorunuyor.",
        ],
    },
    {
        "slug": "acik-kaynak-bakimcilari",
        "title": "Acik Kaynak Bakimcilari Tukeniyor",
        "excerpt": "Milyarlarca kez indirilen kutuphanelerin arkasinda genellikle tek bir gonullu var.",
        "author": "Ipek Tanriverdi",
        "date": "2026-09-30",
        "read_minutes": 7,
        "category": "Yazilim",
        "tone": "t4",
        "body": [
            "Modern bir web uygulamasi yuzlerce dolayli bagimliliga sahip; onemli bir kismi bos zamaninda kod yazan tek kisi tarafindan surduruluyor.",
            "Bakimcilarla yapilan goruslemelerde tema ayni: istek ve sikayet hacmi, gonullu bir insanin kapasitesini coktan asti.",
            "Bu bir isletme riski: bakimci projeyi birakinca devralan kisinin kim oldugu her zaman belli olmuyor.",
        ],
    },
    {
        "slug": "veri-sizintisi-ilk-24-saat",
        "title": "Veri Sizintisi Sonrasi Ilk Yirmi Dort Saat",
        "excerpt": "Haberi aldiniz ve hesabiniz listede. Panige kapilmadan once yapilmasi gereken dort sey var.",
        "author": "Selin Korkmaz",
        "date": "2026-09-27",
        "read_minutes": 3,
        "category": "Guvenlik",
        "tone": "t5",
        "body": [
            "Once sizintinin dogrulanmis olup olmadigini kontrol edin. Dolasan her liste gercek degil; bazilari dogrudan oltalama.",
            "Dogrulandiysa ilk adim o parolayi kullandiginiz DIGER sitelerdeki parolalari degistirmek.",
            "Ikinci adim iki faktorlu dogrulamayi acmak; ucuncusu tum cihazlardaki oturumlari kapatmak.",
        ],
    },
    {
        "slug": "cihaz-ustu-yapay-zeka-gizlilik",
        "title": "Cihaz Ustu Yapay Zeka ve Gizlilik",
        "excerpt": "Veri cihazdan cikmayinca gizlilik kazanimi var; ama yeni bir saldiri yuzeyi de doguyor.",
        "author": "Deniz Aydin",
        "date": "2026-09-24",
        "read_minutes": 6,
        "category": "Mobil",
        "tone": "t6",
        "body": [
            "Cihaz ustu modeller gizlilik acisindan cazip: veri sunucuya gitmez. Ama modelin yerel onbellegi yeni bir hedef.",
            "Uygulama sanal alanindan kacan herhangi bir kod, bu yerel veriye ulasmayi deneyebilir.",
            "Guncelleme mekanizmalarinin saglamligi kritik: imzalanmamis bir model guncellemesi klasik bir tedarik zinciri sorunudur.",
        ],
    },
]
