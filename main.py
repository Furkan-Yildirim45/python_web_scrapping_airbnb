from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from model.comment_model import Comment_Model
from model.product_model import Product_Model
import re


def get_star_rating(driver):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='_16e70jgn']//div[@data-section-id='GUEST_FAVORITE_BANNER']")
            )
        )
        if element:
            span_element = WebDriverWait(element, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     "//div[@data-testid='pdp-reviews-highlight-banner-host-rating']")
                )
            )
            if span_element:
                span = span_element.find_element(By.TAG_NAME, "span")
                if span:
                    text = span_element.get_attribute("textContent")
                    match = re.search(r"(\d,\d)", text)
                    if match:
                        star_rating = match.group(0)
                        print("Star Rating:", star_rating)
                    else:
                        print(text)
    except Exception as _:
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='_16e70jgn']//div[@data-section-id='OVERVIEW_DEFAULT_V2']")
                )
            )
            if element:
                span_element = WebDriverWait(element, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[contains(@class, 'rk4wssy')]")
                    )
                )
                if span_element:
                    span = span_element.find_element(By.TAG_NAME, "span")
                    if span:
                        text = span_element.get_attribute("textContent")
                        print("Star Rating:", text)

        except Exception as e:
            print(e)


def get_comment_info(driver):
    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[@data-testid='pdp-reviews-modal-scrollable-panel']")
        )
    )
    if element:
        dives = element.find_elements(By.XPATH, "//div[@class='r1are2x1 atm_gq_1vi7ecw dir dir-ltr']")
        if dives:
            comment_list = []
            name = ""
            star_point = ""
            for div in dives:
                # h3 isim
                h3_tags = div.find_elements(By.TAG_NAME, 'h3')
                if h3_tags:
                    for h3_tag in h3_tags:
                        print("Name:", h3_tag.text)
                        name = h3_tag.text
                # span yıldız
                span_div = div.find_element(By.XPATH,
                                            "//div[@class='c5dn5hn atm_9s_1txwivl atm_cx_t94yts dir dir-ltr']")
                if span_div:
                    span_star_point = span_div.find_elements(By.TAG_NAME, "span")
                    if span_star_point:
                        for span in span_star_point:
                            print("Yıldız Sayısı:", span.get_attribute("textContent"))
                            star_point = span.get_attribute("textContent")

                # span yorum
                comment_text = div.find_element(By.XPATH,
                                                ".//span[@class='ll4r2nl atm_kd_pg2kvz_1bqn0at dir dir-ltr']").text
                print("Yorum:", comment_text)
                comment_list.append(Comment_Model(comment_point=star_point, comment=comment_text, name=name))
            return comment_list
    return None


def get_comments(driver):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='_16e70jgn']//div[@data-section-id='GUEST_FAVORITE_BANNER']")
            )
        )

        if element:
            a_tags = WebDriverWait(element, 10).until(
                EC.visibility_of_all_elements_located(
                    (By.TAG_NAME, "a")
                )
            )

            if a_tags:
                for a_tag in a_tags:
                    print("Href:", a_tag.get_attribute('href'))
                    comment_url = a_tag.get_attribute("href")
                    driver.get(comment_url)
                    return get_comment_info(driver)
            else:
                print("a etiketi bulunamadı.")
        else:
            print("Henüz değerlendirme mevcut değil.")
    except Exception as e:
        print("Henüz değerlendirme mevcut değil.")
    return None


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


def get_url_and_location(driver):
    driver.implicitly_wait(0.05)
    unique_urls = set()
    unique_locations = set()
    divs = driver.find_elements(By.XPATH, "//div[@aria-live='polite']//div[@class=' dir dir-ltr']")
    if divs:
        for div in divs:
            a_tags = div.find_elements(By.TAG_NAME, 'a')
            if a_tags:
                for a_tag in a_tags:
                    # print(a_tag.get_attribute('href'))
                    unique_urls.add(a_tag.get_attribute("href"))
            locations = div.find_elements(By.XPATH, ".//div[@data-testid='listing-card-title']")
            if locations:
                for location in locations:
                    # print(location.get_attribute("textContent"))
                    unique_locations.add(location.get_attribute("textContent"))
        return unique_urls, unique_locations
    return None


def get_product_price(driver):
    element = WebDriverWait(driver, 20).until(
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


def get_product_star_point(driver):
    element = driver.find_element(By.XPATH, "//div[@class='_16e70jgn']")
    if element:
        print("element")


def open_product_url(product_urls, product_category, product_locations):
    if product_urls != None:
        print("urls none degil")
        for product_url in product_urls:
            driver.get(product_url)
            print("-----------------------------------------")
            print(product_url)

            # ürün ismi ve konum alma
            print(driver.title)
            # Fiyatın yüklenmesini bekleyin
            get_product_price(driver=driver)

            # yorumlar
            comment_list = get_comments(driver)  # none olabilir

            # prduct star raiting
            get_star_rating(driver)
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
    urls, locations = get_url_and_location(driver)
    open_product_url(product_urls=urls, product_category=category, product_locations=locations)

# todo: knk burda selected category i kapatıyorum eger o tıklamada url i yeniden alabilirsem açarım!
# todo: knk bazı divleri bulamıyor! ki a elementlerini bulamıyor!


# todo: eklemem gerekenlerde baba tüm ürünleri ve tüm yorumları almıyor en son buna bir bak!
