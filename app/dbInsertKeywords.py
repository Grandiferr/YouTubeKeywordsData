from models import Keyword, queryset
from pandas import DataFrame
import requests
import webbrowser
from selenium import webdriver
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pyperclip
import time
import csv
import os
from debug import *
from titleToKeywords import strToKeyword




def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def dbInsertKeywords(keywordList, lazy = False):
    keywordList = list(filter(None, [strToKeyword(phrase) for phrase in keywordList]))
    if lazy:
        if DEBUG: (print("dbInsertKeywords:  Using Lazy DB check, no inserting or updating\n"))
        keywordObjects = []
        for phrase in keywordList:
            keyQuery = Keyword.objects(key = phrase)
            if (keyQuery): keywordObjects.append(keyQuery[0])
        if DEBUG: (print("dbInsertKeywords:  Returning lazy DB query\n"))
        return list(set(keywordObjects))        

    if DEBUG: (print("dbInsertKeywords:  Taking keyword string list...\n"))
    #static URL for keywordseverywhere bulk tool
    if DEBUG: (print(""))
    URL = "https://keywordseverywhere.com/ke/4/manual.php"
    if DEBUG: (print("dbInsertKeywords:  Scraping for given keywords at %s...\n", URL))
    #setup browser options
    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=/tmp/tarun")
    download_dir = r"C:\Users\Oliver\Desktop\Misc Code\python\KC\temp"
    preferences = {"download.default_directory": download_dir ,
                "directory_upgrade": True,
                "safebrowsing.enabled": True }
    chrome_options.add_experimental_option("prefs", preferences)
    if DEBUG: (print("dbInsertKeywords:  Getting webdriver for chrome...\n"))
    driver = webdriver.Chrome(executable_path= r'C:\Users\Oliver\dev\cfehome\chromedriver.exe', options=chrome_options)
    fileName = ''
    keywordObjectReturnList = []
    keywordLists = chunks(list(set(keywordList)), 2000)
    for chunk in keywordLists:
        driver.get(URL)
        #find and enter to form
        if DEBUG: (print("dbInsertKeywords:  Trying to find keyword form...\n"))
        form = driver.find_element_by_id("keywords")
        text = ", ".join(chunk)
        if DEBUG: (print("dbInsertKeywords:  Copying to clipboard with pyperclip.copy()...\n"))
        pyperclip.copy(text)
        if DEBUG: (print("dbInsertKeywords:  Pasting with os Keys...\n"))
        form.send_keys(Keys.CONTROL, 'v')
        if DEBUG: (print("dbInsertKeywords:  Finding submit button...\n"))
        button = driver.find_element_by_id("submit")
        if DEBUG: (print("dbInsertKeywords:  Clicking submit button...\n"))
        button.click()
        time.sleep(2)
        if DEBUG: (print("dbInsertKeywords:  Finding CSV download button...\n"))
        CSVDownloadButton = driver.find_element_by_class_name("buttons-csv")
        if DEBUG: (print("dbInsertKeywords:  Trying to click submit button until CSV button is displayed...\n"))
        while not CSVDownloadButton.is_displayed():
            try:
                button.click()
                if DEBUG: (print("dbInsertKeywords:  clicked [SUBMIT]...\n"))
            except:
                pass
        time.sleep(1)
        if DEBUG: (print("dbInsertKeywords:  Clicking CSV download button...\n"))
        CSVDownloadButton.click()
        time.sleep(1)
        if DEBUG: (print("dbInsertKeywords:  Trying to find file that was downloaded...\n"))
        name = str.lower(chunk[0]).replace("&", "").replace("|", "").strip().replace(" ", "-")
        if name == "":
            name = "csv"
        fileName = "C:\\Users\\Oliver\\Desktop\\Misc Code\\python\\KC\\temp\\" + name + ".csv"
        if DEBUG: (print("dbInsertKeywords:  Opening as CSV...\n"))
        try:
            csv_file = open(fileName)
        except NameError:
            print("No file found")
            return []
        reader = csv.reader(csv_file, delimiter=',')
        titleRowSkip = False
        if DEBUG: (print("dbInsertKeywords:  Adding/updating keywords...\n"))
        for row in reader:
            if titleRowSkip:
                phrase = row[1]
                vol = row[5]
                cpc = row[6]
                competition = row[7]
                keyQuery = Keyword.objects(key = phrase)
                if (len(phrase) < 20):
                    if (not keyQuery):
                        
                        kw = Keyword(
                            key = phrase,
                            volume = vol.replace(",", ""),
                            cpc = cpc.replace("$", ""),
                            competition = competition
                        )
                        kw.save()
                        keyQuery = kw
                        print("Saved New keyword:")
                        print(keyQuery.key)
                    else:
                        keyQuery.update_one(set__volume = vol.replace(",", ""))
                        keyQuery.update_one(set__cpc = cpc.replace("$", ""))
                        keyQuery.update_one(set__competition = competition)
                        keyQuery = keyQuery[0]
                        print("Updated keyword:")
                        print(keyQuery.key)
                    if (keyQuery): keywordObjectReturnList.append(keyQuery)
            titleRowSkip = True

        if DEBUG: (print("dbInsertKeywords:  Closing CSV...\n"))
        csv_file.close()
    if DEBUG: (print("dbInsertKeywords:  Closing browser and deleting CSV file...\n"))
    driver.close()
    os.remove(fileName)
    if DEBUG: (print("dbInsertKeywords:  Returning Keyword Object List...\n"))
    return keywordObjectReturnList