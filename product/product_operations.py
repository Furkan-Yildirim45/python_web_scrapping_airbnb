import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from model.comment_model import Comment_Model
from model.product_model import Product_Model


def find_whole_product(driver):
    scroll_to_bottom(driver)
    button_div = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, "//main[@id='site-content']//div[@aria-live='polite' and contains(@class, 'df8mizf')]"))
    )
    if button_div:
        button = button_div.find_element(By.XPATH, "//button[contains(@class, 'l1ovpqvx')]")
        if button:
            print(button.get_attribute("class"))
            driver.execute_script("arguments[0].click();", button)
            print("butona tıklanıldı")
            current_products = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
                (By.XPATH, "//div[@aria-live='polite']//div[@class=' dir dir-ltr']")))
            print(len(current_products))
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                new_products = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
                    (By.XPATH, "//div[@aria-live='polite']//div[@class=' dir dir-ltr']")))
                if len(new_products) > len(current_products):
                    print("yeni içerikler yüklendi")
                    current_products = new_products
                    print(len(current_products))
                else:
                    print("Yeni içerikler yüklenmedi veya tüm içerikler yüklendi.")
                    print(len(current_products))
                    break

            scroll_to_bottom(driver)
def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)


def get_star_rating(driver):
    try:
        banner_xpath = "//div[@class='_16e70jgn']//div[@data-section-id='GUEST_FAVORITE_BANNER']"
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, banner_xpath)))

        if element:
            span_element = WebDriverWait(element, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                            "//div[@data-testid='pdp-reviews-highlight-banner-host-rating']")))
            if span_element:
                star_rating = extract_star_rating(span_element)
                return star_rating
        return None

    except Exception as e:
        try:
            overview_xpath = "//div[@class='_16e70jgn']//div[@data-section-id='OVERVIEW_DEFAULT_V2']"
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, overview_xpath)))

            if element:
                span_element = WebDriverWait(element, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                                "//div[contains(@class, 'rk4wssy')]")))
                if span_element:
                    star_rating = extract_star_rating(span_element)
                    return star_rating
            return None

        except Exception as e:
            print(e)
            return None
def extract_star_rating(element):
    span = element.find_element(By.TAG_NAME, "span")
    if span:
        text = span.get_attribute("textContent")
        match = re.search(r"(\d,\d)", text)
        if match:
            star_rating = match.group(0)
            print("Star Rating:", star_rating)
            return star_rating
        else:
            print(text)
            return text
    return None


def get_comment_info(driver):
    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[@data-testid='pdp-reviews-modal-scrollable-panel']")
        )
    )
    if element:
        comment_list = []
        dives = element.find_elements(By.XPATH, "//div[@class='r1are2x1 atm_gq_1vi7ecw dir dir-ltr']")
        if dives:
            for div in dives:
                name = extract_name(div)
                star_point = extract_star_point(div)
                comment_text = extract_comment_text(div)
                comment_list.append(Comment_Model(comment_point=star_point, comment=comment_text, name=name))
        return comment_list
    return None
def extract_name(div):
    h3_tags = div.find_elements(By.TAG_NAME, 'h3')
    if h3_tags:
        for h3_tag in h3_tags:
            print("Name:", h3_tag.text)
            return h3_tag.text
    return ""
def extract_star_point(div):
    span_div = div.find_element(By.XPATH, "//div[@class='c5dn5hn atm_9s_1txwivl atm_cx_t94yts dir dir-ltr']")
    if span_div:
        span_star_point = span_div.find_elements(By.TAG_NAME, "span")
        if span_star_point:
            for span in span_star_point:
                print("Yıldız Sayısı:", span.get_attribute("textContent"))
                return span.get_attribute("textContent")
    return ""
def extract_comment_text(div):
    comment_text = div.find_element(By.XPATH, ".//span[@class='ll4r2nl atm_kd_pg2kvz_1bqn0at dir dir-ltr']").text
    print("Yorum:", comment_text)
    return comment_text


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


def get_url_and_location(driver):
    driver.implicitly_wait(0.05)
    unique_urls = set()
    unique_locations = set()
    divs = driver.find_elements(By.XPATH, "//div[@aria-live='polite']//div[@class=' dir dir-ltr']")
    if divs:
        for div in divs:
            unique_urls.update(extract_urls(div))
            unique_locations.update(extract_locations(div))
        return list(unique_urls), list(unique_locations)
    return None, None
def extract_urls(div):
    a_tags = div.find_elements(By.TAG_NAME, 'a')
    urls = [a_tag.get_attribute("href") for a_tag in a_tags]
    return urls
def extract_locations(div):
    locations = div.find_elements(By.XPATH, ".//div[@data-testid='listing-card-title']")
    location_texts = [location.get_attribute("textContent") for location in locations]
    return location_texts


def get_product_price(driver):
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH,
                                        "//div[@dir='ltr']//div[@class='_1s21a6e2']//div["
                                        "@data-testid='book-it-default']//div[@class='_1jo4hgw']"))
    )
    if element:
        text = extract_text_from_spans(element)
        print(text)
        return text
def extract_text_from_spans(element):
    spans = element.find_elements(By.TAG_NAME, "span")
    text_list = [span.text for span in spans]
    combined_text = ' '.join(text_list)
    return combined_text


def open_product_url(product_urls, product_category, driver):
    if product_urls is not None:
        print("urls none degil")
        for product_url in product_urls:
            driver.get(product_url)
            print("-----------------------------------------")
            comment_list = get_comments(driver)
            star_rating = get_star_rating(driver)
            print(driver.title)
            model = Product_Model(
                product_url=product_url,
                product_title=driver.title,
                product_price=get_product_price(driver),
                product_category=product_category,
                product_comments=comment_list,
                product_star_point=star_rating,
            )
