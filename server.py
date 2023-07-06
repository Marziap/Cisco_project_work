import requests
import json

access_token = 'YzI3OWI0NmYtYTc0Yy00NDlkLWE5YjUtZTc0NWE3NDNmNjM2YzIzZjU4NTktYTQ2_PE93_e20dd4bc-1498-4b10-a0ba-ded4423515ea'

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
    print(json.dumps(res.json(), indent=4))
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
    print(json.dumps(res.json(), indent=4))
    return

def send_message(room_id, message):
    url = 'https://webexapis.com/v1/messages'
    headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
    }
    params = {'roomId': room_id, 'markdown': message}
    res = requests.post(url, headers=headers, json=params)
    print(res.json())
    return

room_id = create_room("prova")
send_message(room_id, "ciao")
