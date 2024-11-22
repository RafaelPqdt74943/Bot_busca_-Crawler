import requests

from bs4 import BeautifulSoup


Dominio = "https://django-anuncios.solyd.com.br"

URL_automoveis= "https://django-anuncios.solyd.com.br/automoveis/"

def buscar (url):
    try:
        resposta=requests.get(url)
        if resposta.status_code == 200 : 
           return resposta.text
        else:
            print("erro ao fazer requisição")
    except Exception as error:
        print("erro ao fazer requisição")
        print(error)
        

def parsing(resposta_HTML) : 
    try:
        soup = BeautifulSoup(resposta_HTML, 'html.parser') 
        return soup
    except Exception as error : 
        print("erro ao fazer o parsing HTML")
        print(error)   
        
def encontrar_link (soup):
    cards_pai = soup.find("div", class_= "ui three doubling link cards")
    cards = cards_pai.find_all("a")
    
    links = []
    for card in cards : 
        link =card["href"]
        links.append(link)
    
    return links
        
resposta=buscar(URL_automoveis)  
        
if resposta:
    soup=parsing(resposta)
    if soup:
        links = encontrar_link(soup)
        print(links)
            
    
    
    #print(soup.title) # manipulando o HTML
    #print(soup.prettify()) # manipulando o HTML
    #cards_pai = soup.find("div", class_= "ui three doubling link cards")
    #card = cards_pai.find_all("a")
    #print(card[0]["href"])
    
