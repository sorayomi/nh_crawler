from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import os
import argparse
from datetime import datetime

bid_history = []
data = {'title': [], 'pages': [], 'url': [], 'rating': []}


parser = argparse.ArgumentParser()
parser.add_argument('--fname', type=str, default='bango.txt',
                    help='a file that contains a bango list')
parser.add_argument('--save-dir', type=str, default='./',
                    help='save to the directory')

args = parser.parse_args()

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

def download(title, pages, img_id, url, rating, eng_title):
    url = 'https://i.nhentai.net/galleries'
    title = title.replace('/', '')
    if args.save_dir[-1] != '/':
        save_dir = args.save_dir + '/'
    if not os.path.exists(f'{save_dir}{title}'):
        os.makedirs(f'{save_dir}{title}')
    
    # check if downloaded
    if os.path.isfile(f'{save_dir}{title}/info.txt'):
        print(f'{title} has been  downloaded before')
        return

    for page in range(int(pages)-1):
        img_data = requests.get(f'{url}/{img_id}/{page+1}.jpg', stream=True).content
        with open(f'{save_dir}{title}/{page+1}.jpg', 'wb') as f:
            f.write(img_data)

    # download finished; write information file
    with open(f'{save_dir}{title}/info.txt', 'w') as f:
        f.write(f'Title:\t{title}\n')
        f.write(f'English Title:\t{eng_title}\n')
        f.write(f'URL:\t{url}\n')
        f.write(f'pages:\t{pages}\n')
        f.write(f'likes:\t{rating}\n')
        f.write(f'download time:\t{str(datetime.today())}\n')
        f.write(f'\ndownloader: sorayomi\n')

for bango in read_bangos(filename=args.fname):
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
    download(title, pages, img_id, url, favorite, eng_title)
    
    time.sleep(0.1)

print(data)
#df = pd.DataFrame(data)
#print(df)
