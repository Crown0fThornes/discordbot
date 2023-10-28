import re
import traceback
from command_handler import Context, AccessType, CommandArgsError
from command_handler import AccessType
import command_handler
import random
from custom_types import Neighbor, Item, Expectation, Reminder, Giveaway, Poll, Offer
from responses import ResponseRequest, ResponsePackage
from id_bundle import FF
from phoenix_bundle import PHOENIX
import difflib
import discord
import json
import datetime
import time
from PIL import Image
import requests
import os
import wordle_helper

VERSION = "3.1.1";

swear_words = [];
xp_gained = 0;
xp_happy_hour = 1;
last_profitable_message_author_id = 0;

unicodes = {
    0 : "\U00000030\U0000FE0F\U000020E3",
    1 : "\U00000031\U0000FE0F\U000020E3",
    2 : "\U00000032\U0000FE0F\U000020E3",
    3 : "\U00000033\U0000FE0F\U000020E3",
    4 : "\U00000034\U0000FE0F\U000020E3",
    5 : "\U00000035\U0000FE0F\U000020E3",
    6 : "\U00000036\U0000FE0F\U000020E3",
    7 : "\U00000037\U0000FE0F\U000020E3",
    8 : "\U00000038\U0000FE0F\U000020E3",
    9 : "\U00000039\U0000FE0F\U000020E3",
    "boost" : "\U0001F4B0",
    "perk" : "\U0001F5FF",
    "tag" : "\U0001F996",
    "icon" : "\U0001F48E",
    "mail" : "\U00002709",
    "rice" : "\U0001F33E",
    "rainbow" : "\U0001F308",
    "bee" : "\U0001F41D",
    "mushroom" : "\U0001F344",
    "selfie" : "\U0001F933",
    "crown" : "\U0001F451",
    "fox" : "\U0001F98A",
    "snowflake" : "\U00002744",
    "fries" : "\U0001F35F",
    "red_heart" : "\U00002764",
    "blueberry" : "\U0001FAD0",
    "strawberry" : "\U0001F353",
    "coffee" : "\U00002615",
    "t_rex" : "\U0001F996",
    "chicken" : "\U0001F414",
    "coin" : "\U0001FA99",
    "diamond" : "\U0001F48E",
    "crayon" : "\U0001F58D",
    "robot" : "\U0001F916",
    "nails" : "\U0001F485",
    "bank" : "\U0001F3E6",
    "check" : "\U00002705",
    "bot" : "\U0001F916",
    "ant" : "\U0001FAB3",
    "ghost" : "\U0001F47B",
    "back" : "\U000023CF",
    "butterfly" : "\U0001F98B",
    "cheetah" : "\U0001F406",
    "fox" : "\U0001F98A",
    "horse" : "\U0001F40E",
    "puppy" : "\U0001F436",
    "cabinet" : "\U0001F5C4",
    "trophy" : "\U0001F3C6",
    "first" : "\U0001F947",
    "second" : "\U0001F948",
    "third" : "\U0001F949",
    "clover" : "\U00001F34",
    "locked" : "🔒",
    "unlocked" : "🔓",
    "letters" : "\U0001F520",
    "gift" : "\U0001F381",
    "fire" : "\U0001F525",
    "star" : "\U00002B50",
    "anger" : "\U0001F620",
}

crops = {
   "wheat" : 1,
    "corn" : 1,
    "soybean" : 2,
    "sugarcane" : 3,
    "carrot" : 1,
    "indigo" : 5,
    "pumpkin" : 6,
    "cotton" : 6,
    "chilli pepper" : 7,
    "tomato" : 8,
    "strawberry" : 10,
    "potato" : 7,
    "sesame" : 4,
    "pineapple" : 3,
    "lily" : 5,
    "rice" : 3,
    "lettuce" : 7,
    "garlic" : 3,
    "sunflower" : 5,
    "cabbage" : 3,
    "onion" : 8,
    "cucumber" : 3,
    "beetroot" : 3,
    "bell pepper" : 7,
    "ginger" : 6,
    "tea leaf" : 9,
    "peony" : 7,
    "broccoli" : 4,
    "grapes" : 6,
    "mint" : 6,
    "mushroom" : 2,
    "eggplant" : 3,
    "watermelon" : 8,
    "clay" : 5,
    "chickpea" : 4,
    "apple" : 7,
    "raspberry" : 9,
    "cherry" : 13,
    "blackberry" : 16,
    "cacao" : 16,
    "coffee beans" : 12,
    "olive" : 17,
    "lemon" : 18,
    "orange" : 19,
    "peach" : 20,
    "banana" : 20,
    "passion fruit" : 4,
    "plum" : 16,
    "mango" : 20,
    "coconut" : 21,
    "guava" : 22,
    "pomegranate" : 22,
}

crop_emojis = {
    "wheat" : unicodes["bot"],
    "corn" : "<:Corn:1106752626382618644>",
    "soybean" : "<:Soybean:1106753002615865364>",
    "sugarcane" : "<:Sugarcane:1106753005237325824>",
    "carrot" : "<:Carrot:1106752384778117231>",
    "indigo" : "<:Indigo:1106752701590675496>",
    "pumpkin" : "<:Pumpkin:1106752899184349224>",
    "cotton" : "<:Cotton:1106752627330531338>",
    "chilli pepper" : "<:Chili_Pepper:1106752487865716838>",
    "tomato" : "<:Tomato:1106753009607774330>",
    "strawberry" : "<:Strawberry:1106753004209709219>",
    "potato" : "<:Potato:1106752897959596052>",
    "sesame" : "<:Sesame:1106753001303052399>",
    "pineapple" : "<:Pineapple:1106752893975015494>",
    "lily" : "<:Lily:1106752640945246278>",
    "rice" : "<:Rice:1106752999428198470>",
    "lettuce" : "<:Lettuce:1106752702865744013>",
    "garlic" : "<:Garlic:1106752631298338846>",
    "sunflower" : "<:Sunflower:1106753005983899730>",
    "cabbage" : "<:Cabbage:1106752382039228496>",
    "onion" : "<:Onion:1106752786584055809>",
    "cucumber" : "<:Cucumber:1106752628735627344>",
    "beetroot" : "<:Beetroot:1106752376783786094>",
    "bell pepper" : unicodes["bot"],
    "ginger" : "<:Ginger:1106752632267223060>",
    "tea leaf" : "<:Tea_Leaf:1106753007758082058>",
    "peony" : "<:Peony:1106752791524937758>",
    "broccoli" : "<:Broccoli:1106752380814491689>",
    "grapes" : "<:Grapes:1106752700114280488>",
    "mint" : "<:Mint:1106752782322630756>",
    "mushroom" : "<:Mushroom:1106752783333478511>",
    "eggplant" : "<:Eggplant:1106752630354608158>",
    "watermelon" : unicodes["bot"],
    "clay" : "<:Clay:1106752387135320134>",
    "chickpea" : "<:Chickpea:1106752447692677240>",
    "apple" : "<:Apple:1106752372790788156>",
    "raspberry" : "<:Raspberry:1106752997922439178>",
    "cherry" : "<:Cherry:1106752487010082846>",
    "blackberry" : "<:Blackberry:1106752379405213820>",
    "cacao" : "<:Cacao:1106752383612112907>",
    "coffee beans" : "<:Coffee_Bean:1106752625229180959>",
    "olive" : "<:Olive:1106752784906334289>",
    "lemon" : "<:Lemon:1106752639468847142>",
    "orange" : "<:Orange:1106752787615850506>",
    "peach" : "<:Peach:1106752790061137991>",
    "banana" : "<:Banana:1106752375164764200>",
    "passion fruit" : unicodes["bot"],
    "plum" : "<:Plum:1106752793974419456>",
    "mango" : "<:Mango:1106752779793465524>",
    "coconut" : "<:Coconut:1106752623421440001>",
    "guava" : "<:Guava:1106752635656216656>",
    "pomegranate" : "<:Pomegranate:1106752896462237706>",
}

red_wordle_emojis = {
    0: "<:0_a:1117155743754354829>",
    1: "<:0_b:1117155746182869162>",
    2: "<:0_c:1117155748372299877>",
    3: "<:0_d:1117155751329284166>",
    4: "<:0_e:1117155753338359808>",
    5: "<:0_f:1117155755653603339>",
    6: "<:0_g:1117155757931114697>",
    7: "<:0_h:1117155759847899176>",
    8: "<:0_i:1117155761794060389>",
    9: "<:0_j:1117155764054798526>",
    10: "<:0_k:1117155766659465276>",
    11: "<:0_l:1117155768827924651>",
    12: "<:0_m:1117155771440963654>",
    13: "<:0_n:1117155773454233692>",
    14: "<:0_o:1117155775568158845>",
    15: "<:0_p:1117156672889172009>",
    16: "<:0_q:1117156676131377243>",
    17: "<:0_r:1117156678241095731>",
    18: "<:0_s:1117156680904486942>",
    19: "<:0_t:1117156683228139630>",
    20: "<:0_u:1117156685866352813>",
    21: "<:0_v:1117156687774765097>",
    22: "<:0_w:1117156690333274162>",
    23: "<:0_x:1117156692312993833>",
    24: "<:0_y:1117156694837952603>",
    25: "<:0_z:1117156697258086431>"
}

yellow_wordle_emojis = {
    0: "<:1_a:1117151655343955988>",
    1: "<:1_b:1117151657940226138>",
    2: "<:1_c:1117151659534057593>",
    3: "<:1_d:1117151662902083694>",
    4: "<:1_e:1117151664701444216>",
    5: "<:1_f:1117151667037679677>",
    6: "<:1_g:1117151668715389038>",
    7: "<:1_h:1117151670644781086>",
    8: "<:1_i:1117151673173946468>",
    9: "<:1_j:1117151675141079110>",
    10: "<:1_k:1117151677288562688>",
    11: "<:1_l:1117151684423077998>",
    12: "<:1_m:1117151686251786341>",
    13: "<:1_n:1117151687820451880>",
    14: "<:1_o:1117151690014081066>",
    15: "<:1_p:1117151692165750834>",
    16: "<:1_q:1117151694585872527>",
    17: "<:1_r:1117155116135497808>",
    18: "<:1_s:1117151697576411359>",
    19: "<:1_t:1117155118484303872>",
    20: "<:1_u:1117151701112213504>",
    21: "<:1_v:1117155120422068234>",
    22: "<:1_w:1117151704656396338>",
    23: "<:1_x:1117155122238210148>",
    24: "<:1_y:1117151709270118460>",
    25: "<:1_z:1117151711522459649>"
}

green_wordle_emojis = {
    0: "<:2_a:1117132571369816185>",
    1: "<:2_b:1117132573949296762>",
    2: "<:2_c:1117132575677354014>",
    3: "<:2_d:1117132577736765510>",
    4: "<:2_e:1117132584665755779>",
    5: "<:2_f:1117132588964909187>",
    6: "<:2_g:1117132591380836412>",
    7: "<:2_h:1117132601417801840>",
    8: "<:2_i:1117132604202811442>",
    9: "<:2_j:1117132605838602260>",
    10: "<:2_k:1117132609030471761>",
    11: "<:2_l:1117132611228278805>",
    12: "<:2_m:1117132614533398538>",
    13: "<:2_n:1117132616810909786>",
    14: "<:2_o:1117132619121950741>",
    15: "<:2_p:1117133811432570940>",
    16: "<:2_q:1117133815580725441>",
    17: "<:2_r:1117133818487382066>",
    18: "<:2_s:1117133820769095830>",
    19: "<:2_t:1117133824262934628>",
    20: "<:2_u:1117133829031874721>",
    21: "<:2_v:1117133831405850714>",
    22: "<:2_w:1117133833796587671>",
    23: "<:2_x:1117133836355109004>",
    24: "<:2_y:1117133838162874470>",
    25: "<:2_z:1117133841119846410>"
}

purple_wordle_emojis = {
    0: "<:3_a:1129837059624947723>",
    1: "<:3_b:1129837062107963483>",
    2: "<:3_c:1129837064129609940>",
    3: "<:3_d:1129837066319056969>",
    4: "<:3_e:1129837069057921116>",
    5: "<:3_f:1129837071012479076>",
    6: "<:3_g:1129837072904093928>",
    7: "<:3_h:1129837079011004416>",
    8: "<:3_i:1129837081535987853>",
    9: "<:3_j:1129837084128071790>",
    10: "<:3_k:1129837086996971571>",
    11: "<:3_l:1129837088896979015>",
    12: "<:3_m:1129837090977353799>",
    13: "<:3_n:1129837092529254541>",
    14: "<:3_o:1129837095112945694>",
    15: "<:3_p:1129837097470132254>",
    16: "<:3_q:1129837099550527570>",
    17: "<:3_r:1129837504527339670>",
    18: "<:3_s:1129837102486528101>",
    19: "<:3_t:1129837507337531422>",
    20: "<:3_u:1129837509027827712>",
    21: "<:3_v:1129837106051682365>",
    22: "<:3_w:1129837658122752131>",
    23: "<:3_x:1129837109335838770>",
    24: "<:3_y:1129837510667800697>",
    25: "<:3_z:1129837113005842432>",
}

swear_words = [];
test_list = ["some value"];
active_expectations = [];

# p/q chance of returning True
def chance(q, p = 1):
    possibilities = [0] * (q-p-1);
    for i in range(p):
        possibilities.append(1);
    return random.choice(possibilities);
    
@command_handler.Uncontested(type = "MESSAGE", desc = "If a message contains the word greg, Greg will react with an emoji", priority = 2, generic = True)
async def greg_react(context: Context):
    neighbor = Neighbor(context.author.id, context.guild.id);
    if unicodes["star"] in context.content.lower():
        await context.react(unicodes["star"]);
    elif "rose" in context.content.lower() or "159985870458322944" in context.content:
        neighbor = Neighbor(context.author.id, context.guild.id);
        if not neighbor.get_item_of_name("Hype Man"):
            await context.react("\U0001F92C");
        else:
            await context.react("\U0001F615");
    elif "greg" in context.content.lower() or "691338084444274728" in context.content:
        neighbor = Neighbor(context.author.id, context.guild.id);
        if not neighbor.get_item_of_name("Hype Man"):
            await context.react("\U0001F914");
        else:
            await context.react("\U00002764");
    elif chance(5000):
        await context.react("🐄")  
        def key(ctx):
            if not ctx.message.id == context.message.id:
                return False;
            if not ctx.emoji.name == "🐄":
                return False;
            return True;
        ResponseRequest(special_reaction, "cow", "REACTION", context, context, key);
    
    if "greg greg greg" in context.content.lower():
        await context.send("I've been summoned!", reply = True);

@command_handler.Uncontested(type = "MESSAGE", desc = "whatever", generic = True)
async def handle_message_requests(context: Context):
    await ResponseRequest.fulfill_message_requests(context.message, context, Neighbor(context.author_id, context.guild.id));

@command_handler.Uncontested(type = "REACTION", desc = "whatever", generic = True)
async def handle_reaction_requests(context: Context):
    await ResponseRequest.fulfill_reaction_requests(context.reaction, context, Neighbor(context.user.id, context.guild.id));

@command_handler.Uncontested(type = "MESSAGE", desc = "Uses stored expectations to appropriately respond to user messages and reactions.", priority = 1, generic=True)
async def handle_message_expectations(context: Context):
    global active_expectations;
    active_expectations = [x for x in active_expectations if not x.is_expired()];
    expectations_met = [x for x in active_expectations if x.is_match("MESSAGE", context)];
    for expectation in expectations_met:
        kwargs = expectation.values.copy();
        kwargs[expectation.fulfills] = (context.content, expectation);
        await expectation.func(Neighbor(context.author_id, context.guild.id), expectation.activation_context, **kwargs);

@command_handler.Uncontested(type = "REACTION", desc = "Uses stored expectations to appropriately respond to user messages and reactions.", priority = 1, generic=True)
async def handle_reaction_expectations(context: Context):
    global active_expectations;
    active_expectations = [x for x in active_expectations if not x.is_expired()];
    expectations_met = [x for x in active_expectations if x.is_match("REACTION", context)];
    for expectation in expectations_met:
        kwargs = expectation.values.copy();
        kwargs[expectation.fulfills] = (context.emoji, expectation);
        if expectation.func.__name__ == "on_member_join":
            await expectation.func(member=expectation.activation_context.author, **kwargs)
        else:    
            await expectation.func(Neighbor(expectation.activation_context.author_id, expectation.activation_context.guild.id), expectation.activation_context, **kwargs);

@command_handler.Uncontested(type = "MESSAGE", desc = "Removes bad words.", priority = 1)
async def handle_bad_words(context: Context):
    detected = [x for x in context.content.split() if x in swear_words];
    if len(detected) > 0:
        audit_channel = await context.guild.fetch_channel(FF.audit_channel);
        await audit_channel.send(f"<@&{FF.leaders_role}> Be advised: a message from <@{context.author_id}> was deleted:")
        await audit_channel.send(f'"{context.content}"');
        await context.message.delete();
    
@command_handler.Uncontested(type = "MESSAGE", desc = "Incrememnts a Neighbor's server XP each time they send a message.", priority = 2, generic = True)
async def message_xp(context: Context):
    
    neighbor = Neighbor(context.author_id, context.guild.id);
    
    neighbor.expire_items();
    if neighbor.get_item_of_name("Message XP Cooldown"):
        return;
    
    if neighbor.get_item_of_name("Tracker"):
        tracker_item = neighbor.get_item_of_name("Tracker");
        neighbor.vacate_item(tracker_item);
    
    if neighbor.get_item_of_name("Activity-Streak XP Boost"):
        booster = neighbor.get_item_of_name("Activity-Streak XP Boost");
        last_updated = int(booster.get_value("last"));
        if time.time() > last_updated + 86400 and time.time() < last_updated + 86400 * 2:
            current_value = int(booster.get_value("val"));
            new_booster = booster;
            new_booster.update_value("val", (current_value + 1) if current_value < 6 else 6);
            new_booster.update_value("last", int(time.time()));
            neighbor.update_item(new_booster);
        elif time.time() > last_updated + 86400:
            new_booster = booster;
            new_booster.update_value("val", 0);
            new_booster.update_value("last", int(time.time()));
            neighbor.update_item(new_booster);
    else:
        booster = Item("Activity-Streak XP Boost", "retract", -1, last = int(time.time()), val = 0, hidden = "True");
        neighbor.bestow_item(booster);
    
    list_of_possibilites = [];
    
    for i in range(1, 11):
        for ii in range(i):
            list_of_possibilites.append(i * 10);
        
    # print(list_of_possibilites);
    choice = random.choice(list_of_possibilites);
    
    add = 0;
    for booster in neighbor.get_items_of_type("multiplier"):
        mult = int(booster.get_values("multiplier"));
        add += mult * choice;
        
    if neighbor.get_item_of_name("Higher XP I"):
        add += choice * 1.25;
        
    if neighbor.get_item_of_name("Higher XP II"):
        add += choice * 1.5;
    
    if neighbor.get_item_of_name("Higher XP III"):
        add += choice * 1.75;
        
    if neighbor.get_item_of_name("Higher XP IV"):
        add += choice * 2;
        
    milestone_boost = neighbor.get_item_of_name("Milestone Boost");
    if milestone_boost:
        add += choice * (int(milestone_boost.get_value("boost")) / 100);
        
    choice += add;
    global xp_gained
    if xp_happy_hour != 1:
        
        choice *= xp_happy_hour;
        xp_gained += choice;
        
    # spam prevention:
    try:
        with open("last_sender.txt", "r") as fLast:
            last_sender = fLast.readline();
            if str(context.author_id) in last_sender:
                choice *= .5;
    except:
        print("couldn't read file");
        
    if len(context.content) < 10:
        choice *= len(context.content) / 3
    # elif len(context.args) < 3:
    #     choice *= len(context.args) / 1.5
    
    with open("recent_messages.txt", 'r') as fRecent:
        # Read all lines of the file into a list
        lines = fRecent.readlines()
        
        # Join the lines into a single string and replace new line characters with spaces
        text = ' '.join([line.strip() for line in lines])
        
    if context.content in text:
        choice *= .5
        
    while choice > 275:
        choice -= 50;
    
    if choice < 1:
        return
    
    print("Message gets: " + str(choice));
    await inc_xp(neighbor, int(choice), context);
    
    try:
        family_info = {
            "butterflies": 0,
            "cheetahs": 0,
            "foxes": 0,
            "horses": 0,
            "puppies": 0};
        with open('families.txt', 'r') as fFams:
            lines = fFams.readlines();
            family_info["butterflies"] = int(lines[0][:-1]);
            family_info["cheetahs"] = int(lines[1][:-1]);
            family_info["foxes"] = int(lines[2][:-1]);
            family_info["horses"] = int(lines[3][:-1]);
            family_info["puppies"] = int(lines[4][:-1]);
        
        member = await context.guild.fetch_member(neighbor.ID);
        fam = get_family_from_user(member)
        if fam == '0':
            pass;
        elif fam == 'B':
            family_info["butterflies"] = family_info["butterflies"] + int(choice);
        elif fam == 'C':
            family_info["cheetahs"] = family_info["cheetahs"] + int(choice);
        elif fam == 'F':
            family_info["foxes"] = family_info["foxes"] + int(choice);
        elif fam == 'H':
            family_info["horses"] = family_info["horses"] + int(choice);
        elif fam == 'P':
            family_info["puppies"] = family_info["puppies"] + int(choice);
            
        with open("families.txt", "w") as fFams:
            fFams.write(str(family_info["butterflies"]) + "\n");
            fFams.write(str(family_info["cheetahs"]) + "\n");
            fFams.write(str(family_info["foxes"]) + "\n");
            fFams.write(str(family_info["horses"]) + "\n");
            fFams.write(str(family_info["puppies"]) + "\n");
    except Exception as e:
        traceback.print_exc();
        

    neighbor.bestow_item(Item("Message XP Cooldown", "XP Cooldown", int(time.time() + 60)));
    with open("last_sender.txt", "w") as fLast:
        fLast.write(str(context.author_id));
    
    with open("recent_messages.txt", 'a') as fRecent:
        # Append the string to the file
        fRecent.write(" " + context.content);
    
    with open("recent_messages.txt", 'r') as fRecent:
        # Read the file contents into a list of words
        words = fRecent.read().split()
        
    if len(words) > 1000:
        words = words[-1000:]
        with open("recent messages", 'w') as file:
            file.write(' '.join(words)) 
    
    best_this_month = neighbor.get_item_of_name("Best Level This Month");
    if best_this_month:
        if neighbor.get_level() > int(best_this_month.get_value("level")):
            best_this_month.update_value("level", neighbor.get_level());
            try:
                free_count = best_this_month.get_value("free_count");
            except:
                best_this_month.add_value("free_count", 0);
            neighbor.update_item(best_this_month);
    else:
        best_this_month = Item("Best Level This Month", "monthly", -1, level = neighbor.get_level(), free_count = 0, hidden = "true");
        neighbor.bestow_item(best_this_month);
    
