# потоки, мешающие завершению программы - демоны
# при создании демонического потока до запуска программы
# когда основной поток завершает демо поток тоже закроется

# import threading
# import time

# def h():
#     while True:
#         print("Фоновая задача работает")
#         time.sleep(1)
      
# t=threading.Thread(target=h,daemon=True)
# t.start()
# print(f"Основная программа завершится через 3 секунды")
# time.sleep(3)

import socket
import threading

clients=[]
lock=threading.Lock()

def server(client_socket, client_addr):
    print(f"Подключился клиент {client_addr}")
    client_socket.send("приветик в чате".encode('utf-8'))
    with lock:
        for clien in clients:
            if clien != client_socket:
                try:
                    clien.send(f"Клиент {client_addr} присоединяется к чату".encode('utf-8'))
                except:
                    pass

    while True:
        try:
            message = client_socket.recv(1024)
        except:
            break   
        if not message:
            break   
        
        message_decode = message.decode('utf-8')
        print(f"Клиент по адресу {client_addr} отправил сообщение {message_decode}")
        
        with lock:
            for clien in clients:
                if clien != client_socket:
                    try:
                        clien.send(f"{client_addr}: {message_decode}".encode('utf-8'))
                    except:
                        pass

    with lock:
        if client_socket in clients:
            clients.remove(client_socket)
    client_socket.close()
    print(f"Клиент {client_addr} отключился")
    
    with lock:
        for clien in clients:
            try:
                clien.send(f"Клиент {client_addr} покинул чат".encode('utf-8'))
            except:
                pass                

server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
server_socket.bind(("127.0.0.1",5000))
server_socket.listen()

print("Сервер ждет подключения клиента")

while True:
    client_socket,client_adrr=server_socket.accept()
    with lock:
        clients.append(client_socket)
    t=threading.Thread(target=server,args=(client_socket,client_adrr), daemon=True).start()                
