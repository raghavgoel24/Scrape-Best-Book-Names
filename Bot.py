from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
import time


web = "https://www.audible.in/adblbestsellers?ref=a_hp_t1_navTop_pl1cg0c1r0&pf_rd_p=418af36e-a72d-4eab-ae22-877834b57047&pf_rd_r=VD6B4MJTBP0PY25DGWA9"
driver = webdriver.Chrome("D:\Projects\1. Scrape Book Names using Selenium\chromedriver.exe")
driver.get(web)
driver.maximize_window()

#pagination
pagination = driver.find_element(By.XPATH, "//ul[contains(@class, 'pagingElements')]")
pages = pagination.find_elements(By.TAG_NAME, "li")
last_page = int(pages[-2].text)

current_page = 1

book_title = []
book_author = []
book_length = []

while current_page <= last_page:
    time.sleep(2)
    container = driver.find_element(By.CLASS_NAME, "adbl-impression-container ")
    products = container.find_elements(By.XPATH, '//li[contains(@class, "productListItem")]')

    for product in products:
        book_title.append(product.find_element(By.XPATH, ".//h3[contains(@class, 'bc-heading')]").text)
        book_author.append(product.find_element(By.XPATH, ".//li[contains(@class, 'authorLabel')]").text)
        book_length.append(product.find_element(By.XPATH, ".//li[contains(@class, 'runtimeLabel')]").text)

    current_page = current_page + 1    
    next_page = driver.find_element(By.XPATH, "//span[contains(@class, 'nextButton')]")
    next_page.click()

driver.quit()

df = pd.DataFrame({'Title':book_title, 'Author':book_author, 'Length':book_length})
df.to_csv('books_pagination.csv', index=False)
print(df)