@command_handler.Uncontested(type = "REACTION", desc = "Incrememnts a Neighbor's server XP each time they send a reaction.", priority = 2, generic = True)
async def reaction_xp(context: Context):
    
    neighbor = Neighbor(context.author_id, context.guild.id);
    
    neighbor.expire_items(); 
    if neighbor.get_item_of_name("Reaction XP Cooldown"):
        print("Stopping you from react xp")
        return;
    
    if neighbor.get_item_of_name("Activity-Streak XP Boost"):
        booster = neighbor.get_item_of_name("Activity-Streak XP Boost");
        last_updated = int(booster.get_value("last"));
        if time.time() > last_updated + 86400 and time.time() < last_updated + 86400 * 2:
            current_value = int(booster.get_value("val"));
            new_booster = booster;
            new_booster.update_value("val", (current_value + 1) if current_value < 6 else 1);
            new_booster.update_value("last", int(time.time()));
            neighbor.update_item(new_booster);
        elif time.time() > last_updated + 86400:
            new_booster = booster;
            new_booster.update_value("val", 0);
            new_booster.update_value("last", int(time.time()));
            neighbor.update_item(new_booster);
    else:
        booster = Item("Activity-Streak XP Boost", "retract", -1, last = int(time.time()), val = 0);
        neighbor.bestow_item(booster);
    
    list_of_possibilites = [];
    
    for i in range(1, 11):
        for ii in range(i):
            list_of_possibilites.append(i);
        
    # print(list_of_possibilites);
    choice = random.choice(list_of_possibilites);
    
    add = 0;
    for booster in neighbor.get_items_of_type("multiplier"):
        mult = int(booster.get_values("multiplier"));
        add += mult * choice;
        
    choice += add;
    global xp_gained
    if xp_happy_hour != 1:
        
        choice *= xp_happy_hour;
        xp_gained += choice;
        
    # print(choice)

    await inc_xp(neighbor, int(choice), context);
    print("Reaction gets: " + str(choice));

    neighbor.bestow_item(Item("Reaction XP Cooldown", "XP Cooldown", int(time.time() + 60)));

@command_handler.Uncontested(type = "MESSAGE", desc = "Incrememnts a Neighbor's server XP each time they send a celebrate or welcome.", priority = 2, generic = True)
async def celebrate_xp(context: Context):
    
    if not (context.content.startswith("$celebrate") or context.content.startswith("$welcome")):
        return;
    
    neighbor = Neighbor(context.author_id, context.guild.id);
    
    neighbor.expire_items();
    if neighbor.get_item_of_name("Celebrate XP Cooldown"):
        print("Stopping you from celebrate xp")
        return;
    
    if neighbor.get_item_of_name("Activity-Streak XP Boost"):
        booster = neighbor.get_item_of_name("Activity-Streak XP Boost");
        last_updated = int(booster.get_value("last"));
        if time.time() > last_updated + 86400 and time.time() < last_updated + 86400 * 2:
            current_value = int(booster.get_value("val"));
            new_booster = booster;
            new_booster.update_value("val", (current_value + 1) if current_value < 6 else 1);
            new_booster.update_value("last", int(time.time()));
            neighbor.update_item(new_booster);
        elif time.time() > last_updated + 86400:
            new_booster = booster;
            new_booster.update_value("val", 0);
            new_booster.update_value("last", int(time.time()));
            neighbor.update_item(new_booster);
    else:
        booster = Item("Activity-Streak XP Boost", "retract", -1, last = int(time.time()), val = 0);
        neighbor.bestow_item(booster);
    
    list_of_possibilites = [];
    
    for i in range(1, 11):
        for ii in range(i):
            list_of_possibilites.append(i);
    
    # print(list_of_possibilites);
    choice = random.choice(list_of_possibilites);
    
    add = 0;
    for booster in neighbor.get_items_of_type("multiplier"):
        mult = int(booster.get_values("multiplier"));
        add += mult * choice;
        
    choice += add;
    global xp_gained
    if xp_happy_hour != 1:
        
        choice *= xp_happy_hour;
        xp_gained += choice;
        
    # print(choice)

    await inc_xp(neighbor, int(choice), context);
    print("Celebrate gets: " + str(choice));

    neighbor.bestow_item(Item("Celebrate XP Cooldown", "XP Cooldown", int(time.time() + 3600)));

async def harvest_xp(context: Context):
    
    if not context.content.startswith("$harvest"):
        return;
    
    neighbor = Neighbor(context.author_id, context.guild.id);
    
    neighbor.expire_items();

    list_of_possibilites = [];
    
    for i in range(1, 11):
        for ii in range(i):
            list_of_possibilites.append(i);
    
    # for booster in neighbor.get_items_of_type("expand"):
    #     val = int(booster.get_value("val"));
    #     for i in range(11, val + 1):
    #         for ii in range(i):
    #             list_of_possibilites.append(i);
    
    for booster in neighbor.get_items_of_type("retract"):
        val = int(booster.get_value("val"));
        for i in range(val):
            list_of_possibilites = list_of_possibilites[1:];
        
    # print(list_of_possibilites);
    choice = random.choice(list_of_possibilites);
    
    add = 0;
    for booster in neighbor.get_items_of_type("multiplier"):
        mult = int(booster.get_values("multiplier"));
        add += mult * choice;
        
    choice += add;
    global xp_gained
    if xp_happy_hour != 1:
        
        choice *= xp_happy_hour;
        xp_gained += choice;
        
    print("Harvest gets: " + str(choice))

    await inc_xp(neighbor, int(choice), context);

@command_handler.Uncontested(type = "REACTION", desc = "Open a Greg Support ticket.")
async def support_ticket_reaction(context: Context):
    if context.message.id == 1033540464441303200:
        await open_ticket(context.emoji, context.user, context.guild);
        
async def open_ticket(emoji, user, guild):
    target = user.id;
    name = user.display_name;
    name = name.replace(" ", "-")

    support_channel = await guild.fetch_channel(FF.support_request_channel);
    message = await support_channel.fetch_message(1033540464441303200);
    open_tickets_cat = await guild.fetch_channel(FF.open_tickets_category);
    closed_tickets_cat = await guild.fetch_channel(FF.closed_ticket_category);
    open_tickets = open_tickets_cat.channels;
    closed_tickets = closed_tickets_cat.channels;
    mission_control = await guild.fetch_channel(FF.mission_control_channel);
    cm = guild.get_role(FF.leaders_role);
    
    if not emoji is None:
        await message.remove_reaction(emoji, user);

    for ticket in open_tickets:
        if ticket.topic == str(target):
            await ticket.edit(name = name);
            await ticket.send(f"Thank you for reaching out to the Council again. Your private ticket channel is located here <@{user.id}>.");
            return 0;

    for ticket in closed_tickets:
        if ticket.topic == str(target):
            await ticket.edit(name = name, category = open_tickets_cat);

            await ticket.set_permissions(guild.get_role(647883751853916162), read_messages = False);
            await ticket.set_permissions(user, read_messages = True);

            await ticket.send(f"Thank you for reaching out to the Council. Your private ticket channel has been unarchived for you and is located here <@{user.id}>.");
            await mission_control.send(f"<@&{FF.leaders_role}> **be advised**: <@{user.id}> has reopened a support ticket at <#{ticket.id}>");
            return 0;

    ticket = await message.guild.create_text_channel(name = name, category = open_tickets_cat, topic = target);
    await ticket.set_permissions(guild.get_role(647883751853916162), read_messages = False);
    await ticket.set_permissions(user, read_messages = True);
    await ticket.send(f"Thank you for reaching out to the Council via Greg for the first time! Your private ticket channel is located here <@{user.id}>.");
    await mission_control.send(f"<@&{FF.leaders_role}> **be advised**: <@{user.id}> has opened a new support ticket at <#{ticket.id}>");
        
@command_handler.Uncontested(type = "MESSAGE", desc = "If a Neighbor has the Hype Man item, which can be purchased in the rss, then Greg will react to the Neighbor's messages with an emoji.", priority = 2)
async def hype_man_responses(context: Context):
    neighbor = Neighbor(context.author_id, context.guild.id);
    neighbor.expire_items();
    if not neighbor.get_item_of_name("Hype Man"):
        return;
    
    if random.choices([True, False], weights=[0.01, 0.99])[0]:
        target = await context.send(f"$celebrate <@{context.author.id}>");
        celebrate_context = Context(message = target);
        await celebrate(neighbor, celebrate_context);
    elif random.choices([True, False], weights=[0.02, 0.98])[0]:
        await context.send(f"Yeah, listen to what <@{context.author_id}> said! They're the real deal!")
    elif random.choices([True, False], weights=[0.02, 0.98])[0]:
        await context.send(f"Listen up!! Da real <@{context.author_id}> is in the chat!")
    elif random.choices([True, False], weights=[0.05, 0.95])[0]:
        await context.react("\U0001F973");
    elif random.choices([True, False], weights=[0.02, 0.98])[0]:
        await context.send(f"Sup <@{context.author_id}>! You know I love ya!")
    elif random.choices([True, False], weights=[0.05, 0.95])[0]:
        await context.react("\U0001F64C");
    elif random.choices([True, False], weights=[0.05, 0.95])[0]:
        await context.react("\U0001F44F");

async def special_reaction(neighbor, context, response: ResponsePackage):
    if response.name == "cow":
        await context.send("Omg! Thank you so much :) You found my lost cow. I've been looking for her for a long time. For your kindess, resilience, and bravery, enjoy this prize of 5k xp");

        await inc_xp(neighbor, 5000, context);
    
@command_handler.Uncontested(type = "MESSAGE", desc = "Shortcuts for harvest")
async def harvest_shorthand(context: Context):
    if context.content == "h" or context.content == "$harv":
        neighbor = Neighbor(context.author.id, context.guild.id);
        await harvest(neighbor, context);

@command_handler.Uncontested(type = "REACTION", desc = "Giveaway reroll")
async def reroll_react(context: Context):
    if not str(context.emoji) == "<:reroll:1060038218113888266>":
        return;
    target = None;
    with open("giveaways.txt", 'r') as fGiveaways:
        for line in fGiveaways.readlines():
            if str(context.user.id) in line:
                target = context.message;
    if target is None:
        return;
    
    council_role = await context.guild.get_role(FF.leaders_role);
    if context.user.id != context.author_id and not has_role(context.user, council_role):
        return;
            
    with open("winners.txt", 'r') as fWinners:
       winners = fWinners.readlines()

    reacted_users = [];
    for reaction in target.reactions:
        if str(reaction.emoji) == "<:giveaway:1067499350705582124>":
            async for user in reaction.users():
                if not user.id == 691338084444274728:
                    reacted_users.append(user.id)

    entries = [];
    for reacted_user in reacted_users:
        tickets = 10
        for winner in winners:
            if int(winner) == reacted_user:
                tickets -= 1.5;
        if Neighbor(reacted_user, FF.guild).get_item_of_name("Better Giveaway Luck"):
            tickets *= 2;
        tickets = int(tickets) if tickets > 0 else 1
        for i in range(tickets):
            entries.append(reacted_user)
        
    winner = random.choice(entries);
    
    await target.reply(f"Congratulations <@{winner}>! You've won a reroll!\nDM the host for winnings!");
    original_content = target.content;
    lines = original_content.split("\n");
    lines[0] = "Giveaway has ended!";
    lines[3] = f"The winner was <@{winner}>";
    lines[4] = "\n*Council members and the giveaway creator may react with <:reroll:1060038218113888266> to reroll. All members may use $give to start a giveaway!*";
    await target.edit(content="\n".join(lines));
    await target.add_reaction("<:reroll:1060038218113888266>");
        
    with open(fWinners, 'w') as fWinners:
        fWinners.writelines(winners[1:])
        fWinners.write(str(winner) + '\n')

@command_handler.Uncontested(type = "REACTION", desc = "Market", generic = True)
async def farmers_market_reaction(context: Context):
    print("at market")
    #phoenix_market
    if context.guild.id == FF.guild:
        with open("market.txt", "r") as fMarket:
            market_channel_id = int(fMarket.readline());
            # print(market_channel_id);
            if context.channel.id != market_channel_id:
                print("not matching id");
                return;
            message_id = int(fMarket.readline());
            # print(message_id);
            if context.message.id != message_id:
                print("not matching message")
                return;
            
            options = [];
            lines = fMarket.readlines();
            for i, line in enumerate(lines):
                print(f"{i}: {line}");
                if not i % 3 == 0:
                    continue;
                name = line[:-1];
                amt = int(lines[i + 1][:-1]);
                price = int(lines[i + 2][:-1]);
                option = (name, amt, price);
                print(option);
                options.append((name, amt, price));
        
        print([f"{option[0]} {option[1]} {option[2]}" for option in options]); 
        choice = -1;
        emoji = str(context.emoji)
        if emoji == unicodes[0]:
            choice = 0;
        elif emoji == unicodes[1]:
            choice = 1
        elif emoji == unicodes[2]:
            choice = 2
        elif emoji == unicodes[3]:
            choice = 3
        elif emoji == unicodes[4]:
            choice = 4
        
        print("User chose: " + str(choice));
        if choice > -1 and choice < 5:
            pass;
        else:
            return;
    
        neighbor = Neighbor(context.user.id, context.guild.id); 
        silo_item = neighbor.get_item_of_name("Silo");
        sale = options[choice];
        name = sale[0];
        amt = sale[1];
        price = sale[2];
        cur_amt = int(silo_item.get_value(name));
        if int(cur_amt) >= amt:
            silo_item.update_value(name, cur_amt - amt);
            neighbor.update_item(silo_item);
            await inc_xp(neighbor, price, context);
            bc = await context.guild.fetch_channel(FF.bot_channel);
            if neighbor.get_item_of_name("Pings Off"):
                await bc.send("Someone just sold {amt} {name}(s)? for {price}xp at the farmers market!");
            else:
                await bc.send(f"<@{neighbor.ID}> just sold {amt} {name}(s)? for {price}xp at the farmers market!");
        else:
            bc = await context.guild.fetch_channel(FF.bot_channel);
            if neighbor.get_item_of_name("Pings Off"):
                await bc.send(f"Whoops! Someone just attempted to sell {amt} {name}(s)? for {price}xp at the farmers market! But Failed!");
            else:  
                await bc.send(f"Whoops! <@{neighbor.ID}> just attempted to sell {amt} {name}(s)? for {price}xp at the farmers market! But Failed!");
    
    elif context.guild.id == PHOENIX.guild:
        with open("phoenix_market.txt", "r") as fMarket:
            market_channel_id = int(fMarket.readline());
            # print(market_channel_id);
            if context.channel.id != market_channel_id:
                return;
            message_id = int(fMarket.readline());
            # print(message_id);
            if context.message.id != message_id:
                return;
            
            options = [];
            lines = fMarket.readlines();
            for i, line in enumerate(lines):
                print(f"{i}: {line}");
                if not i % 3 == 0:
                    continue;
                name = line[:-1];
                amt = int(lines[i + 1][:-1]);
                price = int(lines[i + 2][:-1]);
                option = (name, amt, price);
                print(option);
                options.append((name, amt, price));
        
        print([f"{option[0]} {option[1]} {option[2]}" for option in options]); 
        choice = -1;
        emoji = str(context.emoji)
        if emoji == unicodes[0]:
            choice = 0;
        elif emoji == unicodes[1]:
            choice = 1
        elif emoji == unicodes[2]:
            choice = 2
        elif emoji == unicodes[3]:
            choice = 3
        elif emoji == unicodes[4]:
            choice = 4
        
        print("choice was " + str(choice));
        if choice > -1 and choice < 5:
            pass;
        else:
            return;
    
        neighbor = Neighbor(context.user.id, context.guild.id); 
        silo_item = neighbor.get_item_of_name("Silo");
        sale = options[choice];
        name = sale[0];
        amt = sale[1];
        price = sale[2];
        cur_amt = int(silo_item.get_value(name));
        if int(cur_amt) >= amt:
            silo_item.update_value(name, cur_amt - amt);
            neighbor.update_item(silo_item);
            await inc_xp(neighbor, price, context);
            bc = await context.guild.fetch_channel(PHOENIX.bot_channel);
            await bc.send(f"<@{neighbor.ID}> just sold {amt} {name}(s)? for {price}xp at the farmers market!");
        else:
            bc = await context.guild.fetch_channel(PHOENIX.bot_channel);
            await bc.send(f"Whoops! <@{neighbor.ID}> just attempted to sell {amt} {name}(s)? for {price}xp at the farmers market! But Failed!");

# @command_handler.Uncontested(type = "JOIN", desc = "Alerts that a member joined the server.")
async def on_join(context: Context, member, priority = 2):
    general = await context.fetch_channel("general_channel")
    await general.send(f"<:ffp_logo:1111011980061462538><:ff_logo:1111011971953872976><:ffj_logo:1111011976320122880><:ffr_logo:1111011982787743866>\n**Welcome to Town, <@{str(member.id)}>**\nIt's great to see you!**\n\nIf you're looking for a neighborhood, tell us a little about you, and we'll tell you a little about us!\n\nWe have three Neighborhoods, one to suit every style of play. __Type $info NH to learn more!__\n\n**Required!: Set your server nickname to be or clearly include your farm name. Thanks for your cooperation!**");

# @command_handler.Uncontested(type = "REMOVE", desc = "Alerts that a member left the server.")
async def on_leave(context: Context, member, priority = 2):
    general = await context.fetch_channel("general_channel");
    await general.send(f"{member} left Town.");
    
    possibilities = [
        "https://tenor.com/view/cat-sticker-line-sticker-bye-sticker-goodbye-sticker-hand-wave-gif-26479344",
        "https://tenor.com/view/hasta-la-vista-baby-arnold-schwarzenegger-the-celebrity-apprentice-hasta-hasta-la-gif-7486141",
        "https://tenor.com/view/jennifer-lawrence-the-mocking-jay-the-hunger-games-hunger-games-mocking-jay-gif-17322681",
        "https://tenor.com/view/this-is-so-sad-gif-25352430",
        "https://tenor.com/view/hug-me-im-sad-sad-girl-gif-24456547",
    ]
    
    await general.send(random.choice(possibilities));

# @command_handler.Uncontested(type = "EDIT", desc = "Alerts that a member left the server.", priority = 3)
async def on_edit(context: Context):
    
    similarity = difflib.SequenceMatcher(None, context.before.content, context.after.content).ratio();
    if similarity < .75:
        audit_channel = context.guild.fetch_channel(context.ID_bundle.audit_channel);
        before_content = convert_mentions_to_text(context, context.before.content);
        after_content = convert_mentions_to_text(context, context.after.content)
        text = f"*A message from <@{context.author_id}> ({context.author}) was edited:*\n> {before_content}\n\n> {after_content}";
        await audit_channel.send(text);

# @command_handler.Uncontested(type = "DELETE", desc = "Alerts that a member left the server.", priority = 3)
async def on_delete(context: Context):
    audit = await context.fetch_channel("audit_channel");
    text = f"*A message from <@{context.author_id}> ({context.author}) was deleted:*\n> {context.content}";
    await audit.send(text);

@command_handler.Loop(minutes = 5)
async def set_time(client):
    guild = client.get_guild(FF.guild);
    vc = await guild.fetch_channel(1092957590427815966);
    current_time_utc = time.time()

    # convert UTC to Eastern Standard Time (EST)
    est_offset = datetime.timedelta(hours=-4)
    est_time = datetime.datetime.fromtimestamp(current_time_utc, datetime.timezone.utc) + est_offset

    # round the minute to the nearest 5
    est_minute = est_time.minute
    est_minute_rounded = 5 * round(est_minute/5)
    est_time = est_time.replace(minute=est_minute_rounded)

    # format the time as a string with AM/PM marker
    est_time_str = est_time.strftime("It's %I:%M%p server time");
    await vc.edit(name=est_time_str)

# @command_handler.Loop(minutes = 5)
# async def free_xp(client):
#     guild = client.get_guild(FF.guild);
#     bc = await guild.fetch_channel(FF.bot_channel);
#     neighbors = Neighbor.read_all_neighbors();
#     for neighbor in neighbors:
#         cur = neighbor.get_level();
#         neighbor.increase_XP(500);
#         new = neighbor.get_level();
#         if new > cur:
#             try:
#                 member = await guild.fetch_member(neighbor.ID);
#             except:
#                 pass;
#             await bc.send(f"{member.display_name} just reached level {new}");
#     Neighbor.write_all_neighbors(neighbors);

