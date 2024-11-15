CREATE DATABASE IF NOT EXISTS Game;  -- this file contains random SQL queries mostly for debug purposes
USE Game; 

DROP TABLE IF EXISTS Inventory; -- due to foreign key reference, this table has to be dropped to truncate Players
DROP TABLE IF EXISTS Items;
DROP TABLE IF EXISTS Players;

TRUNCATE TABLE Items; -- truncate deletes all content in a table, drop deletes the table itself
TRUNCATE TABLE Players;

CREATE TABLE IF NOT EXISTS Players ( 
	Player_id INT NOT NULL AUTO_INCREMENT,
	PlayerName VARCHAR(64) UNIQUE,
	Health INT NOT NULL DEFAULT 100,
	Money INT NOT NULL DEFAULT 0,
	GameTime INT NOT NULL DEFAULT 0,
	GameDay INT NOT NULL DEFAULT 0,

	PRIMARY KEY (Player_id),
	UNIQUE (PlayerName)
);

CREATE TABLE IF NOT EXISTS Inventory ( 
	Item_id INT NOT NULL AUTO_INCREMENT,
	Player_id INT NOT NULL,
	ItemName VARCHAR(32) NOT NULL,
	PRIMARY KEY (Item_id),
	FOREIGN KEY (Player_id) REFERENCES Players(Player_id)
);

CREATE TABLE IF NOT EXISTS Items ( 
	Item_id INT NOT NULL AUTO_INCREMENT,
	ItemName VARCHAR(32) NOT NULL,
	PRIMARY KEY (Item_id),
    UNIQUE (ItemName)
);

-- INSERT INTO TABLE Items (ItemName) -- inserting values into items table makes them available to pick up
-- VALUES ( -- this however, does not currently have any use or function and is therefore not included
--	"Axe", "Knife", "etc..."
-- );

SELECT * FROM Items;
SELECT * FROM Inventory;
SELECT * FROM Players;

