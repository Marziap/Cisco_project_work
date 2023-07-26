import os
import json
from webex_bot.models.command import Command
import server


with open("./add_card.json", "r") as card:
    ADD_CARD = json.load(card)

with open("./addRole_card.json", "r") as card2:
    ADDROLE_CARD = json.load(card2)


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
        