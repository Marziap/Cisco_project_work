import requests
import socket
import json
import datetime
#import psycopg2
import os

from webex_bot.webex_bot import WebexBot
from gpt import Chat

access_token = 'YOUR ACCESS TOKEN HERE'

bot_token = os.getenv("BOT_TOKEN")

def test_token(access_token):
    url = 'https://webexapis.com/v1/people/me'
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    res = requests.get(url, headers=headers)
    print(json.dumps(res.json(), indent=4))
    return

def list_details_of_user(email):
    url = 'https://webexapis.com/v1/people'
    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
    }
    params = {
        'email': email
    }
    res = requests.get(url, headers=headers, params=params)
    print(json.dumps(res.json(), indent=4))
    return

def list_user_administrative_details(person_id):
    url = 'https://webexapis.com/v1/people/{}'.format(person_id)
    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
    }
    res = requests.get(url, headers=headers)
    print(json.dumps(res.json(), indent=4))
    return

def list_rooms():
    url = 'https://webexapis.com/v1/rooms'
    headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
    }
    params={'max': '100'}
    res = requests.get(url, headers=headers, params=params)
    print(json.dumps(res.json(), indent=4))
    return

def get_room_details(room_id):
    url = 'https://webexapis.com/v1/rooms/{}/meetingInfo'.format(room_id)
    headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
    }
    res = requests.get(url, headers=headers)
    print(json.dumps(res.json(), indent=4))
    return

def create_room(title):
    url = 'https://webexapis.com/v1/rooms'
    headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
    }
    params={'title': title}
    res = requests.post(url, headers=headers, json=params)
    response_data = res.json()
    room_id = response_data['id']
    #print(json.dumps(res.json(), indent=4))
    return room_id

def list_room_members(room_id):
    url = 'https://webexapis.com/v1/memberships'
    headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
    }
    params = {'roomId': room_id}
    res = requests.get(url, headers=headers, params=params)
    print(json.dumps(res.json(), indent=4))
    return

def add_user(person_email, room_id):
    url = 'https://webexapis.com/v1/memberships'
    headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
    }
    params = {'roomId': room_id, 'personEmail': person_email}
    res = requests.post(url, headers=headers, json=params)
    #print(json.dumps(res.json(), indent=4))
    return

def send_message(access_token, room_id, message):
    url = 'https://webexapis.com/v1/messages'
    headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
    }
    params = {'roomId': room_id, 'markdown': message}
    res = requests.post(url, headers=headers, json=params)
    #print(res.json())
    return

def get_mails_db():
    # Configurazione della connessione al database
    dbname = 'Cisco_pw'
    user = 'postgres'
    password = '21032002'
    host = 'localhost'
    port = '5432'
    
    try:
        # Connessione al database
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        
        # Creazione di un cursore per eseguire query
        cur = conn.cursor()

        # Esempio di esecuzione di una query
        cur.execute('SELECT email FROM users')

        # Recupero dei risultati
        rows = cur.fetchall()

        # Chiusura del cursore e connessione al database
        cur.close()
        conn.close()

        # Stampa una frase se la connessione è avvenuta con successo
        print('Connessione al database avvenuta con successo!')

        return rows
    except psycopg2.Error as e:
        # Stampa un messaggio di errore se la connessione fallisce
        print('Errore durante la connessione al database:', e)
        return []


def start_bot():
    bot = WebexBot( 
        teams_bot_token = bot_token,
        approved_users=["matteo.rocco68@gmail.com", "marziapirozzi2002@gmail.com"],
    )

    bot.add_command(Chat())
    bot.run()



HOST = 'localhost'  # Indirizzo IP del server
PORT = 6565  # Numero di porta del server

# Crea un socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa il socket all'indirizzo e alla porta desiderati
server_socket.bind((HOST, PORT))

# Mette il socket in ascolto
server_socket.listen(1)

print('Server in ascolto su {}:{}'.format(HOST, PORT))

while True:
    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()

    # Data e ora della connessione (ovvero data e ora dell'incident) 
    now = datetime.datetime.now()
    date = now.strftime('%Y-%m-%d')
    time = now.strftime('%H:%M:%S')

    print('Connessione da:', client_address)

    # Receive data sent by the client
    data = client_socket.recv(1024).decode()

    # Process the received JSON data
    json_data = json.loads(data)

    # Elabora i dati ricevuti
    incident = json_data['incident']
    risk = json_data['risk']
    ip = json_data['ip']

    # Crea una risposta in formato JSON
    response = {
        'message': 'Dati ricevuti correttamente',
    }

    # Codifica la risposta in JSON
    response_json = json.dumps(response)

    # Invia la risposta al client
    client_socket.sendall(response_json.encode())

    # Chiude la connessione
    client_socket.close()

    room_id = create_room("War Room {} {}".format(date, time))

    '''mails = get_mails_db()

    for mail in mails:
        mail = str(mail)[2:-3]
        add_user(mail, room_id)
        print("User {} added".format(mail))
    '''
    
    add_user("matictest@webex.bot", room_id)

    #il bot manderà questo messaggio
    send_message(bot_token, room_id, "incident del giorno: {}\n Avvenuto alle ore {} del {}\n Su macchina con ip: {}\nRischio valutato di livello: {}".format(incident, time, date, ip, risk))
    start_bot()

# Close the server socket
server_socket.close()