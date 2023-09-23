import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests
from PIL import Image

base = "dark"
primaryColor = "purple"
image = Image.open('coursesimg.png')
st.image(image)


def scrape_url():
    base_url ='https://brainlox.com/courses/category/technical'
    resp = requests.get(base_url)
    soup = BeautifulSoup(resp.content,'html.parser')
    
    links = soup.select('h3 a')
    links = [f'https://brainlox.com'+link.get('href') for link in links]
    return(links)

def scrape_data(url):
    resp2 = requests.get(url)
    soup2 = BeautifulSoup(resp2.content,'html.parser')
    row = {}
    row['Course Title'] = soup2.select_one('h2').text
    row['Description'] = '\n'.join([p.text.strip() for p in soup2.select_one('div',{'class':'courses-overview'}).select('p')])
    row['Course url'] = url
    return row

data = []    
urls = scrape_url()
for url in urls:
    scr_text = scrape_data(url) 
    if scr_text:
        data.append(scr_text)

df = pd.DataFrame(data,index=range(1, len(data) + 1))
df.to_csv('data.csv')
st.write(df)
