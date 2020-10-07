from email import utils
from bs4 import BeautifulSoup
from pip._internal.network import session
from selenium import webdriver
import time
from flask import Flask,request, render_template, jsonify
from selenium.webdriver.chrome.options import Options
app = Flask(__name__, template_folder="templates")

@app.route('/')
def index():
    return render_template('home.html')
@app.route('/facebook',  methods=['POST'])
def facebook(page=None):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=options)
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

    page_name = request.json["page"]

    time.sleep(5)
    REQUEST_URL = f'https://m.facebook.com/{page_name}'
    driver.get(REQUEST_URL)
    time.sleep(2)
    scrolls = 15
    retornar = []
    for i in range(1,scrolls):
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      time.sleep(5)
      page = driver.page_source
      soup = BeautifulSoup(page, "html.parser")
      #names = soup.find_all('div', {"class": ['du4w35lb k4urcfbm l9j0dhe7 sjgh65i0']})
      publicaciones = soup.find_all('div', {"class": '_3drp'})
      publicaciones = soup.find_all('article')

      for publicacion in publicaciones:
          try:
            cantidadComentariosYCompartidos = publicacion.find('div', {"class": "_1fnt"})
            print(cantidadComentariosYCompartidos.text)
          except Exception as e:
              print("No tiene comentarios", e)
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
              retornar.append(comentario.text)
    return jsonify(retornar)

if __name__ == '__main__':
    app.run(debug=True)