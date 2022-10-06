#from id
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

from selenium import webdriver
from time import sleep

from datetime import date

today = date.today()
import os

options = webdriver.ChromeOptions()

options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
#if you want to scrape in 'en' , uncomment below two lines and set path to your chrome profile and use always 
# options.add_argument("--user-data-dir=C:/Users/User/AppData/Local/Google/Chrome/User Data/") # change to profile path
# options.add_argument('--profile-directory=Profile 3'.format(getpass.getuser()))

options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)
df = pd.read_csv('vc.csv')

vsbc =[]
for ivc in df.a:
    
    url1 = 'https://www.lotteon.com/p/product/'+ivc
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
    d1 = today.strftime("%d/%m/%Y")
    try:
        discount = soup.find("span",{"class":"discountRate"}).text
    except:discount=0
    mrp=soup.find("span",{"class":"won"}).text
    mrp =mrp.replace(" ",'')
    mrp =mrp.replace("\n",'')
    vg = list([("name",name),("productURL",url1),("date",d1),("star",star),("reviewCount",reviewCount),("monthlyPurchase",monthlyPurchase),("price",mrp),("old_price",oldprice),("discount",discount)])
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

vvcb.to_csv('lv.csv')