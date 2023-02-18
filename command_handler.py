import traceback
import discord
from enum import Enum
import random
import discord
import commands_3 as commands
from custom_types import Neighbor
from importlib import reload as sync
import inspect
from id_bundle import FF

"""
Greg 3.0!
Author: Lincoln Edsall

This script serves as the overhead controller for the client, aka Greg. 
It sets up the intents, listens for events, and prepares the command file.

This script was combined with command_handler.py, where commands are wrapped, and run based off listener events.

persistent_types.py defines types such as Neighbor, Item, and Expectation
	which Greg relies on to allow information to persist
commands.py is where all commands are defined
id_bundle.py provides a list of role, channel, and other relevant ids for the FF discord server
"""

# meta data and intents _____
version = "3.0";
maintenance = True;
# ___________________________

# The AccessType enum creates specific levels of access for different members of a server. 
class AccessType(Enum):
    PUBLIC = 0;          # public commands can be accessed by anyone
    PRIVATE = 1;         # private commands can be accessed by anyone with a neighbors role
    PRIVILEGED = 2;      # privileged commands can be accessed by anyone with a council role

# A context object is constructed when a message is sent or reaction is added in the server. 
#   The context object creates an intuitive way of accessing information about an event.
#   Additionally, the .send() and .react() methods allow for a message or reaction respectively
#   to be sent by Greg into the appropriate context. 
#   This is a mandatory parameter for every textual command created using the Command class
class Context:
    def __init__(self, message: discord.message = None, reaction: discord.reaction = None):
        if not message is None:
            self.guild = message.guild;
            self.channel = message.channel;
            self.author = message.author;
            self.message = message;
            self.content = message.content;
            self.author_id = message.author.id;
            self.author_role_ids = [role.id for role in message.author.roles];
            self.set_access_type();
    def __str__(self):
        return self.content;
    def set_access_type(self):
        if FF.leaders_role.value in self.author_role_ids:
            self.access_type = AccessType.PRIVILEGED;
        elif FF.neighbors_role.value in self.author_role_ids or FF.j_neighbors_role.value in self.author_role_ids or FF.r_neighbors_role.value in self.author_role_ids or FF.p_neighbors_role.value in self.author_role_ids:
            self.access_type = AccessType.PRIVATE;
        else:
            self.access_type = AccessType.PUBLIC;
        print(self.access_type);
        print(self.author_role_ids);
    async def send(self, text: str = None, reply: bool = False, *args, **kwargs):
        if not text is None:
            if reply:
                await self.message.reply(text)
            else:
                await self.channel.send(text);
        else:
            await self.channel.send(*args, **kwargs);

