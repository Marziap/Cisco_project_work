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

# Crea un dizionario per i dati
data = {
    'incident': incident,
    'risk': risk,
    'ip': ip
}

# Codifica il dizionario in JSON
json_data = json.dumps(data)

# Invia il JSON al server
client_socket.sendall(json_data.encode())

# Riceve la risposta dal server
response = client_socket.recv(1024).decode()

# Decodifica la risposta JSON
response_json = json.loads(response)

print('Risposta dal server:', response_json['message'])
#print('Incident:', response_json['incident'])
#print('Risk:', response_json['risk'])
#print('Ip:', response_json['ip'])

# Chiude la connessione
client_socket.close()
