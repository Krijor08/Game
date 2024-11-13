import mysql.connector
from functions import *

globalpid = None

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

elif len(rows) == 1:
	for row in rows:
		globalpid = row
else:
	create_account(startup = str(input('Welcome to ""! \nWrite "continue" to continue from save, or "new" to create new save: \n')),) # there are existing accounts, asking is necessary
try:
	if globalpid == row:
		select()
	else:
		globalpid = select()
except:
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

g.execute("""
		SELECT * FROM Players
		WHERE Player_id = %s;
		""", (globalpid,))
rows = g.fetchall()

print(rows, "playerdata")

playerhealth = rows[2] # g stands for global, 
money = rows[3]
gametime = rows[4]
gameday = rows[5]

gamesave = gameplay(command = str(input("Game loaded! \nTo perform an action, write the corresponding command.\n")), gametime = gametime, gameday = gameday, pid = globalpid) # first start of the main gameplay loop


if gamesave == "save":
	g.execute("""
		   SELECT * FROM Players
		   WHERE Player_id = %s;
		   """, globalpid)
	save(gametime = gametime, gameday = gameday, playerhealth = playerhealth, money = money, pid = globalpid)
