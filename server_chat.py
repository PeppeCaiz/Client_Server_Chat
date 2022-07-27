import socket
import threading
from pathlib import Path


parent = Path(__file__).parent
file = Path(parent, 'BAN.txt')

users_list = []
sock_list = []
adr_list=[]
n_seen= set()

ENC = 'utf-8'
adm_sock = ""
adm_add = ""
n=""

# server's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 49153  # port we want to use


# initialize list/set of all connected client's sockets
client_sockets = set(sock_list)

# create a TCP socket
s = socket.socket()
# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))
# listen for upcoming connections
s.listen(5)

print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")


def kick_user(name, motivo):
    if name in users_list:          
        
        name_index = users_list.index(name)
        print(name_index)
        print(adr_list[name_index])
        client_to_kick = sock_list[name_index]
        client_to_kick.send(f"{motivo}".encode(ENC))






def listen_for_client(cs):

    global adm_add, adm_sock
    n_seen = set(users_list)
    
    m, n = "", ""
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    while True:
        

        try:
            # keep listening for a message from `cs` socket
            msg = cs.recv(1024).decode(ENC)
            
            msg = str(msg)
            
            
            
            if (msg.startswith(".")):
                n = msg.removeprefix(".")
                
                if (n in n_seen):
                    cs.send(f"CLOSE".encode(ENC))
                    cs.close()
                else:
                    n_seen.add(n)
                    so_index=sock_list.index(cs)
                    users_list.insert(so_index, n)
                    
                    
                            
            elif( msg.startswith("$")):
                psw=msg.removeprefix("$")
                if not (psw=="Password"):
                    cs.send(f"CLOSE".encode(ENC))
                
            elif(msg.startswith("/") and (n == "admin")):
                command, argument = msg.split(" ")

                if command== "/ban":
                    print(msg)
                    broadcast(f'-{argument} è stato espulso da un admin!\n')
                    with open(file, 'a+') as f:
                        f.write(f'{argument}\n')
                    kick_user(argument, "BAN")

                elif command == "/kick":
                    print(msg)
                    broadcast(f'-{argument} è stato cacciato da un admin!\n')
                    kick_user(argument, "KICK")
                    
                elif command == "/pardon":
                    print(msg)
                    ban =[]
                    with open(file, "r")as f:
                        ban=f.readlines()
                        ban.remove(f"{argument}\n")
                        with open(file, "w")as w:
                            for names in ban:
                                ind=ban.index(names)
                                w.write(ban[ind])
                        f.close()    
                        
                if msg == "/users list":
                    print(msg)
                    print(users_list)
                    cs.send(f"-Utenti:".encode(ENC))
                    cs.send(f"- {users_list}".encode(ENC))
                    cs.send(f"- {adr_list}\n".encode(ENC))
                    
                
                elif msg =="/bans list":
                    with open(file, "r")as f:
                        bans=f.readlines()
                    cs.send(f"Gli utenti bannati sono: {bans}\n".encode(ENC))                    
            else:
                broadcast(msg)
                
        
        except :
            if cs in sock_list:
                index = sock_list.index(cs)
                sock_list.remove(cs)
                client_sockets.remove(cs)
                cs.close()
                try:
                    nickname = users_list[index]
                    broadcast(f'{nickname}: {adr_list[index]} è uscito dalla chat!')
                    print(f'{nickname} è uscito dalla chat!')
                    users_list.remove(nickname)
                    n_seen.remove(nickname)
                except:
                    print(f'{adr_list[index]} è uscito dalla chat!')
                break

        else:
            with open(file, 'r')as f:
                        bans = f.readlines()
                        
                        if f"{n}\n" in bans:
                            cs.send('BAN'.encode(ENC))
def broadcast(m):
    for cs in client_sockets:
        # and send the message
        cs.send(m.encode(ENC))
    
while True:
    # we keep listening for new connections all the time
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connesso.\n")

    # add the new connected client to connected sockets
    client_sockets.add(client_socket)
    sock_list.append(client_socket)
    adr_list.append(client_address)   
    
    # start a new thread that listens for each client's messages
    t =threading.Thread(target=listen_for_client, args=(client_socket, ))

    # make the thread daemon so it ends whenever the main thread ends
    t.daemon=True
    # start the thread
    t.start()


# close client sockets
for client_socket in sock_list:
    client_socket.send(f"CLOSE".encode(ENC))
    client_socket.close()
# close server socket
s.close()
