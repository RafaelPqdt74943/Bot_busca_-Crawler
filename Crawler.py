import re
import requests
from bs4 import BeautifulSoup

Dominio = "https://django-anuncios.solyd.com.br"
URL_automoveis = f"{Dominio}/automoveis/"

def requisicao(url):
    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            return resposta.text
        else:
            print(f"Erro ao fazer requisição: {resposta.status_code}")
    except requests.RequestException as error:
        print("Erro ao fazer requisição:", error)

def parsing(resposta_HTML):
    try:
        soup = BeautifulSoup(resposta_HTML, 'html.parser')
        return soup
    except Exception as error:
        print("Erro ao fazer o parsing HTML:", error)

def encontrar_links(soup):
    try:
        cards_pai = soup.find("div", class_="ui three doubling link cards")
        if not cards_pai:
            print("Não foi possível encontrar os cartões de links.")
            return []
        cards = cards_pai.find_all("a")
    except Exception as error:
        print("Erro ao encontrar links:", error)
        return []

    links = []
    for card in cards:
        try:
            link = card["href"]
            links.append(link)
        except KeyError:
            pass
    return links

def encontrar_telefone(soup):
    try:
        descricao = soup.find_all("div", class_="sixteen wide column")[2].p.get_text().strip()
    except IndexError:
        print("Erro ao encontrar descrição: elemento não encontrado.")
        return None
    except Exception as error:
        print("Erro ao processar descrição:", error)
        return None

    regex = re.findall(r"\(?0?([1-9]{2})\)?[ \.\-]?(9?\d{4})[ \.\-]?(\d{4})", descricao)
    if regex:
        return ["({}) {}-{}".format(*telefone) for telefone in regex]
    return None

# Executa o processo principal
resposta_busca = requisicao(URL_automoveis)

if resposta_busca:
    soup_busca = parsing(resposta_busca)
    if soup_busca:
        links = encontrar_links(soup_busca)
        for link in links:
            resposta_anuncio = requisicao(Dominio + link)
            if resposta_anuncio:
                soup_anuncio = parsing(resposta_anuncio)
                if soup_anuncio:
                    telefones = encontrar_telefone(soup_anuncio)
                    if telefones:
                        print("Telefones encontrados:", telefones)
                    else:
                        print("Nenhum telefone encontrado.")