# @command_handler.Loop(days = 1, desc = "Sorts the Neighbors text file in order of descending XP once per day.", priority = 4)
async def database_mgmt():
    neighbors = Neighbor.read_all_neighbors();
    neighbors.sort(key=lambda x : x.get_XP());
    Neighbor.write_all_neighbors();

@command_handler.Loop(hours = 12, desc = "Removes unneccesary members.")
async def remove_non_present_members(client):
    guild = client.get_guild(FF.guild);
    
    neighbors = Neighbor.read_all_neighbors();
    print("N:" + str(len(neighbors)))
    new_neighbors = [];
    i = 0;
    for neighbor in neighbors:
        i += 1
        if (i % 10 == 0):
            print(i)
        try:
            await guild.fetch_member(neighbor.ID)
            new_neighbors.append(neighbor);
        except:
            pass
    print("N:" + str(len(new_neighbors)))
    Neighbor.write_all_neighbors(new_neighbors);
        
@command_handler.Loop(hours = 12, desc = "Rose theft!")
async def theft(client):
    guild = client.get_guild(FF.guild);
    
    if not chance(10):
        return
    
    neighbors = Neighbor.read_all_neighbors();
    thefted_from = [];
    i = 0;
    for neighbor in neighbors:
        perchance = 10
        if neighbor.get_item_of_name("SiloGuard(TM) Level 1 Security"):
            perchance = 20
        if neighbor.get_item_of_name("SiloGuard(TM) Level 2 Security"):
            perchance = 40
        if not chance(perchance):
            pass;
        thefted_from.append(neighbor);
        i += 1
        if (i % 10 == 0):
            print(i)
        silo_item: Item = neighbor.get_item_of_name("Silo")
        if silo_item:
            values = silo_item.values;
            for key, val in values.items():
                if not chance(10):
                    pass;
                new_val = str(int(int(val) * .9))
                silo_item.update_value(key, new_val);
            neighbor.update_item(silo_item);
    Neighbor.write_all_neighbors(neighbors);
    
    bc = await guild.fetch_channel(FF.bot_channel);
    res = "**Oh no! The silo thief!\n\n A small amount of crops have been thieved from the silos of some users.\n";
    # for neighbor in thefted_from:
    #     res += f"<@{neighbor.ID}> \n"
    res += "\nSorry about that! Use `$info thief` to learn more!";
    
    await bc.send(res);
    

@command_handler.Loop(days = 1, desc = "Checks once per day for support ticket channels that have had no new messages in 48 hours and archives them." , priority = 4)
async def archive_support(client):
    guild = client.get_guild(FF.guild);
    support_channel = await guild.fetch_channel(FF.support_request_channel);
    message = await support_channel.fetch_message(1033540464441303200);
    open_tickets_cat = await guild.fetch_channel(FF.open_tickets_category);
    closed_tickets_cat = await guild.fetch_channel(FF.closed_ticket_category);
    open_tickets = open_tickets_cat.channels;
    closed_tickets = closed_tickets_cat.channels;
    mission_control = await guild.fetch_channel(FF.mission_control_channel);
    cm = guild.get_role(FF.leaders_role);

    for ticket in open_tickets:
        if ticket.id == FF.mission_control_channel:
            continue;
        try:
            user = await guild.fetch_member(int(ticket.topic));
        except:
            await ticket.edit(category=closed_tickets_cat);
            await ticket.set_permissions(user, read_messages = False);
        last = [message async for message in ticket.history(limit=1)][0];
        if last.created_at.timestamp() + 172800 < time.time():
            await ticket.edit(category=closed_tickets_cat);
            await ticket.set_permissions(user, read_messages = False);

@command_handler.Loop(days = 1, desc = "On tuesdays and thursdays, a new channel called Farmerss Market appears that lets Neighbors sell crops to Greg for XP.")
async def farmers_market_mgmt(client):
            # Determine whether today is a Tuesday or Thursday

    is_today = random.choice([1]);
    if is_today == 2:
        is_today = random.choice([0,1]);
 
    # Get the server and the "Town Square" category
    guild = client.get_guild(FF.guild);
    town_square = await guild.fetch_channel(FF.town_square_category);

    # Look for the "farmers-market" channel in the server
    for channel in guild.channels:
        if channel.name == "\U0001F33Efarmers-market":
            farmers_market_channel = channel;
            await farmers_market_channel.delete();


    # # Get the server and the "Town Square" category
    # guild = client.get_guild(PHOENIX.guild);
    # town_square = await guild.fetch_channel(PHOENIX.general_category);

    # # Look for the "farmers-market" channel in the server
    # for channel in guild.channels:
    #     if channel.name == "\U0001F33Efarmers-market":
    #         farmers_market_channel = channel;
    #         await farmers_market_channel.delete();

    if not is_today:
        return;

    guild = client.get_guild(FF.guild);
    town_square = await guild.fetch_channel(FF.town_square_category);

    farmers_market_channel = None;

    # If it's a Tuesday or Thursday and the channel is not found, create it
    if is_today and farmers_market_channel is None:
        market = await guild.create_text_channel("\U0001F33Efarmers-market", category=town_square)

        crops_for_sale = random.sample(list(crops.items()), 5);

        boost_choice = random.choices([0, 1, 2], weights=[0.15,0.50,0.35])[0];

        options = [];

        res = "";

        for i, crop in enumerate(crops_for_sale):
            amt = random.randint(1, 10 ** (i + 1));
            factor = random.randint(6, 12);
            unit_price = crop[1] * factor + (i * random.randint(4, 6));
            if boost_choice == i:
                increase = random.choice([1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2]);
                # print("increase: " + str(increase));
                unit_price *= increase;
                amt *= increase;
                unit_price = round(unit_price);
                amt = round(amt);
            # print("amt: " + str(amt))
            # print("unit_price: " + str(unit_price))
            total_price = round((unit_price * amt) / 10)
            if i == 3 or i == 4:
                amt = 20;
                total_price = 20;	
            options.append((crops_for_sale[i][0], amt, total_price));
            add = (f"{i}) {options[i][0]} -- offer is {options[i][1]} for {options[i][2]}xp");
            if boost_choice == i:
                add = "**" + add + "**"
            if i == 3 or i == 4:
                add = "*" + add + "*";
            res += "> " + add + "\n";

        await market.send(f"**Welcome to the Farmers Market!**\nFive crops are in demand today. To aceept a transaction, react with the number associated with that transaction. As you may be able to tell, crop #{boost_choice} is in particularly high demand today.")
        target = await market.send(res)

        fMarket = open("market.txt", "w");
        fMarket.write(str(target.channel.id) + "\n")
        fMarket.write(str(target.id) + "\n")
        for option in options:
            fMarket.write(str(option[0]) + "\n");
            fMarket.write(str(option[1]) + "\n");
            fMarket.write(str(option[2]) + "\n");
        fMarket.close();

        await target.add_reaction(unicodes[0]);
        await target.add_reaction(unicodes[1]);
        await target.add_reaction(unicodes[2]);
        await target.add_reaction(unicodes[3]);
        await target.add_reaction(unicodes[4]);
        await target.pin();
        
        # guild = client.get_guild(PHOENIX.guild);
        # town_square = await guild.fetch_channel(PHOENIX.general_category);
        # market = await guild.create_text_channel("\U0001F33Efarmers-market", category=town_square)
        # await market.send(f"**Welcome to the Farmers Market!**\nFive crops are in demand today. To aceept a transaction, react with the number associated with that transaction. As you may be able to tell, crop #{boost_choice} is in particularly high demand today.")
        # target = await market.send(res)
        
        # fMarket = open("phoenix_market.txt", "w");
        # fMarket.write(str(target.channel.id) + "\n")
        # fMarket.write(str(target.id) + "\n")
        # for option in options:
        #     fMarket.write(str(option[0]) + "\n");
        #     fMarket.write(str(option[1]) + "\n");
        #     fMarket.write(str(option[2]) + "\n");
        # fMarket.close();

        # await target.add_reaction(unicodes[0]);
        # await target.add_reaction(unicodes[1]);
        # await target.add_reaction(unicodes[2]);
        # await target.add_reaction(unicodes[3]);
        # await target.add_reaction(unicodes[4]);
        # await target.pin();
        
# @command_handler.Loop(hours = 24, desc = "")
# async def now(client):
#     guild = client.get_guild(FF.guild);
#     current_time = datetime.datetime.now()
#     current_day = current_time.day
#     if current_day == 2:
#         guild = client.get_guild(FF.guild);
#         bc = await guild.fetch_channel(FF.bot_channel);
#         # guild = client.get_guild(PHOENIX.guild);
#         # pbc = await guild.fetch_channel(PHOENIX.bot_channel);
#         await bc.send("It's about that time!");
#         # await pbc.send("It's about that time!");
#         for i in range(5):
#             print(f"{5-i}...");
#             time.sleep(1);
#         neighbors = Neighbor.read_all_neighbors();
#         for readNeighbor in neighbors:
#             neighbor = Neighbor(readNeighbor.ID, readNeighbor.family);
#             cur_level = neighbor.get_level();
#             strip(neighbor, levels = int(cur_level / 2));
#             if int(neighbor.get_family()) == FF.guild:
#                 if neighbor.get_item_of_name("Pings Off"):
#                     pass;
#                 else:
#                     await bc.send(f"<@{neighbor.ID}> has dropped to level {neighbor.get_level()}");
#             elif int(neighbor.get_family() == PHOENIX.guild):
#                 pass;
#                 # if neighbor.get_item_of_name("Pings Off"):
#                 #     pass;
#                 # else:
#                 #     await pbc.send(f"<@{neighbor.ID}> has dropped to level {neighbor.get_level()}");
#             best_this_month = neighbor.get_item_of_name("Best Level This Month");
#             if best_this_month:
#                 neighbor.vacate_item(best_this_month);
#         Neighbor.write_all_neighbors(neighbors);
        
# @command_handler.Loop(minutes = 10, desc = "")
# async def pbc(client):
#         guild = client.get_guild(PHOENIX.guild);
#         pbc = await guild.fetch_channel(PHOENIX.bot_channel);
#         await pbc.send("@everyone--the reckoning is upon you!")
#         await pbc.send("Below is the discord leaderboard for the top 10 members of the server in the past month!")
#         await pbc.send("In one day, the reckoning will ensue. To level the playing field without making everyone start from scratch, each person's level is cut in half at the beginning of each month.")
#         await pbc.send("If you intend/ed to spend or deposit your levels before the reset, you have approx 24 hours to do so. Use $rss to spend those levels baby!")
#         target = await pbc.send("$leaderboard");
#         await leaderboard(Neighbor(691338084444274728, 1008089618090049678), Context(target));

@command_handler.Loop(days = 1, desc = "On the second day of each month, all Neighbors' server XP is reset.")
async def xp_reset(client):
    print('xp reset!');
    guild = client.get_guild(FF.guild);
    current_time = datetime.datetime.now()
    current_day = current_time.day
    if current_day == 1:
        bc = await guild.fetch_channel(FF.bot_channel);
        await bc.send("@everyone--the reckoning is upon you!")
        await bc.send("Below is the discord leaderboard for the top 10 members of the server in the past month!")
        await bc.send("In one day, the reckoning will ensue. To level the playing field without making everyone start from scratch, each person's level is reduced at the beginning of each month.")
        await bc.send("If you intend/ed to spend your levels before the reset, you have approx 24 hours to do so. Use $rss to spend those levels baby!")
        target = await bc.send("$leaderboard");
        await leaderboard(Neighbor(691338084444274728, 647883751853916162), Context(target));
    if current_day == 2:
        ff_guild = client.get_guild(FF.guild);
        bc = await guild.fetch_channel(FF.bot_channel);
        await bc.send("It's about that time!");
        for i in range(5):
            await bc.send(f"{5-i}...");
            time.sleep(5);
        neighbors = Neighbor.read_all_neighbors();
        for readNeighbor in neighbors:
            neighbor = Neighbor(readNeighbor.ID, readNeighbor.family);
            cur_level = neighbor.get_level();
            strip(neighbor, levels = int(cur_level / 2));
            if int(neighbor.get_family()) == FF.guild:
                await bc.send(f"<@{neighbor.ID}> has dropped to level {neighbor.get_level()}");
            best_this_month = neighbor.get_item_of_name("Best Level This Month");
            if best_this_month:
                neighbor.vacate_item(best_this_month);
        await bc.send("That feels much better! All done. #sorrynotsorry")
            
# @command_handler.Loop(days = 1, desc = "Silo thief")
# async def thief(client, n: Neighbor):
#     if chance(10):
#         options = [0,1,2,3,4,5,6,7,8,9];
#         victim_id = random.choice(options);
#         victims = [x for x in Neighbor.read_all_neighbors() if x.ID % 10 == victim_id and x.get_item_of_name("Silo")];
#         for v in victims:
#             neighbor = Neighbor(v.ID, v.family);
#             silo = n.get_item_of_name("Silo");
            
            


# @command_handler.Loop(days = 1, desc = "On mondays, the council is asked to select what derby type is coming up.")
async def derby_channel_mgmt(client, selection = None):
    today = datetime.datetime.today()
    guild = client.get_guild(FF.guild);
    if selection is None and today.weekday() == 0:
        council_chat = await guild.fetch_channel(FF.leaders_bot_channel)
        target = await council_chat.send("It's that time of the week!\nPlease react for the derby type that is this week.");
        await target.add_reaction(unicodes["derby"]);
        await target.add_reaction(unicodes["muscle"])
        await target.add_reaction(unicodes["cat"])
        await target.add_reaction(unicodes["question"])
        await target.add_reaction(unicodes["flower"])
        await target.add_reaction(unicodes["target"])
        Expectation("Derby Type", "REACTION", time.time() + 72000, "derby_channel_mgmt", None, council_chat.id, target.id).persist();
    elif today.weekday() == 0:
        name = "derby-chat"
        if selection == unicodes["muscle"]:
            name = "power-derby-chat";
        elif selection == unicodes["cat"]:
            name = "chill-derby-chat";
        elif selection == unicodes["question"]:
            name = "mystery-derby-chat";
        elif selection == unicodes["flower"]:
            name = "blossom-derby-chat";
        elif selection == unicodes["target"]:
            name = "bingo-derby-chat";
            
@command_handler.Loop(days = 1, desc = "Reminders!")
async def reminders_mgmt(client):
    guild = client.get_guild(FF.guild);

    reminders = [];
    
    with open("reminders.txt", "r") as fReminders:
        for line in fReminders:
            data = line.split(":")
            reminders.append((data[0], data[1], data[2]));
    
    today = datetime.date.today().weekday();
    for reminder in reminders:
        if str(today) in reminder[0]:
            channel = await guild.fetch_channel(int(reminder[1]));
            await channel.send(reminder[2]);
    
        
            
@command_handler.Loop(hours = 10, desc = "Archive unused support channels")
async def archive_support_tickets(client):
    
    category_id = FF.closed_ticket_category  # Replace with the category ID where the channels are located

    guild = client.get_guild(FF.guild); 
    
    category = discord.utils.get(guild.categories, id=category_id)
    if category:
        for channel in category.channels:
            if isinstance(channel, discord.TextChannel):
                user_id = int(channel.topic)
                try:
                    member = await guild.fetch_member(user_id)
                except:
                    print(f'User not found for channel {channel.name}, deleting...')
                    await channel.delete()
    else:
        print(f'Category with ID {category_id} not found in the guild.')
    
    
    support_channel = await guild.fetch_channel(FF.support_request_channel);
    message = await support_channel.fetch_message(1033540464441303200);
    open_tickets_cat = await guild.fetch_channel(FF.open_tickets_category);
    closed_tickets_cat = await guild.fetch_channel(FF.closed_ticket_category);
    open_tickets = open_tickets_cat.channels;
    closed_tickets = closed_tickets_cat.channels;
    mission_control = await guild.fetch_channel(FF.mission_control_channel);
    cm = guild.get_role(FF.leaders_role);

    for ticket in open_tickets:
        if ticket.id == 1033544493728809000:
            continue;
        try:
            user = await guild.fetch_member(int(ticket.topic));
        except:
            await ticket.edit(category=closed_tickets_cat);
            await ticket.set_permissions(user, read_messages = False);
        last = [message async for message in ticket.history(limit=1)][0];
        if last.created_at.timestamp() + 86400 < time.time():
            await ticket.edit(category=closed_tickets_cat);
            await ticket.set_permissions(user, read_messages = False);
            guild = client.get_guild(FF.guild)  # Replace with your guild/server ID

            
# @command_handler.Loop(days = 1, desc = "From the second through fourth of each month, rss items are on sale. Also the 25th through the 28th")
async def sale_mgmt(client):
    choice = 0;
    with open("data/server_info.txt", "w") as fServer:
        if datetime.datetime.today() in [random.randint(1, 31), random.randint(1, 31)]:
            bot_channel = await client.get_guild(FF.guild).fetch_channel(FF.bot_channel);
            choice = random.choices([1, 2, 3], weights=[.9, 0.09, 0.01])[0];
            await bot_channel.send(f"It's your lucky day! Get up to {choice} level(s) off of your purchases in my $rss for the next 24 hours!!");
        else:
            choice = 0
        fServer.write(str(choice))
        
# @command_handler.Loop(days = 1, desc = "Updates swear_words list if necesary.")
async def swear_word_mgmt(client):
    swear_words.clear();
    with open("swearWords.txt") as fWords:
        for line in fWords.readlines():
            swear_words.append(line[:-1]);
            
        
@command_handler.Loop(hours = 8, desc = "If a Neighbor has a passive XP item, the user receives free server XP once per hour.")
async def passive_xp(client):
    # print("running passive");
    neighbors = Neighbor.read_all_neighbors();
    for neighbor in neighbors:
        neighbor.expire_items();
        passive_item = neighbor.get_item_of_name("Hire Rose and Earnest");
        if not passive_item is None:
            new_item = passive_item;
            if passive_item.expiration == -1:
                passive_item.expiration = int(time.time() + 604800);
                new_item.expiration = passive_item.expiration
            time_remaining = int(passive_item.expiration - time.time());
            
            passes_remaining = time_remaining / 28800;
            xp_accumulated = int(passive_item.get_value("so_far"));
            xp_needed = int(passive_item.get_value("needs"));
            if xp_needed < 0:
                continue;
            this_pass = (xp_needed - xp_accumulated) / passes_remaining;
            possibilities = [-.5, -.3, -.2, -.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02 -0.01, 0];
            
            choice = int(this_pass + (this_pass * random.choice(possibilities)));
            if choice <= 0:
                continue;
            new_item.update_value("so_far", xp_accumulated + choice)
            neighbor.increase_XP(choice);
            neighbor.set_legacy_XP(neighbor.get_legacyXP() + choice);
            if time_remaining > 259200:
                new_item.expiration = int(time.time() + 345600);
            neighbor.update_item(new_item);
            
            guild = client.get_guild(neighbor.family);
            if guild.id == FF.guild:
                bot_channel = await guild.fetch_channel(FF.bot_channel);
            # else:
            #     bot_channel = await guild.fetch_channel(PHOENIX.bot_channel);
                
            if random.choice([0, 0, 0, 1]) and not neighbor.get_item_of_name("Pings Off"):
                await bot_channel.send(f"Rose and Earnest just harvested {choice}xp for <@{neighbor.ID}>");
            else:
                user = await guild.fetch_member(neighbor.ID)
                await bot_channel.send(f"Rose and Earnest just harvested {choice}xp for {user.display_name}");
            
    Neighbor.write_all_neighbors(neighbors);

@command_handler.Loop(minutes = 20, desc = "Takes away rss roles if necessary")
async def role_mgmt(client):
    guild = client.get_guild(FF.guild);
    for member in guild.members:
        await set_roles(member, guild);
    
    guild = client.get_guild(PHOENIX.guild);
    for member in guild.members:
        await set_roles(member, guild);

# @command_handler.Loop(minutes = 10, desc = "The barn role icon is changed to a random barn.")
async def change_barn_role_icon(client):
    guild = client.get_guild(FF.guild);

@command_handler.Loop(minutes = 15, desc = "Nick management")
async def nick_mgmt(client):
    guild = client.get_guild(FF.guild);
    async for member in client.get_guild(FF.guild).fetch_members():
        try:
            await set_nick(member, guild);
        except:
            pass
    
    
@command_handler.Loop(minutes = 5, desc = "The rainbow role color is changed to a random color.")
async def change_rainbow_role_color(client):
    guild = client.get_guild(FF.guild);
    rainbow_role = guild.get_role(1055882917429137479);
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    # Convert the integers to hexadecimal strings
    r_hex = hex(r)[2:]  # slice off the "0x" prefix
    g_hex = hex(g)[2:]
    b_hex = hex(b)[2:]

    # Pad the strings with leading zeros if necessary
    r_hex = r_hex.rjust(2, '0')
    g_hex = g_hex.rjust(2, '0')
    b_hex = b_hex.rjust(2, '0')

    # Combine the strings into a single hex code string
    hex_v = f'#{r_hex}{g_hex}{b_hex}'
    await rainbow_role.edit(color=discord.Colour.from_str(hex_v));
    await guild.get_role(FF.blueberry_role).edit(color=discord.Colour.from_str("#01cdfe"));
    await guild.get_role(FF.strawberry_role).edit(color=discord.Colour.from_str("#ff71ce"));
    # guild = client.get_guild(PHOENIX.guild);
    # rainbow_role = guild.get_role(PHOENIX.rainbow_role);
    # await rainbow_role.edit(color=discord.Colour.from_str(hex_v));
    # await guild.get_role(PHOENIX.blueberry_role).edit(color=discord.Colour.from_str("#01cdfe"));
    # await guild.get_role(PHOENIX.strawberry_role).edit(color=discord.Colour.from_str("#ff71ce"));

    
