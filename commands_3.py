from command_handler import Context
from command_handler import AccessType
import command_handler
import random
from custom_types import Neighbor, Item, Expectation, Reminder, Giveaway, Poll, Offer
from id_bundle import FF
import difflib
import discord

VERSION = "3.0";
unicodes = {
    0: "\U00000030\U0000FE0F\U000020E3",
    1: "\U00000031\U0000FE0F\U000020E3",
    2: "\U00000032\U0000FE0F\U000020E3",
    3: "\U00000033\U0000FE0F\U000020E3",
    4: "\U00000034\U0000FE0F\U000020E3",
    5: "\U00000035\U0000FE0F\U000020E3",
    6: "\U00000036\U0000FE0F\U000020E3",
    7: "\U00000037\U0000FE0F\U000020E3",
    8: "\U00000038\U0000FE0F\U000020E3",
    9: "\U00000039\U0000FE0F\U000020E3"
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
    "bell peper" : 7,
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
}

swear_words = [];

@command_handler.Uncontested(desc = "Uses stored expectations to appropriately respond to user messages and reactions.")
async def handle_expectation(context: Context):
    pass

@command_handler.Uncontested(desc = "Removes bad words.")
async def handle_bad_words(context: Context):
    detected = [x for x in context.content.split() if x in swear_words];
    if len(detected) > 0:
        audit_channel = await context.guild.fetch_channel(FF.audit_channel);
        await audit_channel.send(f"<@&{FF.leaders_role}> Be advised: a message from <@{context.author_id}> was deleted:")
        await audit_channel.send(f'"{context.content}"');
        await context.message.delete();
    

@command_handler.Uncontested(desc = "Incrememnts a Neighbor's server XP each time they send a message.")
async def increment_xp(context: Context):
    list_of_possibilites = []
    pass;

@command_handler.Uncontested(desc = "If a Neighbor has the Hype Man item, which can be purchased in the rss, then Greg will react to the Neighbor's messages with an emoji.")
async def hype_man_responses(context: Context):
    pass;

@command_handler.Uncontested(desc = "If a message contains the word greg, Greg will react with an emoji")
async def greg_react(context: Context):
    pass

@command_handler.Loop(days = 1, desc = "Sorts the Neighbors text file in order of descending XP once per day.")
async def database_maitenance():
    pass;

@command_handler.Loop(days = 1, desc = "Checks once per day for support ticket channels that have had no new messages in 48 hours and archives them.")
async def archive_support():
    pass;

@command_handler.Loop(days = 1, desc = "On tuesdays and thursdays, a new channel called Farmers Market appears that lets Neighbors sell crops to Greg for XP.")
async def farmers_market_management():
    pass;

@command_handler.Loop(days = 1, desc = "On the second day of each month, all Neighbors' server XP is reset.")
async def xp_reset():
    pass;

@command_handler.Loop(days = 1, desc = "On mondays, the council is asked to select what derby type is coming up.")
async def derby_channel_mgmt():
    pass;

@command_handler.Loop(days = 1, desc = "From the third through fifth of each month, rss items are on sale.")
async def sale_mgmt():
    pass;

@command_handler.Loop(days = 1, desc = "Updates swear_words list if necesary.")
async def swear_word_mgmt():
    swear_words.clear();
    with open("swearWords.txt") as words:
        for line in words.readlines():
            swear_words.append(line[:-2]);
            
@command_handler.Loop(hours = 1, desc = "If a Neighbor has a passive XP item, the user receives free server XP once per hour.")
async def passive_xp_():
    pass;

@command_handler.Loop(minutes = 5, desc = "Checks if it is time to send a reminder and sends it if so.")
async def reminder_management():
    pass;

@command_handler.Loop(minutes = 5, desc = "The rainbow role color is changed to a random color.")
async def change_rainbow_role_color():
    pass;

