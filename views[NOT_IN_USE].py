import pandas as pd
from flask import Blueprint, render_template, request, send_from_directory, redirect, url_for
from stocks import symbols
import webbrowser

views = Blueprint(__name__, "views")


@views.route("/", methods=['POST', 'GET'])
def home():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from time import sleep

    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get("http://161.97.159.41:8969/options/")

    saved_query = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, r'//*[@id="query_div"]/button'))
    )
    saved_query.click()

    queries = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, r'queries'))
    )
    sleep(0.5)
    query_list = queries.text.split('\n')
    driver.close()
    if request.method == "POST":
        query_chosen = request.form["query"]
        startdate = request.form["startdate"]
        enddate = request.form["enddate"]
        selected_stocks = request.form.getlist('my_checkbox')
        stock_method = request.form["stocks"]
        optionmethod = request.form["optionmethod"]
        interval = request.form["interval"]
        final_query = {
            "query": query_chosen,
            "start date": startdate,
            "end date": enddate,
            "stocks": selected_stocks,
            "option method": optionmethod,
            "stock method": stock_method,
            "interval": interval
        }
        print(final_query)
        foo(final_query)
        return render_template("views.html", queries=query_list, symbols=symbols)
    else:
        return render_template("views.html", queries=query_list, symbols=symbols)


file_path = "/home/tomer/Documents/stocks2/"


def delete_files():
    import os
    for filename in os.listdir(file_path):
        print(filename)
        file = os.path.join(file_path, filename)
        try:
            os.remove(file)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file, e))


def foo(final_query):
    from time import sleep
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from stocks import symbols
    import os

    delete_files()

    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': file_path}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("document.body.style.zoom='75%'")
    driver.get("http://161.97.159.41:8969/options/")

    if final_query["stock method"] == "selected":
        symbols = final_query["stocks"]

    start_year, start_month, start_day = final_query["start date"].split("-")
    end_year, end_month, end_day = final_query["end date"].split("-")

    start_date = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, r'//*[@id="start_date"]'))
    )
    start_date.click()
    start_date.send_keys(start_year)
    start_date.send_keys(Keys.ARROW_LEFT)
    start_date.send_keys(start_month)
    start_date.send_keys(Keys.ARROW_LEFT)
    start_date.send_keys(Keys.ARROW_LEFT)
    start_date.send_keys(start_day)

    end_date = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, r'//*[@id="end_date"]'))
    )
    end_date.click()
    end_date.send_keys(end_year)
    end_date.send_keys(Keys.ARROW_LEFT)
    end_date.send_keys(end_month)
    end_date.send_keys(Keys.ARROW_LEFT)
    end_date.send_keys(Keys.ARROW_LEFT)
    end_date.send_keys(end_day)

    options = [final_query["option method"]] if final_query["option method"] != "Both" else ["Call", "Put"]
    print(options)

    temp = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, r'//*[@id="dataDiv_1"]/input[1]'))
    )

    saved_queries_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, r'//*[@id="query_div"]/button'))
    )
    saved_queries_button.click()

    sleep(1)
    saved_query = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f'#{final_query["query"]} > a'))
    )
    saved_query.click()

    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, r'#query_sideBar > a'))
    )

    element.click()
    sleep(1)

    option_type = Select(WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, r'//*[@id="intervalCmb1"]'))
    ))

    option_type.select_by_visible_text(final_query["interval"])

    if final_query["interval"] == "Monthly":
        element = Select(WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, r'//*[@id="wMonthCmb1"]'))
        ))
        element.select_by_visible_text('Current EOM (3rd Friday)')

    sleep(5)
    for option in options:

        sleep(1)

        option_type = Select(WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, r'//*[@id="callPutCmb1"]'))
        ))
        print(option)
        sleep(1)
        option_type.select_by_visible_text(option)

        for symbol in symbols:

            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, r'//*[@id="dataDiv_1"]/input[1]'))
            )

            element.click()
            element.send_keys(Keys.BACKSPACE)
            element.send_keys(Keys.BACKSPACE)
            element.send_keys(Keys.BACKSPACE)
            element.send_keys(Keys.BACKSPACE)
            element.send_keys(Keys.BACKSPACE)
            element.send_keys(symbol)

            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, r'//*[@id="queryBtn"]'))
            )

            element.click()
            if int(end_year) - int(start_year) > 2:
                driver.switch_to.alert.accept()
                print("over 2 years")

            while True:
                try:
                    driver.switch_to.alert.accept()
                    break
                except Exception as e:
                    pass
            print(f"finished {symbol}")
    for File in os.listdir(file_path):
        if File.endswith(".crdownload"):
            sleep(5)
            print("still downloading")
    sleep(3)
    merge_files(file_path)


@views.route("/file/<filename>")
def get_file(filename):
    return send_from_directory(file_path, filename)


def merge_files(path):
    import os
    df_concat = pd.concat([pd.read_csv(path + f) for f in os.listdir(path)], ignore_index=True)
    df_concat.to_csv(path + "/merged_file.csv", index=False)
    webbrowser.open("http://127.0.0.1:5000/views/file/merged_file.csv")
