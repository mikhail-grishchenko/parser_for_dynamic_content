import pandas as pd
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

driver = Chrome(executable_path='c:/driver/chromedriver.exe')
driver.get('https://www.marvel.com/characters')

num_pages =1
max_num_pages = 74
name_list = []
link_list = []

while num_pages <= max_num_pages:
    element = driver.page_source
    bs = BeautifulSoup(element,"lxml")
    marvel_list = bs.find('div', class_='content-grid content-grid__6').findAll('div', class_='mvl-card mvl-card--explore')

    for elem in marvel_list:
        el_name = elem.find('p', class_='card-body__headline').text
        el_href = elem.find('a', class_='explore__link').get('href')
        name_list.append(str(el_name))
        link_list.append("https://www.marvel.com" + str(el_href))
    num_pages += 1

    cursor = driver.find_element(By.CSS_SELECTOR, "#filter_grid-7 > div > div.content-grid.content-grid__6 > div:nth-child(3) > nav > ul > li.pagination__item.pagination__item-nav.pagination__item-nav-next > span")
    cursor.click()
    time.sleep(3)

names = pd.Series(name_list)
links = pd.Series(link_list)
df = pd.DataFrame([names,links])
df2 = df.T
df2.columns = ['names', 'links']
df2.to_csv('marvel_list.csv')

driver.quit()