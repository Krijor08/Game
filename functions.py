import mysql.connector
import re
from time import sleep

game = mysql.connector.connect( # establish connection to MySQL
	host="localhost",  
	user="Python",     # change these according to your MySQL user credentials,
	password="1234"    # or create a new account with these credentials.
)

print(game)

g = game.cursor() 
game.autocommit = True

g.execute("USE Game;") # if no database is used, MySQL won't know where to find the tables you try to edit

def create_account(startup,):
	if startup == "new":
		
		query = "INSERT INTO Players (PlayerName, Money) VALUES (%s, %s);"
		data = [(str(input("Write the name of the new player: \n")), 0)]
		g.executemany(query, data)
		startup = "continue"
		print("New player made successfully. Restart the game to continue.")
		exit()

	elif startup == "continue":
		sleep(0.5)
	elif startup == "reset":
		print("In order to perform reset, open dbsetup.sql in VSCode and run code. If SQLTools is not installed, or it doesn't work, open MySQL and run code from dbsetup.sql.")
		print("WARNING: That will delete everything, only run dbsetup.sql code if absolutely necessary. \nNOTE: Tables are possibly outdated, double check.")
	else:
		create_account(startup = str(input("Command not recognised, try again\nWrite 'continue' to continue from save, or 'new' to create new save: \n")))

def gameplay(query, gametime, gameday, pid):
	command = query.split(".") # queries often consist of a command like "pick up", and an item or attribute. 
	try:
		data = command[1] # if this doesn't work, the query only has 
	except:
		data = None
	command = command[0]

	print(data)
	print(command)
	sleep(2)
	if re.search("^pick up*", command) :
		pickup(item = data, pid = pid)
	elif command == "inventory":
		inventory(pid = pid)
	elif command == "save":
		return("save")

	if gametime < 21600:
		gameplay(query = str(input("What do you want to do now?\n")), gametime = gametime, gameday = gameday, pid = pid)

	else:
		print("The day is over.")
		gameday += 1
		savegame = str(input("Do you want to save the game?\n"))
		if savegame == "Yes":
			save()

def inventory(pid, ):
	g.execute("""SELECT ItemName, Quantity 
		WHERE Player_id = %s
		JOIN Players ON Players.Player_id = Inventory.Player_id;""", (pid,))
	rows = g.fetchall()
	for row in rows:
		print(row)

def pickup(item, pid, ): # called when items shall be picked up, makes sure the item exists then inserts to inventory
	g.execute("""SELECT ItemName FROM Items
		WHERE ItemName = %s;""", (item,))
	rows = g.fetchall()

	if rows != []:
		itemexists = True
		print(itemexists)
	else:
		itemexists = False
		print("That's not a valid item, try again.", itemexists)

	if itemexists == True:
		query = "INSERT INTO Inventory (ItemName, Player_id) VALUES %s, %s;"
		data = [(item, pid)]
		g.executemany(query, data)
    
def save(gametime, gameday, playerhealth, money, pid):
	query = """UPDATE Players
		SET Health = %s, GameTime = %s, GameDay = %s, Money = %s
		WHERE Player_id = %s;
		"""
	data = (playerhealth, gametime, gameday, money, pid)
	g.execute(query, data)

def select(): # select what account to use. If no account exists, a new one must be made.
	selectplayer = None

	g.execute("SELECT PlayerName FROM Players;")
	rows = g.fetchall()
	for row in rows:
		print(row)
	if len(rows) > 1:
		selectplayer = str(input("Write name to select player: \n"))

		print(f"Player {selectplayer} selected. Starting game...\n")

	elif len(rows) == 1:
		selectplayer = row[0]

		print(f"{selectplayer} is the only player found. Starting game...")

	elif rows == []: 
		print("There are no players, create a new to continue. \n") 

		selectplayer = None

		create_account(startup = "new")
	
	g.execute("SELECT PlayerName, Health, Money, GameTime, GameDay FROM Players WHERE PlayerName = %s;", (str(selectplayer),))
	rows = g.fetchall()

	for row in rows:
		print(row)

	g.execute("SELECT Player_id FROM Players WHERE PlayerName = %s;", (str(selectplayer),))
	row = g.fetchone()

	pid = row[0]

	print(pid)
	return pid
