import os

from selenium import webdriver
import time
from PIL import Image
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# create a new Chrome session
from selenium.webdriver.chrome.options import Options
from waitress import serve
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder="templates")
app.config['UPLOAD_FOLDER'] = './img'
@app.route('/Twitter')
def twitter(img=None):
    return render_template("Twitter.html")
@app.route('/Twittear', methods=["POST"])
def Twittear(f=None):
    f = request.files["image"]
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("- no-sandbox")
    options.add_argument("habilitar-automatización")
    options.add_argument("- disable- infobars ")
    options.add_argument(" - disable-dev-shm-use ")
    driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome()
    driver.implicitly_wait(30)

    # navigate to the application home page
    driver.get("https://twitter.com/login")

    # get the username textbox
    login_field = driver.find_element_by_name("session[username_or_email]")
    login_field.clear()

    # enter username
    login_field.send_keys("ezequielellena0003@gmail.com")
    time.sleep(1)

    # get the password textbox
    password_field = driver.find_element_by_name("session[password]")
    password_field.clear()

    # enter password
    password_field.send_keys("sdfgcv")
    time.sleep(1)
    password_field.submit()
    filename = secure_filename(f.filename)
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    img = Image.open('./img/'+filename)
    #img = Image.open(filename)
    cropped_filename = "C:/Users/eellena/PycharmProjects/twitterScrap/img/"+filename
    img.crop((0, 0, img.size[0], 400)).save(cropped_filename)
    element = driver.find_element_by_xpath("//input[@type='file']")
    driver.execute_script("arguments[0].style.display = 'block';", element)
    element.send_keys(cropped_filename)
    try:
        tweet = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                            "//span[@class='css-901oao css-16my406 css-bfa6kz "
                                                                            "r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0']//span["
                                                                            "@class='css-901oao css-16my406 r-1qd0xha "
                                                                            "r-ad9z0x r-bcqeeo r-qvutc0'][contains(text(),"
                                                                            "'Twittear')]")))
        tweet.click()

    except:
        print("NO")

    driver.quit()
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')