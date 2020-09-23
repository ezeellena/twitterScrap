from email import utils
from bs4 import BeautifulSoup
from pip._internal.network import session
from selenium import webdriver
import time
from PIL import Image
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# create a new Chrome session
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from facebook_scraper import facebook_scraper as fb


driver = webdriver.Chrome()
driver.implicitly_wait(30)
driver.maximize_window()

# navigate to the application home page
driver.get("https://www.facebook.com/login")

# get the username textbox
login_field = driver.find_element_by_id("email")
login_field.clear()

# enter username
login_field.send_keys("ezequielellena_003@hotmail.com")
time.sleep(1)

# get the password textbox
password_field = driver.find_element_by_id("pass")
password_field.clear()

# enter password
password_field.send_keys("sdfgcv.1234")
time.sleep(1)
password_field.submit()

page_name = "BillGates"

time.sleep(5)
REQUEST_URL = f'https://m.facebook.com/{page_name}'
driver.get(REQUEST_URL)
time.sleep(2)
scrolls = 15

for i in range(1,scrolls):
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
  time.sleep(3)
  page = driver.page_source
  soup = BeautifulSoup(page, "html.parser")
  #names = soup.find_all('div', {"class": ['du4w35lb k4urcfbm l9j0dhe7 sjgh65i0']})
  publicaciones = soup.find_all('div', {"class": '_3drp'})



  for publicacion in publicaciones:
      print(publicacion.find('span', {"data-sigil": "comments-token"}).text)
      links = publicacion.find_all('a', href=True, text=True)
      link = links[1]['href']
      print(link)
      REQUEST_URL2 = f'https://m.facebook.com/{link}'
      driver.get(REQUEST_URL2)
      page2 = driver.page_source
      soup2 = BeautifulSoup(page2, "html.parser")
      comentarios = soup2.find_all('div', {"class": '_2b06'})
      for comentario in comentarios:
          print(comentario.text)