@command_handler.Command(AccessType.PUBLIC, desc = "Provides information about greg and an assortment of random things. For example, `$info blossom` provides information on blossom derby.")
async def info(activator: Neighbor, context: Context, type: str = None):
    res = "";
    match "" if type is None else type.lower():
        case None | "":
            res = f"**Hi! my name is Greg :wave:**\nI was created by Lincoln's Farm, & currently running Version {VERSION}.\nI can do lots of things; use $help to find out more.\nVersion 3.0 comes with a more structured code base that makes me easier to maintain and update without any downtime blah blah blah. 3.0 also comes with new features including: reminders, giveaways, polls, and over 10 new rss items to purchase!.";
        case "ff" | "main":
            res = "FF is short for **Friendly Farmers** <:fflogo:1053512963396472852>, the \"main\" Friendly Farmers neighborhood.\n> Tag: #9UPRVCUR\n> Derby Req: Max Points w/o diamond task (2880p normal derby)\n> Level Req: 40\n*As are all of our Neighbors, FF Neighbors are expected to be **F**riendly, **A**ctive, **R**emarkable, **M**unificnet, and **S**ustainable.*";
        case "ffj" | "junior":
            res = "FFJ is short for **Friendly Farmers Junior** <:ffjlogo:1053512965531390102>, the second Friendly Farmers neighborhood.\n> Tag: #PC8VCJ8Q\n> Derby Req: Lvl x 40p (1600p for level 40 player)\n> Level Req: 20\n*As are all of our Neighbors, FFJ Neighbors are expected to be **F**riendly, **A**ctive, **R**emarkable, **M**unificnet, and **S**ustainable.*";
        case "ffr" | "resort":
            res = "FFR is short for **Friendly Farmers Resort** <:ffrlogo:1053512573888241694>, the third Friendly Farmers neighborhood.\n> Tag: #L92LUVQJ\n> Derby Req: None\n> Level Req: 10\n*As are all of our Neighbors, FFR Neighbors are expected to be **F**riendly, **A**ctive, **R**emarkable, **M**unificnet, and **S**ustainable.*";
        case "families" | "family":
            res = "All Neighbors are split into one of five families: The Butterflies, Cheetahs, Foxes, Horses, or Puppies.\nThese are smaller communities within the big Friendly Farmers community to help create bonds and add a bit of fun.\nEach month, families compete for trohpies--aka bragging rights--by participating in some sort of competition. About half the time, family competitions are derby related (sorry FFR!). The other half of the time, families compete in a lot of different ways in game, on disocrd, or even in real life!";
        case "farms" | "farms award":
            res = "FARMS is our model for 'good neighbors'. Good Friendly Farmers neighbors are Friendly, Active, Remarkable, Munificent, and Sustainable.\n\nEvery couple of weeks, we vote for the most FARMS neighbor. This neighbor receives an invitation to join our council of leaders!"
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
        case "animal" | "birthday" | "camping" | "carnival" | "easter" | "fall" | "fishing" | "friends" | "halloween" | "holiday" | "new year" | "new years" | "new year's" | "party" | "picnic" | "summer" | "town" | "trophy" | "yoga":
            res = "An outdated derby type (while outdated derby types have not ever been officialy discontinued by Hay Day, players can reasonably expect to not see these types in current rotation).\n\nIf you want to read more about this type of derby, I recommend visiting the Hay Day wiki page for derby types.\nhttps://hayday.fandom.com/wiki/Derby_Types";
        case "farms award" | "award":
            res = "The FARMS award is a method of __recognition__ and __election__ in Friendly Farmers. FARMS stands for Friendly, Active, Remarkable (in derby), Munificent, and Sustainable: our 5 main attributes as Friendly Farmers."
        case _:
            res = "Hmm... I don't have info on that yet!";
    await context.send(res, reply = True);

@command_handler.Command(AccessType.PUBLIC, desc = "Provides a list of available commands, or alternatively describes the function of a particular command. For example, `$help help`")
async def help(activator: Neighbor, context: Context, command: str = None):
    res = command_handler.Command.generate_help_str(command);
    await context.send(res);

