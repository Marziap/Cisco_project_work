import os
import functions
import json
from flask import Flask, request, Response

from dotenv import load_dotenv

# load environment variables from '.env' file
load_dotenv()

# create flask instance
app = Flask(__name__)


# this is a test endpoint. Add your logic to handle the incident correctly
# As a reference check routers.py file in this repo to learn how to interact with the database:
#  https://github.com/alarmfox/dtlab-api/tree/solution
# Official documentation: https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html

        #TODO: PULSANTE DONE PER REPORT FINALE  -> DA FINIRE, MANCA SCHEDULAZIONE DELLA CHIAMATA + PRENDERE TUTTI I MEX IN CHAT

        #TODO: COMANDO DI BAN PER UN IP #DA CAPIRE COME FARE LA RICHIESTA, DATO UN IP AVERE LE SUE INFORMAZIONI DI UMBRELLA

        #TODO: ATTIVARE UNA CALL


@app.route('/incident', methods=['POST'])
def test() -> str:
    # get incident data from request as json
    data = request.get_json()

    # create room & add users, bot
    room_id = functions.war_room(data['date'], data['time'])
    
    # send first message
    functions.send_message(room_id, f"Incident del giorno: {data['incident']}\nAvvenuto alle ore {data['time']} del {data['date']}\nSu macchina con ip: {data['ip']}\nRischio valutato di livello: {data['risk']}")


    return Response(json.dumps(room_id), mimetype="application/json"), 200

@app.route('/webhook', methods=['POST'])
def catch_webhook() -> str:
    #get the frame from the webhook
    data = request.get_json()
    print(json.dumps(data, indent=4))

    return Response(json.dumps(data), mimetype="application/json"), 200



