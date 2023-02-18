import discord
import commands_3;
import command_handler
from command_handler import Context, Command
from custom_types import Neighbor
import commands_3 as commands
from importlib import reload as sync

"""
Greg 3.0!
Author: Lincoln Edsall

This script serves as the overhead controller for the client. 
It sets up the intents, listens for events, and prepares the command file.

persistent_types.py defines types such as Neighbor, Item, and Expectation
	which Greg relies on to allow information to persist
command_handler.py is where commands are wrapped, and run based off listeners events here
commands.py is where all commands are defined
id_bundle.py provides a list of role, channel, and other relevant ids for FF discord server
"""

# meta data and intents _____
version = "3.0";
intents = discord.Intents.all();
intents.message_content = True;
intents.members = True;
client = discord.Client(intents=intents)
# ___________________________

# This listener is called when the client becomes "ready". Unfortunately, this is called when the code is first run but can also be called
    # randomly based on stuff happening behind the scene in the Discord api. So, it's not a great measure of doing something every time the bot comes online
@client.event
async def on_ready():
    print("All systems go!");
    # bot_member = client.get_guild(FF.guild).get_member(client.user.id);
    # await bot_member.edit(nick=f"Greg V{version}" + (" [Maintenance]" if maintenance else ""));

@client.event
async def on_message(message):
    if message.author.bot:
        return;
    context = Context(message=message);
    neighbor = Neighbor(message.author.id);
    await Command.execute(neighbor, context);
    

# run the client
client.run('NjkxMzM4MDg0NDQ0Mjc0NzI4.GQgSC6.cmp68om7-CpyYMsEA4pObFQ6hAJEqvTB4JeABI');