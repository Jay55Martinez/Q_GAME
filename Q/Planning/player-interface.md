## Memorandum

### TO: PROFESSOR FELLEISEN

### FROM: ETHAN CARPENTER AND MATT STETTER

### DATE: OCT 5, 2023

### SUBJECT: REFEREE DESIGN TASK

**Player** represents the people currently playing the game  
	Data:  
                - **age**: age of Player in days  
                - **points**: number of points scored by Player
                - **owned_pieces**: list of Pieces owned by Player that have not been played  

**Turn** enum represents the different possible turn types
                - **place**, **exchange**, **pass**

**Referee** represents the referee that runs games  
	Data:  
                - **board**: state of pieces on board  
                - **player_list**: list of players (sorted in turn order)  
                - **unused_pieces**: Pieces that are available to be exchanged with a Player  
	Methods:  
                - **take_turn**: called to process the provided Turn and execute it if legal (takes a Turn, and optionally a list of Pieces and a list of Positions)  
                - **broadcast_board_state**: informs the Players of the current state of the board  
                - **broadcast_scores**: informs the Players of the scores that all Players currently have  
		- **broadcast_turn_order**: informs the Players when it is their turn  
