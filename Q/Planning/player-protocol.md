# Player-Referee Interaction Protocol

In the context of future TCP communication using JSON objects, we need to define a concise protocol for player actions and how the referee should respond. Below is the structured Player-Referee Interaction Protocol:

## Player Actions

### 1. Place a Tile on the Board

- **Method**: `place_tile(player_id, tiles, locations)`

   - `player_id`: Unique player identifier initiating the action.
   - `tiles`: List of `Piece` objects to be placed.
   - `locations`: List of `Location` objects specifying where each tile should be placed on the board.

### 2. Exchange Tiles with the Referee

- **Method**: `exchange_tiles(player_id)`

   - `player_id`: Unique player identifier initiating the action.

### 3. Pass the Turn

- **Method**: `pass_turn(player_id)`

   - `player_id`: Unique player identifier passing the turn.

### 4. JSON Move

- **Definition**: Will take in a json_object structured in a way to represent one of the three actions that a player can take. The method will then call the corresponding methods.

- **Method**: `json_move(json_object)`

   - `json_object`: A JSON object structured for a player to request a move.

Each of these methods will create a `GameAction` data structure containing the details of the turn action. `GameAction` has the following fields:

- `action`: A string with values 'place', 'exchange', or 'pass'.
- `pieces`: A list of `Piece` objects to place.
- `location`: A list of positions specifying where to place the tile.

`pieces` and `locations` can both be empty when the `GameAction` represents a pass action

## Referee Response

The `Referee` class should listen for these actions and implement a method like `process_player_action(player_id, GameAction)`. It should accept a `GameAction` and perform the following steps:

1. Check if the move is valid.
2. Update the `GameState` accordingly.

This protocol facilitates communication between players and the referee in a structured and efficient manner, ensuring the integrity of the game. It prepares for future TCP communication by handling JSON moves as well.