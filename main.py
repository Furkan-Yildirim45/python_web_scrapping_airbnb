from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from product.product_operations import find_whole_product, open_product_url, get_url_and_location
from product.project_urls import Project_Url
from service.sql_service import Sql_Service

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





