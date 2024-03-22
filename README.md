# Q Game - README

### Overview

The Q Game is a tile-based game inspired by Qwirkle. While it draws inspiration from the physical game, there are notable differences in its implementation. This program was writen over the course of a single semester as part of the CS4500 curriculum.

## Game Description

The Q Game is designed for 2 to 4 players who strategically place tiles on an infinitely large table. Players earn points by creating contiguous sequences of tiles based on color or shape. The game ends when a player uses all their tiles in a single turn or when all tiles are placed. The player with the highest total score wins.

## Remote Interaction

The interaction between remote player components and the remote admin framework is governed by predefined interaction diagrams. These diagrams outline the communication flow between server and client components, including setup, playing turns, and ending the game.

### Connecting to the Server

- Clients connect to the server and submit a name within 3 seconds.
- The server accepts TCP connections and represents each client as a remote player.
- The order of acceptance determines the age of the players.
- Once enough players have connected, the server initiates a game with a referee.

### Starting a Game

- The referee initiates game setup by sending a setup message to all proxy players.
- Proxy players relay this message to the actual clients, including the game state and a bag of tiles.
- This sets the stage for the game to begin.

### Playing Turns

- During gameplay, the referee communicates with the proxy players, who then interact with the actual players.
- Players take turns, making one of three possible actions: pass, replace tiles, or extend the game state by placing new tiles.
- The referee completes each turn based on the action taken by the player.

### Ending a Game

- Once the game reaches its conclusion, the referee sends a win message to each player, indicating whether they have won or lost.
- This message is relayed through the proxy players to the actual clients.

## Method Call Formats

- All interactions between components are realized through JSON-formatted function calls.
- Each function call consists of a method name and an array of arguments, ensuring interoperability between components in different languages.