@command_handler.Command(AccessType.PUBLIC, desc = "Invites greg to celebrate an event or achievement")
async def celebrate(activator: Neighbor, context: Context):
    first = ['Congratulations!',
		'Yay!! <:blue_red_hearts:856202113339490304>',
        'Wohoo!!',
        'Celebration time!!',
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
        ':fox: On behalf of the fox family...',
        ':horse_racing: On behalf of the horse family...',
        ':dog: On behalf of the puppy family...',
        'The Neighbors of the FF, FFJ, and FFR family want you to know...',
        'Greg, at your service! One day closer to replacing Rose every day!',
        '<:fflogo:1053512963396472852><:fflogo:1053512963396472852><:fflogo:1053512963396472852>',
        '<:fflogo:1053512963396472852><:ffjlogo:1053512965531390102><:ffrlogo:1053512573888241694>'];
        
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
        'Sorry, no gif today. You know how it is. Supply shortages, inflation, etc etc'];
        
    await context.send(random.choice(first), reply = True);
    await context.send(random.choice(second));

@command_handler.Command(AccessType.PUBLIC, desc = "Invites greg to welcome a user to the server.")
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

@command_handler.Command(AccessType.PUBLIC, desc = "Displays a top-10 leaderboard of the Neighbors with the most XP, or other leaderboards with an argument.")
async def leaderboard(activator: Neighbor, context: Context, configure = None):
    
    neighbors = Neighbor.read_all_neighbors();
  
    neighbors = Neighbor.readNeighbors();
    neighbors = sorted(neighbors, key=lambda x: (x.XP if not configure == "legacy" else x.legacyXP))[::-1];

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
            name = cur.nick;
            XP = neighbors[i].XP if not configure == "legacy" else neighbors[i].legacyXP
            if neighbors[i] in leaderboard_neighbors:
                list += f"{c}) **{name}** (XP: {XP})\n";
                c += 1;
            else:
                list += f"{c - 0.5}) *{name}* (XP: {XP})\n";
        i += 1;
        
    await context.send(res + list);
            
@command_handler.Command(AccessType.PUBLIC, desc = "Display's a Neighbor's profile.")
async def profile(activator: Neighbor, context: Context, target = None, inventory = False):
    target_member = context.author if target is None else target;
    target_neighbor = Neighbor(target_member.ID);
    
    pretty_profile = target_neighbor.get_item_of_name("Pretty Profile");
    
    nick = context.guild.get_member(target_member.ID);
    XP = target_neighbor.get_XP();
    
    neighborhood = "";
    if FF.neighbors_role in context.author_role_ids:
        neighborhood += "FF ";
    if FF.p_neighbors_role in context.author_role_ids:
        neighborhood += "FFP ";
    if FF.j_neighbors_role in context.author_role_ids:
        neighborhood += "FFJ ";
    if FF.r_neighbors_role in context.author_role_ids:
        neighborhood += "FFR ";
    if neighborhood == "":
        neighborhood = None;
    
    family = None
    if FF.butterfly_role in context.author_role_ids:
        neighborhood = "B";
    elif FF.cheetah_role in context.author_role_ids:
        neighborhood = "C";
    elif FF.fox_role in context.author_role_ids:
        neighborhood = "F";
    elif FF.horse_role in context.author_role_ids:
        neighborhood = "H";
    elif FF.puppy_role in context.author_role_ids:
        neighborhood = "P";
        
    current_lvl = target_neighbor.get_level();
    next_lvl = current_lvl + 1;

    xp_toward_next_lvl = XP - Neighbor.calculate_xp_for_lvl(current_lvl);
    xp_for_next_lvl = Neighbor.calculate_xp_for_lvl(next_lvl) - Neighbor.calculate_xp_for_lvl(current_lvl);
    
    progress = xp_toward_next_lvl / xp_for_next_lvl;
        
    if pretty_profile is None:
        progress_bar = "\U000025FB" * int(progress * 10)
        progress_bar += "\U000025FC" * int(10 - len(progress_bar));
        
        profile = f"**{nick}**\n";  
        profile += f"**XP: {XP}**\tLevel: {current_lvl}\n";
        profile += progress_bar + "\n";
        if not neighborhood is None and not family is None:
            profile += f"NH: {neighborhood}\n";
            profile += f"Family: {family}\n";
        else:
            profile += "Guest\n";
        
        profile += "\nInventory:\n";
        for item in target_neighbor.inventory:
            profile += "> " + str(item) + "\n";
        
        await context.send(profile);
    else:
        embed = discord.Embed(title=f"**{nick}**", color=target_member.color)
        embed.add_field(name="XP", value=f"{XP}", inline=True)
        embed.add_field(name="Level", value=f"{current_lvl}", inline=True)
        embed.add_field(name="Progress", value=f"{progress_bar}", inline=False)

        if not neighborhood is None and not family is None:
            embed.add_field(name="Neighborhood", value=f"{neighborhood}", inline=True)
            embed.add_field(name="Family", value=f"{family}", inline=True)
        else:
            embed.add_field(name="Status", value="Guest", inline=False)
        embed.set_thumbnail(url=target_member.avatar_url)
        embed.set_footer(text = "Prettier Profile");
        await context.channel.send(embed = embed);
        
