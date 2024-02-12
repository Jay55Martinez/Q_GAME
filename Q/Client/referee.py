import sys
import socket
import logging
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, '..'))
from Player.player import *
from Common.json_io import *


# Represents a Proxy Referee which communicates directly with the player
# Fields:
#   - player: said player
#   - socket: socket to send/recieve to/from
class ProxyRef():
    def __init__(self, socket, player):
        self.player = player
        self.socket = socket
        
    
    def _send(self, message):
        self.socket.send(message.encode('utf-8'))

    def _receive(self):
        response = self.socket.recv(1024).decode('utf-8')
        return response

    # Waits for instructions from the server and executes instruction
    def _listen_for_instruction(self):
        instruction = self._recieve()
        # TODO - What is the terminate message
        terminate_instruction = "eliminated"
        while instruction != terminate_instruction: 
            instruction_type = instruction.keys()[0]
            if instruction_type == 'take-turn':
                self.take_turn(instruction)
            elif instruction_type == 'new-tiles':
                self.new_tiles(instruction)
            elif instruction_type == 'win':
                self.win(instruction)
                break
            
            instruction._receive()

        self.socket.close()

    # Takes this j_take_turn and has the player take a turn
    def take_turn(self, j_take_turn):
        j_pub = j_take_turn["take-turn"]
        pub_state = Json_io.to_j_pub(j_pub[0])
        turn_type, placements = self.player.take_turn(pub_state)
        
        j_turn = Json_io.to_j_turn(turn_type, placements)
        self.send(j_turn)
        
    # Takes this JSetup(JPub, JTile) and sets up the player
    def setup(self, j_setup):
        j_setup = j_setup["setup"]

        pub_state = Json_io.to_j_pub(j_setup[0])
        tiles = Json_io.to_j_tiles(j_setup[1])
        
        self.player.setup(pub_state, tiles)
        self._send("void")
        self._listen_for_instruction()
    
    # Take this JTile and give the new tile to the player
    def new_tiles(self, JTiles):
        tiles = Json_io.from_j_tiles(JTiles)
        self.player.new_tiles(tiles)
        self._send("void")
        
        
    def win(self, JWon):
        won = Json_io.from_j_won(JWon)
        self.player.win(won)
        self._send("void")
