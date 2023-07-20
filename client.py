import socket
import json

HOST = 'localhost'  # Indirizzo IP del server
PORT = 6565  # Numero di porta del server

# Crea un socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connette il client al server
client_socket.connect((HOST, PORT))

# Legge l'input dall'utente
incident = input('Inserisci l\'incident: ')
risk = input('Inserisci il risk: ')
ip = input('Inserisci l\'ip: ')

#Dati da inviare
data = {
    'incident': incident,
    'risk': risk,
    'ip': ip
}

# Trasforma dati in JSON
json_data = json.dumps(data)

# Invia il JSON al server
client_socket.sendall(json_data.encode())

# Riceve la risposta dal server
response = client_socket.recv(1024).decode()

# Decodifica la risposta JSON
response_json = json.loads(response)

print('Risposta dal server:', response_json['message'])

# Chiude la connessione
client_socket.close()