@command_handler.Command(AccessType.PUBLIC, desc = "Displays how much server XP it takes to achieve a level.")
async def level(activator: Neighbor, context: Context, target):
    await context.send(Neighbor.calculate_xp_for_lvl(int(target)));

@command_handler.Command(AccessType.PRIVATE, desc = "Allows Neighbors to purchase discord perks like special roles using server XP")
async def rss(activator: Neighbor, context: Context, shop):
    pass

@command_handler.Command(AccessType.PRIVATE, desc = "Challenges a Neighbor to a three-day server XP-race. Each Neighbor wagers 500xp and the winner earns 1000xp.")
async def challenge(activator: Neighbor, context: Context, target: str):
    pass

@command_handler.Command(AccessType.PRIVATE, desc = "Lets a Neighbor harvest crops.")
async def harvest(activator: Neighbor, context: Context):
    pass

@command_handler.Command(AccessType.PRIVATE, desc = "Displays all crops a Neighbor has harvested.")
async def silo(activator: Neighbor, context: Context):
    pass

@command_handler.Command(AccessType.PRIVILEGED, desc = "Assigns a Neighbor to a family.")
async def assignfamily(activator: Neighbor, context: Context, target: str):
    pass

@command_handler.Command(AccessType.PRIVILEGED, desc = "Changes the prefix for Greg's commands.")
async def prefix(activator: Neighbor, context: Context, new = ""):
    old = command_handler.Command.prefix;
    command_handler.Command.set_prefix(new);
    print("changin prefix");
    await context.send(f"Wow! My prefix has been changed from `{old}` to `{new}`\n*Members should now use `{new}help` instead of `{old}help` to access the help command, for example.*")

@command_handler.Command(AccessType.PRIVILEGED, desc = "Create a recurring reminder.")
async def rCreate(activator: Neighbor, context: Context, channel = None, reminder = None, type = None, interval = None):
    pass

@command_handler.Command(AccessType.PRIVILEGED, desc = "Stop a recurring reminder.")
async def rStop(activator: Neighbor, context: Context, choice = None):
    pass

@command_handler.Command(AccessType.PRIVILEGED, desc = "Create a timed poll.")
async def pCreate(activator: Neighbor, context: Context, text = None, ):
    pass

@command_handler.Command(AccessType.PRIVILEGED, desc = "Create a support ticket channel.")
async def tCreate(activator: Neighbor, context: Context):
    pass

@command_handler.Command(AccessType.PRIVILEGED, desc = "Archive a support ticket channel.")
async def tArchive(activator: Neighbor, context: Context):
    pass

@command_handler.Command(AccessType.PRIVILEGED, desc = "Kicks a member quietly.")
async def remove(activator: Neighbor, context: Context, target, reason = None):
    to_kick = await context.guild.fetch_member(int(target[2:-1]));
    await to_kick.kick(reason=reason);
    pass

