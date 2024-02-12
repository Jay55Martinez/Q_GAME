## Memorandum

### TO: PROFESSOR FELLEISEN

### FROM: ETHAN CARPENTER AND MATT STETTER

### DATE: SEP 27, 2023

### SUBJECT: PROPOSAL FOR FIRST THREE MILESTONES

#### Note: **Bold** is a name

**Status** enum of statuses
	   **success**, **failure**

**Position** represents a position
	   **row**, **column**

**Board** represents the playing field
	Data:
		**peices** 2D python list of Pieces: 	location in the lists is the location on the board
	
**Shape** Enum of piece shape
	**star**, **8star**, **square**, **cirlce**, **clover**, **diamond**
	
**Color** Enum of piece color
	**red**, **green**, **blue**, **yellow**, **orange**, **purple**

**Piece** class reperesenting a piece
	Data:
		**Shape**
		**Color**

**Turn** enum representing the turn types
       **pass**, **exchange**, **place**

**Player** class representing a player
	 Data:
		**age**: the numer of days old the player is
		**points**: the number of points the player has scored
		**tiles**: List of Tile, the tiles in the players possesion

**Referee** class representing a referee
	  Data:
		**board**: a Board
		**unused_pieces**: min_heap of unused pieces, each peice is assigned a random value upon inserting to make random draws easy
		**player_choices**: a list of Turn
		**valid_piece_places**: a list of list of set(Position) where the pieces of a certian type could be placed

**Game** class representing a game
       Data:
		**referee**: the referee for the game
		**players**: list of Player, the players in the game
		**turn_queue**: a FILO queue of the players turns, when a player takes a turn, it is deleted and inserted

