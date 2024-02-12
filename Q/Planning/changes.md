**1. changing the bonus points again and allow more players to participate in a game**

**RANK:** 1
Our current code base can add more than 4 players to the game without a problem. As for changing the bouns points all we need to do is change the value of the global variable 'Q_COMPLETE_POINTS' and 'COMPLETE_HAND_POINTS' which is located in Q/Common/game_state.py.

**2. adding wildcard tiles**

**RANK:** 4
Adding wildcards wouldn't be a straightforward task, as it would necessitate significant modifications to many methods within the map class, such as 'can_play_piece_here,' 'q_completed,' and their helper methods. Instead, we could try having the wildcard iterate through each color and shape, essentially pretending to be each one. We would implement this functionality in the Piece class located in Q/Common/map.py. While this approach simplifies the implementation process, it's worth noting that it may significantly increase the computational runtime of the game, making it less than ideal in terms of performance.

**3. imposing restrictions that enforce the rules of Qwirkle instead of Q**

**RANK:** 3
The major differences about Qwirkle rules compared to Q rules is number of starting referee tiles, trading some of your tiles not all, rotation order. For this we can make an abstract Referee and change some of the methods so that they follow the rulls of Qwirkle. Right now we just have a Referee class but it would not be hard abstracting it out.