#from webex_bot.commands.echo import EchoCommand
from webex_bot.webex_bot import WebexBot
import os

from gpt import Chat

webex_token = os.getenv("BOT_TOKEN")


bot = WebexBot(
    teams_bot_token=webex_token,
    approved_users=["matteo.rocco68@gmail.com", "marziapirozzi2002@gmail.com"],
)

bot.add_command(Chat())

#bot.add_command(EchoCommand())
bot.run()