@command_handler.Command(AccessType.PRIVILEGED, desc = "Kicks a member with theatrics.")
async def kick(activator: Neighbor, context: Context, target, reason = None):
    general = await context.guild.fetch_channel(FF.general_channel.value);
    audit = await context.guild.fetch_channel(FF.audit_channel.value);
    await general.send(f"{target} has been kicked! https://tenor.com/view/thor-avenger-chris-hemsworth-mjolnir-gif-13624915");
    to_kick = await context.guild.fetch_member(int(target[2:-1]));
    await to_kick.kick(reason=reason);

@command_handler.Command(AccessType.PRIVILEGED, desc = "Kicks a member with theatrics.")
async def remove(activator: Neighbor, context: Context, target, reason = None):
    general = await context.guild.fetch_channel(FF.general_channel.value);
    audit = await context.guild.fetch_channel(FF.audit_channel.value);
    await general.send(f"{target} has been kicked! https://tenor.com/view/thor-avenger-chris-hemsworth-mjolnir-gif-13624915");
    to_kick = await context.guild.fetch_member(int(target[2:-1]));
    await to_kick.kick(reason=reason);
    
@command_handler.Command(AccessType.PRIVILEGED, desc = "Kicks a member with theatrics.")
async def erase(activator: Neighbor, context: Context, target, reason = None):
    general = await context.guild.fetch_channel(FF.general_channel.value);
    audit = await context.guild.fetch_channel(FF.audit_channel.value);
    await general.send(f"{target} has been kicked! https://tenor.com/view/thor-avenger-chris-hemsworth-mjolnir-gif-13624915");
    to_kick = await context.guild.fetch_member(int(target[2:-1]));
    await to_kick.kick(reason=reason);
    
@command_handler.Command(AccessType.PRIVILEGED, desc = "Kicks a member with theatrics.")
async def impale(activator: Neighbor, context: Context, target, reason = None):
    general = await context.guild.fetch_channel(FF.general_channel.value);
    audit = await context.guild.fetch_channel(FF.audit_channel.value);
    await general.send(f"{target} has been kicked! https://tenor.com/view/thor-avenger-chris-hemsworth-mjolnir-gif-13624915");
    to_kick = await context.guild.fetch_member(int(target[2:-1]));
    await to_kick.kick(reason=reason);

@command_handler.Command(AccessType.PRIVILEGED, desc = "Kicks a member with theatrics.")
async def deletes(activator: Neighbor, context: Context, target, reason = None):
    general = await context.guild.fetch_channel(FF.general_channel.value);
    audit = await context.guild.fetch_channel(FF.audit_channel.value);
    await general.send(f"{target} has been kicked! https://tenor.com/view/thor-avenger-chris-hemsworth-mjolnir-gif-13624915");
    to_kick = await context.guild.fetch_member(int(target[2:-1]));
    await to_kick.kick(reason=reason);

@command_handler.Command(AccessType.PRIVILEGED, desc = "Bans a member with theatrics.")
async def ban(activator: Neighbor, context: Context):
    pass

@command_handler.Command(AccessType.PRIVILEGED, desc = "Mutes a member.")
async def mute(activator: Neighbor, context: Context):
    pass


def best_string_match(target, candidates):
    
    possibilities = [x for x in candidates if target in x.split()];
    if len(possibilities) == 1:
        return possibilities[0];
    elif len(possibilities) > 1:
        return max(possibilities, key=lambda x : difflib.SequenceMatcher(None, x, target).ratio());
    
    possibilities = [x for x in candidates if target in x];
    if len(possibilities) == 1:
        return possibilities[0];
    elif len(possibilities) > 1:
        return max(possibilities, key=lambda x : difflib.SequenceMatcher(None, x, target).ratio());
        
    return max(candidates, key=lambda x : difflib.SequenceMatcher(None, x, target).ratio());

def remove_emojis(string):
    pass