import json
import asyncio
import functions
import time
import datetime

from webex_bot.models.command import Command
from webex_bot.models.response import Response
from adaptivecardbuilder import *


with open("cards_files/add_card.json", "r") as card:
    ADD_CARD = json.load(card)

with open("cards_files/addRole_card.json", "r") as card2:
    ADDROLE_CARD = json.load(card2)

with open("cards_files/welcome_msg.json", "r") as card3:
    WELCOME_CARD = json.load(card3)

with open("cards_files/activity_card.json", "r") as card4:
    ACTIVITY_CARD = json.load(card4)

class Add(Command):
    def __init__(self):
        super().__init__(
            command_keyword = "add",
            help_message = "Aggiungi l'utente di cui hai bisogno.",
            card = ADD_CARD,
        )
        
    def execute(self, message, attachment_actions, activity):
        email = attachment_actions.inputs['mail']
        functions.add_user(email, functions.room_id)
        functions.update_score_db(email)
        functions.update_dispo_db(email)
        return
    
class AddRole(Command):
    def __init__(self):
        super().__init__(
            command_keyword = "aggiungi",
            help_message = "Aggiungi l'utente di cui hai bisogno.",
            card = ADDROLE_CARD,
        )
    def execute(self, message, attachment_actions, activity):
        ruolo = attachment_actions.inputs['ruoli']
        mails = functions.get_mails_db(ruolo)
        for mail in mails :
            mail = str(mail)[2:-3]
            functions.add_user(mail, functions.room_id)
            functions.update_score_db(mail)
            functions.update_dispo_db(mail)
        return

'''       
class WelcomeMsg(Command):
    def __init__(self):
        super().__init__(
            command_keyword = "welcome",
            help_message = "Informazioni sull'incident",
            card = None,
        )
    def execute(self, message, attachment_actions, activity):
        card = AdaptiveCard()
        
        card.add(TextBlock(text = f"{json_data['incident']}", size = "Medium", weight = "Bolder"))
        card.add(ColumnSet())
        card.add(Column(widht = "stretch"))
        card.add(FactSet())
        card.add(Fact(title = "Orario: ", value = f"{time}"))
        card.add(Fact(title = "Giorno: ", value = f"{date}"))
        card.add(Fact(title = "IP vittima: ", value = f"{ip}"))
        card.add(Fact(title = "Rischio lv: ", value = f"{risk}"))

        card_data = json.loads(asyncio.run(card.to_json()))
        card_payload = {
            "contentType" : "application/vnd.microsoft.card.adaptive",
            "content" : card_data,
        }

        response = Response()
        response.text = "Welcome Card"
        response.attachments = card_payload

        return  response
'''

class GetActivity(Command):
    def __init__(self):
        super().__init__(
            command_keyword = "activity",
            help_message = "Get Activity",
            card = ACTIVITY_CARD,
        )  
    def execute(self, message, attachment_actions, activity):
        device = attachment_actions.inputs['setIP']
        verdict = attachment_actions.inputs['setVerdict']
        
        now = datetime.datetime.fromtimestamp(functions.json_data['now'])
        #now = datetime.datetime.strptime((functions.json_data['now']), "%Y-%m-%d %H:%M:%S")
        time_to = int(round(now.timestamp())) * 1000
        time_from = time_to - 600000

        list = functions.ListAllActivity(device, time_to, time_from, 1000, verdict)
        var = str(list)

        file = open("./files/activity.txt", "w+")
        var = var.replace("{", "")
        var = var.replace("}", "")
        var = var.replace("[", "")
        var = var.replace("]", "")
        var = var.replace("'", "")
        var = var.replace(", ", "\n")

        file.write(var)
        file.close()

        text = functions.send_file(functions.access_token, functions.room_id)

        
        return

class Done(Command):
    def __init__(self):
        super().__init__(
            command_keyword = "done",
            help_message = "Get the report and exit the room.",
            card = None,
        )  
    def execute(self, message, attachment_actions, activity):
        res = functions.list_room_members(functions.room_id)

        for el in res['items']:
            functions.update_dispo_db(el['personEmail'])


        return