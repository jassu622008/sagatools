from flask import Flask

import manager

from flask import render_template

from flask import request

import time

from selenium import webdriver

import pywhatkit as pwk

import re

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("tools/index.html", category="category")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/index")
def index():
    return render_template("tools/index.html", category="category")

@app.route("/whatsapp")
def whatsapp():
    return render_template("tools/whatsapp.html")

@app.route("/email")
def email():
    return render_template("tools/email_text.html")

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        info = request.form['inp_value']
        if "whatsapp" in info:
            return render_template("tools/whatsapp.html")
        if "email" and "text" in info:
            return render_template("tools/email_text.html")
        if "youtube" in info:
            return render_template("tools/youtubevideotop.html")
        if "email" and "web" or "url" in info:
            return render_template("tools/web_email_scraping.html")
        if "phone" in info:
            return render_template("tools/phone_number_scrape.html")
        else:
            return render_template("tools/index.html", war = "sorry no service found please try available services")

@app.route("/send", methods=['GET', 'POST'])
def send():
    try:
        if request.method == "POST":
            input_num = request.form['input_num']
            input_message = request.form['input_message']

            options = webdriver.ChromeOptions()

            options.add_experimental_option('excludeSwitches', ['enable-logging'])

            driver = webdriver.Chrome(options=options)

            driver.get(f"https://web.whatsapp.com/send?phone={input_num}&text={input_message}")

            time.sleep(100)

            driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]').click()

            driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]').click()

            driver.close()

            return render_template("tools/whatsapp.html", message="message sent successfully")
    except Exception as e:
        return str(e)

@app.route("/emails", methods=["GET", "POST"])
def emails():
    if request.method == "POST":
        def listToString(s): 
            str1 = " ," 
            return (str1.join(s))
        data = request.form['data']
        emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", data)
        data = listToString(emails)
        return render_template("tools/email_text.html", list=data)

@app.route("/ydt")
def ydt():
    return render_template("tools/youtubevideotop.html")

@app.route("/get_video", methods=['GET', 'POST'])
def video():
    if request.method == "POST":
        try:
            topic = request.form["topic"]
            if topic == "":
                return render_template("tools/youtubevideotop.html", link="The Topic Should Not Be Empty")
            jassu = pwk.playonyt(topic)
            return render_template("tools/youtubevideotop.html", link="Link of video is : "+jassu)
        except Exception as e:
            return render_template("tools/youtubevideotop.html", link=e)

@app.route("/terms")
def terms():
    return render_template("terms-conditions.html")

@app.route("/pri")
def pri():
    return render_template("privacy_policy.html")

@app.route("/set")
def sef():
    return render_template("tools/web_email_scraping.html")

@app.route("/jassu", methods=["GET", "POST"])
def jassu():
    try:
        if request.method == "POST":
            url = request.form['textarea']
            if len(url.strip()) == 0:
                return render_template("tools/web_email_scraping.html", emails="please enter url")
            else:
                browser = webdriver.Chrome()
                browser.get(url)
                html_source = browser.page_source
                browser.close()
                def listToString(s): 
                    str1 = " ," 
                    return (str1.join(s))
                emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", html_source)
                data = listToString(emails)
                return render_template("tools/web_email_scraping.html", emails=data)
    except Exception:
        return render_template("tools/web_email_scraping.html", emails="Please Check The Url you must include http or https")
@app.route("/phone_web")
def ai_cg():
    return render_template("tools/phone_number_scrape.html")
@app.route("/get_phone", methods=["GET", "POST"])
def get_content():
    if request.method == "POST":
        try:
            def listToString(s): 
                str1 = " ," 
                return (str1.join(s))
            url = request.form['ai_topic']
            res = manager.get_phone_numbers(url)
            result = listToString(res)
            return render_template("tools/phone_number_scrape.html", content=result)
        except Exception:
            return render_template("tools/phone_number_scrape.html", content="please enter url and include http or https")
@app.route("/tools")
def tools():
    return render_template("tools/index.html", category="Tools")

@app.route("/articles")
def articles():
    return render_template("articles/articles.html", category="Articles")

@app.route("/ebooks")
def ebooks():
    return render_template("ebooks/books.html", category="Ebooks")
@app.route("/phone_text")
def phone_text():
    return render_template("tools/phone_text.html")
@app.route("/phones", methods=["GET", "POST"])
def phones():
    if request.method == "POST":
        try:
            def listToString(s): 
                str1 = " ," 
                return (str1.join(s))
            data = request.form['data']
            res_data = re.findall("[\+\d]?(\d{2,3}[-\.\s]??\d{2,3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})", data)
            result = listToString(res_data)
            return render_template("tools/phone_text.html", list=result)
        except Exception as e:
            return render_template("tools/phone_text.html", list=str(e))

if __name__ == "__main__":
    app.run()
