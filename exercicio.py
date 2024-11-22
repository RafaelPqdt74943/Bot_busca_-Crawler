lista = []
print(lista)

def adicionar_dado_lista_string(lista):
    if not lista :            
        for i in range(5):
            i= input("digite o dado que deseja adicionar a lista: ")
            lista.append(i)
            print(lista)
    else:
        print("ocorreu algum erro")
        
        
adicionar_dado_lista_string(lista)

def remover_dado_lista_string(lista):
    if lista:        
        for i in range(5):
            i= input("digite o dado que deseja remover da lista: ")
            lista.remove(i)
            print(lista)
    else:
        print("digite um dado que esteja na lista")
        
remover_dado_lista_string(lista)

dicionario = {}


def adicionar_dado_dicionario(dicionario):
        for i in range(5):
            chave=input("valor da chave? ")
            dado =input("valor do dado? ")
            dicionario.update({chave : dado})
            print(dicionario)
    
            
adicionar_dado_dicionario(dicionario)
            
            
            

