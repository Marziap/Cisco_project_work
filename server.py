import json
import functions
from gpt import Chat
from bot_command import Add
from bot_command import AddRole
from bot_command import GetActivity
from webex_bot.webex_bot import WebexBot

def start_bot(room_id):
    bot = WebexBot( 
        teams_bot_token = functions.bot_token,
        approved_rooms = [room_id],
    )

    bot.add_command(Chat())
    bot.add_command(Add())
    bot.add_command(AddRole())
    bot.add_command(GetActivity())
    bot.run()


HOST = 'localhost'  # Indirizzo IP del server
PORT = 6565  # Numero di porta del server

server_socket = functions.createSocket(HOST, PORT)

print('Server in ascolto su {}:{}'.format(HOST, PORT))

while True:
    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()

    print('Connessione da:', client_address)

    functions.data_from_client(client_socket)

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

    functions.warRoom(functions.json_data['date'], functions.json_data['time'])

    #il bot manderà questo messaggio
    functions.send_message(functions.bot_token, functions.room_id, "incident del giorno: {}\n Avvenuto alle ore {} del {}\n Su macchina con ip: {}\nRischio valutato di livello: {}".format(functions.json_data['incident'], functions.json_data['time'], functions.json_data['date'], functions.json_data['ip'], functions.json_data['risk']))

    #dopo il report update_dispo_db(mail) a true

    start_bot(functions.room_id)

# Close the server socket
server_socket.close()
