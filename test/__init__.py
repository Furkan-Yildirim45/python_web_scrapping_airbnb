import sqlite3

if __name__ == '__main__':
    """conn = sqlite3.connect('data_base.db')
    cursor = conn.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS Kitaplar (id INTEGER PRIMARY KEY, ad TEXT, yazar TEXT, sayfa_sayisi INTEGER)''')
    conn.commit()

    # Veritabanına bağlanma
    kitap_adi = "Yeni Kitap"
    yazar = "Yazarın İsmi"
    sayfa_sayisi = 250

    # Veritabanına veri eklemek için INSERT sorgusu
    cursor.execute("INSERT INTO Kitaplar (ad, yazar, sayfa_sayisi) VALUES (?, ?, ?)", (kitap_adi, yazar, sayfa_sayisi))

    # Tablo içeriğini sorgulama
    cursor.execute("SELECT * FROM Kitaplar")
    veriler = cursor.fetchall()
    print(veriler)

    # Bağlantıyı kapatma
    conn.close()"""

    conn = sqlite3.connect('data_base.db')
    cursor = conn.cursor()

    # Ürünler tablosunu oluşturma
    cursor.execute('''CREATE TABLE IF NOT EXISTS Products (
                        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_url TEXT,
                        product_title TEXT,
                        product_price REAL,
                        product_category TEXT,
                        product_star_point REAL
                    )''')

    # Yorumlar tablosunu oluşturma
    cursor.execute('''CREATE TABLE IF NOT EXISTS ProductComments (
                        comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_id INTEGER,
                        comment TEXT,
                        FOREIGN KEY(product_id) REFERENCES Products(product_id)
                    )''')

    # Değişiklikleri kaydetme
    conn.commit()

    # Örnek bir ürün eklemek
    cursor.execute('''INSERT INTO Products (product_url, product_title, product_price, product_category, product_star_point) 
                    VALUES (?, ?, ?, ?, ?)''', ('www.example.com/product1', 'Ürün 1', 49.99, 'Kategori A', 4.5))

    conn.commit()

    product_id = 1  # Örnek olarak bir ürün ID'si varsayalım

    # Yorumlar listesi
    yorumlar = [
        "Bu ürün harika!",
        "Fiyat performansı iyi.",
        "Kargo biraz geç geldi."
    ]

    # Her bir yorumu ayrı bir comment olarak eklemek
    for yorum in yorumlar:
        cursor.execute("INSERT INTO ProductComments (product_id, comment) VALUES (?, ?)", (product_id, yorum))
    conn.commit()

    cursor.execute("SELECT * FROM ProductComments WHERE product_id = ?",(product_id,))
    id_li_yorumlar = cursor.fetchall()

    for yorum in id_li_yorumlar:
        print(yorum)






"""    # Eklediğimiz ürünün ID'sini almak için
    product_id = cursor.lastrowid

    # Örnek yorumlar eklemek
    yorumlar = [
        ('Çok iyi bir ürün!',),
        ('Fiyat performans ürünü değil.',),
        ('Beklentilerimi karşıladı.',)
    ]

    for yorum in yorumlar:
        cursor.execute('''INSERT INTO ProductComments (product_id, comment) VALUES (?, ?)''', (product_id, yorum[0]))

    # Değişiklikleri kaydetme
    conn.commit()

    # Bağlantıyı kapatma
    conn.close()"""