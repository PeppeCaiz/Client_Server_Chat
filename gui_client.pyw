import socket
import tkinter as tk
import tkinter.scrolledtext as st
from datetime import datetime
from threading import Thread

ENC ='utf-8'

def metti(x, y, z):
    x.grid()
    y.grid()
    z.grid()

def togli(x, y, z):
    x.grid_remove()
    y.grid_remove()
    z.grid_remove()

def listen_for_messages():
    while True:
        
        message = s.recv(1024).decode(ENC)
        print(message)
        text_area.configure(state='normal')
        if(message == "BAN" or message == "KICK" or message == "CLOSE"):
            chiudi()
        else:
            text_area.insert(tk.END, "\n" + message)
        text_area.configure(state='disabled')

def invia_m():
    global s
    global nome
    to_send = e_msg.get()
    
    if to_send.lower() == 'q' : 
        chiudi()
    else:
        # add the datetime, name & the color of the sender
        date_now = datetime.now().strftime('[%Y-%m-%d][%H:%M:%S]')
        message = f"\n{date_now} | {nome} |: {to_send}"
        text_area.configure(state='normal')
        if to_send.startswith('/'):
            if nome=="admin":
                try:
                    command, user =to_send.split(" ")
                    
                    if (command=="/kick"):
                        s.send(f"{command} {user}".encode(ENC))
                        text_area.insert(tk.END,f"\n-{nome}:{command} {user}")
                        
                    elif(command == '/ban'):
                        s.send(f"{command} {user}".encode(ENC))
                        text_area.insert(tk.END,f"\n-{nome}:{command} {user}")
                    
                    elif(command=="/users" and user=="list"):
                        s.send(f"{command} list".encode(ENC))
                        text_area.insert(tk.END,f"\n-{nome}:{command} {user}")
                    
                    elif(command=="/pardon"):
                        s.send(f"{command} {user}".encode(ENC))
                        text_area.insert(tk.END, f"\n-{nome}:{command} {user}")
                    
                    elif(command == "/bans" and user == "list"):
                        s.send(f"{command} list".encode(ENC))
                        text_area.insert(tk.END, f"\n-{nome}:{command} {user}")
                    
                except:
                    if(to_send=="/help"):
                        text_area.insert(tk.END, "\n| /kick User   | Per cacciare un utente\n| /ban User    | Per esiliare un utente\n| /pardon User | Per riammettere un utente\n| /bans list   | Per ricevere una lista degli utenti esiliate\n| /users list  | Per ricevere una lista degli utenti")

            else:
                text_area.insert(tk.END, "\n-I comandi possono essere eseguiti solo dagli admin!")
                
        else:    
            # finally, send the message
            s.send(message.encode(ENC))
        text_area.configure(state='disabled')
        e_msg.delete(0, tk.END)
def change_n():
    global s
    global nome

    metti(l_name, e_name, b_newN)
    togli(l_msg, e_msg, b_msg)
    b_change_n.grid_remove()

    s.send(f"\n-{nome} sta cambiando nome ".encode(ENC))
    e_name.delete(0, tk.END)

def new_name():
    global s
    global nome
    z = nome
    b_change_n.grid_remove()
    text_area.configure(state='normal')
    nome = e_name.get()
    if(nome == ""):
        text_area.insert(tk.END, "\nErrore nome inserito non valido")
    else:
        if(z == nome):
            text_area.insert(tk.END, "\nnon hai cambiato nome ma ti voglio bene lo stesso")
        s.send(f"-il nuovo nome di |{z}| è: |{nome}|".encode(ENC))
        s.send(f".{nome}".encode(ENC))
        text_area.configure(state='disabled')
        togli(l_name, e_name, b_newN)
        metti(l_msg, e_msg, b_msg)
        b_change_n.grid()

