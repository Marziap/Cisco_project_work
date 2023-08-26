import os
import functions
from flask import Flask, request, Response

from dotenv import load_dotenv

# load environment variables from '.env' file
load_dotenv()

# create flask instance
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")

# db connection ana start application
from models import db, User
import json

db.init_app(app)

# create all models
with app.app_context():
    db.create_all()

# this is a test endpoint. Add your logic to handle the incident correctly
# As a reference check routers.py file in this repo to learn how to interact with the database:
#  https://github.com/alarmfox/dtlab-api/tree/solution
# Official documentation: https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html

        #TODO: PULSANTE DONE PER REPORT FINALE  -> DA FINIRE, MANCA SCHEDULAZIONE DELLA CHIAMATA + PRENDERE TUTTI I MEX IN CHAT

        #TODO: COMANDO DI BAN PER UN IP #DA CAPIRE COME FARE LA RICHIESTA, DATO UN IP AVERE LE SUE INFORMAZIONI DI UMBRELLA

        #TODO: CRITERIO DI SCELTA DAL DATABASE

        #TODO: ATTIVARE UNA CALL


@app.route('/incident', methods=['POST'])
def test() -> str:
    # get incident data from request as json
    data = request.get_json()

    #PENSAVO CHE POTREMMO ANCHE NON PASSARE DATE & TIME AL JSON, IN MODO TALE DA DECOMPRIMERE TUTTO QUI DA NOW.
    # create room & add users, bot
    room_id = functions.warRoom(data['date'], data['time'])
    
    # send first message
    functions.send_message(os.getenv("BOT_TOKEN"), room_id, f"Incident del giorno: {data['incident']}\nAvvenuto alle ore {data['time']} del {data['date']}\nSu macchina con ip: {data['ip']}\nRischio valutato di livello: {data['risk']}")


    return Response(json.dumps(room_id), mimetype="application/json"), 200

@app.route('/prova/<ruolo>', methods=['GET'])
def getMails(ruolo) -> str:
    mails = functions.get_mails_db(ruolo)

    return Response(json.dumps(mails), mimetype="application/json"), 200

