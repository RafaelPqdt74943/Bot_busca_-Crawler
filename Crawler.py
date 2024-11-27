# Importação de bibliotecas necessárias
import re  # Para trabalhar com expressões regulares
import threading  # Para trabalhar com threads (execuções paralelas)
import requests  # Para fazer requisições HTTP
from bs4 import BeautifulSoup  # Para parsear HTML (raspagem de dados)

# Definição de constantes do domínio base e URL inicial para busca de anúncios
DOMINIO = "https://django-anuncios.solyd.com.br"
URL_AUTOMOVEIS = "https://django-anuncios.solyd.com.br/automoveis/"

# Listas globais para armazenar links de anúncios e números de telefone
LINKS = []
TELEFONES = []

# Função para realizar requisições HTTP e retornar o conteúdo da página
def requisicao(url):
    try:
        resposta = requests.get(url)  # Faz a requisição HTTP
        if resposta.status_code == 200:  # Verifica se o status da resposta é "OK"
            return resposta.text  # Retorna o conteúdo da página (HTML)
        else:
            print("Erro ao fazer requisição")
    except Exception as error:
        print("Erro ao fazer requisição")
        print(error)

# Função para realizar o parsing do HTML utilizando BeautifulSoup
def parsing(resposta_html):
    try:
        soup = BeautifulSoup(resposta_html, 'html.parser')  # Parseia o HTML
        return soup
    except Exception as error:
        print("Erro ao fazer o parsing HTML")
        print(error)

# Função para encontrar links de anúncios na página principal
def encontrar_links(soup):
    try:
        # Localiza o container com os links de anúncios
        cards_pai = soup.find("div", class_="ui three doubling link cards")
        cards = cards_pai.find_all("a")  # Encontra todos os links (tags <a>) dentro do container
    except:
        print("Erro ao encontrar links")
        return None

    links = []
    for card in cards:  # Itera sobre cada card encontrado
        try:
            link = card['href']  # Extrai o atributo 'href' (URL do anúncio)
            links.append(link)  # Adiciona o link à lista
        except:
            pass  # Ignora erros ao extrair links

    return links

# Função para extrair números de telefone da descrição de um anúncio
def encontrar_telefone(soup):
    try:
        # Localiza a descrição do anúncio (presumivelmente na terceira coluna wide)
        descricao = soup.find_all("div", class_="sixteen wide column")[2].p.get_text().strip()
    except:
        print("Erro ao encontrar descrição")
        return None

    # Utiliza expressão regular para encontrar padrões de números de telefone
    regex = re.findall(r"\(?0?([1-9]{2})[ \-\.\)]{0,2}(9[ \-\.]?\d{4})[ \-\.]?(\d{4})", descricao)
    if regex:
        return regex

# Função que processa os links de anúncios para encontrar telefones
def descobrir_telefones():
    while True:
        try:
            link_anuncio = LINKS.pop(0)  # Remove o primeiro link da lista
        except:
            return None  # Encerra a thread se a lista de links estiver vazia

        # Faz a requisição para o link do anúncio
        resposta_anuncio = requisicao(DOMINIO + link_anuncio)

        if resposta_anuncio:
            soup_anuncio = parsing(resposta_anuncio)  # Parseia o HTML do anúncio
            if soup_anuncio:
                telefones = encontrar_telefone(soup_anuncio)  # Busca telefones no anúncio
                if telefones:
                    for telefone in telefones:  # Itera pelos telefones encontrados
                        print("Telefone encontrado:", telefone)
                        TELEFONES.append(telefone)  # Adiciona à lista global
                        salvar_telefone(telefone)  # Salva o telefone no arquivo

# Função para salvar os números de telefone em um arquivo CSV
def salvar_telefone(telefone):
    # Formata o número de telefone como uma string única
    string_telefone = "{}{}{}\n".format(telefone[0], telefone[1], telefone[2])
    try:
        with open("telefones.csv", "a") as arquivo:  # Abre o arquivo em modo de adição
            arquivo.write(string_telefone)  # Escreve o telefone no arquivo
    except Exception as error:
        print("Erro ao salvar arquivo")
        print(error)

# Ponto de entrada do programa
if __name__ == "__main__":
    # Faz a requisição inicial para a página de automóveis
    resposta_busca = requisicao(URL_AUTOMOVEIS)
    if resposta_busca:
        soup_busca = parsing(resposta_busca)  # Parseia o HTML da página
        if soup_busca:
            LINKS = encontrar_links(soup_busca)  # Encontra links de anúncios

            # Cria uma lista para threads e inicializa 10 threads para processamento paralelo
            THREADS = []
            for i in range(10):
                t = threading.Thread(target=descobrir_telefones)  # Define a função a ser executada por cada thread
                THREADS.append(t)

            for t in THREADS:
                t.start()  # Inicia todas as threads

            for t in THREADS:
                t.join()  # Aguarda a conclusão de todas as threads
                
                
#projeto finalizado
