import requests
from bs4 import BeautifulSoup


url = 'https://finviz.com/screener.ashx?v=111&f=exch_nyse,fa_div_o2,sh_avgvol_o50,sh_relvol_o1,targetprice_below'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

totalText = soup.find("td", class_="count-text").text
totalTickers = int(totalText.split(" ")[1])
totalPages = int(totalTickers / 20) if totalTickers % 20 == 0 else (totalTickers // 20) + 1

tickers = []
for i in range(totalPages):
    url = url + '&r=' + str((i * 20) + 1)
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    tickerList = soup.findAll("tr", class_="table-dark-row-cp")
    tickerList += soup.findAll("tr", class_="table-light-row-cp")
    for j in range(len(tickerList)):
        tickerList[j] = tickerList[j].find("td", class_="screener-body-table-nw").nextSibling.find("a").text
    tickers += tickerList

print(sorted(tickers))
