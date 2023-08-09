import requests
import socket
import json
import datetime
import psycopg2
import os

from webex_bot.webex_bot import WebexBot
from requests_toolbelt.multipart.encoder import MultipartEncoder

from gpt import Chat
from bot_command import Add
from bot_command import AddRole
from bot_command import GetActivity
from dotenv import load_dotenv

load_dotenv()

access_token = os.getenv("WEBEX_TOKEN")

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
    params = {'roomId': room_id, 'markdown': "```\n"+message+"\n```"}
    res = requests.post(url, headers=headers, json=params)
    #print(res.json())
    return

def send_file(access_token, room_id):
     url = 'https://webexapis.com/v1/messages'

     m = MultipartEncoder({'roomId': room_id,
                           'text':"File contenente le activity dell'ip specificato",
                           'files': ('AllActivity.txt', open('./files/activity.txt', 'rb'), 'text/plain')
                         })
     headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': m.content_type
    }
     res = requests.post(url, data=m, headers=headers)
     return res.text


def get_mails_db(ruolo):
    # Configurazione della connessione al database
    dbname = 'dbmtkmnd'
    user = 'postgres'
    password = 'R:=H{98{^43}`kq}5=u_Sx*RJNp_xDF<'
    host = 'ls-e8c110d515b7ab64b18f871e331fdccaaded850e.cngbiakr7x0v.eu-central-1.rds.amazonaws.com'
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
        cur.execute("SELECT email FROM users WHERE disponibilità = true AND ruolo = '{}' ORDER BY score fetch first 2 rows only".format(ruolo))

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

def update_score_db(mail):
    # Configurazione della connessione al database
    dbname = 'dbmtkmnd'
    user = 'postgres'
    password = 'R:=H{98{^43}`kq}5=u_Sx*RJNp_xDF<'
    host = 'ls-e8c110d515b7ab64b18f871e331fdccaaded850e.cngbiakr7x0v.eu-central-1.rds.amazonaws.com'
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
        cur.execute("UPDATE users SET score = score + 1 WHERE email = '" + mail + "'")

        # Recupero dei risultati
        #rows = cur.fetchall()

        # Chiusura del cursore e connessione al database
        conn.commit()
        cur.close()
        conn.close()

        # Stampa una frase se la connessione è avvenuta con successo
        #print('score updated')

        return
    except psycopg2.Error as e:
        # Stampa un messaggio di errore se la connessione fallisce
        print('Errore durante la connessione al database:', e)
        return []

def update_dispo_db(mail):
    # Configurazione della connessione al database
    dbname = 'dbmtkmnd'
    user = 'postgres'
    password = 'R:=H{98{^43}`kq}5=u_Sx*RJNp_xDF<'
    host = 'ls-e8c110d515b7ab64b18f871e331fdccaaded850e.cngbiakr7x0v.eu-central-1.rds.amazonaws.com'
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
        cur.execute("UPDATE users SET disponibilità = not disponibilità WHERE email = '{}'".format(mail))

        # Recupero dei risultati
        #rows = cur.fetchall()

        # Chiusura del cursore e connessione al database
        conn.commit()
        cur.close()
        conn.close()

        # Stampa una frase se la connessione è avvenuta con successo
        #print('dispo updated')

        return
    except psycopg2.Error as e:
        # Stampa un messaggio di errore se la connessione fallisce
        print('Errore durante la connessione al database:', e)
        return []

def start_bot(room_id):
    bot = WebexBot( 
        teams_bot_token = bot_token,
        approved_rooms = [room_id],
    )

    bot.add_command(Chat())
    bot.add_command(Add())
    bot.add_command(AddRole())
    bot.add_command(GetActivity())
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

    mails = get_mails_db("analyst")

    for mail in mails:
        mail = str(mail)[2:-3]
        add_user(mail, room_id)
        #print("User {} added".format(mail))
        update_score_db(mail)
        update_dispo_db(mail)
    
    add_user("matictest@webex.bot", room_id)


    #il bot manderà questo messaggio
    send_message(bot_token, room_id, "incident del giorno: {}\nAvvenuto alle ore {} del {}\nSu macchina con ip: {}\nRischio valutato di livello: {}".format(incident, time, date, ip, risk))

    #dopo il report update_dispo_db(mail) a true

    start_bot(room_id)

# Close the server socket
server_socket.close()
