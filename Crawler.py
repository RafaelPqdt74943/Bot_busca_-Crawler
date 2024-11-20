import requests


URL_automoveis= "https://django-anuncios.solyd.com.br/automoveis/"

def buscar (url):
    try:
        resposta=requests.get(url)
        if resposta.status_code == 200 : 
            print(resposta.text)
        else:
            print("ero ao fazer requisição")
    except Exception as error:
        print("erro ao fazer requisição")
        print(error)
        
buscar(URL_automoveis)