@command_handler.Command(AccessType.PUBLIC, desc = "Provides information about greg and an assortment of random things. For example, `$info blossom` provides information on blossom derby.", generic = True)
async def info(activator: Neighbor, context: Context):
    type = None;
    if len(context.args) > 1:
        type = context.args[1];
    res = "";
    if context.guild.id == 647883751853916162:
        possibilities = ["ff", "main", "ffj", "junior", "ffr", "resort", "family", "blossom", "bingo", "chill", "power", "mystery", "bunny", "farms award", "higher", "wfo", "nh", "neighborhood", "xp", "farmmas", "bank"];
        match "" if type is None else type.lower():
            case None | "":
                res = f"**Hi! my name is Greg :wave:**\nI was created by Lincoln's Farm, & currently running Version {VERSION}.\nI can do lots of things; use $help to find out more.\nVersion 3.0 comes with a more structured code base that makes me easier to maintain and update without any downtime blah blah blah. 3.0 also comes with new features including: reminders, giveaways, polls, and over 10 new rss items to purchase!.\n\nIf you care less about me and more about other stuff (ouch) you can use $info to obtain info about derby types (`$info blossom`), our neighborhoods (`$info FF`), and more! See a list with (`$help info`)";
            case "ffp" | "pro":
                res = "FFP is short for **Friendly Farmers Pro** <:ffp_logo:1111011980061462538>, the newest Friendly Farmers neighborhood.\n> Tag: #LQVJ9QVR\n> Derby Req: Max Points w/ diamond task (3200p normal derby) + speed requirement + task trashing limit\n> Level Req: 60\n> Unique FFP Requirements: Complete tasks within 5 days, 30 trashed-tasks per person limit, Reputation level 18\n*As are all of our Neighbors, FFP Neighbors are expected to be **F**riendly, **A**ctive, **R**emarkable, **M**unificent, and **S**ustainable.*";
                with open("pro_nh_ad.png", 'rb') as file:
                    await context.send(file=discord.File(file))
            case "ff" | "main":
                res = "FF is short for **Friendly Farmers** <:ff_logo:1111011971953872976>, the \"main\", first, OG Friendly Farmers neighborhood.\n> Tag: #9UPRVCUR\n> Derby Req: Max Points w/o diamond task (2880p normal derby)\n> Level Req: 45 (updated June 5th)\n*As are all of our Neighbors, FF Neighbors are expected to be **F**riendly, **A**ctive, **R**emarkable, **M**unificent, and **S**ustainable.*";
                with open("main_nh_ad.png", 'rb') as file:
                    await context.send(file=discord.File(file))
            case "ffj" | "junior":
                res = "FFJ is short for **Friendly Farmers Junior** <:ffj_logo:1111011976320122880>, the second Friendly Farmers neighborhood.\n> Tag: #PC8VCJ8Q\n> Derby Req: Lvl x 40p (1200p for level 30 player)\n> Level Req: 25 (updated June 5th)\n*As are all of our Neighbors, FFJ Neighbors are expected to be **F**riendly, **A**ctive, **R**emarkable, **M**unificent, and **S**ustainable.*";
                with open("junior_nh_ad.png", 'rb') as file:
                    await context.send(file=discord.File(file))
            case "ffr" | "resort":
                res = "FFR is short for **Friendly Farmers Resort** <:ffr_logo:1111011982787743866>, the third Friendly Farmers neighborhood.\n> Tag: #L92LUVQJ\n> Derby Req: None\n> Level Req: 10\n*As are all of our Neighbors, FFR Neighbors are expected to be **F**riendly, **A**ctive, **R**emarkable, **M**unificent, and **S**ustainable.*";
                with open("resort_nh_ad.png", 'rb') as file:
                    await context.send(file=discord.File(file))
            case "families" | "family":
                res = "All Neighbors are split into one of five families: The Butterflies, Cheetahs, Foxes, Horses, or Puppies.\nThese are smaller communities within the big Friendly Farmers community to help create bonds and add a bit of fun.\nEach month, families compete for trohpies--aka bragging rights--by participating in some sort of competition. About half the time, family competitions are derby related (sorry FFR!). The other half of the time, families compete in a lot of different ways in game, on disocrd, or even in real life!";
            case "farms" | "farms award":
                res = "FARMS is our model for 'good neighbors'. Good Friendly Farmers neighbors are Friendly, Active, Remarkable, Munificent, and Sustainable.\n\nEvery couple of weeks, we vote for the most FARMS neighbor. This neighbor receives an invitation to join our council of leaders!"
            case "animal" | "birthday" | "camping" | "carnival" | "easter" | "fall" | "fishing" | "friends" | "halloween" | "holiday" | "new year" | "new years" | "new year's" | "party" | "picnic" | "summer" | "town" | "trophy" | "yoga":
                res = "An outdated derby type (while outdated derby types have not ever been officialy discontinued by Hay Day, players can reasonably expect to not see these types in current rotation).\n\nIf you want to read more about this type of derby, I recommend visiting the Hay Day wiki page for derby types.\nhttps://hayday.fandom.com/wiki/Derby_Types";
            case "blossom":
                res = "A modern derby type.\nBlossom tasks, once comepleted, return to the board for others to take worth more points than before.\n\nImportant notes:\n• Blossom tasks are designated by a flower pin.\n• The task board can only hold a certain number of blossom tasks, so only take quick tasks and complete them ASAP to not leave others hanging!\n• Don't take tasks before bed! As aforementioned, other people would like to take that task too!\n• Only leaders should trash tasks.\n• Use your neighborhood's channels for blossom checks and blossom planning to keep things running smoothly!\n\nRequirements: 3200p in FF, +5 * lvl in FFJ";
            case "bingo":
                res = "A modern derby type.\nCompleting a line on the bingo board gives everyone in the neighborhood extra rewards. To complete a line, the neighborhood must take a certain number of specific tasks to fill bingo squares.\nImportant Notes:\n• Bingo tasks are designated by a star pin.\n• While the neighborhood can technically complete up to three bingo lines, the leaders will likely guide the neighborhood to select one or two lines to aim for.\n\nNo effect on requirements.";
            case "chill":
                res = "A modern derby type.\nA derby without competition. Tasks go back on the board once completed. Tasks are worth 50p each, and players can take up to 5 per day (6 for 2 diamonds). Horseshoes can still be earned.\n\nNo point requirement in any NH!";
            case "power":
                res = "A modern derby type.\nTwice as many tasks are availale, and each is approximately half as difficult.\n\nRequirements: 5760 in FF, +5 * lvl in FFJ.";
            case "mystery":
                res = "A modern derby type.\nMystery tasks, worth 400p, can be found on the task board.\n\nImportant Notes:\n• Any task can appear as a mystery task once taken as long as you are high enough level for it.\n• Low level players can suffer in mystery derby due to getting tasks that are almost impossible for their level. It is recommended to opt out for this derby or only take regular tasks if possible.\n\nRequirements: 3600p in FF, +5 * lvl in FFJ.";
            case "bunny":
                res = "A modern derby type.\nAt certain points throughout the day, all tasks on the board will become bunny tasks. This is called bunny time, and it lasts 10 minutes. They are marked by a pink tint and a bunny pin. If you take a bunny task during bunny time, you can complete it after bunny time ends and it still counts as a bunny task.\nDepending on how many people are playing in the derby, completing about 20 bunny tasks amounts to the Neighborhood catching one bunny.\nEach bunny caught, up to three, will reward the Neighborhood with an extra horseshoe reward at the end of derby. \n\nImportant Notes:\n• After a bunny is caught, the neighborhood may have to wait a day or more for the next bunny to be 'released'.\n• Bunny derby is often combined with other derby types, creating combos such as the leisurely chill bunny derby and the dreaded mystery bunny derby.";
            case "farms award" | "award":
                res = "The FARMS award is a method of __recognition__ and __election__ in Friendly Farmers. FARMS stands for Friendly, Active, Remarkable (in derby), Munificent, and Sustainable: our 5 main attributes as Friendly Farmers."
            case "higher":
                res = "Higher XP 1 increases XP by 25%.\nHigher XP II increases XP by 50%.\nHigher XP III increases XP by 75%.\nHigher XP IV increases XP by 100%"
            case "wfo":
                res = "The World Farmers Organization seeks to protect farmers from bots.";
            case "nh" | "nhs" | "neighborhood" | "neighborhoods" | "all":
                res = "We have four neighborhoods available. \n<:ffp_logo:1111011980061462538>**Friendly Farmers Pro** is our newest Neighborhood, which competes for the global derby leaderboard and requires 10/10 tasks (level 60+; speed requirement; task trashing limit). \n<:ff_logo:1111011971953872976>**Friendly Farmers** is our main Neighborhood, which competes for top 3 in champs league and requires 9/9 tasks (level 45+).\n<:ffj_logo:1111011976320122880>**Friendly Farmers Junior** is our 2nd Neighborhood, which competes for all the champs league horseshoes and requires a certain number of points based on your level (level 25+).\n<:ffr_logo:1111011982787743866>**Friendly Farmers Resort** is our 3rd Neighborhood, which is our non-derby neighborhood (level 10+)."
                # with open("all_nhs_ad", 'rb') as file:
                #     await channel.send(file=discord.File(file))
            case "xp":
                res = "You earn xp every time you message (only once per minute though to prevent spam), but it's a little complex on how much you get per message.\n\nTo put it simply, by default, the list of possibilities ranges from 10-100. When you send a message, I pick from this list of possibilities. The weights of each possibility are such that you get 70xp per message on average. Higher XP I adds 110 to the range of possibilities and increases the average per message. Similarly, Higher XP II adds 120 to the range, and Higher XP III adds 130 to the range. (Use $info higher to learn more). With all three, the average maxes out at 90xp per message.\n\nBeing active for multiple days in a row affects the bottom of the range instead of the top. Basically, for each day consecutively that you are active it reduces the weight of low-xp possibilities. The streak boost maxes out at 6 days and an average of 75xp per message; it resets if you do not send any messages for a day.\n\nCertain boosters available with greg apply a percentage increase (or decrease) to the xp amount that I pick from the range of possibilities.\n\nWith Higher XP I, II, and III + a 6 day streak, your average xp per message is 94.7xp"
            case "farmmas" | "farmmas" | "farm-pass":
                res = "**Farm-mas!**\nOur Neighbors come from many different regions, cultures, and religions and thus each celebrate unique winter holidays. Farm-mas is a winter holiday in Friendly Farmers that all Neighbors can celebrate. It's a time to be grateful for one another and show each other love. The unofficial official dates for Farm-mas is December 9th through 20th This holiday includes celebrations such as the Council's 12 Days of Farm-mas Gift giveaways and other events."
            case "bank":
                res = "XP stored in a GregBanking(TM) account is immune from the monthly reckoning. This XP can be used to buy things from my rss at a price about 25% above market value. You can use $deposit to put xp in your account. There is a 1000xp fee for each deposit."
            case "penalty":
                res = "Derby BEM penalties are the main source of revenue for the Friendly Farmers Treasury ($info treasury).\n\nIn Friendly Farmers Pro and Friendly Farmers (Main), failure to meet derby requirements is associated with being demoted and recieving a BEM penalty. The amount varies based on how many tasks you miss, your level, NH, and even the type of derby. \n\nThe receiver of a BEM penalty must pay to any council member their choice of Bolts, Duct Tape, or Planks (or a mix). Failure to pay may result in being kicked. Penalties may be waived in extenuating circumstances.";
            case "treasury":
                res = "All Council-sanctioned events, for which BEMs are a reward, are funded by the Friendly Farmers Treasury. The treasury itself consists soley of Bolts, Duct Tape, and Planks. Council Members hold these BEMs in their own accounts, and a detailed spreadsheet is kept to ensure all current holdings are accounted for and that all uses are approved.\n\nThe main source of revenue for the treasury is derby BEM penalties ($info penalty). However, the treasury also accepts straight-up donations from Neighbors (contact a council member to make a donation). Additionally, some council-sanctioned events may turn a BEM-profit, which also funds the treasury directly.\n\nExamples of events that are funded by the treasury:\n> • Weekly derby Lotteries\n> • FARMS award rewards\n> • Deco Comp winners' rewards\nWeCouncil members never pay out of pocket for events (Farm-mas gifts are a notable exception)."
            case "thief":
                with open("thief.png", 'rb') as file:
                    await context.send(file=discord.File(file))
                res = "Can you believe it! A silo thief on this side of the Mississippi!\n\nEye witnesses have spotted this suspect breaking into silos in OUR TOWN!!! Unfortunately, due to their mask, it is impossible to identify the suspect. I recommend purchasing upgraded security for your Silo (which I happen to be selling at `$rss`). Trust no one!!\n\n*According to data gathered in the nearest town East, the thief seems to break into 10%% of silos on 10%% of days. From those silos, the thief takes 10%% of the stock of 10%% of its crops.";
            case _:
                best_match = best_string_match(type.lower(), possibilities);
                raise CommandArgsError(f"Hmm... I don't have info on that yet!\n\n*Did you mean `$info {best_match}`?*");
    else:
        possibilities = ["bp", "pr", "blossom", "bingo", "chill", "power", "mystery", "bunny", "higher", "wfo", "xp", "farmmas", "bank"];
        match "" if type is None else type.lower():
            case None | "":
                res = f"**Hi! my name is Greg :wave:**\nI was created by Lincoln's Farm from Friendly Farmers, & currently running Version {VERSION}.\nI can do lots of things; use $help to find out more.\nVersion 3.0 comes with a more structured code base that makes me easier to maintain and update without any downtime blah blah blah. 3.0 also comes with new features including: reminders, giveaways, polls, and over 10 new rss items to purchase!.\n\nIf you care less about me and more about other stuff (ouch) you can use $info to obtain info about derby types (`$info blossom`), our neighborhoods (`$info PR`), and more! See a list with (`$help info`)";
            case "blossom":
                res = "A modern derby type.\nBlossom tasks, once comepleted, return to the board for others to take worth more points than before.\n\nImportant notes:\n• Blossom tasks are designated by a flower pin.\n• The task board can only hold a certain number of blossom tasks, so only take quick tasks and complete them ASAP to not leave others hanging!\n• Don't take tasks before bed! As aforementioned, other people would like to take that task too!";
                res += "\n\nNH Notes:\n> ";
                res += context.ID_bundle.info["blossom"].replace("\n", "\n> ")
            case "bingo":
                res = "A modern derby type.\nCompleting a line on the bingo board gives everyone in the neighborhood extra rewards. To complete a line, the neighborhood must take a certain number of specific tasks to fill bingo squares.\nImportant Notes:\n• Bingo tasks are designated by a star pin.";
                res += "\n\nNH Notes:\n> ";
                res += context.ID_bundle.info["bingo"].replace("\n", "\n> ")
            case "chill":
                res = "A modern derby type.\nA derby without competition. Tasks go back on the board once completed. Tasks are worth 50p each, and players can take up to 5 per day (6 for 2 diamonds). Horseshoes can still be earned.";
                res += "\n\nNH Notes:\n> ";
                res += context.ID_bundle.info["chill"].replace("\n", "\n> ")
            case "power":
                res = "A modern derby type.\nTwice as many tasks are availale, and each is approximately half as difficult.";
                res += "\n\nNH Notes:\n> ";
                res += context.ID_bundle.info["power"].replace("\n", "\n> ")      
            case "mystery":
                res = "A modern derby type.\nMystery tasks, worth 400p, can be found on the task board.\n\nImportant Notes:\n• Any task can appear as a mystery task once taken as long as you are high enough level for it.";
                res += "\n\nNH Notes:\n> ";
                res += context.ID_bundle.info["mystery"].replace("\n", "\n> ")
            case "bunny":
                res = "A modern derby type.\nAt certain points throughout the day, all tasks on the board will become bunny tasks. This is called bunny time, and it lasts 10 minutes. They are marked by a pink tint and a bunny pin. If you take a bunny task during bunny time, you can complete it after bunny time ends and it still counts as a bunny task.\nDepending on how many people are playing in the derby, completing about 20 bunny tasks amounts to the Neighborhood catching one bunny.\nEach bunny caught, up to three, will reward the Neighborhood with an extra horseshoe reward at the end of derby. \n\nImportant Notes:\n• After a bunny is caught, the neighborhood may have to wait a day or more for the next bunny to be 'released'.\n• Bunny derby is often combined with other derby types, creating combos such as the leisurely chill bunny derby and the dreaded mystery bunny derby.";
                res += "\n\nNH Notes:\n> ";
                res += context.ID_bundle.info["bunny"].replace("\n", "\n> ")
            case "animal" | "birthday" | "camping" | "carnival" | "easter" | "fall" | "fishing" | "friends" | "halloween" | "holiday" | "new year" | "new years" | "new year's" | "party" | "picnic" | "summer" | "town" | "trophy" | "yoga":
                res = "An outdated derby type. (Outdated derby types have not been officialy discontinued by Hay Day, players can reasonably expect to not see these types in current rotation).\n\nIf you want to read more about this type of derby, I recommend visiting the Hay Day wiki page for derby types.\nhttps://hayday.fandom.com/wiki/Derby_Types";
            case "higher":
                res = "Higher XP 1 increases XP by 25%.\nHigher XP II increases XP by 50%.\nHigher XP III increases XP by 75%.\nHigher XP IV increases XP by 100%"
            case "wfo":
                res = "The World Farmers Organization seeks to protect farmers from bots.";
            case "xp":
                res = "You earn xp every time you message (only once per minute though to prevent spam), but it's a little complex on how much you get per message.\n\nTo put it simply, by default, the list of possibilities ranges from 10-100. When you send a message, I pick from this list of possibilities. The weights of each possibility are such that you get 70xp per message on average. Higher XP I adds 110 to the range of possibilities and increases the average per message. Similarly, Higher XP II adds 120 to the range, and Higher XP III adds 130 to the range. (Use $info higher to learn more). With all three, the average maxes out at 90xp per message.\n\nBeing active for multiple days in a row affects the bottom of the range instead of the top. Basically, for each day consecutively that you are active it reduces the weight of low-xp possibilities. The streak boost maxes out at 6 days and an average of 75xp per message; it resets if you do not send any messages for a day.\n\nCertain boosters available with greg apply a percentage increase (or decrease) to the xp amount that I pick from the range of possibilities.\n\nWith Higher XP I, II, and III + a 6 day streak, your average xp per message is 94.7xp"
            case "bank":
                res = "XP stored in a GregBanking(TM) account is immune from the monthly reckoning. This XP can be used to buy things from my rss at a price about 25% above market value. You can use $deposit to put xp in your account. There is a 1000xp fee for each deposit."
            case _:
                # replace CHANNEL_NAME with the name of the channel you want to search for
                channel = discord.utils.get(context.guild.channels, name='greg-info')
                
                messages = [];
                async for message in channel.history(limit=None):
                    messages.append(message.content);
                message_list = []
                for message in messages:
                    message_content = message.split(':')
                    message_tuple = (message_content[0], message_content[1])
                    message_list.append(message_tuple)

                potential_blubrs = [];
                for blurb in message_list:
                    prompts = blurb[0].split(" | ");
                    prompt = type.lower();
                    if prompt in prompts:
                        potential_blubrs.append(blurb);
                
                class AdminCustomizationError(ValueError):
                    pass;
                
                if len(potential_blubrs) > 1:
                    raise AdminCustomizationError(f"The prompt {type.lower()} is assigned to multiple prompts.");   
                elif len(potential_blubrs) == 0:
                    best_match = best_string_match(type.lower(), possibilities);
                    raise CommandArgsError(f"Hmm... I don't have info on that yet!\n\n*Did you mean `$info {best_match}`?*");
                else:
                    res = potential_blubrs[0][1];
            
    await context.send(res, reply = True);

@command_handler.Command(AccessType.PUBLIC, desc = "Provides a list of available commands, or alternatively describes the function of a particular command. For example, `$help help`", generic = True)
async def help(activator: Neighbor, context: Context):
    if len(context.args) > 1:
        res = command_handler.Command.generate_help_str(context.args[1]);
    else:
        res = command_handler.Command.generate_help_str(None, context.guild.id == FF.guild);
    await context.send(res);

@command_handler.Command(AccessType.PUBLIC, desc = "Welcome to Greg!")
async def hello(activator: Neighbor, context: Context):
    await context.send("**Hello, I am Greg!**\n\nI am a Bot, and I do most of the work around here :rolling_eyes:\n\nI was programmed by one of our Council Members <@355169964027805698>, and I have two main purposes:\n> 1. For fun! I control our server's level system. You can chat anywhere in the server to level up, then spend your levels on cool discord perks. For example: special role colors, role icons, nickname tags, and more.\n> 2. For business! I control our server's modmail system in <#1033207181857800242>, our reminders, our welcome messages, and more.\n\nYou're going to get to know me very well!\n\nAnd oh yeah, Rose is my mortal enemy.", reply = True);

@command_handler.Command(AccessType.PUBLIC, desc = "Get the tag of an FF Neighborhood with `$tag FFP`, `$tag FF`, `$tag FFJ`, or `$tag FFR`")
async def tag(activator: Neighbor, context: Context):
    if len(context.args) < 2:
        raise CommandArgsError("`$tag` expects 1 argument: the name of the neighborhood to display the tag of")
    else:
        match context.args[1].lower():
            case "ffp" | "pro":
                res = "#LQVJ9QVR"
            case "ff" | "main":
                res = "#9UPRVCUR"
            case "ffj" | "junior":
                res = "#PC8VCJ8Q"
            case "ffr" | "resort":
                res = "#L92LUVQJ"
            case _:
                raise CommandArgsError("That's not one of the FF neighborhoods!");
        await context.send(res, reply = True);

