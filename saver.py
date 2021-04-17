from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import os

bid_history = []
data = {'title': [], 'pages': [], 'url': [], 'rating': []}

def query_bid(bid):
    url = f'https://nhentai.net/g/{bid}/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, features='html.parser')
    try:
        jp_title = soup.find_all('h2', {'class': 'title'})[0].text 
    except:
        jp_title = None
    
    try:
        eng_title = soup.find_all('h1', {'class': 'title'})[0].text
    except:
        eng_title = None

    img_id = soup.find_all('meta', {'itemprop': 'image'})[0]['content'].split('/')[-2]
    tags = soup.find_all("span", {'class':'tags'})[2].find_all('span', {'class', 'name'})
    pages = soup.find_all("span", {'class':'tags'})[-2].find_all('span', {'class', 'name'})[0].text
    tags = [tag.text.replace(' ', '-') for tag in tags]

    favorite = int(soup.find_all('span', {'class', 'nobold'})[0].text[1:-1])

    return jp_title, eng_title, pages, url, tags, favorite, img_id

def read_bangos(filename='bango.txt'):
    bangos = []
    with open(filename, 'r') as f:
        for line in f:
            bangos.append(line.strip())
    return bangos

def download(title, pages, img_id):
    url = 'https://i.nhentai.net/galleries'
    title = title.replace('/', '')
    if not os.path.exists(title):
        os.mkdir(f'{title}')
    for page in range(int(pages)-1):
        #print(f'{url}/{img_id}/{page+1}.jpg')
        img_data = requests.get(f'{url}/{img_id}/{page+1}.jpg', stream=True).content
        with open(f'{title}/{page+1}.jpeg', 'wb') as f:
            f.write(img_data)
            #shutil.copyfileobj(img_data.raw, f)

for bango in read_bangos():
    res = requests.get(f'https://nhentai.net/g/{bango}')
    soup = BeautifulSoup(res.text, features='html.parser')
    mangas = soup.find_all('div', {'class': 'gallery'})
            
    jp_title, eng_title, pages, url, tags, favorite, img_id = query_bid(bango)
    print(jp_title, favorite)
    if jp_title is not None:
        title = jp_title
    elif eng_title is not None:
        title = eng_title
    else:
        title = None
    data['title'].append(title)
    data['pages'].append(pages)
    data['url'].append(url)
    data['rating'].append(favorite)
    download(title, pages, img_id)
    time.sleep(0.1)

print(data)
#df = pd.DataFrame(data)
#print(df)
