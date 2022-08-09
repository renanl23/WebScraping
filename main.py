import pandas as pd
import requests
from bs4 import BeautifulSoup

url_olx = {
    'venda' : 'https://rn.olx.com.br/rio-grande-do-norte/natal/imoveis/venda',
    'aluguel' : 'https://rn.olx.com.br/rio-grande-do-norte/natal/imoveis/aluguel'
}

url_vivareal = {
    'venda':'https://www.vivareal.com.br/venda/rio-grande-do-norte/natal/',
    'aluguel':'https://www.vivareal.com.br/aluguel/rio-grande-do-norte/natal/',
    'casa': 'https://www.vivareal.com.br/venda/rio-grande-do-norte/natal/casa_residencial/',
    'apartamento':'https://www.vivareal.com.br/venda/rio-grande-do-norte/natal/apartamento_residencial/',
    'cobertura': 'https://www.vivareal.com.br/venda/rio-grande-do-norte/natal/cobertura_residencial/',
    'flat':'https://www.vivareal.com.br/venda/rio-grande-do-norte/natal/flat_residencial/'
}

url_trovit = {
    'venda' : 'https://imoveis.trovit.com.br/index.php/cod.search_homes/type.1/what_d.natal/sug.0/isUserSearch.1/origin.11',
    'aluguel': 'https://imoveis.trovit.com.br/index.php/cod.search_homes/type.2/what_d.natal/sug.0/isUserSearch.1/origin.11'
}


url = url_vivareal['venda']

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

def getWebScrapingResponse(url):
    req = requests.get(url, headers=header)
    if req.status_code == 200:
        print('HTTP 200 OK')
        req_soup = BeautifulSoup(req.content, 'html.parser')
        return req_soup
    else:
        print(req)
        return

def executarWebScraping(url):
    # Capturar anuncios no Viva Real
    # Paginação: ?pagina=X
    vivaRealWebScraping(getWebScrapingResponse(url))


def vivaRealWebScraping(htmlContent):
    indexElement = 0
    url = 'https://www.vivareal.com.br'
    # Capturar link no título do anuncio
    lista = htmlContent.findAll('a', {"class":"js-card-title"})

    # link1 = url+lista[0].get('href')
    # print(link1)
    # vivaRealWebScrapingElement(link1)

    # São exibidos 36 anuncios por página
    for item in lista:
        indexElement += 1
        link = url+item.get('href')
        print(vivaRealWebScrapingElement(link))
    print(indexElement)

def getTextFromElement(Element):
    if Element is None:
        return ''
    else:
        return Element.text.strip()

def vivaRealWebScrapingElement(vivaRealURL):
    resp = getWebScrapingResponse(vivaRealURL)
    titulo = getTextFromElement(resp.find('h1', {"class": "js-title-view"}))
    endereco = getTextFromElement(resp.find('p', {"class": "js-address"}))
    condominio = getTextFromElement(resp.find('span', {"class": "js-condominium"}))
    area = getTextFromElement(resp.find('li', {"class": "js-area"}))
    banheiros = getTextFromElement(resp.find('li', {"class": "js-bathrooms"}))
    vagasEstacionamento = getTextFromElement(resp.find('li', {"class": "js-parking"}))
    preco = getTextFromElement(resp.find('h3', {"class": "js-price-sale"}))
    anuncio = {
        'titulo': titulo,
        'endereco': endereco,
        'condominio': condominio,
        'area': area,
        'banheiros': banheiros,
        'vagasEstacionamento': vagasEstacionamento,
        'preco': preco
        }
    return anuncio

executarWebScraping(url)