@command_handler.Command(AccessType.PUBLIC, desc = "Invites greg to celebrate an event or achievement", generic = True)
async def celebrate(activator: Neighbor, context: Context):
    if context.guild.id == 647883751853916162:
        first = ['Congratulations!',
            'Yay!! <:blue_red_hearts:856202113339490304>',
            'Wohoo!!',
            'Amazing!!',
            'Celebration time!!',
            'Let\'s goooo!',
            ':star_struck::star_struck:',
            'I\'ve taken a quick break from my chores on the farm to say…',
            ':raised_hands: :raised_hands:',
            ':smiley_cat: :smile_cat: :smirk_cat:',
            ':tada::tada::tada:',
            'slay !!',
            'Hey, don\'t start the party without ~~Rose, your favorite FF Helper!~~ Greg, your *favorite* FF Helper.',
            ':men_with_bunny_ears_partying::people_with_bunny_ears_partying::women_with_bunny_ears_partying:',
            'Greg ~~V2.0~~ **V3.0** is here, we should be celebrating *that*!! But if you insist...',
            'I\'ve been waiting for this one!',
            'Let\'s celebrate!!'
            ':butterfly: On behalf of the butterfly family...',
            ':leopard: On behalf of the cheetah family...',
            ':fox: Oxn behalf of the fox family...',
            ':horse_racing: On behalf of the horse family...',
            ':dog: On behalf of the puppy family...',
            'The Neighbors of the FFP, FF, FFJ, and FFR family want you to know...',
            'Greg, at your service! One day closer to replacing Rose every day!',
            '<:ff_logo:1111011971953872976><:ff_logo:1111011971953872976><:ff_logo:1111011971953872976>',
            '<:ff_logo:1111011971953872976><:ffj_logo:1111011976320122880><:ffr_logo:1111011982787743866>'
            '<:ffr_logo:1111011982787743866><:ffr_logo:1111011982787743866><:ffr_logo:1111011982787743866>',
            '<:ffp_logo:1111011980061462538><:ffp_logo:1111011980061462538><:ffp_logo:1111011980061462538>',
            'Drum roll please...',
            'You summoned me... for this?',
            ];
            
        second = ['~~Wait, what happened? I missed it :grimacing:~~ \nJust kidding. Rose would have missed it, but I could never!',
            'https://tenor.com/view/snoop-dogg-rap-hip-hop-west-coast-crips-gif-24898891',
            'https://tenor.com/view/celebrate-weekend-vibe-friday-be-like-gif-4811973',
            'https://tenor.com/view/baby-yoda-babyyoda-gif-20491479',
            'https://tenor.com/view/schitts-creek-david-i-feel-like-that-needs-to-be-celebrated-gif-13054100',
            'https://tenor.com/view/%E0%A4%B0%E0%A4%BE%E0%A4%A7%E0%A4%BE%E0%A4%B8%E0%A5%8D%E0%A4%B5%E0%A4%BE%E0%A4%AE%E0%A5%80-fire-works-celebrate-gif-12772532',
            'https://tenor.com/view/cookie-monster-dancing-swag-ernie-sesame-street-gif-23523854',
            'https://tenor.com/view/leonardo-dicaprio-cheers-%C5%9Ferefe-celebration-celebrating-gif-20368613',
            'https://tenor.com/view/madagascar-zuba-this-calls-for-a-celebration-celebration-celebrate-gif-22777408',
            'https://tenor.com/view/dace-gif-25608746'
            'https://tenor.com/view/fortnite-dance-fortnite-emote-default-dance-meme-school-background-gif-26343206',
            'https://tenor.com/view/omg-schock-cat-gif-20299170',
            'https://tenor.com/view/omg-wow-really-surprised-feeling-it-gif-15881647',
            'https://www.youtube.com/watch?v=HPuD7w_TbSc',
            'https://tenor.com/view/bb13-big-brother13-lawon-exum-bblawon-bb13lawon-gif-14741549',
            'https://tenor.com/view/yeah-yeaa-yippie-yippi-happy-gif-23469210',
            'https://tenor.com/view/trump-shuffle-gif-19016904',
            'https://tenor.com/view/excited-hive-hivechat-community-blockchain-gif-18465569',
            'https://tenor.com/view/excited-so-gif-23170060',
            'https://tenor.com/view/abbott-elementary-hyped-turnt-lit-turn-up-gif-25388930',
            'Sorry, no gif today kid. You know how it is. Supply chain issues, inflation, etc etc',
            'https://tenor.com/view/nice-clap-hand-gif-23085040',
            'https://tenor.com/view/iconic-rupaul-rupauls-drag-race-all-stars-legendary-show-stopping-gif-26155592',];
    else:
        first = ['Congratulations!',
            'Yay!! <:blue_red_hearts:856202113339490304>',
            'Wohoo!!',
            'Amazing!!',
            'Celebration time!!',
            'Let\'s goooo!',
            ':star_struck::star_struck:',
            'I\'ve taken a quick break from my chores on the farm to say…',
            ':raised_hands: :raised_hands:',
            ':smiley_cat: :smile_cat: :smirk_cat:',
            ':tada::tada::tada:',
            'slay !!',
            'Hey, don\'t start the party without ~~Rose, your favorite FF Helper!~~ Greg, your *favorite* FF Helper.',
            ':men_with_bunny_ears_partying::people_with_bunny_ears_partying::women_with_bunny_ears_partying:',
            'Greg ~~V2.0~~ **V3.0** is here, we should be celebrating *that*!! But if you insist...',
            'I\'ve been waiting for this one!',
            'Let\'s celebrate!!'
            'Greg, at your service! One day closer to replacing Rose every day!',
            'You summoned me... for this?']
            
        second = ['~~Wait, what happened? I missed it :grimacing:~~ \nJust kidding. Rose would have missed it, but I could never!',
            'https://tenor.com/view/snoop-dogg-rap-hip-hop-west-coast-crips-gif-24898891',
            'https://tenor.com/view/celebrate-weekend-vibe-friday-be-like-gif-4811973',
            'https://tenor.com/view/baby-yoda-babyyoda-gif-20491479',
            'https://tenor.com/view/schitts-creek-david-i-feel-like-that-needs-to-be-celebrated-gif-13054100',
            'https://tenor.com/view/%E0%A4%B0%E0%A4%BE%E0%A4%A7%E0%A4%BE%E0%A4%B8%E0%A5%8D%E0%A4%B5%E0%A4%BE%E0%A4%AE%E0%A5%80-fire-works-celebrate-gif-12772532',
            'https://tenor.com/view/cookie-monster-dancing-swag-ernie-sesame-street-gif-23523854',
            'https://tenor.com/view/leonardo-dicaprio-cheers-%C5%9Ferefe-celebration-celebrating-gif-20368613',
            'https://tenor.com/view/madagascar-zuba-this-calls-for-a-celebration-celebration-celebrate-gif-22777408',
            'https://tenor.com/view/dace-gif-25608746'
            'https://tenor.com/view/fortnite-dance-fortnite-emote-default-dance-meme-school-background-gif-26343206',
            'https://tenor.com/view/omg-schock-cat-gif-20299170',
            'https://tenor.com/view/omg-wow-really-surprised-feeling-it-gif-15881647',
            'https://www.youtube.com/watch?v=HPuD7w_TbSc',
            'https://tenor.com/view/bb13-big-brother13-lawon-exum-bblawon-bb13lawon-gif-14741549',
            'https://tenor.com/view/yeah-yeaa-yippie-yippi-happy-gif-23469210',
            'https://tenor.com/view/trump-shuffle-gif-19016904',
            'https://tenor.com/view/excited-hive-hivechat-community-blockchain-gif-18465569',
            'https://tenor.com/view/excited-so-gif-23170060',
            'https://tenor.com/view/abbott-elementary-hyped-turnt-lit-turn-up-gif-25388930',
            'Sorry, no gif today kid. You know how it is. Supply chain issues, inflation, etc etc'];
        
    await context.send(random.choice(first), reply = True);
    await context.send(random.choice(second));

@command_handler.Command(AccessType.PUBLIC, desc = "Invites greg to welcome a user to the server.", generic = True)
async def welcome(activator: Neighbor, context: Context):
    choices = [
        'https://tenor.com/view/welcome-gif-23701526',
        'https://tenor.com/view/come-hello-welcome-gif-25024386',
        'https://tenor.com/view/welcome-welcome-to-the-team-minions-gif-21749603',
        'https://tenor.com/view/baby-yoda-welcome-gif-22416975',
        'https://tenor.com/view/welcome-gif-24657148',
        'https://tenor.com/view/simpson-gif-25340727',
        'https://tenor.com/view/welcome-gif-26452760',
    ]
    
    await context.send(random.choice(choices));

@command_handler.Command(AccessType.PUBLIC, desc = "Displays a top-10 leaderboard of the Neighbors with the most XP, or other leaderboards with an argument.", generic = True)
async def leaderboard(activator: Neighbor, context: Context):
    
    configure = None if not len(context.args) > 1 else context.args[1];
    
    if configure == "families":
        family_info = {
            "butterflies": 0,
            "cheetahs": 0,
            "foxes": 0,
            "horses": 0,
            "puppies": 0};
        with open('families.txt', 'r') as fFams:
            lines = fFams.readlines();
            family_info["butterflies"] = lines[0];
            family_info["cheetahs"] = lines[1];
            family_info["foxes"] = lines[2];
            family_info["horses"] = lines[3];
            family_info["puppies"] = lines[4];
            
        res = "";
        for key, val in family_info.items():
            res += f"**{key}:** {val}"
        await context.send(res);
        return
    
    neighbors = Neighbor.read_all_neighbors();
    neighbors = sorted(neighbors, key=lambda x: (x.XP if not configure == "legacy" else x.legacyXP))[::-1];
    neighbors = [x for x in neighbors if (int(x.get_family()) == context.guild.id)]

    length = len(neighbors) if configure == "all" else (10 if (configure is None or not configure.isnumeric()) else int(configure));

    leaderboard_neighbors = [x for x in neighbors if (not context.guild.get_member(x.ID) is None and not context.guild.get_member(x.ID).bot)][:length];
    
    if configure is None:
        res = "**Official Discord Leaderboard!**\nThe following users are the top 10 members with the most xp.\n";
    elif configure == "all":
        res = "**Discord Leaderboard!**\nAll users in server listed in order of xp.\n";
    elif configure == "legacy":
        res = "**Legacy Discord Leaderboard!**\nIn an alternate universe, in which XP is never reset nor used to buy things in my rss...\nAka: Top 10 XP earners of all time:\n"
    else:
        res = "**Discord Leaderboard!**\nTop " + str(length) + " users in server listed in order of xp.\n";

    list = "";
    c = 1;
    i = 0;

    while c < length + 1 and i < len(neighbors):
        cur = context.guild.get_member(neighbors[i].ID);
        if not cur is None:
            name = cur.display_name;
            XP = neighbors[i].XP if not configure == "legacy" else neighbors[i].legacyXP
            if neighbors[i] in leaderboard_neighbors:
                list += f"{c}) **{name}** (XP: {XP})\n";
                c += 1;
            else:
                list += f"{c - 0.5}) *{name}* (XP: {XP})\n";
        i += 1;
        
    await context.send(res + list);
            
@command_handler.Command(AccessType.PUBLIC, desc = "Display's a Neighbor's profile.", generic = True)
async def profile(activator: Neighbor, context: Context):
    if len(context.args) > 1:
        try:
            target = await context.guild.fetch_member(int(parse_mention((context.args[1]))));
        except:
            candidates = [x.nick for x in context.guild.members if not x.nick is None];
            candidates.extend([x.name for x in context.guild.members if (x.nick is None) or (not x.nick == x.name)]);
            
            name = best_string_match(context.args[1], [str(x) for x in candidates]);
            # print(name);
            target = discord.utils.get(context.guild.members, display_name = name);
            target = target if not target is None else discord.utils.get(context.guild.members, name = name);
    else:
        target = None;
        
    target_member = context.author if target is None else target;
    target_neighbor = Neighbor(target_member.id, context.guild.id);
    
    target_neighbor.expire_items();
    
    pretty_profile = target_neighbor.get_item_of_name("Prettier Profile");
    
    nick = context.guild.get_member(target_member.id);
    XP = target_neighbor.get_XP();
        
    current_lvl = target_neighbor.get_level();
    next_lvl = current_lvl + 1;

    xp_toward_next_lvl = XP - Neighbor.get_XP_for_level(current_lvl);
    xp_for_next_lvl = Neighbor.get_XP_for_level(next_lvl) - Neighbor.get_XP_for_level(current_lvl);
    
    progress = xp_toward_next_lvl / xp_for_next_lvl;
    progress_bar = "\U000025FB" * int(progress * 10)
    progress_bar += "\U000025FC" * int(10 - len(progress_bar));
        
    if not context.guild.id == FF.guild:
        neighborhood = "";
        user_role_ids = [role.id for role in target_member.roles];
        if context.ID_bundle.main_nh in user_role_ids:
            neighborhood += " PR";
        if context.ID_bundle.baby_nh in user_role_ids:
            neighborhood += " BP"
        profile = f"**{target_member.display_name}**\n";  
        profile += f"**Level: {current_lvl}**\tXP: {XP}\n";
        profile += progress_bar + "\n";
        # if not neighborhood is None and not family is None:
        profile += f"NH: {neighborhood}\n"; 
        profile += "\nExpiring Soon:\n";
        inventory = target_neighbor.get_inventory(); 
        original_len = len(inventory);
        inventory = [x for x in inventory if x.expiration != -1]
        displayed = 0;
        if len(inventory) == 0:
            profile += "> None!\n";
        else:
            inventory.sort(key = lambda x : 10000000000 if x.expiration == -1 else x.expiration);
            for i, item in enumerate(inventory):
                displayed += 1;
                if i > 4:
                    break;
                profile += "> " + str(item) + "\n";
        if original_len > displayed:
            profile += "*Use `$inventory` to view full inventory*";
        await context.send(profile);
    elif pretty_profile is None:
        neighborhood = get_neighborhood_from_user(target_member);
        family = get_family_from_user(target_member).upper();
        profile = f"**{target_member.display_name}**\n";  
        profile += f"**Level: {current_lvl}**\tXP: {XP}\n";
        profile += progress_bar + "\n";
        # if not neighborhood is None and not family is None:
        profile += f"NH: {neighborhood}\n";
        profile += f"Family: {family}\n";
        # else:
        #     profile += "Guest\n";
        
        profile += "\nExpiring Soon:\n";
        inventory = target_neighbor.get_inventory(); 
        original_len = len(inventory);
        inventory = [x for x in inventory if x.expiration != -1]
        displayed = 0;
        if len(inventory) == 0:
            profile += "> None!\n";
        else:
            inventory.sort(key = lambda x : 10000000000 if x.expiration == -1 else x.expiration);
            for i, item in enumerate(inventory):
                displayed += 1;
                if i > 4:
                    break;
                profile += "> " + str(item) + "\n";
        if original_len > displayed:
            profile += "*Use `$inventory` to view full inventory*";
        await context.send(profile);
    else:
        neighborhood = get_neighborhood_from_user(target_member);
        family = get_family_from_user(target_member);
        embed = discord.Embed(title=f"**{nick}**", color=target_member.color)
        embed.add_field(name="XP", value=f"{XP}", inline=True)
        embed.add_field(name="Level", value=f"{current_lvl}", inline=True)
        embed.add_field(name="Progress", value=f"{progress_bar}", inline=False)

        if not neighborhood is None and not (family == 0 or family == "0"):
            embed.add_field(name="Neighborhood", value=f"{neighborhood}", inline=True)
            embed.add_field(name="Family", value=f"{family}", inline=True)
        else:
            embed.add_field(name="Status", value="Guest", inline=False)
        embed.set_thumbnail(url=target_member.display_avatar.url)
        embed.set_footer(text = "Prettier Profile");
        target = await context.channel.send(embed = embed);
        
@command_handler.Command(AccessType.PUBLIC, desc = "Profile that shows all inventory items.", generic = True)
async def inventory(activator: Neighbor, context: Context):
    if len(context.args) > 1:
        try:
            target = await context.guild.fetch_member(int(parse_mention((context.args[1]))));
        except:
            candidates = [x.nick for x in context.guild.members if not x.nick is None];
            candidates.extend([x.name for x in context.guild.members if (x.nick is None) or (not x.nick == x.name)]);
            
            name = best_string_match(context.args[1], [str(x) for x in candidates]);
            # print(name);
            target = discord.utils.get(context.guild.members, display_name = name);
            target = target if not target is None else discord.utils.get(context.guild.members, name = name);
    else:
        target = None;
        
    target_member = context.author if target is None else target;
    target_neighbor = Neighbor(target_member.id, context.guild.id);
    
    target_neighbor.expire_items();
    
    pretty_profile = target_neighbor.get_item_of_name("Prettier Profile");
        
    profile = "\nFull Inventory:\n";
    inventory =  target_neighbor.get_inventory(); 
    if len(inventory) == 0:
        profile += "> Empty!";
    else:
        inventory.sort(key = lambda x : 10000000000 if x.expiration == -1 else x.expiration);
        for item in inventory:
            profile += "> " + str(item) + "\n";
    
    await context.send(profile);
        
@command_handler.Command(AccessType.PUBLIC, desc = "Displays how much server XP it takes to achieve a level.", generic = True)
async def level(activator: Neighbor, context: Context):
    if len(context.args) > 1:
        if not context.args[1].isnumeric() or int(context.args[1]) < 1 or int(context.args[1]) > 999999:
            raise CommandArgsError("When passed with an argument, `level` expects a number between 1 and 999999.")
        level = int(context.args[1]);
        await context.send(f"It takes **{Neighbor.get_XP_for_level(level)}xp** to reach level {level}");
    else:
        await context.send(f"You need **{activator.get_XP_for_next_level()}xp** to reach your next level");

@command_handler.Command(AccessType.PRIVILEGED, desc = "", generic = True)
async def invis(activator: Neighbor, context: Context):
    role = context.guild.get_role(1084644944431554570);
    new_color = discord.Colour(int('36393f', 16));
    await role.edit(color = new_color)
    1084644944431554570

@command_handler.Command(AccessType.PUBLIC, desc = "Calculates the BEM penalty for a neighbor of a certain level and number of missed tasks. For example, `$penalty 50 5` calculates the BEMs required of a level 50 player who misses 5 tasks.")
async def penalty(activator: Neighbor, context: Context):
    try:
        level = int(context.args[1]);
        tasks_missed = int(context.args[2]);
    except:
        raise CommandArgsError("`penalty` expects two arguments: player level and # of tasks missed");

    penalty_per_task = int(level / 10);

    total_penalty = penalty_per_task * tasks_missed;
    penalty = min(total_penalty, int(level / 2));
    power_derby_penalty = min(real_round(total_penalty / 2), int(level / 2))

    await context.send(f"A level {level} player who misses {tasks_missed} tasks owes **{penalty} BEMs** in normal derby!!", reply = True)
    await context.send(f"However, this player would only owe *{power_derby_penalty}* during a power derby.")
    await context.send(f"||During code gold, they owe {penalty * 2} BEMs during non-power derbies, and {power_derby_penalty * 2} during power derby. Please check with a council member or the announcements channel to see if this week is a code gold week.||");
    
def real_round(x):
    decimal = x - int(x);
    if decimal >= .5:
        return int(x) + 1;
    else:
        return int(x);


#  Note to self: fix best_this_month: Actually update special offer count & check before showing category

