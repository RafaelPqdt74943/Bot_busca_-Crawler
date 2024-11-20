import requests

from bs4 import BeautifulSoup



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
        
resposta=buscar(URL_automoveis)  
        
if resposta:
    soup=parsing(resposta)
    print(soup.title) # manipulando o HTML
    #print(soup.prettify()) # manipulando o HTML
