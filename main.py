import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def select_category(driver, selected_category):
    div_for_label = driver.find_element(By.XPATH, "//div[@id='categoryScroller']")
    scroll_button = div_for_label.find_element(By.XPATH, "//button[@data-shared-element-id='next-button']")

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
                            break
                        else:
                            print("Şu anki kategori 'Üçgen evler' değil, devam ediliyor...")
                            scroll_button.click()
                            print("Scroll butonuna tıklandı")
                    else:
                        print("category button bulunamadı")
                        scroll_button.click()
                        print("Scroll butonuna tıklandı")

def setNewUrl(driver):
    a_tags = driver.find_elements(By.TAG_NAME, 'a')
    a_elements = []
    for a_tag in a_tags:
        href_value = a_tag.get_attribute('href')
        a_elements.append(href_value)
    return a_elements[0]


def get_a_element(url):
    driver.get(url)
    dives = driver.find_elements(By.XPATH, "//div[@aria-live='polite']")
    if dives:
        unique_links = set()  # Set oluştur
        for div in dives:
            a_tags = div.find_elements(By.TAG_NAME, 'a')
            if a_tags:
                print("a element bulundu")
                for a_tag in a_tags:
                    href_value = a_tag.get_attribute('href')
                    if href_value:
                        print(href_value)
            else:
                print("a elementi bulunamadı.")


if __name__ == '__main__':
    url = "https://www.airbnb.com.tr/"
    options = Options()
    # Selenium'un Chrome tarayıcısı üzerinden çalışması için gerekli ayarlar
    options.add_argument("--headless")  # Arka planda çalıştırma
    options.add_argument("--disable-gpu")  # GPU kullanmama
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    category = "Üçgen evler"
    select_category(driver=driver, selected_category=category)  # tamamıyla ayarlandı!
    new_url = setNewUrl(driver=driver)
    get_a_element(url=new_url) #a etiketini buluyor bazen bulamayabiliyor!


#a etiketini buluyorum. onu alıp içine girmek var şimdi!!!!