@command_handler.Command(AccessType.PRIVATE, desc = "Allows Neighbors to purchase discord perks like special roles using server XP", generic = True)
async def rss(activator: Neighbor, context: Context, response: ResponsePackage = None):
    
    current_date = datetime.date.today();
    target_date = datetime.date(current_date.year, 10, 2);
    
    if current_date >= target_date:
        with open('new_rss.json') as fRSS:
            rss_info = json.load(fRSS)
    else:
        with open('rss.json') as fRSS:
            rss_info = json.load(fRSS)
        
    if activator.get_level() < 3:
        await context.send("Whoops! You're too poor to access my RSS. Try again at level 3!");
        return;
        
    best_this_month = activator.get_item_of_name("Best Level This Month");
        
    if not response or response.name == "main":
        res = "**Welcome to Greg's Roadside Shop!**\n";
        res += "Here, you can buy an assortment of items with your server xp levels.\n"
        res += "Below are the several categories of items I offer. React with the emoji that corresponds to the one you would like to open.\n\n";

        locked = False;
        category_emojis = []
        for category in rss_info:
            if category["name"] == "Special Offers":
                if activator.get_level() > 5 or activator.get_level() < 5:
                    continue;
            if category["name"] == "Icons":
                if context.guild.id != FF.guild:
                    continue;
            if int(best_this_month.get_value("level")) < category['unlock']:
                res += f"> {unicodes[category['emoji']]} *Unlocks at level {category['unlock']}* {unicodes['locked']}\n";
                locked = True;
            else:
                res += f"> {unicodes[category['emoji']]} {category['name']}\n";
                category_emojis.append(unicodes[category['emoji']]);
        if locked:
            res += "\n" + unicodes['unlocked'] + "*To unlock a category, you must attain a certain level. Once you unlock a category, it will be available until the next __reckoning__.*";
        
        if response is None:
            target = await context.send(res);
            target_context = Context(target);
        else:
            target_context = response.response_context;
            target = target_context.message;
            await target.clear_reactions();
            await target.edit(content = res);
            
        def key(context):
            if not context.message.id == target.id:
                return False;
            if not context.user.id == activator.ID:
                return False;
            if not context.emoji.name in category_emojis:
                return False;
            return True;
        ResponseRequest(rss, "category", "REACTION", context, target_context, key)
        
        for emoji in category_emojis:
            await target.add_reaction(emoji);
    
    elif response.name == "category" or response.name == "re-category":
        activation_context = response.activation_context;
        target_context = response.response_context;
        target = target_context.message;
        await target.clear_reactions();
        
        if response.name == "category":
            chosen_category = None;           
            for category in rss_info:
                print(unicodes[category['emoji']]);
                if response.content.name == unicodes[category['emoji']]:
                    chosen_category = category;
        else:
            chosen_category = response.values["category"];
                
        item_emojis = [];
        res = f"**Greg's Roadside Shop: {chosen_category['name']}**\n";
        res += chosen_category['description'] + "\n\n";
        for item in chosen_category['items']:
            #check if correct server
            if item["name"] == "*Family Logo Tag* -- Best Seller":
                if context.guild.id != FF.guild:
                    continue;
            if item["name"] == "Phoenix Merch":
                if context.guild.id != PHOENIX.guild:
                    continue;
            item_emojis.append(unicodes[item['emoji']]);
            res += f"> {unicodes[item['emoji']]} {item['name']}\n";
        res += f"*You are viewing category: {chosen_category['name']}. React with {unicodes['back']} to select a different category*";

        await target.edit(content = res);

        item_emojis.append(unicodes['back'])
        def key(context):
            if not context.user.id == activator.ID:
                return False;
            if not context.emoji.name in item_emojis:
                return False;
            if not context.message.id == target.id:
                return False;
            return True;
        ResponseRequest(rss, "item", "REACTION", context, target_context, key, category = chosen_category)
        
        for emoji in item_emojis:
            await target.add_reaction(emoji);
        
    elif response.name == "item":
        
        activation_context = response.activation_context;
        target_context = response.response_context;
        target = target_context.message;
        await target.clear_reactions();
        chosen_category = response.values["category"];
        chosen_item = None;
        
        for item in chosen_category['items']:
            if response.content.name == unicodes[item['emoji']]:
                chosen_item = item;
                break;
        else:
            response.name = "main";
            await rss(activator, context, response);
            return;

        res = f"**{chosen_item['name']}**\n";
        res += f"{chosen_item['description']}\n"
        bank = False;
        if 'warning' in chosen_item:
            res += f"> Warning: {chosen_item['warning']}\n"
        if 'cost' in chosen_item:
            cost = int(chosen_item['cost']);
            if activator.get_level() >= cost:
                xp_conversion = Neighbor.get_XP_for_level(activator.get_level()) - Neighbor.get_XP_for_level(activator.get_level() - cost);
                res += f"> Cost: {cost} levels [xp conversion ≈ {xp_conversion}xp]\n";
            else:
                res += f"> Cost: {cost} levels [xp conversion ≈ {Neighbor.get_XP_for_level(cost)}]\n";
            if activator.get_item_of_name("GregBanking(TM)"):
                res += f"> Bank xp cost: " + str(int(Neighbor.get_XP_for_level(int(chosen_item['cost'])) * 1.25)) + "xp\n"
                bank = True;
        else:
            if chosen_item['name'] == "Highest Bidder":
                with open("data/trex_cost.txt", "r") as fRex:
                    cost = int(fRex.readline());
                    label = cost
                    res += f"> Cost: {cost} levels\n"
            else:
                res += f"> Cost: **{int(chosen_item['min_cost'])}-{int(chosen_item['max_cost'])}**\n"
        res += f"> Lasts: {chosen_item['duration_label']}\n"
        res += f"*React with {unicodes['check']} to confirm purchase*";
        confirmation_emojis = [];
        confirmation_emojis.append(unicodes['check']);
        if bank:
            res += f"\n*React with {unicodes['bank']} to purchase this item with xp in your GregBanking account.*"
            confirmation_emojis.append(unicodes['bank'])
        confirmation_emojis.append(unicodes['back']);
        
        await target.edit(content = res);
        
        def key(context):
            if not context.user.id == activator.ID:
                return False;
            if not context.emoji.name in confirmation_emojis:
                return False;
            if not context.message.id == target.id:
                return False;
            return True;
        ResponseRequest(rss, "confirmation", "REACTION", context, target_context, key, category = chosen_category, item = chosen_item)
        
        await target.add_reaction(unicodes['check']);
        if activator.get_item_of_name("GregBanking(TM)"):
            await target.add_reaction(unicodes['bank']);
        await target.add_reaction(unicodes['back']);
        
    elif response.name == "confirmation":
        activation_context = response.activation_context;
        target_context = response.response_context;
        target = target_context.message;
        chosen_category = response.values["category"];
        chosen_item = response.values["item"];
        
        cost = int(chosen_item["cost"])
        xp_cost = int(Neighbor.get_XP_for_level(int(chosen_item['cost'])) * 1.25);
        if response.content.name == unicodes['check']:
            if not activator.get_level() >= int(chosen_item["cost"]):
                await context.send("Whoops! You're too poor for this item.")
                ResponseRequest(rss, "confirmation", "REACTION", context, target_context, response.key, category = chosen_category, item = chosen_item)
                return;
            else:
                if not activator.get_item_of_name(chosen_item["name"]):
                    strip(activator, levels = cost);
                else:
                    await context.send("You already have this item!");
                    return;
        elif response.content.name == unicodes['bank']:
            bank_item = activator.get_item_of_name("GregBanking(TM)")
            if not int(bank_item.get_value("xp")) >= xp_cost:
                await context.send("Whoops! You're too poor for this item.")
                ResponseRequest(rss, "confirmation", "REACTION", context, target_context, response.key, category = chosen_category, item = chosen_item)
                return;
            else:
                if not activator.get_item_of_name(chosen_item):
                    xp = int(bank_item.get_value("xp"));
                    xp -= xp_cost;
                    bank_item.update_value("xp", xp);
                    activator.update_item(bank_item);
                else:
                    await context.send("You already have this item!");
                    return;
        elif response.content.name == unicodes['back']:
            response.name = "re-category";
            response.content = unicodes[chosen_category['emoji']]
            await rss(activator, context, response);
            return;
        
        if 'duration' in chosen_item:
            duration = int(time.time()) + int(chosen_item['duration']);
        else:
            duration = -1;
            
        item = chosen_item;
            
        match item['type']:
            case "passive":
                give = Item(item['name'], item['type'], duration, needs = Neighbor.get_XP_for_level(cost + 2), so_far = 0);
            case "bank":
                give = Item(item['name'], item['type'], duration, opened = int(time.time()), xp = 10000, interest = 0);
            case "tag":
                give = Item(item['name'], item['type'], duration, val = datetime.datetime.now().month - 1)
            case _:
                give = Item(item['name'], item['type'], duration);
                
        if 'special_offer' in chosen_item:
            best_this_month = activator.get_item_of_name("Best Level This Month");
            free_count_so_far = int(best_this_month.get_value("free_count"));
            best_this_month.update_value("free_count", free_count_so_far + 1); 
            activator.update_item(best_this_month);
                
        await context.send(f"Congrats! Your new item: {item['name']} has been applied!");
        await context.send(f"Your new level: {activator.get_level()}");
        activator.bestow_item(give);
        user = await context.guild.fetch_member(activator.ID);
        await set_nick(user, context.guild);
        await set_roles(user, context.guild);

                 
@command_handler.Command(AccessType.PRIVATE, desc = "Turn off Greg pings with `$pings off` or back on with `$pings on`", generic = True)
async def pings(activator: Neighbor, context: Context, choice = None):
    if len(context.args) < 2:
        raise CommandArgsError("`$pings` expects one argument: `on` or `off`");
    match context.args[1].lower():
        case "on":
            ping_item = activator.get_item_of_name("Pings Off");
            activator.vacate_item(ping_item);
            await context.send("Pings... back on!")
        case "off":
            ping_item = activator.get_item_of_name("Pings Off");
            if ping_item:
                await context.send("Already have pings off!");
                return;
            else:
                ping_item = Item("Pings Off", "pings", -1);
                activator.bestow_item(ping_item);
                await context.send("Pings have been turned off! You should only recieve a ping from greg at the very end of each month and when you open a Greg ticket. If you get any other pings, contact Lincoln or use $report.\n\nUse `$pings on` to get pings back");
                return;
        case _:
            raise CommandArgsError("`$pings` expects one argument: `on` or `off`");

@command_handler.Command(AccessType.PUBLIC, desc = "Send a meme!", generic = True)
async def meme(activator: Neighbor, context: Context):
    image_directory = './memes'  # change this to the directory containing your images
    image_list = os.listdir(image_directory)
    random_image = random.choice(image_list)
    image_path = os.path.join(image_directory, random_image)

    with open(image_path, 'rb') as f:
        picture = discord.File(f)
        await context.send(file=picture, reply = True);
    
@command_handler.Command(AccessType.PRIVATE, desc = "Lets a Neighbor harvest crops.", generic = True)
async def harvest(activator: Neighbor, context: Context, response: ResponsePackage = None):

    if response is None:
        if random.choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 1]):
            await context.send("Did you know? Try `$sell` to sell the entire contents of your silo! Or wait for the farmers market channel to appear for potentially much higher returns.", reply = True);

        activator.expire_items();
        
        GMO_item = activator.get_item_of_name("GMO Crops");
        
        if activator.get_item_of_name("Harvest Cooldown") and not activator.get_item_of_name("HarvestNow(TM) Fertilizer"):

            await context.send(f"Whoops! You've already harvested in the past hour. Crops don't grow overnight you know! Well...");
            return;
        elif activator.get_item_of_name("Harvest Cooldown") and activator.get_item_of_name("HarvestNow(TM) Fertilizer"):
            await context.send("Your HarvestNow(TM) Fertilizer is being used now.")
            harvest_block_item = activator.get_item_of_name("Harvest Cooldown");
            fertilizer_item = activator.get_item_of_name("HarvestNow(TM) Fertilizer");
            activator.vacate_item(harvest_block_item);
            activator.vacate_item(fertilizer_item);
            activator.bestow_item(Item("HarvestNowBlock", "block", time.time() + 3600));
        cur = time.time();
        # print(activator.get_inventory());
        new_bock = Item("Harvest Cooldown", "harvest", (cur + 3600));
        activator.bestow_item(new_bock);
        # print(activator.get_inventory());

        silo_item = activator.get_item_of_name("Silo");
        if silo_item is None:
            current_silo = {name: 0 for name, val in crops.items()};
            temp = Item("Silo", "silo", -1, **current_silo);
            activator.bestow_item(temp);
            
        else:
            old_silo = {name: int(val) for name, val in silo_item.values.items()}
            old_values = list(old_silo.values());
            
            current_silo = {name: 0 for name, val in crops.items()};
            for i, key in enumerate(current_silo.keys()):
                if i < len(old_values):
                    current_silo[key] = old_values[i]
            
        
        list_crops = list(crops.items());
        list_with_probabilities = [];
        for crop in list_crops:
            for i in range(int((50 - crop[1]) ** 1.5)):
                list_with_probabilities.append(crop);
        
        to_harvest, xp_per_harvest = random.choice(list_with_probabilities);

        amt_to_harvest = random.randint(1, 100);
        
        if GMO_item:
            amt_to_harvest *= 2;
            if amt_to_harvest > 100: 
                amt_to_harvest -= random.randint(0,100);
        
        current_silo[to_harvest] += amt_to_harvest;
        
                
        new_silo_item = Item("Silo", "silo", -1, **current_silo);
        activator.update_item(new_silo_item)
                
        res = f"Wohoo! You harvested {amt_to_harvest} {to_harvest}"
        target = await context.send(res);
        
        random_key = random.choice(list(crop_emojis.keys()))
        random_value = crop_emojis[random_key];
        await target.add_reaction(random_value);
        if to_harvest == random_key:
            def key(ctx):
                if not ctx.message.id == target.id:
                    return False;
                if not ctx.emoji.name == random_value:
                    return False;
                return True;
            ResponseRequest(harvest, "crop", "REACTION", context, Context(target), key);
        await harvest_xp(context);
    else:
        await context.send("It's a perfect match! Enjoy 1000xp as your reward.");
        await inc_xp(activator, 1000, context);
        
    
async def wordle_easy(activator: Neighbor, context: Context, response: ResponsePackage = None):
    with open("words.txt", "r") as fWords:
        words = [line.strip() for line in fWords.readlines()]
    with open("answers.txt", "r") as fAnswers:
        answers = [line.strip() for line in fAnswers.readlines()]
    answers = answers[0:1499]
    
    if response is None:
        res = "**Welcome to Greg's ";
        res += green_wordle_emojis[22] + yellow_wordle_emojis[14] + green_wordle_emojis[17] + green_wordle_emojis[3] + red_wordle_emojis[11] + green_wordle_emojis[4];
        res += "!**\n\nI have already selected a word! Guess valid 5-letter words in this channel and I will give clues toward the answer. If you write a message that is not a valid 5 letter word in my dictionary, I will just ignore it. You have two minutes to make each guess.\n\n**Scoring:** Tom will also play alongside you and I will reveal his guesses once you have successfully guessed the word. You will get XP based on how many guesses it takes you to get the word. If you get the word in fewer guesses than Tom, you will get double XP! Let's begin, guess your first word!\n\n**Note:** Different forms of words are fair game. For example, plural words may be chosen as the Wordle and may be guessed.";
        target = await context.send(res, reply = True);
        response_context = Context(message = target)
        answer = random.choice(answers);
        # await context.send(answer);
        def key(context):
            if not context.content.lower() in words:
                return False;
            return True;
        ResponseRequest(wordle_easy, "guess", "MESSAGE", context, response_context, answer = answer, key = key, guesses = [])
    else:
        guess_list = response.values["guesses"];
        answer = response.values["answer"];
        candidate = response.content.lower();
        guess_list.append(candidate);
        response = wordle_helper.get_response(answer, candidate);
        if len(guess_list) == 1:
            await context.send("Red: This letter is not in the word.\nYellow: This letter is in the word in a different position (careful, this is slightly different from NYT Wordle mechanics)\nGreen: This letter is in the word in this position\nPurple: Easy Mode Only, This letter is in the word in this position AND another position")
        if not "0" in response and not "1" in response:
            # correct!
            res = "**You got it!!**\n\n";
            for guess in guess_list[-9:]:
                response = wordle_helper.get_response(answer, guess);
                for i, char in enumerate(guess):
                    if response[i] == "0":
                        res += red_wordle_emojis[ord(char) - 97];
                    elif response[i] == "1":
                        res += yellow_wordle_emojis[ord(char) - 97];
                    elif response[i] == "2":
                        res += green_wordle_emojis[ord(char) - 97];
                    elif response[i] == "3":
                        res += purple_wordle_emojis[ord(char) - 97];
                res += "\n";
            target = await context.send(res);
            
            res = "**Let's see how Tom did!**\n\n";
            word_info = wordle_helper.WordInfo();
            tom_guesses = [];
            while not word_info.is_word_complete():
                possible = word_info.cleanse(words);
                if len(possible) == 0 or len(tom_guesses) > 15:
                    await context.send("Uh oh! Something has gone wrong on my end.");
                    return
                sorted = wordle_helper.sort_by_letter_frequency(possible);
                difficulty = int(len(possible) / 2);
                if difficulty == 0:
                    difficulty += 1;
                if len(sorted) > difficulty:
                    next_guess = random.choice(sorted[:difficulty]);
                else:
                    next_guess = random.choice(sorted);
                tom_guesses.append(next_guess);
                response = wordle_helper.get_response(answer, next_guess);
                word_info.register_guess(next_guess, response)
                for i, char in enumerate(next_guess):
                    if response[i] == "0":
                        res += red_wordle_emojis[ord(char) - 97];
                    elif response[i] == "1":
                        res += yellow_wordle_emojis[ord(char) - 97];
                    elif response[i] == "2":
                        res += green_wordle_emojis[ord(char) - 97];
                    elif response[i] == "3":
                        res += purple_wordle_emojis[ord(char) - 97];
                res += "\n";
            await context.send(res);
            num_guesses = len(guess_list);
            num_tom_guesses = len(tom_guesses);
            if num_guesses < 9:
                xp = 25 * (9 - len(guess_list));
                if len(guess_list) < len(tom_guesses):
                    await context.send(f"Wow! You beat tom by {len(tom_guesses) - len(guess_list)} guesses!\n\nYou get {xp}xp for getting the word in {len(guess_list)}, doubled for beating Tom! {xp * 2}xp total!");
                    xp *= 2;
                else:
                    await context.send(f"Unfortunately you did not beat tom!!\n\nHowever, you get {xp}xp for getting the word in {len(guess_list)}!");
                await inc_xp(activator, xp, context);
            else:
                await context.send(f"Unfortunately, {len(guess_list)} guesses is too many to earn XP! Good job getting the Wordle though, better luck next time!");
        else:
            res = "";
            for guess in guess_list[-9:]:
                response = wordle_helper.get_response(answer, guess);
                for i, char in enumerate(guess):
                    if response[i] == "0":
                        res += red_wordle_emojis[ord(char) - 97];
                    elif response[i] == "1":
                        res += yellow_wordle_emojis[ord(char) - 97];
                    elif response[i] == "2":
                        res += green_wordle_emojis[ord(char) - 97];
                    elif response[i] == "3":
                        res += purple_wordle_emojis[ord(char) - 97];
                res += "\n";
            target = await context.send(res);
            response_context = Context(message = target);
            def key(context):
                if not context.content.lower() in words:
                    return False;
                return True;
            ResponseRequest(wordle_easy, "guess", "MESSAGE", context, response_context, answer = answer, key = key, guesses = guess_list)


async def wordle_hard(activator: Neighbor, context: Context, response: ResponsePackage = None):
    with open("words.txt", "r") as fWords:
        words = [line.strip() for line in fWords.readlines()]
    with open("answers.txt", "r") as fAnswers:
        answers = [line.strip() for line in fAnswers.readlines()]
    answers = answers[0:3499]
    
    if response is None:
        res = "**Welcome to Greg's ";
        res += green_wordle_emojis[22] + yellow_wordle_emojis[14] + green_wordle_emojis[17] + green_wordle_emojis[3] + red_wordle_emojis[11] + green_wordle_emojis[4];
        res += " HARD MODE!**\n\nYou know the drill! Hard mode wordle works the same as regular mode with a few changes. Firstly, there are 1500 more possible Wordles. Secondly, you play against Rose instead of Tom, who is better at guessing. Thirdly, more XP is available to be won but you must get the word in 6 guesses or less instead of 8 to earn any. Finally, no purple letters will be shown.\n\n**Scoring:** Rose will also play alongside you and I will reveal her guesses once you have successfully guessed the word. You will get XP based on how many guesses it takes you to get the word. If you get the word in fewer guesses than Rose, you will get double XP! Let's begin, guess your first word!\n\n**Note:** Different forms of words are fair game. For example, plural words may be chosen as the Wordle and may be guessed.";
        target = await context.send(res, reply = True);
        response_context = Context(message = target)
        answer = random.choice(answers);
        # answer = "dived"
        # await context.send(answer);
        def key(context):
            if not context.content.lower() in words:
                return False;
            return True;
        ResponseRequest(wordle_hard, "guess", "MESSAGE", context, response_context, answer = answer, key = key, guesses = [])
    else:
        guess_list = response.values["guesses"];
        answer = response.values["answer"];
        candidate = response.content.lower();
        guess_list.append(candidate);
        response = wordle_helper.get_response(answer, candidate);
        if len(guess_list) == 1:
            await context.send("Red: This letter is not in the word.\nYellow: This letter is in the word in a different position (careful, this is slightly different from NYT Wordle mechanics)\nGreen: This letter is in the word in this position\n~~Purple: Easy Mode Only, This letter is in the word in this position AND another position~~")
        if not "0" in response and not "1" in response:
            # correct!
            res = "**You got it!!**\n\n";
            for guess in guess_list[-9:]:
                response = wordle_helper.get_response(answer, guess);
                for i, char in enumerate(guess):
                    if response[i] == "0":
                        res += red_wordle_emojis[ord(char) - 97];
                    elif response[i] == "1":
                        res += yellow_wordle_emojis[ord(char) - 97];
                    elif response[i] == "2" or response[i] == "3":
                        res += green_wordle_emojis[ord(char) - 97];
                res += "\n";
            target = await context.send(res);
            
            res = "**Let's see how Rose did!**\n\n";
            word_info = wordle_helper.WordInfo();
            tom_guesses = [];
            choices = [i + 1 for i in range(5)];
            difficulty = random.choice(choices)
            while not word_info.is_word_complete():
                possible = word_info.cleanse(words);
                if len(possible) == 0 or len(tom_guesses) > 15:
                    await context.send("Uh oh! Something has gone wrong on my end.");
                    return
                sorted = wordle_helper.sort_by_letter_frequency(possible);
                if len(sorted) > difficulty:
                    next_guess = random.choice(sorted[:difficulty]);
                else:
                    next_guess = random.choice(sorted);
                tom_guesses.append(next_guess);
                response = wordle_helper.get_response(answer, next_guess);
                word_info.register_guess(next_guess, response)
                for i, char in enumerate(next_guess):
                    if response[i] == "0":
                        res += red_wordle_emojis[ord(char) - 97];
                    elif response[i] == "1":
                        res += yellow_wordle_emojis[ord(char) - 97];
                    elif response[i] == "2" or response[i] == "3":
                        res += green_wordle_emojis[ord(char) - 97];
                res += "\n";
            await context.send(res);
            num_guesses = len(guess_list);
            num_tom_guesses = len(tom_guesses);
            if num_guesses < 7:
                xp = 85 * (7 - len(guess_list));
                if len(guess_list) < len(tom_guesses):
                    await context.send(f"Wow! You beat Rose by {len(tom_guesses) - len(guess_list)} guesses!\n\nYou get {xp}xp for getting the word in {len(guess_list)}, doubled for beating Rose! {xp * 2}xp total!");
                    xp *= 2;
                else:
                    await context.send(f"Unfortunately you did not beat Rose!!\n\nHowever, you get {xp}xp for getting the word in {len(guess_list)}!");
                await inc_xp(activator, xp, context);
            else:
                await context.send(f"Unfortunately, {len(guess_list)} guesses is too many to earn XP! Good job getting the Wordle though, better luck next time!");
        else:
            res = "";
            for guess in guess_list[-9:]:
                response = wordle_helper.get_response(answer, guess);
                for i, char in enumerate(guess):
                    if response[i] == "0":
                        res += red_wordle_emojis[ord(char) - 97];
                    elif response[i] == "1":
                        res += yellow_wordle_emojis[ord(char) - 97];
                    elif response[i] == "2":
                        res += green_wordle_emojis[ord(char) - 97];
                    elif response[i] == "2" or response[i] == "3":
                        res += green_wordle_emojis[ord(char) - 97];
                res += "\n";
            target = await context.send(res);
            response_context = Context(message = target);
            def key(context):
                if not context.content.lower() in words:
                    return False;
                return True;
            ResponseRequest(wordle_hard, "guess", "MESSAGE", context, response_context, key = key, answer = answer, guesses = guess_list)

