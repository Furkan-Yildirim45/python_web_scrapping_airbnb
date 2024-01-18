import os
import sqlite3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from product.product_operations import find_whole_product, open_product_url, get_url_and_location
from product.project_urls import Project_Url
from service.sql_service import ProductService, CommentService


def _terminal_UI():
    global product, product_id
    # burdan itibaren veritabanıyla birşeyler yapabilmeyi eklicem!
    product_service = ProductService()
    comment_service = CommentService()
    while True:
        print("1 : Tüm ürünleri getir.")
        print("2 : Sadece yorumları olan ürünleri getir.")
        print("3 : ID'si şu olan ürünü getir.")
        print("4 : ID'si şu olan ürünün yorumlarını getir.")
        print("5 : Lokasyonu şu olan ürünleri getir.")
        print("6 : Ürün fiyatı şu aralıktakileri getir.")
        print("7 : Ürün şundan ucuz aralıktakini getir.")
        print("8 : Ürün şundan pahalı aralıktakini getir.")
        print("9 : En çok yorumlanan ürünü getir.")
        print("10: En yüksek oy alan ürünü getir.")
        print("11: Tüm ürünleri sil.")
        print("12: Yorumları silinecek ürünü belirle.")
        print("13: Tüm yorumları sil.")
        print("q/Q: Çıkmak için kullanılacak seçenek.")

        user_input = (input("Lütfen bir seçenek seçiniz."))

        if user_input == '1':
            products = product_service.get_products()
            for product in products:
                print(f"ID: {product.product_id} - Title: {product.product_title}")
        elif user_input == '2':
            products_with_comments = product_service.get_products_with_comments()
            for product in products_with_comments:
                print(f"ID: {product.product_id} - Title: {product.product_title}")
        elif user_input == '3':
            product_id = int(input("ID'si girilecek ürünün ID'sini girin: "))
            product = product_service.get_product(product_id)
            print(f"ID: {product.product_id} - Title: {product.product_title}")
        elif user_input == '4':
            product_id = int(input("Yorumları getirilecek ürünün ID'sini girin: "))
            comments = comment_service.get_comments_for_product(product_id)
            for comment in comments:
                print(f"ID: {product_id} - Text: {comment.comment_text}")
        elif user_input == '5':
            location = input("Lokasyonu girin: ")
            products_by_location = product_service.get_products_by_location(location)
            for product in products_by_location:
                print(f"ID: {product.product_id} - Title: {product.product_title}")
        elif user_input == '6':
            min_price = float(input("Minimum fiyatı girin: "))
            max_price = float(input("Maksimum fiyatı girin: "))
            products_by_price_range = product_service.get_products_by_price_range(min_price, max_price)
            for product in products_by_price_range:
                print(f"ID: {product.product_id} - Title: {product.product_title} - Price: {product.product_price}")
            print("(en sağdaki fiyatlar indirimli fiyatlardır!)")
        elif user_input == '7':
            price = float(input("Bir fiyat belirleyin: "))
            products_cheaper_than = product_service.get_products_cheaper_than(price)
            for product in products_cheaper_than:
                print(f"ID: {product.product_id} - Title: {product.product_title} - Price: {product.product_price}")
        elif user_input == '8':
            price = float(input("Bir fiyat belirleyin: "))
            products_pricier_than = product_service.get_products_pricier_than(price)
            for product in products_pricier_than:
                print(f"ID: {product.product_id} - Title: {product.product_title} - Price: {product.product_price}")
        elif user_input == '9':
            most_reviewed_product = product_service.get_most_reviewed_product()
            if most_reviewed_product:
                print(f"En çok yorumlanan ürün: {most_reviewed_product.product_title}")
            else:
                print("Henüz yorumlanan ürün bulunamadı.")
        elif user_input == '10':
            highest_rated_product = product_service.get_highest_rated_product()
            if highest_rated_product:
                print(f"En yüksek oy alan ürün: {highest_rated_product.product_title}")
            else:
                print("Henüz oy alan ürün bulunamadı.")
        elif user_input == '11':
            product_service.delete_all_products()
            print("Tüm ürünler silindi.")
        elif user_input == '12':
            product_id = int(input("Yorumları silinecek ürünün ID'sini girin: "))
            comment_service.delete_all_comments_for_product(product_id)
            print(f"ID'si {product_id} olan ürüne ait tüm yorumlar silindi.")
        elif user_input == '13':
            confirm = input("Tüm yorumları silmek istediğinizden emin misiniz? (E/H): ")
            if confirm.lower() == 'e':
                comment_service.delete_all_comments()
                print("Tüm yorumlar silindi.")
            else:
                print("İşlem iptal edildi.")
        elif user_input.lower() == 'q':
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçenek. Lütfen tekrar deneyin.")


def _main_selenium_widget():
    options = Options()
    # Selenium'un Chrome tarayıcısı üzerinden çalışması için gerekli ayarlar
    options.add_argument("--headless")  # Arka planda çalıştırma
    options.add_argument("--disable-gpu")  # GPU kullanmama
    driver = webdriver.Chrome(options=options)
    driver.get(Project_Url.url_project_category)
    find_whole_product(driver)
    urls = get_url_and_location(driver) # ürünlerin urllerini alıyor
    urls = list(urls)
    #Tüm linkleri açmak için bu fonksiyona gidiyoruz ve budan dallanıyor.
    open_product_url(product_urls=urls, product_category=Project_Url.category, driver=driver)
    #işlem seçme konsol arayüzü kodu
    _terminal_UI()


if __name__ == '__main__':
    if os.path.exists('data_base.db'):
        conn = sqlite3.connect('data_base.db')
        cursor = conn.cursor()

        # Veritabanında tabloların varlığını kontrol etme
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        if tables:
            # Veriler varsa yapılacak işlemler
            print("Veritabanında veriler mevcut!")
            _terminal_UI()
        conn.close()
    else:
        print("Veritabanı dosyası bulunamadı.")
        _main_selenium_widget()


