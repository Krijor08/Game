import mysql.connector
import re
from time import sleep

game = mysql.connector.connect( # establish connection to MySQL
	host="localhost",
	user="Python",
	password="1234"
)

print(game)

g = game.cursor() 
g.autocommit = True

g.execute("USE Game;") # remember to "use" databases before trying to edit them

def create_account(startup,):
	if startup == "new":
		try:
			query = "INSERT INTO Players (PlayerName, Money) VALUES (%s, %s);"
			data = [(str(input("Write the name of the new player: \n")), 0)]
			g.executemany(query, data)
			startup = "continue"
		except:
			print("An error occured, please try again.")
			create_account(startup = "new")

	elif startup == "continue":
		sleep(0.5)
	elif startup == "reset":
		print("In order to perform reset, open dbsetup.sql and run code. If SQLTools is not installed, or it doesn't work, open MySQL and run code from dbsetup.sql.")
		print("WARNING: That will delete everything, only run dbsetup.sql code if absolutely necessary. \nNOTE: Tables are possibly outdated, double check.")
	else:
		create_account(startup = str(input("Command not recognised, try again\nWrite 'continue' to continue from save, or 'new' to create new save: \n")))

def gameplay(command, gametime, gameday, pid):
	command = command.split(".")
	try:
		data = command[1]
	except:
		data = None
	command = command[0]

	print(data)
	print(command)
	sleep(2)
	if re.search("^pick up*", command) :
		pickup(item = data, pid = pid)
	elif command == "inventory":
		pass#inventory(pid = pid)
	elif command == "save":
		return("save")

	if gametime < 21600:
		gameplay(command = str(input("What do you want to do now?\n")), gametime = gametime, gameday = gameday, pid = pid)

	else:
		print("The day is over.")
		gameday += 1
		savegame = str(input("Do you want to save the game?\n"))
		if savegame == "Yes":
			save()

# def inventory(pid, ):
#	g.execute("""SELECT ItemName, Quantity 
#		WHERE Player_id = %s
#		JOIN Players ON Players.Player_id = Inventory.Player_id;""", (pid,))
#	rows = g.fetchall()
#	for row in rows:
#		print(row)

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
	query = """UPDATE Player
		SET Health = %s, GameTime = %s, GameDay = %s, Money = %s
		WHERE Player_id = %s;
		"""
	data = (playerhealth, gametime, gameday, money, pid)
	g.execute(query, data)

def select(): # select what account to use. If no account exists, a new one must be made.
	selectplayer = None

	g.execute("SELECT PlayerName FROM Players;")
	rows = g.fetchall()

	if len(rows) > 1:
		for row in rows:
			print(row)
		selectplayer = str(input("Write name to select player: \n"))

		g.execute("SELECT * FROM Players WHERE PlayerName = %s;", (selectplayer,))
		rows = g.fetchall()

		print("Player", selectplayer, "selected. Starting game...\n")
		for row in rows:
			print(row)
		sleep(1)

	elif len(rows) == 1:
		for row in rows:
			print(row)

		selectplayer = row

		g.execute("SELECT PlayerName, Health, Money, GameTime, GameDay FROM Players WHERE PlayerName = %s;", selectplayer)
		rows = g.fetchall()

		for row in rows:
			print(row)

		print("Starting game...")

	elif rows == []: 
		print("There are no players, create a new to continue. \n") 

		selectplayer = None

		create_account(startup = "new")

	g.execute("SELECT Player_id FROM Players WHERE PlayerName = %s;", selectplayer)
	rows = g.fetchone()

	for row in rows:
		continue

	pid = row
	return pid
