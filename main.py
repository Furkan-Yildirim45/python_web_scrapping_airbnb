import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def beautifulSoup():
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    selected_category = soup.find_all('span', string='Üçgen evler')
    if selected_category:
        for span in selected_category:
            print("Span içeriği:", span.text)
    else:
        print("Span etiketi bulunamadı.")


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
                    category_button = WebDriverWait(driver,100).until(
                        EC.visibility_of_element_located((By.XPATH, "//div[@id='categoryScroller']//span[contains(text(), '{}')]".format(category)))
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



def select_place_in_site(driver):
    dives = driver.find_elements(By.XPATH, "//div[@class=' dir dir-ltr']")
    unique_links = set()  # Set oluştur

    for div in dives:
        a_elements = div.find_elements(By.TAG_NAME, "a")
        for a_element in a_elements:
            link = a_element.get_attribute("href")
            unique_links.add(link)

    # Set içindeki benzersiz linkleri yazdır
    for link in unique_links:
        print("a elementi:", link)


if __name__ == '__main__':
    url = "https://www.airbnb.com.tr/"
    options = Options()
    # Selenium'un Chrome tarayıcısı üzerinden çalışması için gerekli ayarlar
    options.add_argument("--headless")  # Arka planda çalıştırma
    options.add_argument("--disable-gpu")  # GPU kullanmama
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    category = "Üçgen evler"
    select_category(driver=driver, selected_category=category) #tamamıyla ayarlandı!
    select_place_in_site(driver=driver) #test edilecek bu

# suanda işte categorilerden category seçebiliyorum ve tıklayabiliyorum ona.
# şimdi de model olarak verileri göstertip onları çekmem gerkeiyor!
# knk şimdi şöyle birşey var ben burdan yorumlara vs ulaşamıyorum yani burdan a etketine tıklatmalıyım ve ordan diğer sayfaya gitmem
# gerekiyor ki ordan verileri alabileyim!!!
# bunu nasıl yaparım ????

"""
knk burda şu şekilde bi durum söz konusu: burda birçok ilan var ve ben bunları elimle aşşagıya dogru kaydırdıgım her vakitte daha fazlası
çıkıyor ortaya tüm verileri alabilmek için sürekli olarak otomatik olarak aşşağıya kaydırılması ve o şekilde divleri alabilmem gerkeiyor!

şimdi modelin geldigi o divi bulucam
"""
