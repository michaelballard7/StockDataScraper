from os import chdir
import pandas as pd
import requests 
from tabulate import tabulate
from bs4 import BeautifulSoup 

chdir("/Users/MichaelBallard/Desktop/stockScraper/data")

universe = pd.read_csv("../data/assetUniverseDirty.csv", index_col=None)

universe = universe.drop(universe.columns[universe.columns.str.contains('unnamed',case = False)],axis = 1)

raw_table  = tabulate(universe,headers='keys', tablefmt='psql')

prices_by_ticker = {}
market_caps = []
last_prices = []

for i in range(0,len(universe)):
    market_caps.append(0)
    last_prices.append(0)

for i in range(0,5):
    headers = {'User-Agent': 'Mozilla/<version> (<system-information>) <platform> (<platform-details>) <extensions>'}
    url = 'https://www.zacks.com/stock/quote/{}'.format(universe['Symbol'][i])
    req = requests.get(url, headers=headers)
    html = req.text.strip()
    soup = BeautifulSoup(html,'lxml')
    table = soup.findAll("table", class_="abut_bottom")
    try:    
        ticker = universe['Symbol'][i]
        last_price = soup.find(class_="last_price")
        last_prices[i] = last_price.text
        price = {ticker:last_price.text}
    except:
        price = {ticker:0}
        last_prices[i] = 0
    prices_by_ticker = prices_by_ticker.copy()
    prices_by_ticker.update(price)

    for tr in table:
        for td in tr.find_all("td"):
            if td.text == "Market Cap":
                try:
                    market_caps[i]=td.find_next_sibling("td").text 
                except: 
                    market_caps[i] = None 

universe['Last Price'] = last_prices
universe['Market Cap'] = market_caps
universe.to_csv("assetUniverseClean.csv")

    