# Regular commands, which can be called by anyone with the correct access type using "$" + command name
#   Commands are registered using the Command(access_type, desc) decorator
class Command:
    available_commands = {};
    prefix = None;
    def __init__(self, access_type: AccessType, desc: str = None):
        self.access_type = access_type;
        self.desc = desc;
    def __call__(self, func):
        
        self.name = func.__name__;
        Command.available_commands[func.__name__] = self;

        async def wrapper(activator: Neighbor, context: Context):
            print("hello!");
            if context.access_type.value < self.access_type.value:
                await context.send(f"You do not meet the necessary AccessType for command `{self.name}`: `{self.access_type.name}`.");
                return;
            args = context.content.split(" ")[1:];
            try:
                await func(activator, context, *args);
            except TypeError:
                traceback.print_exc();
                await context.send(f"The command did not execute. It seems to have expected different arguments than you provided. If you believe this is incorrect, it could be an issue with the command's code.\n*You can use `$help {func.__name__}` to learn more about how to use this command, `$report` to report a bug, or `$request` to request a feature.*", reply = True);
            except Exception as e:
                traceback.print_exc();
                res = "Runtime error:\n";
                res += str(e);
                if context.guild.id == FF.guild:
                    res += "\n<@355169964027805698> ur bot broke fix it\n";
                else:
                    res += "\nIf you are so inclined, submit a bug report using $report\n."
                res += random.choice(["https://tenor.com/view/bruh-be-bruh-beluga-gif-25964074", "https://tenor.com/view/facepalm-really-stressed-mad-angry-gif-16109475", "https://tenor.com/view/yikes-david-rose-david-dan-levy-schitts-creek-gif-20850879", "https://tenor.com/view/disappointed-disappointed-fan-seriously-what-are-you-doing-judging-you-gif-17485289"])
                await context.send(res);
            
        self.run = wrapper;
            
        return wrapper
    
    async def execute(activator: Neighbor, context: Context):
        if Command.prefix is None:
            raise ValueError("Prefix not set. Please define with Command.set_prefix(new: str)") 
        if context.content.startswith(Command.prefix):
            target = context.content.split(" ")[0][1:];
            for name, command in Command.available_commands.items():
                if name == target:
                    await command.run(activator, context);
                    
    def set_prefix(new: str):
        Command.prefix = new;
    def generate_help_str(target: str = None):
        res = "";
        if not target is None:
            for name, command in Command.available_commands.items():
                if name == target:
                    res += f"**{Command.prefix}{name}** | *{command.access_type.name}* | {command.desc}"
        else:
            res += "**The following commands are available:**\n";
            res += "A command can be called by typing `" + Command.prefix + "` + `command name` + `argument(s), if any`\n";
            res += "For example, `$help` is a command call with no arguments that generates a list of available commands, while `$help help` is a command call with the additional argument `help` that generates a description of the 'help' command.\n\n"

            for name, command in Command.available_commands.items():
                res += f"> **{Command.prefix}{name}** | *{command.access_type.name}*\n";
        return res;
    
# Uncontested commands are not like regular commands. These commands are run every time someone sends
#   a message, adds a reaction, etc. This is useful, for example, when you need to incrememnt someone's
#   server xp every time they send a message. This means the bot should look for all messages sent,
#   instead of any particular command call
class Uncontested:
    available_commands = {};
    def __init__(self, desc: str = None):
        self.desc = desc;
    def __call__(self, func):
        Uncontested.available_commands[func.__name__] = self;

        async def wrapper(context: Context):
            args = context.content.split(" ")[1:];
            try:
                return await func(context, *args);
            except TypeError:
                traceback.print_exc();
                return context.send(f"The command did not execute. It seems to have expected different arguments than you provided. If you believe this is incorrect, it could be an issue with the command's code.\n*You can use `$help {func.__name__()}` to learn more about how to use this command.*", reply = True);
            except Exception as e:
                traceback.print_exc();
                res = "Runtime error:\n";
                res += e
                res += "\n<@355169964027805698> ur bot broke fix it\n";
                res += random.choice(["https://tenor.com/view/bruh-be-bruh-beluga-gif-25964074", "https://tenor.com/view/facepalm-really-stressed-mad-angry-gif-16109475", "https://tenor.com/view/yikes-david-rose-david-dan-levy-schitts-creek-gif-20850879", "https://tenor.com/view/disappointed-disappointed-fan-seriously-what-are-you-doing-judging-you-gif-17485289"])
                return context.send(res, reply = True);
        
        return wrapper


# Some maitenance and management duties need to be performed on a time interval, instead of in response
#   to a user action. For example, a loop command may run every 10 minutes, or every 24 hours.
#   Notably, Greg only checks to run these loop commands every 5 minutes, so this is the minimum loop time.
#   Again, since Greg only runs these once every 5 minutes, setting a loop to run every x minutes will be most accurate
#   if x is a multiple of 5.
class Loop:
    available_commands = {};

    def __init__(self, minutes: int = None, hours: int = None, days: int = None, desc: str = ""):
        total = 0;
        if not minutes is None:
            total += minutes;
        if not hours is None:
            total += hours * 60;
        if not days is None:
            total += days * 1440;

        if (total < 5):
            raise ValueError("Timer argument must be 5 minutes or greater due to task loop");

        self.timer = total;

    def __call__(self, func):
        Loop.available_commands[func.__name__] = self;

        async def wrapper():
            try:
                return await func();
            except Exception as e:
                print("help");
        
        return wrapper
    
Command.set_prefix("$");

print(Command.available_commands);