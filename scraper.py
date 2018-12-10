

from os import chdir
import pandas as pd
import requests 
from tabulate import tabulate
from bs4 import BeautifulSoup 

chdir("/Users/MichaelBallard/Desktop/stockScraper/data")

universe = pd.read_csv("../data/assetUniverse.csv", index_col=None)

raw_table  = tabulate(universe,headers='keys', tablefmt='psql')

market_caps = []
volumes = {}
prices = {}


for i in range(0,len(universe)):
    headers = {'User-Agent': 'Mozilla/<version> (<system-information>) <platform> (<platform-details>) <extensions>'}
    url = 'https://www.zacks.com/stock/quote/{}'.format(universe['Symbol'][i])
    req = requests.get(url, headers=headers)
    html = req.text.strip()
    soup = BeautifulSoup(html,'lxml')
    table = soup.findAll("table", class_="abut_bottom")

    ticker = universe['Symbol'][i]
    last_price = soup.find(class_="last_price")
    price = {ticker:last_price.text}
    prices = prices.copy()
    prices.update(price)
    print("Last Prices",prices)

    for tr in table:
        for td in tr.find_all("td"):
            if td.text == "Avg. Volume":
                avg_volume = td.text
                value = td.find_next_sibling("td").text
                data = {universe['Symbol'][i]: value}
                volumes = volumes.copy()
                volumes.update(data)
                market_caps.append({'company': ticker,'marketCap': value})
                print(td.text, market_caps)









