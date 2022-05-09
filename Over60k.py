#! Python3

import requests
import pandas as pd
import re
from datetime import datetime as dt
from bs4 import BeautifulSoup
import time

def get_links(url):
    print('Please wait while I gather your data')
    url_2=url+'&startrow=25'
    url_3=url+'&startrow=50'
    url_4=url+'&startrow=75'
    url_5=url+'&startrow=100'
    url_6=url+'&startrow=125'
    url_7=url+'&startrow=150' 
    url_8=url+'&startrow=175'
    url_9=url+'&startrow=200'
    url_10=url+'&startrow=225'
    url_11=url+'&startrow=250'
    url_12=url+'&startrow=275'
    url_13=url+'&startrow=300'
    url_14=url+'&startrow=325'
    url_15=url+'&startrow=350'
    urls=[url,url_2,url_3,url_4,url_5,url_6,url_7,url_8,url_9,url_10,url_11,url_12,url_13,url_14,url_15]
    links=[]
        
    for i in urls:   
        website=requests.get(i, verify=r'C:\Users\Passettr\OneDrive - Florida Department of Financial Services\Desktop\dfs_bundle.crt')
        websiteText=website.text
        soup=BeautifulSoup(websiteText,features="html.parser")

        for link in soup.find_all('a'):
            links.append(link.get('href'))

    stringLinks=[str(i) for i in links]
    jobLinks=[]
    salaries=[]
    title=[]
    r=re.compile('/job/.*') 
    firstScrape=list(filter(r.match,stringLinks))
    for i in firstScrape:
        jobLinks.append('https://jobs.myflorida.com'+i)
        
    for i in jobLinks:
        website=requests.get(i, verify=r'C:\Users\Passettr\OneDrive - Florida Department of Financial Services\Desktop\dfs_bundle.crt')
        websiteText=website.text
        soup=BeautifulSoup(websiteText,features="html.parser")
        element1=soup.select('#content > div > div.jobDisplayShell > div > div.job > span > p:nth-child(5)')
        for i in element1:
            try:
                salaries.append(element1[0].text.strip())
                break
            except IndexError:
                salaries.append('Could not locate salary') 
        element2=soup.select('#job-title')
        title.append(element2[0].text.strip())
        
    stringSalaries=[str(i) for i in salaries]
    stringTitle=[str(i) for i in title]
    
    df=pd.DataFrame(list(zip(stringTitle,stringSalaries,jobLinks)),columns=['Title','Salary','Links'])
    def make_clickable(val):
        return '<a href="{}">{}</a>'.format(val)
    df.style.format({'Links': make_clickable})
    filt=df['Salary'].str.contains('[6-8]\d,\d\d\d|\$[3-4],\d\d\d.*[Bb][iI]|[5-9],\d\d\d.*[Mm][Oo][Nn][Tt][Hh]|\$[3-9]\d.*[hH][oOrR]|Could not locate salary',regex=True, na=False)
    df=df.loc[filt]
    mask = '%m-%d-%Y'
    dte = dt.now().strftime(mask)
    fname = r'C:\Users\Passettr\OneDrive - Florida Department of Financial Services\Desktop\PeopleFirst\PositionsAndSalaries_{}.xlsx'.format(dte)
    df.to_excel(fname, index=False)
    print(r'Success! Please see your results at C:\Users\Passettr\OneDrive - Florida Department of Financial Services\Desktop\PeopleFirst')
    time.sleep(5)
    
get_links('https://jobs.myflorida.com/search/?q=&locationsearch=tallahassee&searchby=location&d=10')