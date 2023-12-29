from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from model.product_model import Product_Model
import re


def select_category(driver, selected_category):
    div_for_label = driver.find_element(By.XPATH, "//div[@id='categoryScroller']")
    wait = WebDriverWait(driver, 10)
    scroll_button = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//button[@data-shared-element-id='next-button' and @type='button']")))

    if div_for_label:
        categories = div_for_label.text.split("\n")
        print(categories)
        for category in categories:
            if category == selected_category:
                print(f"Kategori bulundu: {selected_category}")
                while True:
                    category_button = WebDriverWait(driver, 100).until(
                        EC.visibility_of_element_located(
                            (By.XPATH, "//div[@id='categoryScroller']//span[contains(text(), '{}')]".format(category)))
                    )
                    if category_button:
                        print("category button bulundu")
                        if category_button.text == category:
                            print("Üçgen evler kategorisi bulundu")
                            driver.execute_script("arguments[0].click();", category_button)
                            print("{} kategorisine tıklandı".format(category_button.text))
                            return driver.current_url
                        else:
                            print("Şu anki kategori 'Üçgen evler' değil, devam ediliyor...")
                            scroll_button.click()
                            print("Scroll butonuna tıklandı")
                    else:
                        print("category button bulunamadı")
                        scroll_button.click()
                        print("Scroll butonuna tıklandı")


def get_a_element(driver):
    driver.implicitly_wait(0.05)
    unique_urls = set()
    divs = driver.find_elements(By.XPATH, "//div[@aria-live='polite']//div[@class=' dir dir-ltr']")
    if divs:
        for div in divs:
            a_tags = div.find_elements(By.TAG_NAME, 'a')
            if a_tags:
                for a_tag in a_tags:
                    #print(a_tag.get_attribute('href'))
                    unique_urls.add(a_tag.get_attribute("href"))
        return unique_urls
    return None

def get_product_price(driver):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,
                                        "//div[@dir='ltr']//div[@class='_1s21a6e2']//div["
                                        "@data-testid='book-it-default']//div[@class='_1jo4hgw']"))
    )
    if element:
        spans = element.find_elements(By.TAG_NAME, "span")
        text_list = [span.text for span in spans]
        combined_text = ' '.join(text_list)
        print(combined_text)
        return combined_text

def open_product_url(product_urls, product_category):
    if product_urls != None:
        print("urls none degil")
        for product_url in product_urls:
            driver.get(product_url)
            print("-----------------------------------------")
            print(product_url)

            #ürün ismi ve konum alma
            print(driver.title)
            # Fiyatın yüklenmesini bekleyin
            get_product_price(driver=driver)
            #konum bilgisi alınıcak!!!

            # model = Product_Model(product_title=title,product_location=location,product_url=product_url,product_category=product_category,)



if __name__ == '__main__':
    main_url = "https://www.airbnb.com.tr/"
    url_ucgen_evler = "https://www.airbnb.com.tr/?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&search_mode=flex_destinations_search&flexible_trip_lengths%5B%5D=one_week&location_search=MIN_MAP_BOUNDS&monthly_start_date=2024-01-01&monthly_length=3&price_filter_input_type=0&channel=EXPLORE&search_type=category_change&price_filter_num_nights=5&category_tag=Tag%3A8148"
    options = Options()
    # Selenium'un Chrome tarayıcısı üzerinden çalışması için gerekli ayarlar
    options.add_argument("--headless")  # Arka planda çalıştırma
    options.add_argument("--disable-gpu")  # GPU kullanmama
    driver = webdriver.Chrome(options=options)
    driver.get(url_ucgen_evler)
    category = "Üçgen evler"
    #get_a_element(driver=driver)
    open_product_url(product_urls=get_a_element(driver), product_category=category)

# todo: knk burda selected category i kapatıyorum eger o tıklamada url i yeniden alabilirsem açarım!
# todo: knk bazı divleri bulamıyor! ki a elementlerini bulamıyor!
