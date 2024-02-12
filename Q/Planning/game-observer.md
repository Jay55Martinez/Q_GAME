## Memorandum

### TO: PROFESSOR FELLEISEN

### FROM: MATT STETTER AND JAY MARTINEZ

### DATE: OCT 26, 2023

### SUBJECT: GAME-OBSERVER MACHANISM

**Observer** Represents the public view of the game. Includes number of players left in the game, all of the players scores, the current players turn, a deepcopy of the board, and the number of referee pieces left

    Data:
        **public_state** the public knowledge of the game. Same information that players recieve

        **current_player** the current player whos turn it is

    Methods:
        **get_current_player_move** : returns the move that the current player is going to make

        **display_public_state** : renders the public state of the game into a gui window that displays the public knowledge of the game

        **current_first_place** : returns the player who is in the lead

        **current_last_place** : returns the player who is in last place that is not elimated yets

        **eliminated_players** : returns a list of all of the eliminated players from the gaem

        **last_move** : returns the last move

**PublicState** Represents the public knowledge of the game. This class would be static and will have no methods. Includes a deepcopy of the current board, list of all the players scores, list of all eliminated players, and the last move that was made. 

    Data:
        **board** a deepcopy of the current state of the board

        **last_move** a tuple containing the turn type and tile placements

        **scores_of_players** a dictionary where the player id is the key and the value is the score of the player

**GameState** Represents the private knowledge of the game. This class is used to update and run the game. Includes, players, board, and referee tiles. We will have an observer for them game which GameState will send updates to.

    Data:
        **board** the board that the players are playing on

        **referee_tiles** the tiles that the players pick up from 

        **players** all the players currently playing the game

        **game_over** boolean true if the game is over

        **eliminated_players** a list of all of the eliminated players

        **turn_queue** the order that the players take their turn based on youngest to oldest

        **observer** the 

    Methods: 
        **get_last_turn** : returns the last players turn 

        **create_public_state** : creates a PublicState based on the game

        **init_observer** : uses create_public_state to create an observer for this game state

        **update_observer_after_player_turn** : updates the observer after a player makes their move

        **update_observer_after_elimination** : updates the observer after a player is emlimated

        ---------------

        **update_observer** : abstracted version of the other update method

The basic idea for this implementation is that the GameState will create and update an observer.

For future implementation, these are the additions that we need to make to our code base to add a game-observer mechanism. 