from bot_command import Chat
from bot_command import Add
from bot_command import AddRole
from bot_command import GetActivity
from bot_command import Done
from webex_bot.webex_bot import WebexBot

import os
from dotenv import load_dotenv
load_dotenv()


bot = WebexBot( 
    teams_bot_token = os.getenv("BOT_TOKEN"),
    approved_rooms = [],
)

bot.add_command(Chat())
bot.add_command(Add())
bot.add_command(AddRole())
bot.add_command(GetActivity())
bot.add_command(Done())
bot.run()