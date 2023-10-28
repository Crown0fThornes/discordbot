# "Greg"
Custom Discord Bot 

commands.py consists of the commands, uncontested commands, and loop commands for the Greg discord bot. The handler scripts, which interpret user and server actions and pass them off to the correct command (if necessary), and other supporting-role files are ommitted here. 

Commands are run when a user calls them by name. For example, the info() command function is run when a user in the server types "$info". Greg implements minimal typo detection as well; if a user's command call is within 75% accurate of the actual spelling, the command will call e.g. "$infp" calls info()

Uncontested commands fall into two categories: reaction responses and message responses. These functions run on every reaction or every message respectively

Loop commands fall into two categories: timed and daily. These functions run on a timed interval from when the bot begins running or at approximately 6pm EST (+/- 5 minutes) each day.
