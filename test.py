from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get(
"https://www.airbnb.com.tr/rooms/923263841627767180?adults=1&category_tag=Tag%3A8148&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1685011202&search_mode=flex_destinations_search&check_in=2024-01-02&check_out=2024-01-07&source_impression_id=p3_1704127415_tofNbfBc3rzawHhj&previous_page_section_name=1000"
)

def get_star_rating(driver):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='_16e70jgn']//div[@data-section-id='GUEST_FAVORITE_BANNER']")
            )
        )
        if element:
            print("element 1")
            span_element = WebDriverWait(element, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     "//div[@data-testid='pdp-reviews-highlight-banner-host-rating']")
                )
            )
            if span_element:
                print("span element 1")
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
                print("element 2")
                span_element = WebDriverWait(element, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[contains(@class, 'rk4wssy')]")
                    )
                )
                if span_element:
                    print("span element 2")
                    span = span_element.find_element(By.TAG_NAME, "span")
                    if span:
                        text = span_element.get_attribute("textContent")
                        match = re.search(r"(\d,\d)", text)
                        if match:
                            star_rating = match.group(0)
                            print("Star Rating:", star_rating)
                        else:
                            print(text)
        except Exception as e:
            print(e)



get_star_rating(driver)


