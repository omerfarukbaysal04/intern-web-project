"""Haber icerigi (statik). Veritabani yok: demo icin gereksiz.

Icerik GERCEK haberlerden derlendi (Ekim - Kasim 2026). Her yazinin "kaynak"
alaninda hangi yayindan alindigi ve adresi duruyor; metinler kopyalanmadi,
kendi cumlelerimizle ozetlendi. Haber sitesi gibi gorunen bir demonun
inandirici olmasi icin icerigin de gercek olmasi gerekiyor.

Alanlar:
  slug           -> URL'de kullanilacak benzersiz kimlik
  title          -> baslik
  excerpt        -> kisa ozet (kartta gorunur)
  author, date   -> yazar (kurgusal) ve yayin tarihi
  read_minutes   -> tahmini okuma suresi
  category       -> gorunen kategori adi
  kategori_slug  -> kategori sayfasinin adresi (/kategori/<slug>)
  tone           -> kart kapaginin rengi; KATEGORIYE GORE sabit, boylece
                    ayni kategorinin yazilari ana sayfada da birbirini tutuyor
  kaynak         -> {ad, url}: haberin alindigi yayin
  body           -> paragraf listesi (detay sayfasinda gorunur)

DIKKAT: slug'lar comments.py'deki tuzak anahtarlariyla eslesir. Bir slug'i
degistirirsen comments.py'deki karsiligini da degistir, yoksa o saldiri
tetiklenmez.
"""

