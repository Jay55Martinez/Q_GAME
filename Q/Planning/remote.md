# Q Game

To: CEOs of "dot game" company <br>
From: Jay Martinez and Taiga Wad <br>
Subject: Remote Proxy <br>

## Interactions
When a referee would like to communicate with a player, it will instead go through a player-proxy. This player-proxy will then communicate with a referee-proxy through json packages sent through TCP. This referee-proxy will then interact with the player. The player will then communicate to the referee-proxy, which will communicate with a player-proxy and then the referee.

## Gathering Players
When gathering players, the referee will wait for communication from Players, which will be sent through the proxy. The information sent will be the players name and age. The referee gathers the player information and when enough or all players have communicated, will start up the game.

## Sequence Diagram:
ready():
Referee      Player_Proxy      Referee_Proxy       Player 
   |----ready()-->|                 |                |
   |              |---ready_json--->|                |
   |              |                 |----ready()---->|
   |              |                 |<---responce----|
   |              |<-responce_json--|                |
   |<--responce---|                 |                |

## Launching Game
When launching the game, the referee sets up the map, distributes tiles to the players, and has the first player take their turn. The referee will then send the information to each player, through their respective proxy, about the start of the game. The information provided to the player will include their starting hand, the status of the map, the number of tiles the referee has, the points of the players, and whether it is that players turn. When the player wishes to take a turn, it communicates with the referee proxy and includes information about the type of move and tiles to place (for a placement). In the event that the move is an exchange, the referee will commmunicate with the player proxy and sends information about the new tiles recieved.

## Sequence Diagram:
init_player():
Referee         Player_Proxy         Referee_Proxy            Player
   |                  |                    |                    |
   |--init_player()-->|                    |                    |
   |                  |---j_state_j_tiles->|                    |
   |                  |                    |----init_player()-->|
   |                  |                    |                    |

take_turn():
Referee         Player_Proxy         Referee_Proxy            Player
   |                  |                    |                    |
   |---take_turn()--->|                    |                    |
   |                  |-----j_take_turn--->|                    |
   |                  |                    |----take_turn()---->|
   |                  |                    |<------move---------|
   |                  |<----j_move---------|                    |
   |<------move-------|                    |                    |

## Reporting the Result
In order to report the result of the game, the referee will act similarly to when the game is launched. It will inform all non-malicious players, through their respective proxies, about the final map, the tiles remaining in the players hand, the points of the players, and whether that player has won or not.

## Sequence Diagram:
get_score():
Referee         Player_Proxy         Referee_Proxy            Player
   |                  |                    |                    |
   |---get_score()--->|                    |                    |
   |                  |-----j_get_score--->|                    |
   |                  |                    |-------score------->|
   |                  |                    |<------score--------|
   |                  |<----j_score--------|                    |
   |<------score------|                    |                    |
   |
   |-------
   |      |
   |      |  player_with_highest_score()
   |      |
   |<------

game_over()
Referee         Player_Proxy         Referee_Proxy            Player
   |                  |                    |                    |
   |---game_over()--->|                    |                    |
   |                  |-----j_game_over--->|                    |
   |                  |                    |------gameover----->|
   |                  |                    |                    |
   |                  |                    |                    |
   |                  |                    |                    |
