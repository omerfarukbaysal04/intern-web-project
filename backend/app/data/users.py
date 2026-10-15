"""Sahte kullanici verisi (demo). Veritabani yok -- posts.py gibi dict.

DIKKAT: parolalar duz metin ve oturum cerezi basit (imzasiz). Gercek bir
uygulamada ASLA boyle yapilmaz; burada bilerek basit tutuldu cunku bu bir
guvenlik DEMO'su (ornegin XSS ile cerez calmayi gosterebilmek icin).
"""

USERS = {
    "omerfaruk": {
        "parola": "1234",
        "email": "omerfaruk@teknopanorama.test",
        "uyelik": "Premium",
        "ad": "Ömer Faruk",
    },
    "deniz": {
        "parola": "deniz123",
        "email": "deniz@teknopanorama.test",
        "uyelik": "Standart",
        "ad": "Deniz Aydın",
    },
    "selin": {
        "parola": "selin123",
        "email": "selin@teknopanorama.test",
        "uyelik": "Standart",
        "ad": "Selin Korkmaz",
    },
}
