import re

import requests

from bs4 import BeautifulSoup


Dominio = "https://django-anuncios.solyd.com.br"

URL_automoveis= "https://django-anuncios.solyd.com.br/automoveis/"

def requisicao (url):
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
    try:
        cards_pai = soup.find("div", class_= "ui three doubling link cards")
        cards = cards_pai.find_all("a")
    except:
        print(" erro ao encontrar link")
        return None
    
    links = []
    for card in cards : 
        try:
            link =card["href"]
            links.append(link)
        except:
            pass
    return links

def encontrar_telefone (soup):
    try:
        descricao = soup.find_all("div", class_ ="sixteen wide column")[2].p.get_text().strip()
    except:
        print(" erro ao encontrar descrição")
        return None
    
    regex = re.findall(r"\(?0?([1-9]{2})[\-\.\)]{0,2}(9[ \-\.]?\d{4})[ \-\.]?(\d{4})", descricao)
    if regex:
        return regex
    
    
    


        
resposta_busca=requisicao(URL_automoveis)  
        
if resposta_busca:
    soup_busca=parsing(resposta_busca)
    if soup_busca:
        links = encontrar_link(soup_busca)
        for link in links :
            resposta_anuncio=requisicao(Dominio + links[0])  
            if resposta_anuncio : 
                soup_anuncio = parsing(resposta_anuncio)       
                if soup_anuncio : 
                    print(encontrar_telefone(soup_anuncio))
    
    
    #print(soup.title) # manipulando o HTML
    #print(soup.prettify()) # manipulando o HTML
    #cards_pai = soup.find("div", class_= "ui three doubling link cards")
    #card = cards_pai.find_all("a")
    #print(card[0]["href"])
    
