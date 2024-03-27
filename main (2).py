import time
import requests
from bs4 import BeautifulSoup

link = "https://hotline.ua/big-home/holodilniki/"
pages_qty = 42

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'accept-language': 'uk-UA,uk;q=0.9,ru;q=0.8,en-US;q=0.7,en;q=0.6'
}

sess = requests.session()

fridges_data = []
shops_data = []

def getAllData():
    for i in range(pages_qty):
        if i == 0:
            continue
        time.sleep(1)
        link = f"https://hotline.ua/big-home/holodilniki/?p={i}" 
        r = sess.get(link, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        items = soup.find_all('div', {'class': 'list-item'})
        for item in items:
            link = item.find('a', {'class': 'item-title'})['href']
            name = item.find('a', {'class': 'item-title'}).text.strip()
            fridges_data.append({
                'name': name,
            })

def getShopsData():
    for item in fridges_data:
        r = sess.get(item['detailed_data_link'], headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        content = soup.find_all('div', {'class': 'list'})[1]
        list_items = content.find_all('div', {'class': 'list__item row flex'})
        for list_item in list_items:
            price = list_item.find('span', {'class': 'price__value'}).text.strip()
            shop_name = list_item.find('a', {'class': 'shop__title'}).text.strip()
            print(price, shop_name)

getAllData()
getShopsData()

print("done!")
