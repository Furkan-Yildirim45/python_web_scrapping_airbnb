from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get(
    "https://www.airbnb.com.tr/rooms/675353327273735596?adults=1&category_tag=Tag%3A8148&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1488398046&search_mode=flex_destinations_search&check_in=2024-01-06&check_out=2024-01-11&source_impression_id=p3_1704024296_QJCys5NmoXwlrHzC&previous_page_section_name=1000&federated_search_id=14b76631-b293-43bd-9d88-b293b5f44392"
)


def get_comment_info(driver):
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[@data-testid='pdp-reviews-modal-scrollable-panel']")
        )
    )
    if element:
        dives = element.find_elements(By.XPATH, "//div[@class='r1are2x1 atm_gq_1vi7ecw dir dir-ltr']")
        if dives:
            for div in dives:
                # h3 isim
                h3_tags = div.find_elements(By.TAG_NAME, 'h3')
                if h3_tags:
                    for h3_tag in h3_tags:
                        print("Başlık:", h3_tag.text)

                # span yıldız
                span_div = div.find_element(By.XPATH,"//div[@class='c5dn5hn atm_9s_1txwivl atm_cx_t94yts dir dir-ltr']")
                if span_div:
                    span_star_point = span_div.find_elements(By.TAG_NAME, "span")
                    if span_star_point:
                        for span in span_star_point:
                            print("Yıldız Sayısı:", span.get_attribute("textContent"))

                # span yorum
                comment_text = div.find_element(By.XPATH,".//span[@class='ll4r2nl atm_kd_pg2kvz_1bqn0at dir dir-ltr']").text
                print("Yorum:", comment_text)


def get_comments(driver):
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
                get_comment_info(driver)
        else:
            print("a etiketi bulunamadı.")
    else:
        print("Henüz değerlendirme mevcut değil.")
        #burda yorumları boş göndericeksin!


get_comments(driver)
