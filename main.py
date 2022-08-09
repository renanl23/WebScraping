import pandas as pd
import requests
from bs4 import BeautifulSoup

# OLX bloqueia requisição do python
url_olx = {
    'venda' : 'https://rn.olx.com.br/rio-grande-do-norte/natal/imoveis/venda',
    'aluguel' : 'https://rn.olx.com.br/rio-grande-do-norte/natal/imoveis/aluguel'
}

url_vivareal = {
    'venda':'https://www.vivareal.com.br/venda/rio-grande-do-norte/natal/',
    'aluguel':'https://www.vivareal.com.br/aluguel/rio-grande-do-norte/natal/'
}

url_trovit = {
    'venda' : 'https://imoveis.trovit.com.br/index.php/cod.search_homes/type.1/what_d.natal/sug.0/isUserSearch.1/origin.11',
    'aluguel': 'https://imoveis.trovit.com.br/index.php/cod.search_homes/type.2/what_d.natal/sug.0/isUserSearch.1/origin.11'
}


url = url_trovit['venda']

def getWebScrapingResponse(url):
    req = requests.get(url)
    if req.status_code == 200:
        print('HTTP 200 OK')
        req_soup = BeautifulSoup(req.content, 'html.parser')
        return req_soup
    else:
        print(req)
        return

def executarWebScraping(url):
    req = requests.get(url)
    if (req.status_code == 200):
        print('HTTP 200 OK')
        req_soup = BeautifulSoup(req.content, 'lxml')
        trovitWebScraping(req_soup)
    else:
        print(req)
        return

def trovitWebScraping(htmlContent):
    indexElement = 0
    trovitElements = htmlContent.findAll("div", {"class": "js-item"})
    # for trovitElement in trovitElements:
    #     urlElement = trovitElement.find('a').get('href')
    #     trovitWebScrapingElement(urlElement)

    elementTest = trovitElements[0].find('a').get('href')
    print(indexElement + 1)
    print(elementTest)
    trovitWebScrapingElement(elementTest)

def trovitLinkRedirectHandle(urlElement):
    reqElement = getWebScrapingResponse(urlElement)
    urlRedirectElement = reqElement.find('body').find('meta').get('content').split('url=',1)[1]
    if 'quintoandar' in urlRedirectElement:
        print('Quindo Andar Link')
        print(urlRedirectElement)
        quintoAndarWebScraping(urlElement)

    else:
        print('Não é link do Quinto Andar')
        print(urlRedirectElement)

def quintoAndarLinkRedirectHandle(urlElement):
    reqElement = getWebScrapingResponse(urlElement)
    text = reqElement.find('body')
    print(text)
    # return eval(reqElement.find('body').get('onload').split('location.href=')[1])

def trovitWebScrapingElement(urlElement):
    #reqElement = getWebScrapingResponse(urlElement)
    #print(reqElement)
    trovitLinkRedirectHandle(urlElement)

def quintoAndarWebScraping(urlElement):
    quintoAndarLinkRedirectHandle(urlElement)
    # quintoAndarURL = quintoAndarLinkRedirectHandle(urlElement)
    # print(quintoAndarURL)




executarWebScraping(url)
