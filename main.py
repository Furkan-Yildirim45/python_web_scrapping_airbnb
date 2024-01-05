from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from product.product_operations import find_whole_product, open_product_url, get_url_and_location
from product.project_urls import Project_Url
from service.sql_service import ProductService, CommentService

if __name__ == '__main__':
    options = Options()
    # Selenium'un Chrome tarayıcısı üzerinden çalışması için gerekli ayarlar
    options.add_argument("--headless")  # Arka planda çalıştırma
    options.add_argument("--disable-gpu")  # GPU kullanmama
    driver = webdriver.Chrome(options=options)
    driver.get(Project_Url.url_project_category)
    find_whole_product(driver)
    urls, locations = get_url_and_location(driver)
    urls = list(urls)
    locations = list(locations)
    open_product_url(product_urls=urls, product_category=Project_Url.category,driver=driver)

    #burdan itibaren veritabanıyla birşeyler yapabilmeyi eklicem!
    product_service = ProductService()
    comment_service = CommentService()
    while True:
        print("1 :Tüm ürünleri getir.")
        print("2 :Sadece yorumları olan ürünleri getir.")
        print("3 :Id si şu olan ürünü getir.")
        print("4 :Id si şu olan ürünün yorumlarını getir.")
        print("5 :Lokasyonu şu olan ürünleri getir.")
        print("6 :ürün fiyatı şu aralıktakileri getir.")
        print("7 :ürün şundan ucuz veya fazla aralıktakini getir.")
        print("8 :ürün şundan pahalı veya fazla aralıktakini getir.")
        print("9 :tüm ürünleri sil.")
        print("q/Q :Çıkmak için kullanıcağınız seçenektir.")
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
                print(f"ID: {comment.comment_id} - Text: {comment.comment_text}")
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
            product_service.delete_all_products()
        elif user_input == '10':
            product_id = int(input("Yorumları silinecek ürünün ID'sini girin: "))
            comment_service.delete_all_comments_for_product(product_id)
            print(f"ID'si {product_id} olan ürüne ait tüm yorumlar silindi.")
        elif user_input == '11':
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


