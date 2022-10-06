from __future__ import print_function
import os.path

import pandas as pd
from bs4 import BeautifulSoup
from google.oauth2 import service_account
import numpy as np
import pandas as pd
from pyrsistent import b
import requests
import getpass
from selenium.webdriver.common.by import By
from datetime import date
from selenium import webdriver
from time import sleep


url = "https://www.lotteon.com/p/product/LO1815262971?sitmNo=LO1815262971_1815262972&mall_no=1&dp_infw_cd=SCHchocolate"
import os

options = webdriver.ChromeOptions()
#if you want to scrape in 'en' , uncomment below two lines and set path to your chrome profile and use always 
# options.add_argument("--user-data-dir=C:/Users/User/AppData/Local/Google/Chrome/User Data/") # change to profile path
# options.add_argument('--profile-directory=Profile 3'.format(getpass.getuser()))
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")


options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)

driver.get(url)
sleep(5)
# serch = str(input("search product: "))
serch = "chocolate"
ser = driver.find_element(By.ID,"headerSearchId")
sleep(1)
ser.click()
sleep(1)
ser.send_keys(serch)
sleep(1)
driver.find_element(By.CLASS_NAME,"btnSearchInner").click()
sleep(5)
i1=[]
res = []
for i in range(0,1):
    sleep(1)
    cvb = driver.page_source
    soup1 = BeautifulSoup(cvb, 'html.parser')
    sleep(2)
    links = soup1.find("ul",{"class":"srchProductList"})

    mainl=links.findAll('a',{"class":"srchGridProductUnitLink"})
    
    for im in mainl :
        i1.append([im.get('href')])
    

    sleep(5)
    try:
        driver.find_element(By.CLASS_NAME,"srchPaginationNext").click()
        sleep(5)
    except:break
    
    
for i in i1:
    if i not in res:
        res.append(i)
            
        
        vsbc =[]
for ivc in res[0:4]:
    url1 = ivc[0]
    driver.get(url1)
    sleep(4)
    g=driver.find_elements(By.CLASS_NAME,'morePropertyBtn')
    for i in g:
        sleep(1)
        i.click()
    sleep(2)




    v = driver.page_source

    # v = driver.find_element(By.CLASS_NAME,'propertyBox')


    soup = BeautifulSoup(v, 'html.parser')
    sou = soup.find('div',{"class":"details detailCollapse required active"})
    dt = [x.text.strip() for x in sou.find_all('dt')]
    dd = [x.text.strip() for x in sou.find_all('dd')]

    tt =[x.text.strip() for x in soup.find_all('strong',{"class":"title"})]

    myList = list(zip(dt, dd))
    name = soup.find("div",{"class":"productName"}).text
    
    try:
        star = soup.find("em").text
    except:star=0
    try:    
        oldprice = soup.find("div",{"class":"listPrice"}).text
        oldprice = int ( ''.join(filter(str.isdigit, oldprice) ) )
    except:pass

    try:
        monthlyPurchase = soup.find("span",{"class":"monthlyPurchase"}).text
        monthlyPurchase = int ( ''.join(filter(str.isdigit, monthlyPurchase) ) )
    except:monthlyPurchase=0
    
    try:
        reviewCount = soup.find("span",{"class":"count"}).text
    except:reviewCount=0
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    try:
        discount = soup.find("span",{"class":"discountRate"}).text
    except:discount=0
    mrp=soup.find("span",{"class":"won"}).text
    mrp =mrp.replace(" ",'')
    mrp =mrp.replace("\n",'')
    vg = list([("name",name),("productURL",url1),("searchKEyword",serch),("date",d1),("star",star),("reviewCount",reviewCount),("monthlyPurchase",monthlyPurchase),("price",mrp),("old_price",oldprice),("discount",discount)])
    vg = dict(vg)

    dc = soup.find('div',{"class":"propertyBox"})
    try:
        tt =[x.text.strip() for x in dc.find_all('strong',{"class":"title"})]
        ts=[x.text.strip() for x in dc.find_all('p',{"class":"text"})]
        myList1 = list(zip(tt, ts))
        myList1=dict(myList1)
        try:
            tt =[x.text.strip() for x in dc.find('strong',{"class":"title"})]
            ts=[x.text.strip() for x in dc.find('p',{"class":"text"})]
            myList1 = list(zip(tt, ts))
            myList1=dict(myList1)
        except:pass
    except:
        pass


    images=[]
    vh= soup.find("div",{"class":"productVisualThumbsWrap initTransform noNav"})
    i = 0
    cd=vh.findAll('img')
    for img in cd :
        yg =(img.get('src'))
        cut=yg.find('dims')
        images.append(yg[0:cut])
        i=i+1

    a ={"img":images}
    a.update(myList)
    a.update(myList1)

    a.update(vg)
    vsbc.append(a)
    
import pandas as pd 
vvcb = pd.DataFrame(vsbc)
vvcb.to_csv(serch+'_lotten.csv')