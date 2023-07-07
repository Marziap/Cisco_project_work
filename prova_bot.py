import requests
from flask import Flask, request, jsonify
from webexteamssdk import WebexTeamsAPI
import openai

# Inizializza l'API di OpenAI
openai.api_key = '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'

# Inizializza l'API di Webex Teams
webex_teams_api = WebexTeamsAPI(access_token='OTczNjJlOTItMTc0NC00ZWYzLWI5OWUtNDhhYjRkZmQyZGMzMWNmOWYxMGUtZDhl_PE93_f3ac1f51-fe1c-4cae-bfb1-d6b499e75142')

# Inizializza l'app Flask
app = Flask(__name__)

# Endpoint per la ricezione dei messaggi
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    message_id = data['data']['id']
    room_id = data['data']['roomId']
    message = webex_teams_api.messages.get(message_id)
    if message.personId == 'prova_openAI@webex.bot':
        # Ignora i messaggi inviati dal bot stesso
        return jsonify({}), 200
    else:
        # Processa il messaggio
        response = process_message(message.text)
        # Invia la risposta
        webex_teams_api.messages.create(roomId=room_id, text=response)
        return jsonify({}), 200

# Funzione per processare il messaggio utilizzando OpenAI
def process_message(message):
    # Invia il messaggio a OpenAI per ottenere una risposta
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=message,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Avvio dell'app Flask
if __name__ == '__main__':
    app.run()