@command_handler.Command(AccessType.PRIVATE, desc = "Play Wordle!", generic=True)
async def wordle(activator: Neighbor, context: Context, answer = None, guesses = None):
    
    with open("words.txt", "r") as fWords:
        words = [line.strip() for line in fWords.readlines()]
    
    with open("answers.txt", "r") as fWords:
        answers = [line.strip() for line in fWords.readlines()]
    answers = answers[0:99]
    
    if guesses is None:
        if not activator.get_item_of_name("Greg Wordle Minigame") and not activator.get_item_of_name("Wordle 2 (Hard Mode)"):
            await context.send("Whoops! Looks like you haven't purchased the Wordle minigame from my rss yet!\n\nPlay with someone else or buy it for yourself by calling $rss. #sorrynotsorry");
            return;
        if activator.get_item_of_name("Wordle 2 (Hard Mode)"):
            await wordle_hard(activator, context);
            return;
        else:
            await wordle_easy(activator, context);
            return;
        res = "**Welcome to Greg's ";
        res += green_wordle_emojis[22] + yellow_wordle_emojis[14] + green_wordle_emojis[17] + green_wordle_emojis[3] + red_wordle_emojis[11] + green_wordle_emojis[4];
        res += "!**\n\nI have already selected a word! Guess valid 5-letter words in this channel and I will give clues toward the answer. If you write a message that is not a valid 5 letter word in my dictionary, I will just ignore it. You have two minutes to make each guess.\n\n**Scoring:** Tom will also play alongside you and I will reveal his guesses once you have successfully guessed the word. You will get XP based on how many guesses it takes you to get the word. If you get the word in fewer guesses than Tom, you will get double XP! Let's begin, guess your first word!\n\n**Note:** Different forms of words are fair game. For example, plural words may be chosen as the Wordle and may be guessed.";
        target = await context.send(res, reply = True);
        response_context = Context(message = target)
        answer = random.choice(answers);
        # answer = "dived"
        # await context.send(answer);
        active_expectations.append(Expectation("wordle", "MESSAGE", int(time.time() + 300), wordle, fulfills="guesses",activation_context=context,response_context=response_context, answer = answer, guesses = []));
    else:
        candidate = guesses[0].lower();
        if not candidate in words:
            return
        answer = guesses[1].values["answer"];
        guess_list = guesses[1].values["guesses"];
        guesses[1].meet()
        guess_list.append(candidate);
        response = wordle_helper.get_response(answer, candidate);
        if response == "22222":
            # correct!
            res = "**You got it!!**\n\n";
            for guess in guess_list:
                response = wordle_helper.get_response(answer, guess);
                for i, char in enumerate(guess):
                    if response[i] == "0":
                        res += red_wordle_emojis[ord(char) - 97];
                    elif response[i] == "1":
                        res += yellow_wordle_emojis[ord(char) - 97];
                    elif response[i] == "2":
                        res += green_wordle_emojis[ord(char) - 97];
                res += "\n";
            target = await context.send(res);
            
            res = "**Let's see how Tom did!**\n\n";
            word_info = wordle_helper.WordInfo();
            tom_guesses = [];
            choices = [i + 1 for i in range(20)];
            difficulty = random.choice(choices)
            while not word_info.is_word_complete():
                possible = word_info.cleanse(words);
                if len(possible) == 0 or len(tom_guesses) > 15:
                    await context.send("Uh oh! Something has gone wrong on my end.");
                    return
                sorted = wordle_helper.sort_by_letter_frequency(possible);
                if len(sorted) > difficulty:
                    next_guess = random.choice(sorted[:difficulty]);
                else:
                    next_guess = random.choice(sorted);
                tom_guesses.append(next_guess);
                response = wordle_helper.get_response(answer, next_guess);
                word_info.register_guess(next_guess, response)
                for i, char in enumerate(next_guess):
                    if response[i] == "0":
                        res += red_wordle_emojis[ord(char) - 97];
                    elif response[i] == "1":
                        res += yellow_wordle_emojis[ord(char) - 97];
                    elif response[i] == "2":
                        res += green_wordle_emojis[ord(char) - 97];
                res += "\n";
            await context.send(res);
            if len(guess_list) < 8:
                xp = 50 * (7 - len(guess_list));
                if len(guess_list) < len(tom_guesses):
                    await context.send(f"Wow! You beat tom by {len(tom_guesses) - len(guess_list)} guesses!\n\nYou get {xp}xp for getting the word in {len(guess_list)}, doubled for beating Tom! {xp * 2}xp total!");
                    xp *= 2;
                else:
                    await context.send(f"Unfortunately you did not beat tom!!\n\nHowever, you get {xp}xp for getting the word in {len(guess_list)}!");
                await inc_xp(activator, xp, context);
            else:
                await context.send(f"Unfortunately, {len(guess_list)} guesses is too many to earn XP! Good job getting the Wordle though, better luck next time!");
        else:
            res = "";
            for guess in guess_list:
                response = wordle_helper.get_response(answer, guess);
                for i, char in enumerate(guess):
                    if response[i] == "0":
                        res += red_wordle_emojis[ord(char) - 97];
                    elif response[i] == "1":
                        res += yellow_wordle_emojis[ord(char) - 97];
                    elif response[i] == "2":
                        res += green_wordle_emojis[ord(char) - 97];
                res += "\n";
            target = await context.send(res);
            response_context = Context(message = target);
            active_expectations.append(Expectation("wordle", "MESSAGE", int(time.time() + 300), wordle, fulfills="guesses",activation_context=context,response_context=response_context, answer = answer, guesses = guess_list))
  
@command_handler.Command(AccessType.PRIVATE, desc = "Play hangman!", generic=True)
async def hangman(activator: Neighbor, context: Context, response: ResponsePackage = None):
    with open("hangman.txt", "r") as fAnswers:
        answers = [line.strip() for line in fAnswers.readlines()]
    
    if response is None:
        res = "**Welcome to Greg's Hangman!**\n\nGuess singular letters or words until you can confidently guess the phrase.\n\nYou can make 10 mistakes. Letters cost 1 mistake each, words cost 3. I have already chosen a phrase, you may begin guessing. Good luck!";
        answer = random.choice(answers).lower();
        target = await context.send(res);
        so_far = "";
        for ch in answer:
            if ch in "abcdefghijklmnopqrstuvwxyz":
                so_far += "_"
            else:
                so_far += ch;
        await context.send(f"`{so_far}`");
        words = answer.split(" ");
        lengths = [len(word) for word in words];
        lengths.append(1);
        print(answer);
        def key(c):
            return len(c.content) == 1 or len(c.content) == len(answer);
        ResponseRequest(hangman, "guess", "MESSAGE", context, Context(target), key, guessed = [], answer = answer, so_far = so_far, wrong  = 0);
    else:
        guessed = response.values["guessed"];
        answer = response.values["answer"];
        so_far = response.values["so_far"];
        wrong = response.values["wrong"];
        
        guess = response.content.lower();
        new = "";
        
        for ans_char, so_far_char in zip(answer, so_far):
            if ans_char == guess:
                new = new + guess;
            else:
                new = new + so_far_char;
                
        if guess == answer:
            await context.send(answer);
            return;
        if so_far == new:
            await context.send("Ouch! Not in the word.");
            await context.send(f"`{so_far}`");
            wrong += 1
            await context.send(f"Mistakes remaining: {wrong}")
        else:
            await context.send("Yes!");
            await context.send(f"`{new}`");
        
        guessed.append(guess);
        if wrong >= 10:
            await context.send("Sorry, no more guesses!");
            await context.send(answer);
            return;
        
        def key(c):
            return len(c.content) == 1;
        
        ResponseRequest(hangman, "guess", "MESSAGE", context, Context(target), key, guessed = guessed, answer = answer, so_far = new, wrong = wrong);
        
        
            
    
@command_handler.Command(AccessType.PRIVATE, desc = "Displays all crops a Neighbor has in their silo.", generic = True)
async def silo(activator: Neighbor, context: Context):
    
    if chance(10):
        await context.send("Did you know? Whoops, `$sell` doen't exist anymore my bad.", reply = True);
    
    silo_item = activator.get_item_of_name("Silo");
    res = "Your silo:\n";
    if silo_item is None:
        res += "Empty!";
    else:
        current_silo = silo_item.values;
        sorted_names = sorted(current_silo.keys())
        sorted_vals = [];
        for i in range(len(sorted_names)):
            sorted_vals.append(current_silo[sorted_names[i]]);
        for i in range(len(sorted_names)):
            name = sorted_names[i];
            val = sorted_vals[i];
            if not int(val) == 0:
                res += f"> {name}: {val}\n"; 
    target = await context.send(res);
    
    if activator.get_item_of_name("SiloGuard(TM) Level 2 Security"):
        await target.add_reaction("<:Strongman:1158159363828101232>");

@command_handler.Command(AccessType.PRIVATE, desc = "Sell your entire silo!", generic = True)
async def sell(activator: Neighbor, context: Context, response: ResponsePackage = None):
    silo_item = activator.get_item_of_name("Silo");
    if not silo_item:
        await context.send("You don't have a silo silly!");
        return;
    
    if response is None:
        rates = [0.63467546, 0.872456, 0.900124323, 0.9578765, 0.52332, 0.5111, 1.1344, 0.6333, 0.7555, 0.768794, 0.60987, 0.79023938, 0.510203, 0.9203904957, 0.77473, 0.891920, 0.5, 0.6230, 0.920, 1.10029, 0.7002235, 0.601234, 0.50123, 1.034, 0.91340, 0.65431, 0.6230, 0.71029, 0.9192, 0.712, 0.99999999999]
        rate = rates[datetime.datetime.now().day];
        current_silo = silo_item.values.items();
        total_value = 0;
        for crop, amt in current_silo:
            total_value += int(amt) * crops[crop]
        
        offer = int(rate * total_value);
        offer = int(.6666667 * offer);
            
        target = await context.send(f"Today, I would be willing to purchase your entire silo for {offer}xp. If you like this offer, react to accept. If you don't like this offer, check back another day!");
        
        def key(context):
            if not context.message.id == target.id:
                return False;
            if not context.user.id == activator.ID:
                return False;
            if not context.emoji.name == unicodes["check"]:
                return False;
            return True;
        ResponseRequest(sell, "confirmation", "REACTION", context, Context(target), key, offer = offer);
        
        await target.add_reaction(unicodes['check']);
    else:
        offer = response.values["offer"];
        await inc_xp(activator, offer, context);
        await context.send(f"It's done! Your silo is now empty and I have given you {offer}xp in exchange.");
        activator.vacate_item(silo_item);
    

@command_handler.Command(AccessType.PRIVATE, desc = "Automatically host a 24H giveaway & earn xp for doing so. Example: `$give 89 BEMs`\nIf you want to do a giveaway with more than one winner, write [#] somewhere in your message. Example: `$give [3] 89 BEMs` to have 3 winners.")
async def give(activator: Neighbor, context: Context):
    if len(context.args) < 2:
        raise CommandArgsError("`$give` needs to know what you want to give away! Try $help give");
    res = "__**New Giveaway**__\n"
    res += "\n> **" + " ".join(context.args[1:]) + "**";
    res += f"\n> Hosted generously by <@{activator.ID}>";
    match = re.search(r'\[(\d+)\]', context.content)
    if match:
        winners = int(match.group(1))
        res += "> Winners: " + winners;
    res += "\n<@827634110238556160> this giveaway ends in 24H!";
    res += "\nReact with <:giveaway:1067499350705582124> to enter!";
    
    gc = await context.guild.fetch_channel(context.ID_bundle.giveaway_channel);
    target = await gc.send(res);
    await target.add_reaction("<:giveaway:1067499350705582124>");
    with open("giveaways.txt", "a") as fGiveaways:
        fGiveaways.write(str(target.id) + " " + str((int(time.time()) + 86400)) + "\n");
    
@command_handler.Command(AccessType.PRIVATE, desc = "Open your bank profile, if you have a GregBanking(TM) savings account. Use `$info bank` to learn more.")
async def bank(activator: Neighbor, context: Context):
    bank_item = activator.get_item_of_name("GregBanking(TM)");
    if bank_item is None:
        await context.send("I'm sorry! You do not yet have a savings account open at GregBanking(TM). Please open an account using `$rss`.", reply = True);
    else:
        opened = int(bank_item.get_value("opened"));
        interest = int(bank_item.get_value("interest"));
        XP = int(bank_item.get_value("xp"));
        user = await context.guild.fetch_member(activator.ID);
        
        res = f"**{user.display_name}'s GregBanking(TM) Account**\n";
        res += f"Account open since {datetime.datetime.fromtimestamp(opened)}\n\n";
        res += f"Balance: {XP}xp\n";
        res += f"Interest rate: 5%\n";
        res += f"Interest accumulated so far: {interest}xp\n\n";
        res += f"Use `$deposit` to make a deposit\n";
        res += f"Use `$close_account` to close your account and withdraw the full balance.";
        
        target = await context.send(res);
        
@command_handler.Command(AccessType.PRIVATE, desc = "Deposit levels into your GregBanking(TM) savings account. Use `$info bank` to learn more.")
async def deposit(activator: Neighbor, context: Context):
    bank_item = activator.get_item_of_name("GregBanking(TM)");
    if bank_item is None:
        await context.send("I'm sorry! You do not yet have a savings account open at GregBanking(TM). Please open an account using `$rss`.", reply = True);
    else:
        if len(context.args) < 2:
            raise CommandArgsError("`$deposit` expects one argument: amount of xp to deposit");
        amount_to_deposit = int(context.args[1]);
        if amount_to_deposit < 1001:
            await context.send("Whoops! You can't deposit that few XP.");
        elif amount_to_deposit > activator.get_XP():
            await context.send("Whoops! You're too poor to deposit that much XP.");
        else:
            new_bank_item = bank_item; 
            new_bank_item.update_value("xp", str(int(bank_item.get_value("xp")) + int(amount_to_deposit) - 1000));
            activator.update_item(new_bank_item);
            strip(activator, xp = amount_to_deposit);
            await context.send(f"Done! {amount_to_deposit - 1000}xp was deposited into your account after fees were applied.")

# @command_handler.Command(AccessType.PRIVATE, desc = "Withdraw levels from your GregBanking(TM) savings account. Use `$info bank` to learn more.")
async def withdraw(activator: Neighbor, context: Context):
    bank_item = activator.get_item_of_name("GregBanking(TM)");
    if bank_item is None:
        await context.send("I'm sorry! You do not yet have a savings account open at GregBanking(TM). Please open an account using `$rss`.", reply = True);
    else:
        if len(context.args) < 2:
            raise CommandArgsError("`$deposit` expects one argument: amount of xp to deposit");
        amount_to_withdrawal = int(context.args[1]);
        if amount_to_withdrawal >= int(bank_item.get_value("xp")):
            await context.send("Whoops! You're too poor to withdraw that much XP! (If you are trying to withdraw all of your xp, use `$close_account`)");
        else:
            if len(context.args) < 2:
                raise CommandArgsError("`$deposit` expects one argument: amount of xp to deposit");
            new_bank_item = bank_item;
            new_bank_item.update_value("xp", str(int(bank_item.get_value("xp")) - int(amount_to_withdrawal)));
            activator.update_item(new_bank_item);
            await inc_xp(activator, int(amount_to_withdrawal * 0.75), context)
            await context.send(f"Done! {amount_to_withdrawal}xp has been withdrawn from your account. After taxes, {int(amount_to_withdrawal * 0.75)}xp was applied to your profile");

# @command_handler.Command(AccessType.PRIVATE, desc = "Close your GregBanking(TM) savings account, if you have one. Use `$info bank` to learn more.")
async def close_account(activator: Neighbor, context: Context):
    bank_item = activator.get_item_of_name("GregBanking(TM)");
    if bank_item is None:
        await context.send("I'm sorry! You do not yet have a savings account open at GregBanking(TM). Please open an account using `$rss`.", reply = True);
    else:
        XP = int(bank_item.get_value("xp"));
        activator.vacate_item(bank_item);
        await inc_xp(activator, int(XP * 0.75), context)
        await context.send(f"Done! {XP}xp has been withdrawn from your account. After taxes, {int(XP * 0.75)}xp was applied to your profile.");
        await context.send("Your GregBanking(TM) Savings Account has been successfully closed");

@command_handler.Command(AccessType.PRIVATE, desc = "Steal from another user, if you have Hire Alfred from the rss.")
async def steal(activator: Neighbor, context: Context):
    if not activator.get_item_of_name("Hire Alfred"):
        context.send("Whoops! You need to purchase Alfred's loyalty from my RSS. Use `$rss` to purchase.")
    else:
        if len(context.args) < 2:
            raise CommandArgsError("`$steal` expects one argument: @mention of user to steal from.");
        else: 
            id = context.args[1][2:-1];
            try:
                member = await context.guild.fetch_member(id);
            except:
                raise CommandArgsError("`$steal` expects one argument: @mention of user to steal from.")
            neighbor = Neighbor(id, context.guild.id);
            
            possibilities = [-.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02 -0.01, 0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1];
            choice = 2000 + 2000 * random.choice(possibilities);
            choice = choice if neighbor.XP >= choice else neighbor.XP;
            
            await inc_xp(activator, choice, context);
            neighbor.strip(xp=choice);
            await context.send(f"Alfred has stolen {choice} from <@{id}>");
            activator.vacate_item(activator.get_item_of_name("Hire Alfred"));
                
@command_handler.Command(AccessType.PRIVATE, desc = "Turn on or off your invisibility cloak, if you have one.")
async def cloak(activator: Neighbor, context: Context):
    cloak_item = activator.get_item_of_name("Invisibility Cloak");
    if cloak_item is None:
        await context.send("I'm sorry! You do not yet have an invisibility cloak. Use `$rss` to purchase one!", reply = True);
    else:
        if len(context.args) < 2 or not context.args[1] in ["on", "off"]:
            raise CommandArgsError("`$cloak` expects one argument: 'on' to put on cloak or 'off' to take off cloak");
        role = context.guild.get_role(FF.invisibility_role);
        user = await context.guild.fetch_member(activator.ID);
        if context.args[1] == "on":
            await user.add_roles(role)
        elif context.args[1] == "off":
            await user.remove_roles(role);

@command_handler.Command(AccessType.PRIVATE, desc = "Request a new feature. For example, `$request 10000xp for all neighbors` (don't actually say this).", generic = True)
async def request(activator: Neighbor, context: Context):
    if not len(context.args) > 1:
        raise CommandArgsError("You didn't request anything, silly!\nType `$request` followed by the feature you would like to request.");
    with open("data/requests.txt", "a") as fRequests:
        fRequests.write(context.author.display_name);
        fRequests.write(context.content[9:]);

@command_handler.Command(AccessType.PRIVATE, desc = "Report an issue. Please be detailed. For example, `$report When I bought the strawberry tag in the RSS, it said I don't have enough levels even though I do.`.", generic = True)
async def report(activator: Neighbor, context: Context):
    if not len(context.args) > 1:
        raise CommandArgsError("You didn't report anything, silly!\nType `$report` followed by the issue you would like to report.");
    await context.send(f'Your report has been logged: "{"".join(context.args[1:])}"');
    with open("data/reports.txt", "a") as fRequests:
        fRequests.write(context.author.display_name);
        fRequests.write("\n")
        fRequests.write(context.content[8:]);
        fRequests.write("\n")

@command_handler.Command(AccessType.PRIVILEGED, desc = "Opens a support ticket with a specific person.")
async def chat(activator: Neighbor, context: Context):
    if not len(context.args) > 1:
        raise CommandArgsError("`$chat` takes one argument: who to open a chat room with");
    try:
        id = parse_mention(context.args[1]);
    except ValueError:
        raise CommandArgsError("`$chat` please tag the person you would like to create a chat room for")
    
    user = await context.guild.fetch_member(id);

    await open_ticket(None, user, context.guild);
    

@command_handler.Command(AccessType.PRIVILEGED, desc = "Changes the prefix for Greg's commands.")
async def prefix(activator: Neighbor, context: Context, new = ""):
    old = command_handler.Command.prefix;
    command_handler.Command.set_prefix(new);
    # print("changin prefix");
    await context.send(f"Wow! My prefix has been changed from `{old}` to `{new}`\n*Members should now use `{new}help` instead of `{old}help` to access the help command, for example.*")

