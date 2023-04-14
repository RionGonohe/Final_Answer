#!/usr/bin/env python
# coding: utf-8

# In[6]:


from bs4 import BeautifulSoup
import re
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

url = ["https://r.gnavi.co.jp/7jhnbmee0000/","https://r.gnavi.co.jp/8c7vagfr0000/","https://r.gnavi.co.jp/h205800/","https://r.gnavi.co.jp/e1kh7y1t0000/",
       "https://r.gnavi.co.jp/hezjd3hz0000/","https://r.gnavi.co.jp/cenx1p070000/","https://r.gnavi.co.jp/8s5sck6x0000/","https://r.gnavi.co.jp/8xyzuzh00000/",
       "https://r.gnavi.co.jp/rjjws3wf0000/","https://r.gnavi.co.jp/8fdxg25n0000/","https://r.gnavi.co.jp/jfc20d3r0000/","https://r.gnavi.co.jp/h202901/",
       "https://r.gnavi.co.jp/sfuv44700000/","https://r.gnavi.co.jp/e50gh1f30000/","https://r.gnavi.co.jp/h319200/","https://r.gnavi.co.jp/kazpfer20000/",
       "https://r.gnavi.co.jp/99v2drub0000/","https://r.gnavi.co.jp/h808600/","https://r.gnavi.co.jp/seb4scgs0000/","https://r.gnavi.co.jp/mbe6jyj60000/",
       "https://r.gnavi.co.jp/kvsp3hem0000/","https://r.gnavi.co.jp/r13tsgea0000/","https://r.gnavi.co.jp/43ajb3au0000/","https://r.gnavi.co.jp/jjer2g4c0000/",
       "https://r.gnavi.co.jp/h769100/","https://r.gnavi.co.jp/ajbs6r5w0000/","https://r.gnavi.co.jp/7du6d0zx0000/","https://r.gnavi.co.jp/h024100/",
       "https://r.gnavi.co.jp/ngz3mahs0000/","https://r.gnavi.co.jp/h406900/","https://r.gnavi.co.jp/ee28wz0x0000/","https://r.gnavi.co.jp/3wehu6dr0000/",
       "https://r.gnavi.co.jp/h9ve2z7e0000/","https://r.gnavi.co.jp/h540200/","https://r.gnavi.co.jp/ee28wz0x0000/","https://r.gnavi.co.jp/khvvc2tf0000/",
       "https://r.gnavi.co.jp/7h6bv4pp0000/","https://r.gnavi.co.jp/ceabu2zh0000/","https://r.gnavi.co.jp/b1tw4zy50000/","https://r.gnavi.co.jp/h062400/",
       "https://r.gnavi.co.jp/rjs18gpn0000/","https://r.gnavi.co.jp/h024100/","https://r.gnavi.co.jp/pmt4y6sk0000/","https://r.gnavi.co.jp/h316600/",
       "https://r.gnavi.co.jp/14w4f6br0000/","https://r.gnavi.co.jp/1whwd62r0000/","https://r.gnavi.co.jp/ss7k8xua0000/","https://r.gnavi.co.jp/h095700/",
       "https://r.gnavi.co.jp/3kge6che0000/","https://r.gnavi.co.jp/cgxwnhe90000/"]
store_info = []

driver_path = "/path/to/chromedriver"
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

for x in url:
    time.sleep(3)
    driver.get(x)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # 店名
    pattern = r'<title>(.*?)\s*（.*?）\s*-?\s*ぐるなび'
    match = re.search(pattern, str(soup))
    store_name = match.group(1)

    # 電話番号
    pattern = r'<li><span class="number">(\d{2,4}-\d{2,4}-\d{4})'
    match = re.search(pattern, str(soup))
    tell = match.group(1)
    
    #メールアドレス
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.findall(pattern, str(soup))
    if match:
        a = match
        email_list = a
        email = email_list[0]
    else:
        email= " "

    #都道府県
    pattern = r'<span class="region">(.*?[都道府県])'
    match = re.search(pattern, str(soup))
    prefectures = match.group(1)

    #市区町村
    pattern = r'<span class="region">(.*?[市区町村].*?\d+-\d+)'
    match = re.search(pattern, str(soup))
    town = match.group(1)
    town = re.sub(r'[\d-]+', '', town)
    town = re.sub(r'.*?[都道府県]+', '', town)

    #番地
    pattern = r'<span class="region">.+?(\d\S+)\s*</span>'
    match = re.search(pattern, str(soup))
    address = match.group(1)

    #建物名
    pattern = r'<span class="locality">(.*?)</span>'
    match = re.search(pattern, str(soup))
    if match:
        building = match.group(1)
    else:
        building = " "

    #URL
    a_tag = soup.find("a", {"class": "sv-of double"})
    url = a_tag.get("href")

    #SSL
    if driver.current_url.startswith('https://'):
        ssl = "True"
    else:
        ssl = "False"
    
    store_info.append({'店舗名': store_name,
                       '電話番号': tell,
                       'メールアドレス':email,
                       '都道府県': prefectures,
                       '市区町村': town,
                       '番地': address,
                       '建物名': building,
                       'URL': url,
                       'SSL': ssl})


# In[7]:


df = pd.DataFrame(store_info)
df = df.reset_index(drop=True)
df_styled = df.style.set_properties(**{'text-align': 'left'}).set_table_styles([{'selector': 'th', 'props': [('text-align', 'left')]}])
df_styled


# In[8]:


import pandas as pd
df = pd.DataFrame(store_info)
df.to_csv("1-2.csv", index=False)


# In[ ]:




