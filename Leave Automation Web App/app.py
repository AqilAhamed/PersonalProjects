from flask import Flask, render_template, request
import time
import threading

app = Flask(__name__)

@app.route('/', methods = ["POST", "GET"])
def home():
    return render_template("index.html")

@app.route('/done', methods = ["POST", "GET"])
def results():
    def auto(x):
        from selenium import webdriver
        import time
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        web = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        formLink = x[6] # change this form link accordingly and SAVE file
        web.get(formLink)
        time.sleep(2)

        # Next button
        sel_button = web.find_element('xpath', '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
        sel_button.click()

        time.sleep(2)

        # Rank / Name
        sname = x[2]
        name = web.find_element('xpath', '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        name.send_keys(sname)

        # Intake
        sintake = x[3]
        intake = web.find_element('xpath', '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        intake.send_keys(sintake)

        # Role in team
        if x[4]=="GL":
            role_button = web.find_element('xpath', '//*[@id="i13"]/div[3]/div')
            role_button.click()
        else:
            role_button = web.find_element('xpath', '//*[@id="i16"]/div[3]/div')
            role_button.click()

        # Date
        smonth = x[5] #Change month number accordingly
        month = web.find_element('xpath', '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/input')
        month.send_keys(smonth)

        sday = x[0]
        day = web.find_element('xpath', '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/input')
        day.send_keys(sday)

        syear = x[7]
        year = web.find_element('xpath', '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/input')
        year.send_keys(syear)

        # Type of Leave
        AL = '//*[@id="i28"]/div[3]/div'
        OL = '//*[@id="i31"]/div[3]/div'
        OIL = '//*[@id="i34"]/div[3]/div'
        EDO = '//*[@id="i37"]/div[3]/div'

        if x[1] == 'AL':
            sel_button = web.find_element('xpath', AL)
            sel_button.click()
        elif x[1] == 'OL':
            sel_button = web.find_element('xpath', OL)
            sel_button.click()
        elif x[1] == 'OIL':
            sel_button = web.find_element('xpath', OIL)
            sel_button.click()
        elif x[1] == 'EDO':
            sel_button = web.find_element('xpath', EDO)
            sel_button.click()


        # Finish | Unhighlight code below when you wanna submit
        fin_button = web.find_element('xpath', '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div[2]/span/span')
        fin_button.click()

        time.sleep(1)
        web.quit()

    #######################################################################################################################################################################

    name = request.form["fname"]
    intake = request.form["fintake"]
    role = request.form["frole"]
    month = request.form["fmonth"]
    txtfile = request.files["txtfile"]
    url = request.form["url"]
    year = request.form["year"]

    # Format is [day, leave type]
    f = txtfile
    leaves = []
    for x in f:
        x = x.decode("utf-8")
        leaves.append(x.split())

    # Start multithreading
    for i in leaves:
        t = threading.Thread(target=auto, args=[i+[name, intake, role, month, url, year]]) # 2,3,4,5,6,7
        t.start()
        time.sleep(5)


    return render_template("done.html")




if __name__ == "__main__":
    app.run()
