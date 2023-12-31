import requests
import socket
import json
import psycopg2
import os
import openai

from requests_toolbelt.multipart.encoder import MultipartEncoder

from dotenv import load_dotenv

load_dotenv()


dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSW")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
access_token = os.getenv("WEBEX_TOKEN")
bot_token = os.getenv("BOT_TOKEN")
auth_umbrella = os.getenv("UMBRELLA_AUTH")
openai.api_key =  os.getenv("OPENAI_TOKEN")


# Connessione al database
conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
)


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
    if res.status_code != 200:
        print(json.dumps(res.json(), indent=4))
        return
    else:
        return (res.json())['id']

def list_room_members(room_id):
    url = 'https://webexapis.com/v1/memberships'
    headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
    }
    params = {'roomId': room_id}
    res = requests.get(url, headers=headers, params=params)
    return print(json.dumps(res.json(), indent=4))

def add_user(person_email, room_id):
    url = 'https://webexapis.com/v1/memberships'
    headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
    }
    params = {'roomId': room_id, 'personEmail': person_email}
    res = requests.post(url, headers=headers, json=params)
    if res.status_code != 200:
        print(json.dumps(res.json(), indent=4))
    return

def send_message(room_id, message):
    url = 'https://webexapis.com/v1/messages'
    headers = {
    'Authorization': 'Bearer {}'.format(access_token), #PROVA A MANDARE MEX SENZA ACCESS TOKEN NEI PARAMS
    'Content-Type': 'application/json',
    }
    params = {'roomId': room_id, 'markdown': '``` txt\n' + message + '\n```'}
    res = requests.post(url, headers=headers, json=params)
    if res.status_code != 200:
        print(json.dumps(res.json(), indent=4))
    return

def send_file(room_id):
     url = 'https://webexapis.com/v1/messages'

     m = MultipartEncoder({'roomId': room_id,
                           'text':"File contenente le activity dell'ip specificato",
                           'files': ('AllActivity.csv', open('./files/activity.csv', 'rb'), 'text/csv')
                         })
     headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': m.content_type
    }
     res = requests.post(url, data=m, headers=headers)
     return res.text

def get_mails_db(ruolo):
    try:        
        # Creazione di un cursore per eseguire query
        cur = conn.cursor()

        # Esempio di esecuzione di una query
        cur.execute("SELECT email FROM users WHERE disponibilità = true AND ruolo = '{}'".format(ruolo))

        # Recupero dei risultati
        rows = cur.fetchall()

        # Chiusura del cursore e connessione al database
        cur.close()

        # Stampa una frase se la connessione è avvenuta con successo
        print('Connessione al database avvenuta con successo!')

        return rows
    except psycopg2.Error as e:
        # Stampa un messaggio di errore se la connessione fallisce
        print('Errore durante la connessione al database:', e)
        return []

def update_score_db(mail):  
    try:
        # Creazione di un cursore per eseguire query
        cur = conn.cursor()
        

        # Esempio di esecuzione di una query
        cur.execute("UPDATE users SET score = score + 1 WHERE email = '{}'".format(mail))


        # Recupero dei risultati
        #rows = cur.fetchall()

        # Chiusura del cursore e connessione al database
        conn.commit()
        cur.close()

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
    
    try:        
        # Creazione di un cursore per eseguire query
        cur = conn.cursor()
        # Esempio di esecuzione di una query
        cur.execute("UPDATE users SET disponibilità = not disponibilità WHERE email = '{}'".format(mail))

        # Recupero dei risultati
        #rows = cur.fetchall()

        # Chiusura del cursore e connessione al database
        conn.commit()
        cur.close()

        # Stampa una frase se la connessione è avvenuta con successo
        #print('dispo updated')

        return
    except psycopg2.Error as e:
        # Stampa un messaggio di errore se la connessione fallisce
        print('Errore durante la connessione al database:', e)
        return []

def list_all_activity(ip, time_to, time_from, limit, verdict):
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

def update_umbrellaTK():
    url = "https://api.umbrella.com/auth/v2/token"
    payload = 'grant_type=client_credentials'
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "Authorization": f"Basic {auth_umbrella}"
    }
    response = requests.request('POST', url, headers=headers, data = payload)
    token = response.json()
    if token == None:
        print ("ERROR IN THE CREATION OF THE UMBRELLA TOKEN.")
    else:
        return token['access_token']

def war_room(date, time):
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

def create_meeting(roomId, title, time_start, time_end, password):
    url='https://webexapis.com/v1/meetings'
    headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
    }
    timezone='Europe/Rome' #SE CI FOSSE NECESSITA' DI CAMBIARE REGIONE SI PUO' SEMPLICEMENTE AGGIORNARE QUESTO PARAMETRO CON IL FUSORARIO DESIDERATO
    if password.isspace() != True:
        params = {'roomId': roomId, 'title': title, 'start': time_start, 'end': time_end, 'timezone': timezone, 'enabledAutoRecordMeeting': True}
    else:
        params = {'roomId': roomId, 'title': title, 'password': password, 'start': time_start, 'end': time_end, 'timezone': timezone, 'enabledAutoRecordMeeting': True}

    res = requests.post(url, headers=headers, json=params)
    if res.status_code != 200:
        print(json.dumps(res.json(), indent=4))
        return
    else:
        return (json.dumps(res.json(), indent=4))

def list_recordings(meetingId):
    url = 'https://webexapis.com/v1/recordings'
    headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
    }
    params = {'meetingId':meetingId}
    res = requests.get(url, headers=headers, params=params)
    if res.status_code != 200:
        return (print(json.dumps(res.json(), indent=4)))
    else :
        dict = ((res.json())['items'])[0]
        list = []
        list.append(dict['downloadUrl'])
        list.append(dict['playbackUrl'])
        list.append(dict['password'])
        print(json.dumps(res.json(), indent=4))
        return list
