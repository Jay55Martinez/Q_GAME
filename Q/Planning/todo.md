TODO:
Updated TODO List for the final:
- when a invalid tile gets defined e.g. Piece("triangle", "black") then we return a Board Piece what should happen when a player has a board piece. I think they should be kicked
- when setup if there is not enough tiles to deal to everyone the game throws an error this should be handled
- when a player takes there turn out of order




(Ranked in most important to least important)
- add docstring to classes and methods
- move JSON parsing to separate module
- clean up git repo 
    - put tests in the right directories
    - remove unused files

Completed:
- Debug the game running
    - fix score bug
    - get game to end when player places all of there tiles
    - get game to end when all players pass 
- make player_id -> player_name
    - ensure that player_name is unique 
- move referee.py and UnitTests/referee_test.py to a new directory Referee
- Get View to work 
    - display the game state
    - update the window after the turn 
    - remove 'removed' player from being displayed on the screen
- Add catch clauses to taking a turn so that if a player disconnects mid turn they get
  removed and the game does not crash
- When a player gets removed thier tiles should be add back to the referee tiles
- placing a Q could be set to 8 and the one for finishing the game could be set to 4

