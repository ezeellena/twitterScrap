import json
from email import utils

import requests
from bs4 import BeautifulSoup
from pip._internal.network import session
from selenium import webdriver
import time
import lxml
from flask import Flask,request, render_template, jsonify
from selenium.webdriver.chrome.options import Options
app = Flask(__name__, template_folder="templates")

@app.route('/')
def index():
    return render_template('home.html')
@app.route('/facebook',  methods=['POST'])
def facebook():
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

    if "https://www.facebook.com/" in page_name:
        page_name = page_name.replace("https://www.facebook.com/", "https://m.facebook.com/")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }
        response = requests.get(page_name, headers=headers).text
    except Exception as e:
        print("Error 1 - Obtener Response ", e)
    driver.get(page_name)
    retornar = []
    pageDrive= driver.page_source
    comentarios = BeautifulSoup(pageDrive, "lxml").find_all('div', {"class": '_2b06'})
    cantidadComentarios = len(comentarios)
    ingresoABuscarmg = BeautifulSoup(pageDrive, "lxml").find_all('a', {"class": '_45m8'})
    ingresoABuscarmg = ingresoABuscarmg[0].attrs['href']
    driver.get("https://m.facebook.com/"+ingresoABuscarmg)
    pageMg = driver.page_source
    LikesYcantComent = []
    cantidadComentarios = {"cantidadComentarios",cantidadComentarios}
    LikesYcantComent.append(cantidadComentarios)
    mgmememd = BeautifulSoup(pageMg, "html.parser").find_all('span', {"class": '_10tn'})
    for mg in mgmememd:
        text = mg.contents[0].attrs['aria-label']
        LikesYcantComent.append(text)

    for comentario in comentarios:
        NombrePersona = comentario.next.text
        ComentarioPersona = comentario.next.next_sibling.text
        print(NombrePersona)
        print(ComentarioPersona)

        Coment = {"Nombre_Persona": NombrePersona,
               "Comentario_Persona": ComentarioPersona}
        retornar.append(Coment)

    return jsonify(retornar,LikesYcantComent)

if __name__ == '__main__':
    app.run(debug=True)