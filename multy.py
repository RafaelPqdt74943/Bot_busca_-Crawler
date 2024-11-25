import time
import threading

def fazer_requicao_web ():
    print("fazendo requisição....")
    time.sleep(3)
    print("terminei a requisiçao")
    
thread_1 = threading.Thread(target=fazer_requicao_web)
thread_1.start()

thread_2 = threading.Thread(target=fazer_requicao_web)
thread_2.start()

thread_3 = threading.Thread(target=fazer_requicao_web)
thread_3.start()

