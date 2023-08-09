import json
import server
import asyncio
from test import ListAllActivity

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
        server.add_user(email, server.room_id)
        server.update_score_db(email)
        server.update_dispo_db(email)
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
        mails = server.get_mails_db(ruolo)
        for mail in mails :
            mail = str(mail)[2:-3]
            server.add_user(mail, server.room_id)
            server.update_score_db(mail)
            server.update_dispo_db(mail)
        return
        
class WelcomeMsg(Command):
    def __init__(self):
        super().__init__(
            command_keyword = "welcome",
            help_message = "Informazioni sull'incident",
            card = None,
        )
    def execute(self, message, attachment_actions, activity):
        card = AdaptiveCard()
        
        card.add(TextBlock(text = f"{server.incident}", size = "Medium", weight = "Bolder"))
        card.add(ColumnSet())
        card.add(Column(widht = "stretch"))
        card.add(FactSet())
        card.add(Fact(title = "Orario: ", value = f"{server.time}"))
        card.add(Fact(title = "Giorno: ", value = f"{server.date}"))
        card.add(Fact(title = "IP vittima: ", value = f"{server.ip}"))
        card.add(Fact(title = "Rischio lv: ", value = f"{server.risk}"))

        card_data = json.loads(asyncio.run(card.to_json()))
        card_payload = {
            "contentType" : "application/vnd.microsoft.card.adaptive",
            "content" : card_data,
        }

        response = Response()
        response.text = "Welcome Card"
        response.attachments = card_payload

        return  response


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
        time_to = int(round((server.now).timestamp())) * 1000
        time_from = time_to - 600000

        
        list = ListAllActivity(device, time_to, time_from, 1000, verdict)
        var = str(list)

        file = open("./files/activity.txt", "w+")
        var = var.replace("{", "")
        var = var.replace("}", "")
        var = var.replace("[", "")
        var = var.replace("]", "")
        var = var.replace("'", "")
        var = var.replace(", ", "\n")

        file.write(var)

        text = server.send_file(server.access_token, server.room_id)

        file.close()
        return
