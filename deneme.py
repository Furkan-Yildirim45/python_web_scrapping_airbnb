from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get(
    "https://www.airbnb.com.tr/rooms/51831969?adults=1&category_tag=Tag%3A8148&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1245037032&search_mode=flex_destinations_search&check_in=2024-01-07&check_out=2024-01-12&source_impression_id=p3_1703769971_od%2B6wdFGREA5fMYL&previous_page_section_name=1000&federated_search_id=0ff07fac-5c90-4c73-a69a-8616169ff782")

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@dir='ltr']//div[@class='_1s21a6e2']//div[@class='_1cvivhm']//div[@class='_m6lwl6']"))
)
if element:
    print("element")
