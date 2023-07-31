import openai
import os
from webex_bot.models.command import Command
from dotenv import load_dotenv

load_dotenv()

openai.api_key =  os.getenv("OPENAI_TOKEN")

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


class Chat(Command):
    def __init__(self):
        super().__init__(
            command_keyword="chat",
            help_message="chiedi qualcosa a chat gpt",
            card=None,
        )
        
    def execute(self, message, attachment_actions, activity):
        domanda = message.strip()
        print("Domanda: {}".format(domanda))
        response_message = gpt3_chat(domanda)
        return response_message
    

