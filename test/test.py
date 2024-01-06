import re

def get_min_price_with_decimal(price_string):
    # Fiyatları bulmak için regular expression kullanalım
    prices = re.findall(r'\d+\.*\d*', price_string)  # Ondalık kısmı da içeren ifadeleri bulalım
    prices = [price.replace(".", "") for price in prices]  # Nokta işaretini kaldıralım
    prices = [int(price) for price in prices]  # Sayısal ifadeleri integer'a çevirelim

    if prices:  # Eğer fiyatlar varsa
        return min(prices)  # En küçük fiyatı döndürelim
    else:
        return None  # Fiyat bulunamazsa None döndürelim


def get_product_price(price_string):
    # Fiyatları bulmak için regular expression kullanalım
    prices = re.findall(r'\d+\.*\d*', price_string)  # Ondalık kısmı da içeren ifadeleri bulalım
    prices = [price.replace(".", "") for price in prices]  # Nokta işaretini kaldıralım
    prices = [int(price) for price in prices]  # Sayısal ifadeleri integer'a çevirelim
    return min(prices)

# Örnek fiyat stringleri
prices = [
    '5.199 ₺',
    '1.030 ₺ 850 ₺  gece',
    '4.736 ₺ 4.000 ₺  gece',
    '10.000 ₺  gece',
    '1.000 ₺  gece',
    '6.701 ₺ 4.700 ₺  gece',
    '16.587 ₺  gece',
    '6.225 ₺  gece',
    '3.000 ₺  gece',
    '3.800 ₺ 3.040 ₺  gece',
    '3.000 ₺  gece',
    '5.148 ₺ 3.700 ₺  gece',
    '3.000 ₺  gece',
    '13.401 ₺  gece',
    '3.950 ₺  gece',
    '2.500 ₺  gece',
    '2.300 ₺  gece',
    '1.500 ₺  gece',
    '4.948 ₺',
    '2.100 ₺  gece'
]

"""# Her bir fiyatı işleyelim
for price_string in prices:
    min_price = get_min_price_with_decimal(price_string)
    if min_price is not None:
        print(f"En düşük fiyat: {min_price}")
    else:
        print("Fiyat bulunamadı.")"""

price = get_product_price(prices[2])
print(price)
# bu kodu veritabanına kaydetmeden önce veriyi çekince onu uygun formata getirtip en düşüğü kaydetmek ve sonra o şekilde test etmeyi dene
#!!!!!!!!