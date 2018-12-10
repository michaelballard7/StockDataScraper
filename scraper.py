from os import chdir
import pandas as pd
import requests 
from tabulate import tabulate
from bs4 import BeautifulSoup 

chdir("/Users/MichaelBallard/Desktop/stockScraper/data")

universe = pd.read_csv("../data/assetUniverse.csv", index_col=None)

universe = universe.drop(universe.columns[universe.columns.str.contains('unnamed',case = False)],axis = 1)

raw_table  = tabulate(universe,headers='keys', tablefmt='psql')

market_caps = []
prices = {}

for i in range(0,len(universe)):
    market_caps.append(0)
for i in range(0,3):
    headers = {'User-Agent': 'Mozilla/<version> (<system-information>) <platform> (<platform-details>) <extensions>'}
    url = 'https://www.zacks.com/stock/quote/{}'.format(universe['Symbol'][i])
    req = requests.get(url, headers=headers)
    html = req.text.strip()
    soup = BeautifulSoup(html,'lxml')
    table = soup.findAll("table", class_="abut_bottom")
    try:    
        ticker = universe['Symbol'][i]
        last_price = soup.find(class_="last_price")
        price = {ticker:last_price.text}
    except:
        # bug here, attached a null to empty ticker data, leave values consistent
        print("no value")
        continue
    prices = prices.copy()
    prices.update(price)
    # print("Last Prices",prices)

    for tr in table:
        for td in tr.find_all("td"):
            if td.text == "Market Cap":
                try:
                    market_caps[i]=td.find_next_sibling("td").text 
                except: 
                    market_caps[i] = None 
    universe['Market Cap'] = market_caps

print(universe.head(3))

    









