import requests
import socket
import json
import psycopg2
import os
import openai

from requests_toolbelt.multipart.encoder import MultipartEncoder

from dotenv import load_dotenv

load_dotenv()

access_token = os.getenv("WEBEX_TOKEN")

bot_token = os.getenv("BOT_TOKEN")

auth_umbrella = os.getenv("UMBRELLA_AUTH")

openai.api_key =  os.getenv("OPENAI_TOKEN")

room_id = None
json_data= None

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

def delete_room(room_id):
    url = f'https://webexapis.com/v1/rooms/{room_id}'
    headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
    }
    res = requests.delete(url, headers=headers)
    print(json.dumps(res.json(), indent=4))
    return

def get_room_details(room_id):
    url = 'https://webexapis.com/v1/rooms/{}/meetingInfo'.format(room_id)
    headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
    }
    res = requests.get(url, headers=headers)
    #print(json.dumps(res.json(), indent=4))
    return (json.dumps(res.json(), indent=4))

def create_room(title):
    url = 'https://webexapis.com/v1/rooms'
    headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
    }
    params={'title': title}
    res = requests.post(url, headers=headers, json=params)
    response_data = res.json()
    global room_id
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
    #print(json.dumps(res.json(), indent=4))
    return res.json()

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
    'Content-Type': 'application/json',
    }
    params = {'roomId': room_id, 'markdown': '``` txt\n' + message + '\n```'}
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
    dbname = 'db_matic'
    user = 'postgres'
    password = os.getenv("DB_PASSW")
    host = os.getenv("DB_HOST")
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
        cur.execute("SELECT email FROM users WHERE disponibilità = true AND ruolo = '{}'".format(ruolo))

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
    dbname = 'db_matic'
    user = 'postgres'
    password = os.getenv("DB_PASSW")
    host = os.getenv("DB_HOST")
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
        cur.execute("UPDATE users SET score = score + 1 WHERE email = '{}'".format(mail))


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
    except Exception as e:
        print(e)
        return []

def update_dispo_db(mail):
    # Configurazione della connessione al database
    dbname = 'db_matic'
    user = 'postgres'
    password = os.getenv("DB_PASSW")
    host = os.getenv("DB_HOST")
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

def ListAllActivity(ip, time_to, time_from, limit, verdict):
    url = "https://api.umbrella.com/reports/v2/activity?from={}&to={}&limit={}&ip={}&verdict={}".format(time_from, time_to, limit, ip, verdict)


    umbrella_tk = update_umbrellaTK()
    headers = {
        'Authorization':'Bearer {}'.format(umbrella_tk)
    }

    res = requests.get(url, headers = headers)

    try:
        response_data = res.json()
    except json.JSONDecodeError as e:
        print("Error decoding JSON response:", e)
        print("Response content:", res.content)
        response_data = None  # O qualsiasi altra azione appropriata che desideri intraprendere

    list = []

    for el in response_data["data"] :
        dominio = str(el["domain"])
        verdetto = str(el["verdict"])

        dict = {'verdetto' : verdetto, 'dominio' : dominio}
        if dict not in list :
            list.append(dict)

    return list

def createSocket(host, port):
    # Crea un socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Associa il socket all'indirizzo e alla porta desiderati
    server_socket.bind((host, port))

    # Mette il socket in ascolto
    server_socket.listen(1)

    return server_socket

def warRoom(date, time):
    room_id = create_room("War Room {} {}".format(date, time))

    mails = get_mails_db("analyst")

    for mail in mails:
        mail = mail[0]
        #mail = str(mail)[2:-3]
        add_user(mail, room_id)
        #print("User {} added".format(mail))
        update_score_db(mail)
        update_dispo_db(mail)
    
    add_user("matictest@webex.bot", room_id)  
    return room_id

def data_from_client(client_socket):
    # Receive data sent by the client
    data = client_socket.recv(1024).decode()

    global json_data
    # Process the received JSON data
    json_data = json.loads(data)

    return

def update_umbrellaTK():
    url = "https://api.umbrella.com/auth/v2/token"
    payload = 'grant_type=client_credentials'
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "Authorization": f"Basic {auth_umbrella}"
    }
    response = requests.request('POST', url, headers=headers, data = payload)
    token = json.loads(response.text)
    return token['access_token']

def gpt3_chat(input_message):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=input_message,
        max_tokens=100,
        temperature=0.7,
        n=1,
        stop=None,
        timeout=10
    )
    return response.choices[0].text.strip()




    