def invia_p():
    psw = e_pass.get()

    if(nome=="admin"):
        if(psw=="Password"):
            s.send(f".{nome}".encode(ENC))
            s.send(f"${psw}".encode(ENC))
            
            text_area.configure(state="normal")
            text_area.insert(tk.END, "il tuo nome e': "+nome+"\n")
            text_area.insert(tk.END, "/help per ricevere la lista dei comandi\n")
            text_area.configure(state='disabled')
            togli(l_pass, e_pass, b_pass)
            metti(l_msg, e_msg, b_msg)
            b_change_n.grid()
            e_name.delete(0, tk.END)
            e_pass.delete(0, tk.END)
            e_name.grid_remove()
            l_name.grid_remove()
        else:
            chiudi()
        
    

def invia_n():
    global nome
    text_area.configure(state='normal')
    nome = e_name.get()
    if(nome == ""):
        text_area.insert(tk.END, "\nErrore nome inserito non valido")
        
    elif(nome=="admin"):
        metti(l_pass,e_pass,b_pass)
        b_name.grid_remove()
    else:
        s.send(f".{nome}".encode(ENC))
        
        text_area.insert(tk.END, "il tuo nome e': "+nome+"\n")
        text_area.configure(state='disabled')
        e_name.delete(0, tk.END)
        togli(l_name, e_name, b_name)
        metti(l_msg, e_msg, b_msg)
        b_change_n.grid()
        
def chiudi():
    
    Win.quit()
    s.close()
    

Win = tk.Tk()
Win.geometry("820x550")
Win.title("Questa è la chat")
Win.protocol('WM_DELETE_WINDOW', chiudi)

UpFrame = tk.Frame(Win)
UpFrame.pack(side=tk.TOP, fill=tk.X, pady=10)

MidFrame = tk.Frame(Win)
MidFrame.pack(fill=tk.X, pady=10)

BottomFrame = tk.Frame(Win)
BottomFrame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

nome = tk.StringVar()
mess = tk.StringVar()
psw = tk.StringVar()

l_name = tk.Label(UpFrame, text="Nome ")
l_name.grid(row=0, column=0)
e_name = tk.Entry(UpFrame, textvariable=nome)
e_name.grid(row=0, column=1)

l_pass = tk.Label(UpFrame, text="Password: ")
l_pass.grid(row=0, column=2)
l_pass.grid_remove()

e_pass = tk.Entry(UpFrame, textvariable=psw, show='*')
e_pass.grid(row=0, column=3)
e_pass.grid_remove()

b_pass= tk.Button(UpFrame, text="Invia dati", command=invia_p)
b_pass.grid(row=0,column=4)
b_pass.grid_remove()

b_newN = tk.Button(UpFrame, text="Invia il nuovo nome", command=new_name)
b_newN.grid(row=0, column=2, padx=10)
b_newN.grid_remove()

b_name = tk.Button(UpFrame, text="Invia il nome", command=invia_n)
b_name.grid(row=0, column=2, padx=10)
#   Mid Frame
text_area = st.ScrolledText(MidFrame, state='disabled')
text_area.grid(row=0, column=0, columnspan=2)
text_area.configure(state='normal')

b_change_n = tk.Button(MidFrame, text="Cambia nome", command=change_n)
b_change_n.grid(row=0, column=2, sticky=tk.W, padx=10)
b_change_n.grid_remove()
#   Bottom Frame
l_msg = tk.Label(BottomFrame, text="Invia un messaggio ")
l_msg.grid(row=0, column=0)
l_msg.grid_remove()

# Box di invio messagi
e_msg = tk.Entry(BottomFrame, width=70, textvariable=mess)
e_msg.grid(row=0, column=1)
e_msg.grid_remove()

# pulsante per inviare i messaggi
b_msg = tk.Button(BottomFrame, text="Invia", width=20, command=invia_m)
b_msg.grid(row=0, column=2, padx=10)
b_msg.grid_remove()






SERVER_HOST = "127.0.0.1"
SERVER_PORT = 49153  # server's port

s = socket.socket()

text_area.configure(state='normal')

text_area.insert(tk.END, f"[*] Connettendo a {SERVER_HOST}:{SERVER_PORT}...\n")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))

text_area.insert(tk.END, "[+] Connesso.\n")

text_area.configure(state='disabled')

t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread

t.start()
# close the socket
Win.mainloop()
s.close()