@command_handler.Command(AccessType.PRIVILEGED, desc = "Set a role to have the trophy tag.")
async def trophy(activator: Neighbor, context: Context):
    if not len(context.args) > 1:
        raise CommandArgsError("`$trophy` expects at least one argument: @mentions for the roles to give trophy tags");
    with open("trophy.txt", "w") as fTrophy:
        fTrophy.write("");
    with open("trophy.txt", "w") as fTrophy:
        for i, arg in enumerate(context.args):
            if i == 0:
                continue;
            try: 
                id = parse_mention(arg);
                fTrophy.write(str(id) + "\n");
            except:
                raise CommandArgsError("`$trophy` only accepts mentions as arguments")

@command_handler.Command(AccessType.PRIVILEGED, desc = "Kicks a member quietly.")
async def remove(activator: Neighbor, context: Context, target, reason = None):
    to_kick = await context.guild.fetch_member(int(target[2:-1]));
    await to_kick.kick(reason=reason);
    pass

@command_handler.Command(AccessType.PRIVILEGED, desc = "Kicks a member with theatrics.")
async def kick(activator: Neighbor, context: Context, reason = None):
    if len(context.args) < 2:
        raise CommandArgsError("Need to @mention someone to kick");
    else:
        target = context.args[1];
    general = await context.guild.fetch_channel(FF.general_channel);
    audit = await context.guild.fetch_channel(FF.audit_channel);
    await general.send(f"{target} has been kicked! https://tenor.com/view/the-wheel-of-time-wheel-of-time-saidar-one-power-true-source-gif-26196681");
    to_kick = await context.guild.fetch_member(int(target[2:-1]));
    await to_kick.kick(reason=reason);
    await audit.send(to_kick.name + " has been kicked.")

@command_handler.Command(AccessType.PRIVILEGED, desc = "Kicks a member with theatrics.")
async def remove(activator: Neighbor, context: Context, reason = None):
    if len(context.args) < 2:
        raise CommandArgsError("Need to @mention someone to kick");
    else:
        target = context.args[1];
    general = await context.guild.fetch_channel(FF.general_channel);
    audit = await context.guild.fetch_channel(FF.audit_channel);
    await general.send(f"{target} has been kicked! https://tenor.com/view/thor-avenger-chris-hemsworth-mjolnir-gif-13624915");
    to_kick = await context.guild.fetch_member(int(target[2:-1]));
    await to_kick.kick(reason=reason);
    await audit.send(to_kick.name + " has been kicked.")
    
@command_handler.Command(AccessType.PRIVILEGED, desc = "Kicks a member with theatrics.")
async def erase(activator: Neighbor, context: Context):
    if len(context.args) < 2:
        raise CommandArgsError("Need to @mention someone to kick");
    else:
        target = context.args[1];
    general = await context.guild.fetch_channel(FF.general_channel);
    audit = await context.guild.fetch_channel(FF.audit_channel);
    await general.send(f"{target} has been kicked! https://tenor.com/view/thor-avenger-chris-hemsworth-mjolnir-gif-13624915");
    to_kick = await context.guild.fetch_member(int(target[2:-1]));
    await to_kick.kick(reason=reason);
    await audit.send(to_kick.name + " has been kicked.")
    
@command_handler.Command(AccessType.PRIVILEGED, desc = "Kicks a member with theatrics.")
async def impale(activator: Neighbor, context: Context, reason = None):
    if len(context.args) < 2:
        raise CommandArgsError("Need to @mention someone to kick");
    else:
        target = context.args[1];
    general = await context.guild.fetch_channel(FF.general_channel);
    audit = await context.guild.fetch_channel(FF.audit_channel);
    await general.send(f"{target} has been kicked! https://tenor.com/view/the-wheel-of-time-wheel-of-time-saidar-one-power-true-source-gif-26196681");
    to_kick = await context.guild.fetch_member(int(target[2:-1]));
    await to_kick.kick(reason=reason);
    await audit.send(to_kick.name + " has been kicked.")

@command_handler.Command(AccessType.PRIVILEGED, desc = "Kicks a member with theatrics.")
async def delete(activator: Neighbor, context: Context, reason = None):
    if len(context.args) < 2:
        raise CommandArgsError("Need to @mention someone to kick");
    else:
        target = context.args[1];
    general = await context.guild.fetch_channel(FF.general_channel);
    audit = await context.guild.fetch_channel(FF.audit_channel);
    await general.send(f"{target} has been kicked! https://tenor.com/view/thor-avenger-chris-hemsworth-mjolnir-gif-13624915");
    to_kick = await context.guild.fetch_member(int(target[2:-1]));
    await to_kick.kick(reason=reason);
    await audit.send(to_kick.name + " has been kicked.")

@command_handler.Command(AccessType.PRIVILEGED, desc = "Bans a member with theatrics.")
async def ban(activator: Neighbor, context: Context, reason = None):
    general = await context.guild.fetch_channel(context.ID_bundle.general_channel);
    audit = await context.guild.fetch_channel(FF.audit_channel.value);
    await general.send(f"{target} has been banned! https://tenor.com/view/bongocat-banhammer-ban-hammer-bongo-gif-18219363");
    to_ban = await context.guild.fetch_member(int(target[2:-1]));
    await to_ban.ban(reason=reason);
    await audit.send(to_ban.name + " has been banned.")
    

@command_handler.Command(AccessType.PRIVILEGED, desc = "Mutes a member.")
async def mute(activator: Neighbor, context: Context, reason = None):
    general = await context.guild.fetch_channel(context.ID_bundle.general_channel);
    await general.send("This feature has not been implemented.")

@command_handler.Command(AccessType.DEVELOPER, desc = "Overrides all cooldown items.")
async def override(activator: Neighbor, context: Context):
    if not len(context.args) > 1:
        raise CommandArgsError("```override``` expectes 1 argument: the id of the player whose cooldowns need overridden")
    id = int(context.args[1]);
    neighbor = Neighbor(id, FF.guild);
    inventory = neighbor.get_inventory();
    for item in inventory:
        if "cooldown" in item.name.lower():
            neighbor.vacate_item(item);
            await context.send(f"`item: {item.name} overriden for player with id: {id}`");

def parse_mention(content):
    open = False;
    res = "";
    for l in content:
        if l == "<":
            open = True;
        if l == ">":
            open = False;
        if open and l.isnumeric():
            res += l;

    if res == "":
        raise ValueError("Not an ID");
    
    return int(res);

def best_string_match(target, candidates):
    
    possibilities = [x for x in candidates if target.lower() in [x.lower() for x in x.split()]];
    # print(possibilities);
    if len(possibilities) == 1:
        return possibilities[0];
    elif len(possibilities) > 1:
        return max(possibilities, key=lambda x : difflib.SequenceMatcher(None, x, target, autojunk=False).ratio());
    
    possibilities = [x for x in candidates if target.lower() in x.lower()];
    # print(possibilities);
    if len(possibilities) == 1:
        return possibilities[0];
    elif len(possibilities) > 1:
        return max(possibilities, key=lambda x : difflib.SequenceMatcher(None, x, target, autojunk=False).ratio());
    return max(candidates, key=lambda x : difflib.SequenceMatcher(None, x, target, autojunk=False).ratio());


def convert_mentions_to_text(context: Context, str):
    role_id = "";
    start_pos = 0;
    end_pos = 0;
    for letter, i in enumerate(str):
        if letter == "<" and str[i + 1] == "@":
            start_pos = i;
            for ii in range(i + 2, len(str), 1):
                if not str[ii] == ">":
                    role_id += str[ii];
                else:
                    end_pos == ii;
                    break;
            break;
    try:
        role = context.guild.get_role(int(role_id));
        name = role.name;
        str = str[0:i] + "@" + name + str[ii + 1:];
        return str;
    except:
        pass;

async def set_nick(user, guild, was_changed = False):
    
    neighbor = Neighbor(user.id, guild.id);
    user_role_ids = [role.id for role in user.roles];

    name = user.display_name;

    new_nick = name;
    
    with open('families.json') as fFamilies:
        families = json.load(fFamilies)
    with open("rss.json") as fRSS:
        rss = json.load(fRSS);

    tags = [x["tag"] for x in families];

    for tag in tags:
        new_nick = new_nick.replace(tag, "");
        
    old_tags = [x["old_tag"] for x in families]
    
    for old_tag in old_tags:
        new_nick = new_nick.replace(old_tag, "");
        
    new_nick = new_nick.replace("❤", "");
    new_nick = new_nick.replace("{CM} ", "");
    new_nick = new_nick.replace(" {CM}", "");

    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                        "]+", re.UNICODE)
    
    new_nick = re.sub(emoj, '', new_nick)

    new_nick = new_nick.strip();
    
    if not neighbor.get_item_of_name("Invisibility Cloak"):
    
        # if 648188387836166168 in user_role_ids:
        #     new_nick = new_nick + " {CM}";
    
        for family in families:
            if family["role_id"] in user_role_ids:
                if neighbor.get_item_of_name("*Family Logo Tag* -- Best Seller") is None:
                    new_nick = family["old_tag"] + " " + new_nick;
                else:
                    new_nick = unicodes[family["emoji"]] + new_nick;
                    
        tag_items = neighbor.get_items_of_type("tag");
        
        for tag_item in tag_items:
            if tag_item.name == "*Family Logo Tag* -- Best Seller":
                continue;
            cur = None;
            for category in rss:
                if not cur is None:
                    break;
                if category["name"] == "Tags":
                    if not cur is None:
                        break;
                    for item in category["items"]:
                        try:
                            if item["name"] == tag_item.name:
                                emojis = None;
                                values = None;
                                emoji = None;
                                try:
                                    emojis = item["emojis"];
                                except:
                                    try:
                                        values = item["values"];
                                    except:
                                        emoji = item["emoji"];
                                if not emojis is None:
                                    cur = random.choice(emojis);
                                    cur = chr(int(cur, 16));
                                elif not values is None:
                                    cur = values[int(tag_item.get_value("val"))]
                                    cur = chr(int(cur, 16));
                                else:
                                    cur = unicodes[emoji];
                        except:
                            print("Issue with " + tag_item.name);
                            continue;
            new_nick = cur + new_nick;
        
        with open("trophy.txt", "r") as fTrophy:
            for line in fTrophy.readlines():
                if int(line) in user_role_ids:
                    new_nick = unicodes["trophy"] + new_nick;
            
        with open("top_3.txt", "r") as fTop:
            for i, line in enumerate(fTop.readlines()):
                if int(line) == user.id:
                    if i == 0:
                        new_nick = unicodes["first"] + new_nick;
                    if i == 1:
                        new_nick = unicodes["second"] + new_nick;
                    if i == 2:
                        new_nick = unicodes["third"] + new_nick;
                            
        if neighbor.ID == 788800859101331519:
            new_nick = "\U0001F381" + new_nick;

    # print(new_nick)
    if new_nick != name:
        try:
            await user.edit(nick = new_nick[0:32]);
            print(new_nick);
        except Exception as e:
            traceback.print_exc();
            if was_changed:
                pass
                # await user.send(f"Hi! Greg here. It looks like you changed your nickname to {user.nick} although it should be {new_nick} to be in line with Greg's monopoly. I tried to change it for you but for some reason I was unsuccessful, probably because I do not have permission to.")
        
async def set_roles(user, guild):
    if guild.id == FF.guild:
        role_ids = [FF.strawberry_role, FF.blueberry_role, FF.chicken_icon, FF.coin_icon, FF.diamond_icon, FF.barn_icon, FF.greg_icon, FF.rainbow_role, FF.invisibility_role];
    else: 
        role_ids = [PHOENIX.strawberry_role, PHOENIX.blueberry_role, "", "", "", "", "", PHOENIX.rainbow_role, PHOENIX.invisibility_role];
    names = ["Strawberry Tag", "Blueberry Tag", "Hay Day Chicken", "Hay Day Coin", "Hay Day Diamond", "The Barns of Friendly Farmers Collection", "Hay Day Greg", "*Rainbow Role* -- Best Seller", "Invisibility Cloak"];

    user_role_ids = [role.id for role in user.roles];

    neighbor = Neighbor(user.id, guild.id);
    neighbor.expire_items();
    for i, id in enumerate(role_ids):
        item = neighbor.get_item_of_name(names[i]);
        if item is None and id in user_role_ids:
            role = guild.get_role(id);
            await user.remove_roles(role);
        elif not item is None and not id in user_role_ids:
            role = guild.get_role(id);
            await user.add_roles(role);
        
        
def strip(neighbor, levels: int = None, xp: int = None):
    if not xp is None:
        neighbor.set_XP(neighbor.get_XP() - xp);
    elif not levels is None:
        cur_level = neighbor.get_level();
        distance_to_next_level = Neighbor.get_XP_for_level(cur_level + 1) - Neighbor.get_XP_for_level(cur_level);
        percent_progress_to_next_level = neighbor.get_XP_for_next_level() / distance_to_next_level;
        
        new_level = cur_level - levels;
        neighbor.set_XP(Neighbor.get_XP_for_level(new_level));
        new_distance_to_next_level = Neighbor.get_XP_for_level(new_level + 1) - Neighbor.get_XP_for_level(new_level);
        add = int(new_distance_to_next_level * percent_progress_to_next_level);
        neighbor.increase_XP(add);
        
async def inc_xp(neighbor: Neighbor, amount, context=None):
    member = await context.guild.fetch_member(neighbor.ID);
    name = member.display_name;
    cur_lvl = neighbor.get_level();
    neighbor.increase_XP(amount);
    new_lvl = neighbor.get_level();
    
    if new_lvl > cur_lvl:
        best_this_month = neighbor.get_item_of_name("Best Level This Month");
        best_this_month = int(best_this_month.get_value("level"))
        if new_lvl > best_this_month:
            best_this_month = new_lvl;
        
        target = await context.guild.fetch_channel(context.ID_bundle.bot_channel);
        
        if not neighbor.get_item_of_name("Hype Man") is None:
            await target.send("<@" + str(member.id) + "> has advanced to level " + str(new_lvl) + "!\nKeep it up, I have always believed in you! <3 :)");
        elif neighbor.get_item_of_name("Pings Off"):
            await target.send(name + " has advanced to level " + str(new_lvl) + "!");
        elif new_lvl == 3:
            await target.send("<@" + str(member.id) + "> has advanced to level " + str(new_lvl) + "!" + "\n*You can now access my roadside shop! Try it out with $rss!*");
        elif new_lvl == 5 and best_this_month == 5:
            await target.send("<@" + str(member.id) + "> has advanced to level " + str(new_lvl) + "!" + "\n*You have unlocked a few special offers in my roadside shop! Try it out with $rss!*");
        elif chance(5) or new_lvl % 10 == 0:
            choices = ["Fantastic! And when you reach a milestone level you can get a free 3 day booster. Not bad, eh?", "Did you know? Use $rss to spend your levels on cool items!", "Wohoo! Thanks for being active!", "Beware! At the beginning of each month, the __reckoning__ halves all players' levels! Don't worry though, I will send a reminder before it happens.", "Remember! As you begin to level up more, items in the $rss become comparatively more expensive because they cost a constant number of levels!", "Great job! Rose is jealous for sure!", "Nice! If you're looking for more ways to earn XP, try $harvest once per hour then sell your crops at the farmers market!", "Ping! Annoyed with my pings? Try `$pings off`", "P.S. The boosters category of my roadside shop can make you much richer. Try `$rss`!", "Haven't you heard the rumors? No?\nI heard of a silo thief o'er in the nearest town East us. Best keep an eye out. `$info thief` will tell ya e'erything I know."];
            await target.send("<@" + str(member.id) + "> has advanced to level " + str(new_lvl) + "!" + "\n*" + random.choice(choices) + "*");
        else:
            await target.send(name + " has advanced to level " + str(new_lvl) + "!");
            
        if (new_lvl == 5 or new_lvl == 10 or new_lvl == 20 or new_lvl == 30 or new_lvl == 50 or new_lvl == 100) and best_this_month == new_lvl:
            await target.send("You have also reached a milestone level for the first time this month! Congratulations.")
            await target.send(f"You reached level {new_lvl} so you will get {new_lvl}% extra xp per message for 72 hours.")
            boost = Item("Milestone Boost", "milestone_boost", int(time.time() + 259200), boost = new_lvl);
            neighbor.bestow_item(boost);
            
async def assign_family(client, before, after):
    guild = before.guild;
    targetAF = await guild.fetch_channel(FF.assign_family_channel);
    targetBC = await guild.fetch_channel(FF.bot_channel);

    name = after.display_name;

    neighborhood_before = get_neighborhood_from_user(before);
    neighborhood_after = get_neighborhood_from_user(after);
    # print(neighborhood_after);

    family_before = get_family_from_user(before);
    family_after = get_family_from_user(after);

    # print(neighborhood_after);
    if not neighborhood_after is None and family_after == "0":
        # print("here");
        await pick_family(after);
    else:
        return 0;
    
async def pick_family(after):
    guild = after.guild;
    targetAF = await guild.fetch_channel(FF.assign_family_channel);
    targetBC = await guild.fetch_channel(FF.bot_channel);
    
    # await targetAF.send("While I would love to assign this player a family, this feature is currently under construction. Please pardon my dust. This player will be assigned a family soon.")
    # return 0;

    neighborhood_after = get_neighborhood_from_user(after).lower();

    with open("families.json") as fFamilies:
        family_info = json.load(fFamilies);
        
    votes = {};
    
    unique_player_count = 0;
    
    players_in_nh_count = 0;
    
    for member in guild.members:
        role_ids = [role.id for role in member.roles];
        if FF.p_neighbors_role in role_ids:
            unique_player_count += 1;
            if neighborhood_after == "ffp":
                players_in_nh_count += 1;
        elif FF.neighbors_role in role_ids:
            unique_player_count += 1;
            if neighborhood_after == "ff":
                players_in_nh_count += 1;
        elif FF.j_neighbors_role in role_ids:
            unique_player_count += 1;
            if neighborhood_after == "ffj":
                players_in_nh_count += 1;
        elif FF.r_neighbors_role in role_ids:
            unique_player_count += 1;
            if neighborhood_after == "ffr":
                players_in_nh_count += 1;
    
    for family in family_info:
        family_count = 0;
        family_in_nh_count = 0;
        votes[family['name']] = 0;
        for member in guild.members:
            role_ids = [role.id for role in member.roles];
            if family["role_id"] in role_ids:
                family_count += 1;
                if neighborhood_after == "ffp" and FF.p_neighbors_role in role_ids:
                    family_in_nh_count += 1;
                elif neighborhood_after == "ff" and FF.neighbors_role in role_ids:
                    family_in_nh_count += 1;
                elif neighborhood_after == "ffj" and FF.j_neighbors_role in role_ids:
                    family_in_nh_count += 1;
                elif neighborhood_after == "ffr" and FF.r_neighbors_role in role_ids:
                    family_in_nh_count += 1;
        # await targetAF.send(f"There are {unique_player_count} unique players in FF town & there are {players_in_nh_count} farms in {neighborhood_after}.")
        # await targetAF.send(f"There are {family_count} players in the {family['name']} family, and {family_in_nh_count} in {neighborhood_after}")
        
        family_count_disparity = (unique_player_count / 5 - family_count);
        family_count_disparity = family_count_disparity if family_count_disparity >= 0 else 0;
        
        family_in_nh_count_disparity = (players_in_nh_count / 5 - family_in_nh_count);
        family_in_nh_count_disparity = family_in_nh_count_disparity if family_in_nh_count_disparity >= 0 else 0;
        
        vote_count = int(family_count_disparity / 2 + family_in_nh_count_disparity ** 2 + 1) ** 2;
        votes[family['name']] = vote_count;
        
        # await targetAF.send(f"Therefore, the {family['name']} family gets {vote_count} votes.");
                    
    choices = [];
    for family in family_info:
        for i in range(votes[family['name']]):
            choices.append(family);
            
    family_decision = random.choice(choices);
    
    role = guild.get_role(int(family_decision["role_id"]));
    await after.add_roles(role);
    
    await targetAF.send(f'<:ffp_logo:1111011980061462538><:ff_logo:1111011971953872976><:ffj_logo:1111011976320122880><:ffr_logo:1111011982787743866>\n**Welcome to Friendly Farmers!** <@{after.id}>')
    await targetAF.send('It\'s time for you to be assigned a Family :butterfly::leopard::fox::racehorse::dog:!')
    await targetAF.send('Give me just a moment to consider to which you belong.')
    time.sleep(9.5);
    
    while True:
        time.sleep(3.0);
        candidate = random.choice(family_info);
        if candidate == family_decision and chance(3):
            await targetAF.send('Alright, I think I\'ve got it!') 
            await targetAF.send("Congratulations!" + ' you are now a member of the **' + candidate["name"] + ' Family** ' + unicodes[candidate["emoji"]]);
            await targetAF.send('"' + candidate["description"] + '"');
            break;
        else:
            if chance(3):
                continue;
            await targetAF.send('Hmm... does the ' + candidate["name"] + ' Family sound right?');
            await targetAF.send("No, no I don't think so.");

def get_neighborhood_from_user(user):
    guild = user.guild;
    if has_role(user, guild.get_role(FF.neighbors_role)):
        return "FF";
    if has_role(user, guild.get_role(FF.j_neighbors_role)):
        return "FFJ";
    if has_role(user, guild.get_role(FF.p_neighbors_role)):
        return "FFP";
    if has_role(user, guild.get_role(FF.r_neighbors_role)):
        return "FFR";
    return None;

def has_role(user, role):
    return True if role == user.get_role(role.id) else False;

def get_family_from_user(user):
    guild = user.guild;
    if has_role(user, guild.get_role(FF.butterfly_role)):
        return "B";
    if has_role(user, guild.get_role(FF.cheetah_role)):
        return "C";
    if has_role(user, guild.get_role(FF.fox_role)):
        return "F";
    if has_role(user, guild.get_role(FF.horse_role)):
        return "H";
    if has_role(user, guild.get_role(FF.puppy_role)):
        return "P";
    return "0";	

