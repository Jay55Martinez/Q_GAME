## Memorandum

### TO: PROFESSOR FELLEISEN

### FROM: MATT STETTER AND JAY MARTINEZ

### DATE: OCT 18, 2023

### SUBJECT: REFEREE STATE DESIGN

**GameState** state of current game, including spare tiles, players, and game board

    Data:

        **board** a Board containing all of the pieces played on the board

        **players** list of Players that stores a score, list of tiles, and an ID

        **referee_tiles** list of tiles that the referee can pull from to exchange and give tiles to players

        **turn_queue** sorted queue of the Players by youngest with the birthday

    Methods:

        **get_next_player** Gets the next player in the list and moves through so the next player is on deck

        **get_placed_pieces** Returns a 2d array of all of the positions of pieces

        **commit** Takes a turn, a player ID, and optionally a list of tiles and locations. This method is called by the referee, assuming that the referee has already checked the legitimacy of
        the turn. This serves as the final step before the move is saved onto the board.

        **number_unused** Returns the length of the list of unused tiles that are available for players to exchange with

        **serialize** Returns a string representation of the current game board. This is used for saving the current game state.

        **deserialize** Takes a string representation of a GameState using the same format as "serialize" to load the game back to its state.

**Referee** The referee has a copy of the game state, and processes moves requested by players to determine their legality before kicking the player, or performing the move on the Board through the GameState.

    Data:

        **state** Current state of the board, including ability to commit moves to the board.

        **state_log** List of RefereeState instances for the past n turns that stores the state of the board and game. Used for restoring 

    Methods:

        **take_turn** Main interface for players to request moves. Takes a turn type, a player ID, and optionally a list of tiles and positions. Validates the requested move, and then commits the move to the Board through the commit method in GameState.

        **restore** Takes an integer that tells the Referee how many turns to go back. (1 means restore back to the previous turn)

**RefereeState** Stores the previous state of the referee. Contains the same fields as the referee, but with different methods. Contains an interface for serializing the data in the referee, including the game state, such that the referee can save and restore a game.

    Data:

        **state** Deep copy of the game board that is stored.

    Methods:

        **save** Takes a file name, and serializes the data in the GameState in order to save the current state of the game.

        **load** Takes a file name and returns a RefereeState that contains a GameState with the state of the game stored in the serialized representation in the file.