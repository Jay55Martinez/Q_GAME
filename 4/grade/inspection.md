Pair: mysterious-mongooses \
Commit: [b2b4b8ccfc1b5518d4fc40f700a3784fe0a6905b](https://github.khoury.northeastern.edu/CS4500-F23/mysterious-mongooses/tree/b2b4b8ccfc1b5518d4fc40f700a3784fe0a6905b) \
Self-eval: https://github.khoury.northeastern.edu/CS4500-F23/mysterious-mongooses/blob/1d4047fe814d2d6c62d3d13e2c54a76a565320aa/4/self-4.md \
Score: 15/70 \
Grader: Can Ivit

## Self Evaluation [5/20]
- [-5] First two links in the 3rd question are inaccurate.

## Programming [10/40]
- [-5] Rendering game state
  - There is no signature and purpose statement for [`View`](https://github.khoury.northeastern.edu/CS4500-F23/mysterious-mongooses/blob/b2b4b8ccfc1b5518d4fc40f700a3784fe0a6905b/Q/Common/game_state.py#L7) constructor. What is `game`? After reading the code, I understand that it is the game state, but it is unclear.
  - Rendering functionality relies on previously rendered pictures of tiles.

- [-5] The game state does not have a method for scoring a placement. 
  - The subtasks for scoring are distirbuted among multiple methods in the map and the game state and the purpose statement of some of these methods do not match to their signature. For example `q_completed` method returns a number instead of a boolean. 
  - There is no composite scoring method with a clear signature and purpose statement that combines these multiple helper methods.

- [-10] No unit tests for scoring a placement
- [-5] None of the methods related to scoring checks the number of tiles placed.
- [-5] None of the methods related to scoring checks the bonus for finishing (player places all tiles in their possession).


## Design [0/10]
- The design lists some methods but it is unclear
  - whether the methods are in referee or players
  - who calls the methods on who
  - in which order the methods will be called
- The design also conflates the logical protocol between the referee and the players with remote protocol (JSON, TCP)

At minimum, a player should have a method to `take turn` and `accept tiles`. The referee first calls `take turn` method on the player to inform the player about the current state of the game and receive their desired move. The referee than calls `accept tiles` method on the same player to give the player as many tiles as they placed or exchanged.  
