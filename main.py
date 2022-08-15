import pandas as pd
import requests
from bs4 import BeautifulSoup

url_vivareal = {
    'venda':'https://www.vivareal.com.br/venda/rio-grande-do-norte/natal/',
    'aluguel':'https://www.vivareal.com.br/aluguel/rio-grande-do-norte/natal/',
    'casa': 'https://www.vivareal.com.br/venda/rio-grande-do-norte/natal/casa_residencial/',
    'apartamento':'https://www.vivareal.com.br/venda/rio-grande-do-norte/natal/apartamento_residencial/',
    'cobertura': 'https://www.vivareal.com.br/venda/rio-grande-do-norte/natal/cobertura_residencial/',
    'flat':'https://www.vivareal.com.br/venda/rio-grande-do-norte/natal/flat_residencial/'
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
        return None

def executarWebScraping(url):
    # Capturar anuncios no Viva Real
    # Quantidade de Anuncios ?size=[] (Até 250)
    # Paginação: ?pagina=X
    quantidadeAnuncio = '?size=250'
    vivaRealWebScraping(getWebScrapingResponse(url+quantidadeAnuncio))


def vivaRealWebScraping(htmlContent):
    indexElement = 0
    url = 'https://www.vivareal.com.br'
    # Capturar link no título do anuncio
    lista = htmlContent.findAll('a', {"class":"js-card-title"})

    # link1 = url+lista[0].get('href')
    # print(link1)
    # objeto = vivaRealWebScrapingElement(link1)
    # print(objeto)

    # São exibidos 250 anuncios por página
    anuncioLista = []

    for item in lista:
        indexElement += 1
        link = url+item.get('href')
        anuncio = vivaRealWebScrapingElement(link)
        # dataTable = pd.DataFrame.from_dict(anuncio, orient='index')
        if anuncio is None:
            break
        else:
            print('Anuncio ' + str(indexElement) + ' capturado')
            anuncioLista.append(anuncio)
    if not anuncioLista is None:
        df = pd.DataFrame(anuncioLista)
        df.to_csv('vivareal.csv',encoding='utf-8', index=False)
    # precisa instalar o módulo openpyxl
    # df.to_excel('vivareal.xlsx',encoding='utf-8', index=False)


def getTextFromElement(Element):
    if Element is None:
        return ''
    else:
        return Element.text.strip()

def catchIndexError(Element):
  try:
     return Element[0]
  except IndexError:
    return None

def vivaRealWebScrapingElement(vivaRealURL):
    resp = getWebScrapingResponse(vivaRealURL)
    # Não retornou HTTP 200
    if resp is None:
        return None

    titulo = getTextFromElement(resp.find('h1', {"class": "js-title-view"}))
    endereco = getTextFromElement(resp.find('p', {"class": "js-address"}))
    condominio = getTextFromElement(resp.find('span', {"class": "js-condominium"}))
    area = getTextFromElement(resp.find('li', {"class": "js-area"}))
    suite = getTextFromElement(catchIndexError(resp.select(".js-bathrooms > small")))
    banheiros = getTextFromElement(resp.find('li', {"class": "js-bathrooms"}))
    #retira o texto de suite de dentro da tag banheiro
    banheiros = banheiros.replace(suite, '')
    vagasEstacionamento = getTextFromElement(resp.find('li', {"class": "js-parking"}))
    preco = getTextFromElement(resp.find('h3', {"class": "js-price-sale"}))
    anuncio = {
        'titulo': titulo,
        'endereco': endereco,
        'condominio': condominio,
        'area': area,
        'banheiros': banheiros,
        'suite': suite,
        'vagasEstacionamento': vagasEstacionamento,
        'preco': preco
        }
    return anuncio

executarWebScraping(url)
