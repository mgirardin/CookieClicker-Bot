from selenium import webdriver
from time import sleep
import re
from word2number import w2n

def qtd_cookies():
    return element_qtdCookies.text.partition(' ')[0]

def product_price(element):
    content = element.find_element_by_class_name("content")
    price = element.find_element_by_class_name("price").text
    price_text = price.partition(' ')[0]
    
    if(price_text == ""):
        return ''
    
    try:
        price_text = price_text.replace(',', '')
        price_float = float(price_text.strip())
    except:
        price_float = 0
    
    if(price.partition(' ')[2] != ""):
        multiplier = w2n.word_to_num(price.partition(' ')[2])
        price_float*=multiplier
    return price_float

def is_product_available(element):
    element_class = element.get_attribute("class")
    element_class = element_class.partition(' ')[2]
    
    isEnabled = (element_class.partition(' ')[0] == "unlocked")
    isUnlocked = (element_class.partition(' ')[2] == "enabled")
    
    return isEnabled and isUnlocked

def buy_item():
    best_item_index = -1
    best_item_price = 1
    is_available = [False for i in range(0,product_size)]
    for i in range(0, product_size):
        if(is_product_available(product_array[i])):
            is_available[i] = True

    for i in range(0, product_size):
        if(product_price(product_array[i])==''):
            continue
        cur_price = float(product_price(product_array[i]))
        firstAvailable = best_item_index==-1
        betterChoice = (cur_price/int(best_item_price)<=2**(i-best_item_index)) 
        if(firstAvailable or betterChoice):
            best_item_index=i
            best_item_price=product_price(product_array[i])
    if(best_item_index!=-1 and is_available[best_item_index]):
        product_array[best_item_index].click()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=selenium_data_dir")
#chrome_options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("https://orteil.dashnet.org/cookieclicker/")
sleep(10)
element_cookie = driver.find_element_by_id("bigCookie")
element_qtdCookies = driver.find_element_by_id("cookies")
product_size = 16

product_array = []
for i in range(0, product_size):
    product_array.append(driver.find_element_by_id("product" + str(i)))

while True:
    try:
        element_cookie.click()
        if(int(qtd_cookies())>50):
            buy_item()
    except:
        print("Impossivel de apertar")
    print(qtd_cookies())


