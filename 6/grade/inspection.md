Pair: mysterious-mongooses \
Commit: [386879e93c55c32669bb5c06b40edb66e5daa68d](https://github.khoury.northeastern.edu/CS4500-F23/mysterious-mongooses/tree/386879e93c55c32669bb5c06b40edb66e5daa68d) \
Self-eval: https://github.khoury.northeastern.edu/CS4500-F23/mysterious-mongooses/blob/fd8c744563de57661858ee00a529abca64d12628/6/self-6.md \
Score: 105/210 \
Grader: Jessica Su

95/180: Programming Task:\
-55: no self eval\
-10: There should be one function that manages an individual round. This is so that we can if a round consisted of all passes or all replacements where we would end the game\
-10: Referee does not inform winners that they won or lost\
-10: Managing an individual turn should be in one function. This allows us to kick out and recognize the behavior misbehaving players which may never return a result, throw an error, etc. in the take turn function which should be implemented

10/30: Design Task:\
-10: Referee should instantiate an observer that receives game states after a turn. The referee should inform observer of a new game state after every turn. The observer be able to display the past or current map, score, and players in the game. The game state does not have enough information about when a turn has finished to be able to update the observer. "When a turn has finished" include scoring the turn, kicking out the player if the turn was invalid, and determining whether this turn resulted in the game ending.

To perform one turn, the referee will need to call multiple game state functions in a order (function call to apply turn action, function call that kicks out player if move was invalid, function call to score the move, function call to check whether the game has ended etc) and only the referee knows to call upon these functions in this order and be able to update the observer after game state is updated with all information after turn.

-10: Does not describe how a single person may wish to interact with the observer’s view. One way of doing this is to have clickable arrows so that an user can go through visualized game states.
