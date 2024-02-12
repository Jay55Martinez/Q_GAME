import copy
import json
import queue
import random
import os
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import sys
import re
from json import JSONDecoder, JSONDecodeError
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, '..'))
from json_io import Json_io
from public_game_state import PublicState
from game_state import GameState
from map import *
from turn import Turn
from Player.player import Player, Birthday
from Player.strategy import Strategy


#          ____                      ____  _        _       
#         / ___| __ _ _ __ ___   ___/ ___|| |_ __ _| |_ ___ 
#        | |  _ / _` | '_ ` _ \ / _ \___ \| __/ _` | __/ _ \
#        | |_| | (_| | | | | | |  __/___) | || (_| | ||  __/
#         \____|\__,_|_| |_| |_|\___|____/ \__\__,_|\__\___|

# Represents the information that the referee knows. i.e the private knowledge of the game


class GameStateSpec(GameState):

    def __init__(self, config, score_configs):
        self.config = config
        self.score_configs = score_configs
        self.board = Json_io.from_j_map(json.dumps(config['map']))
        self.referee_tiles = Json_io.from_j_tiles(json.dumps(config['tile*']))
        self.players = [Json_io.from_j_player(json.dumps(jplayer)) for jplayer in config['players']]
        self.points_from_q = score_configs['qbo']
        self.points_from_finish = score_configs['fbo']
        self.eliminated_players = []
        self.pass_exchange_counter = 0
        self.game_over = False
        self.turn_queue = self.get_player_order()
        self.current_player = self.get_next_player()
        self.starting_player = self.current_player
        
    # creates a deepcopy of the gamestate
    def __deepcopy__(self, memo):
        new_state = GameStateSpec(self.config, self.score_configs)
        new_state.referee_tiles = copy.deepcopy(self.referee_tiles)
        new_state.board = copy.deepcopy(self.board)
        new_state.players = copy.deepcopy(self.players)
        new_state.current_player = copy.deepcopy(self.current_player)
        new_state.game_over = copy.deepcopy(self.game_over)
        new_state.starting_player = copy.deepcopy(self.starting_player)
        new_state.pass_exchange_counter = copy.deepcopy(self.pass_exchange_counter)
        new_state.turn_queue = self.turn_queue
        return new_state
    
    def get_player_order(self):
        """Sorts the players in order of youngest to oldest based on the players birthday

        Returns:
            Queue(Player): sorted queue of players from yongest to oldest
        """
        turn_order = queue.Queue(len(self.players))

        for player in self.players:
            turn_order.put(player)
        return turn_order
       
    def setup_player(self, player_name):
        try:
            player = self.find_player_with_name(player_name)
            if len(player.tiles) > 0:
                player.setup(self.create_public_state(), player.tiles)
            else:
                tiles = self._get_tiles_to_deal(6)
                player.setup(self.create_public_state(), tiles)
        except RuntimeError:
            self.eliminate_player_name(player_name)