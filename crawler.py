from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

target_tags = ['chikan', 'rape', 'netorare', 'schoolgirl-uniform', 'nakadashi', 'defloration', 'cheating', 'virginity', 'corruption', 'kemomimi']
bid_history = []
data = {'title': [], 'similarity': [], 'url': [], 'rating': []}

def similarity(tags):
    count = 0
    for tag in tags:
        if tag in target_tags:
            count += 1
    return count / len(target_tags)

def query_bid(bid):
    url = f'https://nhentai.net/g/{bid}/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, features='html.parser')
    try:
        jp_title = soup.find_all('h2', {'class': 'title'})[0].text 
    except:
        jp_title = 'null'
    tags = soup.find_all("span", {'class':'tags'})[2].find_all('span', {'class', 'name'})
    tags = [tag.text.replace(' ', '-') for tag in tags]

    favorite = int(soup.find_all('span', {'class', 'nobold'})[0].text[1:-1])

    return jp_title, url, tags, favorite


for tag in target_tags:
    for page in range(5):
        res = requests.get(f'https://nhentai.net/search/?q={tag}+language%3Achinese&sort=popular&page={page}')
        soup = BeautifulSoup(res.text, features='html.parser')
        mangas = soup.find_all('div', {'class': 'gallery'})
        for manga in mangas:
            bid = manga.contents[0]['href'].split('/')[-2]
            if bid not in bid_history:
                bid_history.append(bid)
                jp_title, url, tags, favorite = query_bid(bid)
                print(jp_title, favorite)
                data['title'].append(jp_title)
                data['url'].append(url)
                data['rating'].append(favorite)
                data['similarity'].append(similarity(tags))
                time.sleep(0.1)

df = pd.DataFrame(data)
df = df.sort_values(by=['similarity', 'rating'], ascending=False)
df.to_csv(f'summary.csv', index=False)
