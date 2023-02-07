import selenium
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By

# Generate url for products
def get_url(product):
    product = product.replace(' ', '%20')
    template = 'https://www.aliexpress.com/wholesale?SearchText={}'
    url = template.format(product)
    return url

def automate_scroll(driver):
    # To automate the scroll up and scroll down the website
    # Define an initial value
    temp_height=0
    while True:
        #Looping down the scroll bar
        driver.execute_script("window.scrollBy(0,1000)")
        #sleep and let the scroll bar react
        time.sleep(5)
        #Get the distance of the current scroll bar from the top
        check_height = driver.execute_script("return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
        #If the two are equal to the end
        if check_height==temp_height:
            break
        temp_height=check_height
        
    time.sleep(10)

def get_all_products_aliexpress(card):
    pImg = card.find('img', 'manhattan--img--36QXbtQ product-img')
    try:
        product_image = 'https:'+pImg['src']
    except TypeError:
        product_image = ''
    
    product_name = card.find('div', 'manhattan--title--24F0J-G cards--title--2rMisuY').text.encode('ascii', 'ignore')
    product_name = str(product_name, 'utf-8').strip()
    
    product_price = card.find('div', 'manhattan--price--WvaUgDY').text.strip()

    anchor_tag = card.get('href')
    product_buy_link = 'https:'+anchor_tag
    
    # create a tuple to save the details
    aliexpress_info = (product_image, product_name, product_price, product_buy_link)
    return aliexpress_info

def main(product):
    records_aliexpress = []
    url_aliexpress = get_url(product)
    # setting some configuration for our driver
    driver = webdriver.Chrome(executable_path='C:\\chrome_driver_directory\\chromedriver.exe')
    driver.get(url_aliexpress)
    driver.maximize_window()
    time.sleep(3)
    
    automate_scroll(driver)

    # Generate the BeautifulSoup Object
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    aliexpress_cards = soup.find_all('a', 'manhattan--container--1lP57Ag cards--gallery--2o6yJVt')
    
    for aliexpress_everyProduct in aliexpress_cards:
        aliexpress_productDetails = get_all_products_aliexpress(aliexpress_everyProduct)
        records_aliexpress.append(aliexpress_productDetails)
        
    # Here we are using Pandas Data Frame to save products information in a csv file
    col = ['Product_Image', 'Product_Name', 'Product_Price', 'Product_Buy_Link']
    aliexpress_data = pd.DataFrame (records_aliexpress, columns=col)
    aliexpress_data.to_csv('C:\\your_directory\\AliExpressData.csv')
    
    driver.quit()

product = input('Enter Product You Are Looking For: ')
main(product)