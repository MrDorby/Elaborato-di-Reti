#!/usr/bin/env python3
"""Script relativa alla chat del client utilizzato per lanciare la GUI Tkinter."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt
"""La funzione che segue ha il compito di gestire la ricezione dei messaggi."""
def receive():
    while True:
        try:
            #quando viene chiamata la funzione receive, si mette in ascolto dei messaggi che
            #arrivano sul socket
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            #visualizziamo l'elenco dei messaggi sullo schermo
            #e facciamo in modo che il cursore sia visibile al termine degli stessi
            msg_list.insert(tkt.END, msg)
            # Nel caso di errore e' probabile che il client abbia abbandonato la chat.
        except (OSError, ConnectionAbortedError): 
            #client_socket.send(bytes(msg, "utf8"))
            #client_socket.detach()
            break

"""La funzione che segue gestisce l'invio dei messaggi."""
def send(event=None):
    # gli eventi vengono passati dai binders.
    msg = my_msg.get()
    # libera la casella di input.
    my_msg.set("")
    # invia il messaggio sul socket
    try:
        client_socket.send(bytes(msg, "utf8"))
    except OSError:
        msg_list.insert(tkt.END,"Necessaria una chiusura!")
    finally:
        if msg == "{quit}":
            client_socket.close()
            finestra.destroy() #in più
            #client_socket.detach() #in più

"""La funzione che segue viene invocata quando viene chiusa la finestra della chat."""
def on_closing(event=None):
    #client_socket.send(bytes("{quit}", "utf8"))
    my_msg.set("{quit}")
    send() #originale
    #client_socket.send()
    #finestra.destroy() #in più

finestra = tkt.Tk()
finestra.title("Chat_Laboratorio")

#creiamo il Frame per contenere i messaggi
messages_frame = tkt.Frame(finestra)
#creiamo una variabile di tipo stringa per i messaggi da inviare.
my_msg = tkt.StringVar()
#indichiamo all'utente dove deve scrivere i suoi messaggi
my_msg.set("Scrivi qui i tuoi messaggi.")
#creiamo una scrollbar per navigare tra i messaggi precedenti.
scrollbar = tkt.Scrollbar(messages_frame)

# La parte seguente contiene i messaggi.
msg_list = tkt.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
msg_list.pack(side=tkt.LEFT, fill=tkt.BOTH)
msg_list.pack()
messages_frame.pack()

#Creiamo il campo di input e lo associamo alla variabile stringa
entry_field = tkt.Entry(finestra, textvariable=my_msg)
# leghiamo la funzione send al tasto Return
entry_field.bind("<Return>", send)

entry_field.pack()
#creiamo il tasto invio e lo associamo alla funzione send
send_button = tkt.Button(finestra, text="Invio", command=send)
#integriamo il tasto nel pacchetto
send_button.pack()

finestra.protocol("WM_DELETE_WINDOW", on_closing)

#----Connessione al Server----
HOST = input('Inserire il Server host: ')
PORT = input('Inserire la porta del server host: ')
if not PORT:
    PORT = 53000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
# Avvia l'esecuzione della Finestra Chat.
tkt.mainloop()
