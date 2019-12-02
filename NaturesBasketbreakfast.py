#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 12:03:54 2019

@author: prakharj
"""

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import csv
import datetime


def is_float(strin):
  try:
    return float(strin) and '.' in strin  # True if string is a number contains a dot
  except ValueError:  # String is not a number
    return False

def smallest(a, y, z):
    M = a
    if y < M:
        M = y    
    if z < M:
        M = z
        if y < z:
            M = y
    return M

while(1):
    now = datetime.datetime.now()
    month = str(now.month)
    day = str(now.day)
    if len(month) ==1:
        month = '0'+ month
    if len(day) ==1:
        day = '0'+ day
    filedate = str(now.year)+'/'+ month +'/'+ day
    filenamedate = str(now.year)+ now.strftime("%b") + day

# Web extraction of web page nature's basktet    
    print("scheduled to run nature basket scrapper")
    now1 = datetime.datetime.now()
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    driver = webdriver.Chrome(chrome_options=options)
    webpage = 'http://www.naturesbasket.co.in/Online-grocery-shopping/Breakfast--Dairy---Bakery/11_0_0' 
    driver.get(webpage)
    while(1):
     try:
         wrg = driver.find_element_by_id('ctl00_ContentPlaceHolder1_lblText1')
         break
     except Exception:
         driver.refresh()
         driver.get(webpage)
         time.sleep(5)
    time.sleep(6)
    Resultfile = open(filenamedate+"_NB_file_dairy_cleaned.csv",'a',encoding='utf-8',newline='')
    head = csv.writer(Resultfile)
    head.writerow(["Name","Quantity","Price","City","Date","Source","Category","CodeVersion"])
    Resultfile.close()         
    with open('citylist.csv') as csvfile:
         spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
         for row in spamreader:
            cityname = row[0]
            while(1):
             try:
                h = driver.find_element_by_id('verticalmenuhead')
                break
             except Exception:
                driver.refresh
            s4 = driver.find_element_by_tag_name('body')
            st= str(s4.get_attribute('innerHTML'))
            try:
                city = Select(driver.find_element_by_id('ctl00_ddlCitySearch'))
            except Exception:
                city = Select(driver.find_element_by_id('ctl00_ddlCities'))
            
            city.select_by_value(cityname)
            try:
                yes = driver.find_element_by_id('btnPinOk')
                yes.click()
            except Exception:
                driver.refresh()
            else:    # Infinite scrolling 
               
                SCROLL_PAUSE_TIME = 12
                    
                # Get scroll height
                last_height = driver.execute_script("return document.body.scrollHeight")
                
                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight*0.90);")
                
                    time.sleep(SCROLL_PAUSE_TIME)
                
                    # Calculate new scroll height and compare with last scroll height
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
               
                x = driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "search_PSellingP", " " ))] | //*[contains(concat( " ", @class, " " ), concat( " ", "linkdisabled", " " ))] | //*[contains(concat( " ", @class, " " ), concat( " ", "search_PSelectedSize", " " ))]')
                sname = driver.find_elements_by_class_name('search_Ptitle')
                squantity =driver.find_elements_by_class_name('search_PSelectedSize')
                sprice = driver.find_elements_by_class_name('search_PSellingP')
                Resultfile = open(filenamedate+"_NB_file_dairy_cleaned.csv",'a',encoding='utf-8',newline='')
                wr = csv.writer(Resultfile)
                name =[]
                quantity =[]
                price =[]
                for ip in sname:
                    if ip.text:
                        name.append(ip.text)
                for ip in squantity:
                    if ip.text:
                        quantity.append(ip.text)
                for ip in sprice:
                    if ip.text:
                        price.append(ip.text)
                veglist = []
                val = smallest(len(name),len(price),len(quantity))
                for i in range(0,val-1):
                    veglist.append(name[i])
                    veglist.append(quantity[i])
                    veglist.append(price[i][1:])
                    veglist.append(cityname)
                    veglist.append(filedate)
                    veglist.append(webpage)
                    veglist.append('Dairy')
                    wr.writerow(veglist)
                    veglist =[]
                Resultfile.close()
#extraction completed for the day and system goes into sleep mode                
    driver.quit()
    print('completed')
    time.sleep(62000)     