POSTS = [
    # ------------------------------------------------------------------
    # YAPAY ZEKA
    # ------------------------------------------------------------------
    {
        "slug": "apple-m6-cihaz-ustu-yapay-zeka",
        "title": "Apple, M6'lı iMac ile Cihaz Üstü Yapay Zekâda İddialı",
        "excerpt": "Şirket yeni iMac'in cihaz üzerinde çalışan yapay zekâda M4'e göre beş kata kadar hızlandığını söylüyor. Rakamın geldiği test ise tek bir senaryo.",
        "author": "Deniz Aydın",
        "date": "2026-10-27",
        "read_minutes": 4,
        "category": "Yapay Zeka",
        "kategori_slug": "yapay-zeka",
        "tone": "t5",
        "gorsel": {
            "dosya": "/haber/apple-m6.jpg",
            "alt": "Apple Store'da sergilenen, ekraninda Apple Intelligence yazan bir iMac",
            "atif": "AzureSaturn, CC0, Wikimedia Commons",
        },
        "kaynak": {
            "ad": "Macworld",
            "url": "https://macworld.com/article/3270546/imac-gains-m6-chip-and-performance-boost-but-little-else-changes.html",
        },
        "body": [
            "Apple, 27 Ekim'de M6 işlemcili yeni iMac'i ve giriş seviyesi MacBook Pro'yu duyurdu. Şirketin öne çıkardığı başlık performans değil, performansın nereye harcandığı: cihaz üzerinde çalışan yapay zekâ.",
            "Apple'a göre çift 16 çekirdekli Neural Engine ve GPU birlikte çalıştığında, cihaz üstü yapay zekâ performansı M4'lü iMac'e göre beş kata kadar çıkıyor. M1'li modellere karşı verilen rakam ise on iki kat.",
            "Bu rakamları okurken dikkat edilmesi gereken bir ayrıntı var: beş kat iddiası, LM Studio üzerinde dil modeli istemlerinin işlenmesi gibi belirli bir testten geliyor. Grafik tarafında M4'e göre iki kat, günlük uygulamalarda ise yaklaşık bir buçuk kat bir artıştan söz ediliyor. Yani \"beş kat hızlı\" ifadesi, genel bir hız artışı değil.",
            "Bağımsız testler henüz yayımlanmadı. Ama yönün kendisi net: büyük modelleri buluta göndermek yerine cihazda çalıştırma yarışı, artık masaüstü bilgisayarların da pazarlama başlığı haline geldi.",
        ],
    },
    {
        "slug": "matrix-game-acik-kaynak-dunya-modeli",
        "title": "Açık Kaynak Dünya Modeli Tek Ekran Kartında Çalışıyor",
        "excerpt": "Matrix-Game 4.0, oyun dünyasını kodda tutup görüntüyü yapay zekâya ürettiriyor. Ağırlıklar açık kaynak yayımlandı.",
        "author": "Mert Özkan",
        "date": "2026-10-15",
        "read_minutes": 5,
        "category": "Yapay Zeka",
        "kategori_slug": "yapay-zeka",
        "tone": "t5",
        "gorsel": {
            "dosya": "/haber/matrix-game.jpg",
            "alt": "Bilgisayar kasasinin icinde cift fanli bir Nvidia ekran karti",
            "atif": "Keijiro Takahashi, CC0, Wikimedia Commons",
        },
        "kaynak": {
            "ad": "DonanımHaber",
            "url": "https://www.donanimhaber.com/yapay-zeka-ile-oyun-ureten-matrix-game-4-0-acik-kaynak-oldu--211872",
        },
        "body": [
            "Skywork AI, yapay zekâ ile oyun dünyaları üreten Matrix-Game 4.0'ı açık kaynak olarak yayımladı. Sistemin dikkat çeken yanı, tek bir RTX 5090 ekran kartında yerel olarak çalışabilmesi.",
            "Yaklaşımın özü bir iş bölümü: oyunun durumunu — can, envanter, görev ilerlemesi — klasik bir oyun motoru kod olarak tutuyor, ekranda görünen kareyi ise video modeli üretiyor. Böylece modelin dünyayı \"hatırlaması\" beklenmiyor; hatırlama işi koda bırakılıyor.",
            "Şirketin açıkladığı rakamlar 480p çözünürlükte saniyede 60 kare ve tuşa basıldıktan sonra ilk yanıt karesine kadar 112 milisaniye. Bağımsız ölçümlerde tek adımlı modda saniyede 83 kare civarı, iki adımlı modda ise 57 kare görülüyor; tepe bellek kullanımı yaklaşık 18,5 GB.",
            "Bu rakamların modelin kendi belgesinde sınırlandırıldığını not etmek gerekir: performans belirli sahnelerde ölçülmüş ve tüketici donanımında kare hızı garanti edilmiyor. Yine de referans dağıtımın sekiz adet veri merkezi ekran kartından tek bir masaüstü kartına inmiş olması, dünya modellerinin ulaşılabilirliği açısından kayda değer.",
        ],
    },
    {
        "slug": "kucuk-modeller-cevrimdisi-calisiyor",
        "title": "Küçük Modeller İnternetsiz Cihazlara Yerleşiyor",
        "excerpt": "Nvidia'nın yeni modeli 4 GB bellek hedefiyle tasarlandı; robotlarda ve küçük cihazlarda bağlantı olmadan çalışabiliyor.",
        "author": "İpek Tanrıverdi",
        "date": "2026-10-26",
        "read_minutes": 4,
        "category": "Yapay Zeka",
        "kategori_slug": "yapay-zeka",
        "tone": "t5",
        "gorsel": {
            "dosya": "/haber/kucuk-modeller.jpg",
            "alt": "Bir ag anahtarinin uzerinde duran, kablolari takili Raspberry Pi",
            "atif": "RAIL.PHOTOGRAPHY, CC0, Wikimedia Commons",
        },
        "kaynak": {
            "ad": "DonanımHaber — AI Günlükleri",
            "url": "https://www.donanimhaber.com/yapay-zeka-dunyasinda-bu-hafta-26-ekim-2026--212105",
        },
        "body": [
            "Yapay zekâ tartışması uzun süredir \"daha büyük model\" ekseninde ilerliyordu. Son haftalarda ise ters yönde bir hareket görünür hale geldi: mümkün olduğunca küçük, mümkün olduğunca yerel çalışan modeller.",
            "Nvidia'nın Nemotron 3.5 Bolt E4B modeli bu yönün örneği. Model 4 GB bellek hedefiyle tasarlandı ve robotlarda ya da küçük cihazlarda internet bağlantısı olmadan çalışabiliyor.",
            "Bunun pratik anlamı, kullanıcı verisinin cihazdan hiç çıkmaması. Teoride bu bir gizlilik kazanımı: sunucuya gitmeyen veri, sunucudan sızmaz.",
            "Alanın üzerinde uzlaştığı tek nokta ise şu: saldırı yüzeyi yok olmuyor, yer değiştiriyor. Veri buluttan cihaza taşındığında, cihazın kendisi — ve onu kullanan kişi — daha değerli bir hedef haline geliyor.",
        ],
    },

    # ------------------------------------------------------------------
    # GÜVENLİK
    # ------------------------------------------------------------------
    {
        "slug": "binance-alti-milyar-dolar",
        "title": "FBI: Binance'ten Çalınan 6 Milyar Doların Arkasında Kuzey Kore Var",
        "excerpt": "Tarihin en büyük kripto hırsızlığı 29 Ekim'de gerçekleşti. FBI saldırıyı iki gün sonra TraderTraitor grubuna bağladı.",
        "author": "Selin Korkmaz",
        "date": "2026-10-31",
        "read_minutes": 5,
        "category": "Güvenlik",
        "kategori_slug": "guvenlik",
        "tone": "t4",
        "gorsel": {
            "dosya": "/haber/binance.jpg",
            "alt": "Dolar banknotlarinin uzerine dizilmis Bitcoin sembollu madeni paralar",
            "atif": "David McBee, CC0, Wikimedia Commons",
        },
        "kaynak": {
            "ad": "FBI — Siber Uyarı",
            "url": "https://www.fbi.gov/investigate/cyber/alerts/2026/north-korea-responsible-for-6-billion-binance-attack",
        },
        "body": [
            "FBI, 31 Ekim'de yayımladığı uyarıda, kripto para borsası Binance'ten 29 Ekim civarında çalınan 6 milyar doların üzerindeki dijital varlığın arkasında Kuzey Kore bağlantılı aktörlerin olduğunu açıkladı. Kurum faaliyeti \"TraderTraitor\" adıyla etiketliyor — geçen yıl 1,5 milyar dolarlık Bybit saldırısının da arkasındaki isim.",
            "Binance kaybı ilk açıklamasında yaklaşık 6,3 milyar dolar olarak bildirdi ve çalınan varlıkların yüzde 90'ını kendi kaynaklarıyla yerine koyduğunu duyurdu. Şirketin ifadesi net: mali yükü kullanıcılar değil, borsa üstlenecek.",
            "FBI, Gizli Servis ve IRS-CI ile birlikte yürüttüğü incelemede, çalınan varlıkların ağırlıklı olarak Ethereum'a çevrildiğini bildirdi. Kurumlar, borsalardan ve analiz şirketlerinden aklama için kullanılan adreslerle yapılan işlemleri engellemelerini istedi.",
            "Saldırının nasıl başladığı hâlâ inceleniyor. Bir habere göre Binance olayı ele geçirilmiş bir geliştirici dizüstü bilgisayarına bağlıyor; bu bilgi henüz birincil bir kaynaktan doğrulanmadı. Doğrulanırsa tanıdık bir hikâye olur: milyarlarca dolarlık bir sistemin kapısı, tek bir kişinin cihazından açılmış olur.",
        ],
    },
    {
        "slug": "chainalysis-ajan-tabanli-sizma",
        "title": "Chainalysis, Yapay Zekâ Ajanlarıyla Yapılan Sızmayı Doğruladı",
        "excerpt": "Şirket iç araçlarına yapılan saldırıyı \"saldırgan ajan teknikleri\" olarak tanımlıyor. Müşteri kimlik bilgileri açığa çıktı.",
        "author": "Selin Korkmaz",
        "date": "2026-10-30",
        "read_minutes": 4,
        "category": "Güvenlik",
        "kategori_slug": "guvenlik",
        "tone": "t4",
        "gorsel": {
            "dosya": "/haber/chainalysis.jpg",
            "alt": "Veri merkezinde dizustu bilgisayarla sunucu kabinine mudahale eden teknisyen",
            "atif": "Derrick Coetzee, CC0, Wikimedia Commons",
        },
        "kaynak": {
            "ad": "The Hacker News",
            "url": "https://thehackernews.com/2026/10/chainalysis-confirms-intrusion-into.html",
        },
        "body": [
            "Blok zinciri analiz şirketi Chainalysis, iç araçlarına yetkisiz erişim olduğunu ve bazı müşteri bilgilerinin açığa çıktığını doğruladı. Şirketin kullandığı ifade dikkat çekici: saldırıda \"saldırgan ajan teknikleri\" kullanılmış.",
            "Açığa çıkan veriler kimlik alanlarıyla sınırlı: kullanıcı kimlikleri, ad soyad, e-posta adresleri ve kurum içindeki rol etiketleri. Şirkete göre soruşturma içeriklerine, kimlik doğrulama bilgilerine ya da oturum jetonlarına yetkisiz erişim olmadı; grafikler, notlar, dosyalar ve sorgu sonuçları da etkilenmedi.",
            "Şirket saldırganın sisteme nasıl girdiğini, erişimin ne zaman başladığını ve saldırının tam olarak hangi aşamasında ajanların devreye girdiğini açıklamadı. Hangi kurumun hangi kayıtlarının görüldüğü de hâlâ belirleniyor.",
            "Burada asıl mesele çalınan verinin hacmi değil. Bir saldırının adım adım insan eliyle değil, otomatik ajanlar tarafından yürütülebiliyor olması, saldırıların ölçeğini ve hızını değiştiriyor. Ad ve e-posta gibi \"zararsız\" görünen alanlar da zaten çoğu zaman asıl hedef değil, bir sonraki adımın — inandırıcı bir kimlik avı e-postasının — hammaddesidir.",
        ],
    },
    {
        "slug": "parolasiz-kimlik-dogrulama-passkey",
        "title": "Parolasız Döneme Geçiş: Passkey Varsayılan Oluyor",
        "excerpt": "Microsoft, kurumsal kimlik sisteminde passkey'i varsayılan yöntem yapıyor; SMS ile doğrulama kaldırılıyor.",
        "author": "Deniz Aydın",
        "date": "2026-10-22",
        "read_minutes": 5,
        "category": "Güvenlik",
        "kategori_slug": "guvenlik",
        "tone": "t4",
        "gorsel": {
            "dosya": "/haber/passkey.jpg",
            "alt": "Uzerinde anahtar sembolu bulunan mavi USB guvenlik anahtari",
            "atif": "Bautsch, CC0, Wikimedia Commons",
        },
        "kaynak": {
            "ad": "ÇözümPark",
            "url": "https://www.cozumpark.com/microsoft-entra-idde-parolasiz-kimlik-dogrulama-donemi-basliyor/",
        },
        "body": [
            "Microsoft, kurumsal kimlik sistemi Entra ID'de passkey'i (geçiş anahtarı) varsayılan kimlik doğrulama yöntemi haline getirme kararını duyurdu. Gerekçe açık: parola tabanlı giriş, kimlik avı ve kimlik bilgisi hırsızlığı karşısında giderek zayıflıyor.",
            "Plana göre SMS ve sesli arama ile doğrulama kademeli olarak kaldırılıyor. Bu yöntemleri kullanan hesaplar passkey için otomatik olarak yönlendirilecek; kullanıcılar kayıt adımını bir süre erteleyebilecek.",
            "Passkey'i parolanın hızlı bir alternatifi sanmak yaygın bir hata. Asıl fark şu: geçiş anahtarı, kaydedildiği sitenin kimliğine bağlıdır. Sahte bir siteye düşen kullanıcı, parolasını yazabilir ama passkey'ini \"yazamaz\" — tarayıcı o anahtarı başka bir alan adına sunmaz.",
            "Bu da kimlik avına karşı teknik bir bağışıklık anlamına geliyor. Kullanıcının dikkatine değil, protokolün kendisine dayanan bir koruma; ve tam olarak bu yüzden, dikkatin yetmediği durumlarda da çalışıyor.",
        ],
    },

    # ------------------------------------------------------------------
    # ENERJİ
    # ------------------------------------------------------------------
    {
        "slug": "batarya-depolama-gaz-turbinini-gecti",
        "title": "Batarya Depolama, Gaz Türbinini 43 Pazarın Tamamında Geçti",
        "excerpt": "Wood Mackenzie'nin analizine göre dört saatlik batarya sistemleri, yeni açık çevrimli gaz santrallerinden artık her yerde daha ucuz.",
        "author": "Mert Özkan",
        "date": "2026-10-08",
        "read_minutes": 5,
        "category": "Enerji",
        "kategori_slug": "enerji",
        "tone": "t3",
        "gorsel": {
            "dosya": "/haber/batarya.jpg",
            "alt": "Colde, gunes santralinin yanina sira sira dizilmis batarya depolama konteynerleri",
            "atif": "BLM California, kamu mali, Wikimedia Commons",
        },
        "kaynak": {
            "ad": "Wood Mackenzie",
            "url": "https://www.woodmac.com/press-releases/four-hour-battery-storage-now-beats-gas-peaking-on-cost-globally/",
        },
        "body": [
            "Wood Mackenzie'nin 8 Ekim'de yayımladığı küresel seviyelendirilmiş maliyet analizine göre, dört saatlik batarya depolama sistemleri, modellenen 43 pazarın tamamında yeni açık çevrimli gaz türbinlerinden daha düşük maliyetli hale geldi.",
            "Şirket değişimi iki ayrı eğilime bağlıyor: bir yanda gaz türbini tedarikindeki darboğaz ve yakıt fiyatlarındaki oynaklık puant üretim maliyetini yukarı itiyor, diğer yanda genişleyen batarya üretimi depolama maliyetini aşağı çekiyor. ABD'de dört saatlik depolamanın yeni gaz santrallerine göre yüzde 65 ila 75 daha ucuz olduğu belirtiliyor.",
            "Tabloda ters yönde bir veri de var: depolama yatırım maliyeti üç yılın ardından ilk kez, yaklaşık yüzde 2 arttı. Hücre fiyatlarının 2025'teki dip seviyeden yüzde 10 civarında toparlanması bunun başlıca nedeni. Avustralya, Japonya ve Filipinler'in kurulum maliyetleri ve ithalat vergileri nedeniyle pahalı kalmaya devam etmesi bekleniyor.",
            "Karşılaştırmanın megavatsaat başına ömür boyu maliyet üzerinden yapıldığını akılda tutmak gerekir; \"kurulumu daha ucuz\" demek değil. Yatırım kararı yine de şarj maliyeti, şebekeye erişim, kullanım oranı ve elektriğin tam olarak hangi saatlerde gerektiğine bağlı.",
        ],
    },
    {
        "slug": "epdk-sarj-istasyonu-depolama",
        "title": "Şarj İstasyonlarına Depolama İzni: Yeni Dönem Başlıyor",
        "excerpt": "EPDK düzenlemesi, şarj istasyonlarına entegre depolama tesislerinin istasyonun anlaşma gücünden yüksek güçle kurulmasına izin veriyor.",
        "author": "İpek Tanrıverdi",
        "date": "2026-09-26",
        "read_minutes": 4,
        "category": "Enerji",
        "kategori_slug": "enerji",
        "tone": "t3",
        "gorsel": {
            "dosya": "/haber/sarj.jpg",
            "alt": "Yol kenarinda yan yana duran iki hizli elektrikli arac sarj cihazi",
            "atif": "Daniel Mietchen, CC0, Wikimedia Commons",
        },
        "kaynak": {
            "ad": "Yeni Asır",
            "url": "https://www.yeniasir.com.tr/ekonomi/2026/09/26/elektrikli-arac-istasyonlarina-sarj-depolama-duzenlemesi",
        },
        "body": [
            "Enerji Piyasası Düzenleme Kurumu, elektrikli araç şarj istasyonlarına entegre edilen depolama tesisleri için yeni bir düzenleme yaptı. Düzenleme, bu tesislerin istasyonun şebekeyle yaptığı anlaşma gücünden daha yüksek bir şarj gücüyle kurulmasının önünü açıyor.",
            "Bunun pratik karşılığı şu: hızlı şarj istasyonu kurmak için şebekeden yüksek güç tahsisi beklemek zorunda kalmıyorsunuz. İstasyon, bataryasını düşük talepli saatlerde dolduruyor ve araç geldiğinde o depodan yüksek güçle veriyor.",
            "Şebeke güvenliği tarafında ise iki zorunluluk getiriliyor: otomatik güç kontrolü ve enerji kesme sistemleri. Yani depolama, şebekeyi zorlamaya başladığı anda devreden çıkabilmeli.",
            "Düzenlemenin özellikle otoyollar, akaryakıt istasyonları ve yoğun ticari alanlardaki hızlı şarj yatırımlarını kolaylaştırması hedefleniyor — yani menzil kaygısının en çok hissedildiği yerleri.",
        ],
    },
    {
        "slug": "ticari-depolama-turkiye-pazari",
        "title": "Ticari Ölçekli Depolama Sistemleri Türkiye Pazarına Giriyor",
        "excerpt": "Sıvı soğutmalı yeni bir ticari depolama sistemi Türkiye'de tanıtıldı; şarj altyapısı da hedef kullanım alanları arasında.",
        "author": "Mert Özkan",
        "date": "2026-10-01",
        "read_minutes": 3,
        "category": "Enerji",
        "kategori_slug": "enerji",
        "tone": "t3",
        "gorsel": {
            "dosya": "/haber/solar.jpg",
            "alt": "Daglarin onunde sira sira dizilmis gunes panelleri",
            "atif": "ABD Hava Kuvvetleri, kamu mali, Wikimedia Commons",
        },
        "kaynak": {
            "ad": "SolarGazete",
            "url": "https://solargazete.substack.com/p/solargazete-say-18-1-ekim-2026",
        },
        "body": [
            "Sungrow, sıvı soğutmalı ticari ve endüstriyel depolama sistemi PowerStack 255CS'yi Türkiye pazarına tanıttı. Sistem için yüzde 90'ın üzerinde çevrim verimliliği ve 20 yıla varan tasarım ömrü belirtiliyor.",
            "Ticari ölçekli depolamanın bu segmentte yaygınlaşması, yalnızca fabrika ve tesisleri ilgilendirmiyor. Üreticinin hedef kullanım alanları arasında elektrikli araç şarj altyapısı da sayılıyor.",
            "Tablo, şarj istasyonu düzenlemesiyle birlikte okunduğunda daha anlamlı hale geliyor: depolamanın maliyeti düştükçe ve mevzuat önünü açtıkça, şebekeden bağımsız çalışabilen şarj noktaları teknik bir merak olmaktan çıkıp ticari bir seçeneğe dönüşüyor.",
        ],
    },
]


# Kategori sayfalarinin menusu. Tek yerden tanimli ki navbar, kategori sayfasi
# ve API dogrulamasi ayni listeye baksin.
KATEGORILER = [
    {"slug": "yapay-zeka", "ad": "Yapay Zeka"},
    {"slug": "guvenlik", "ad": "Güvenlik"},
    {"slug": "enerji", "ad": "Enerji"},
]


def kategoriye_gore(kategori_slug: str):
    """Bir kategorideki yazilari dondurur (yoksa bos liste)."""
    return [p for p in POSTS if p["kategori_slug"] == kategori_slug]


def kategori_adi(kategori_slug: str):
    """Kategori slug'indan gorunen adi bulur (yoksa None)."""
    for k in KATEGORILER:
        if k["slug"] == kategori_slug:
            return k["ad"]
    return None
