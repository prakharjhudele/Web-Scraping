import requests
#import csv
from bs4 import BeautifulSoup
import re
from functools import partial  
from operator import is_not
from dateutil import parser
import pandas as pd
from datetime import timedelta, date


links = []
news_data = []
filter_null = partial(filter, partial(is_not, None))
proxies = {
  "http": "your http proxy",
  "https": "your https proxy"
}

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

start_dt = date(2019, 9, 12)             
end_dt = date(2019,9,13)
for dt in daterange(start_dt, end_dt):
    #print(dt.strftime("%Y-%m-%d"))
    url = "https://www.thehindubusinessline.com/archive/web"  # no trailing /
    myurl = ".html"
    Daystr = str(dt.year) + "/" + str(dt.month) + "/" + str(dt.day)
    final_url = '/'.join([url, Daystr]) + myurl
#    print(final_url)
    try:
        page = requests.get(final_url, proxies=proxies)
        
        soup = BeautifulSoup(page.text, 'html.parser')

        last_links = soup.find(class_='left-column')

        artist_name_list_items = last_links.find_all('a')
        for artist_name in artist_name_list_items:
            
            links.append(artist_name.get('href'))
            L =list(filter_null(links))
            
            regex = re.compile(r'https')
            
            selected_files = list(filter(regex.match, L))
#            print(selected_files)     
#        print(list(page))
    except Exception as e:
        print(e)
        print("continuing....")
        continue

for url in selected_files:
        news_category = url.split('/')[-3]
        try:
            data = requests.get(url, proxies=proxies)
            soup = BeautifulSoup(data.content, 'html.parser')
        
            last_links2 = soup.find(id='ControlPara')                
            last_links3 = last_links2.find_all('p')
            metadate = soup.find('meta', attrs={'name': 'publish-date'})['content']
            #print(metadate)
            metadate = parser.parse(metadate).strftime('%m-%d-%Y')
            metaauthor = soup.find('meta', attrs={'name': 'twitter:creator'})['content']
            news_articles = [{'news_headline': soup.find('div', 
                                                         attrs={"class": "title-bor-bottom"}).string,
                          'news_article':  last_links3,
                         'news_author':  metaauthor,
                          'news_date': metadate,
                            'news_category': news_category}
                        ]
        
            news_data.extend(news_articles)        
#        print(list(page))
        except Exception as e:
            print(e)
            print("continuing....")
            continue
     
df =  pd.DataFrame(news_data)
#    print(news_data)
df = df[['news_headline', 'news_article', 'news_category','news_author', 'news_date']]
#    return df
print(df)
df.to_csv("hblmar2018.csv",encoding = 'utf-8', index = False)