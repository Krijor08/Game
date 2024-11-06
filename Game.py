import mysql.connector
from functions import *

game = mysql.connector.connect(
	host="localhost",
	user="Python",
	password="1234"
)

print(game, "\n\n\n\n\n\n\n")

g = game.cursor()

g.execute("USE Game;") # remember to "use" databases before trying to edit them

g.execute("SELECT Player_id FROM Players;") # check if any records exist in players table, if not no players exist
rows = g.fetchall()

print(rows, "<-- if this shows [] there are no accounts")

if rows == []: # if there's no save, there's nothing to continue on, skip asking entirely
	create_account(startup = "new", )
else:
	create_account(startup = str(input('Welcome to ""! \nWrite "continue" to continue from save, or "new" to create new save: \n')),) # there are existing accounts, asking is necessary

globalpid = select() # the select() function returns a value, which is the unique player id

print(globalpid, "Game pid") # pid stands for Player ID

for x in range(3): # "loading" for interesting effect
	print("Starting up")
	sleep(0.5)
	print("Starting up.")
	sleep(0.5)
	print("Starting up..")
	sleep(0.5)
	print("Starting up...\n")
	sleep(0.5)

g.execute("SELECT GameTime FROM Players WHERE Player_id = %s;", (globalpid,)) # fetch GameTime from Players table, stored in Players table because different players have different GameTime. Only needs to be done once
rows = g.fetchone() # only expects one row, fetches the result from the SQL query as a tuple
for row in rows: # to get the contents in a tuple out from the tuple, I use a for loop. 
	ggametime = row 
print(ggametime) # debug purposes only

g.execute("SELECT GameDay FROM Players WHERE Player_id = %s;", (globalpid,)) # fetch GameDay from Players table
rows = g.fetchone() # only expects one row
for row in rows:
	ggameday = row
	print(ggameday) # debug purposes only

gameplay(command = str(input("Game loaded! \nTo perform an action, write the corresponding command.\n")), gametime = ggametime, gameday = ggameday, pid = globalpid) # first start of the main gameplay loop
