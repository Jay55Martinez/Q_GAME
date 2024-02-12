import sys
import time
import json
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, '..'))
from Player.strategy import Strategy
from Player.player import Player, Birthday
from Common.json_io import *
from Common.public_game_state import PublicState

#        ____                      ____  _                       
#       |  _ \ _ __ _____  ___   _|  _ \| | __ _ _   _  ___ _ __ 
#       | |_) | '__/ _ \ \/ / | | | |_) | |/ _` | | | |/ _ \ '__|
#       |  __/| | | (_) >  <| |_| |  __/| | (_| | |_| |  __/ |   
#       |_|   |_|  \___/_/\_\\__, |_|   |_|\__,_|\__, |\___|_|   
#                            |___/               |___/           

# Represents a Proxy Player which comunicates to an actual Player through a ProxyReferee.
# Proxy Player inherits the Player class
class ProxyPlayer(Player):
    
    def __init__(self, name, socket, wait_time=None, strategy=None):
        
        super.__init__(name, 0, strategy)
        self.socket = socket
        if wait_time == None:
            self.wait_time = 5
        else:
            self.wait_time = wait_time
     
            
    def __repr__(self):
        return Player.__repr__(self) + f', Socket: {self.socket}'
    
    def __eq__(self, __value: object) -> bool:
        try:
            return Player.__eq__(self, __value) and self.socket == __value.socket
        except TypeError as e:
            return False
        
    #__Private_Methods__#
    
    def _send_and_recieve(self, message):
        """sends a message to prox_referee and waits for a responce to return

        Args:
            message (str): a string in json format
        Returns:
            str : a string in json format
        """
        self.socket.send(message.encode('utf-8'))
        response = self.socket.recv(1024).decode('utf-8')
        return response
        
    
    def _send(self, message):
        """sends a message to this prox_referee and does not wait for a responce

        Args:
            message (str): a sting in json format
        """
        self.socket.send(message.encode('utf-8'))
        current_time = time.time()
        while time.time() - current_time <= self.wait_time:
            response = self.socket.recv(1024).decode('utf-8')
        if response != "void":
            raise RuntimeError("player did not recieve void")

    
    #___________________#
        
    def take_turn(self, pub_state):
        """Takes this public state and sends it as a take-turn message.

        Args:
            pub_state (PublicState): the public knowledge of the current GameState.

        Returns:
            Tuple(Turn, [(Placement, Piece)]) : Turn denotes the move type: place, exchange, or pass.
            the list of tuples of Placements and Pieces denotes the placements of a place move.
        """
        self.public_state = pub_state
        j_take_turn = json.dumps({"take-turn":[Json_io.to_j_pub(pub_state)]})

        j_turn = self._send_and_recieve(j_take_turn)
        
        turn_type = Json_io.from_j_action(j_turn["turn-type"])
        turn_placements = Json_io.from_j_placements(j_turn["tile*"])

        return (turn_type, turn_placements)
    
    def setup(self, m, st):
        """Takes the public state and the tiles and sends a setup message to this ProxyReferee.

        Args:
            m (PublicState): the public knowledge of the GameState.
            st ([Tile]): list of tiles for the players hand.
        """
        self.public_state = m
        self.tiles = st
        j_setup = json.dumps({"setup" : [Json_io.from_j_pub(m), Json_io.from_j_tiles(st)]})
        self._send(j_setup)
                
    def new_tiles(self, ts):
        """Takes the list of tiles and sends it as a new-tiles message to this ProxyReferee.

        Args:
            ts ([Tile]): list of tiles for the players hand.
        """
        self.tiles += ts
        
        j_new_tiles = {"new-tiles" : [Json_io.from_j_tiles(ts)]}
        
        self._send(j_new_tiles)
    
    def win(self, won):
        """Sends a win message to this ProxyReferee letting the player know if they won or not.

        Args:
            won (Bool): True if the player won False if the player lost.
        """
        self.won_game = won
        j_win = json.dumps({"win" : [Json_io.from_j_win(won)]})
        self._send(j_win)