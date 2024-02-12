# This player will preform cheats 
# it will take in the cheat that it is going to preform as an argument
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, '..'))
from Common.public_game_state import PublicState
from Common.turn import Turn
from Common.map import Piece
from Player.player import Player, Birthday
from Player.strategy import Strategy

class Cheating_Player(Player):
    def __init__(self, name, birthday, strategy=None, cheat=None):
        super().__init__(name, birthday, strategy)
        self.cheat = cheat
        
    def non_adjacent_coordinate(self, public_state):
        for tile in self.tiles:
            positions = public_state.board.get_valid_locations(tile)
            if positions:
                non_adj_coord = positions[0]
                non_adj_coord.row += 1081
                return (Turn.place, [(tile, non_adj_coord)])
        return (Turn.exchange, [])
    
    def no_fit(self, public_state):
        self.tiles.append(Piece("board", "board"))
        for tile in self.tiles:
            positions = public_state.board.get_valid_locations(tile)
            if positions:
                return (Turn.place, [(Piece("board", "board"), positions[0])])
        return (Turn.exchange, [])
    
    def tiles_not_owned(self, public_state):
        if not Piece("square", "red") in self.tiles:
            positions = public_state.board.get_valid_locations(Piece("square", "red"))
            if positions:
                return (Turn.place, [(Piece("square", "red"), positions[0])])
        if not Piece("square", "blue") in self.tiles:
            positions = public_state.board.get_valid_locations(Piece("square", "blue"))
            if positions:
                return (Turn.place, [(Piece("square", "blue"), positions[0])])
        if not Piece("square", "green") in self.tiles:
            positions = public_state.board.get_valid_locations(Piece("square", "green"))
            if positions:
                return (Turn.place, [(Piece("square", "green"), positions[0])])
        if not Piece("square", "purple") in self.tiles:
            positions = public_state.board.get_valid_locations(Piece("square", "purple"))
            if positions:
                return (Turn.place, [(Piece("square", "purple"), positions[0])])
        if not Piece("square", "orange") in self.tiles:
            positions = public_state.board.get_valid_locations(Piece("square", "orange"))
            if positions:
                return (Turn.place, [(Piece("square", "orange"), positions[0])])
        if not Piece("square", "yellow") in self.tiles:
            positions = public_state.board.get_valid_locations(Piece("square", "yellow"))
            if positions:
                return (Turn.place, [(Piece("square", "yellow"), positions[0])])
        return (Turn.exchange, [])

    def take_turn(self, pub_state):
        if self.cheat == "non-adjacent-coordinate":
            return self.non_adjacent_coordinate(pub_state)
        elif self.cheat == "tile-not-owned":
            return self.tiles_not_owned(pub_state)
        elif self.cheat == "not-a-line":
            return Strategy.get_next_turn(pub_state, self.tiles, Strategy.dag_cheat)
        elif self.cheat == "no-fit":
            return self.no_fit(pub_state)
        if self.cheat == "bad-ask-for-tiles":
            self.tiles += [Piece("square", "red"), Piece("square", "red"), Piece("square", "red"), Piece("square", "red"), Piece("square", "red"), Piece("square", "red"), Piece("square", "red"), Piece("square", "red"), Piece("square", "red")]
            return (Turn.exchange, [])
        return super().take_turn(pub_state)

    def new_tiles(self, st):
        if self.cheat == "bad-ask-for-tiles":
            self.tiles += [Piece("square", "red"), Piece("square", "red"), Piece("square", "red"), Piece("square", "red"), Piece("square", "red"), Piece("square", "red"), Piece("square", "red"), Piece("square", "red"), Piece("square", "red")]
            return (Turn.exchange, [])
        super().new_tiles(st)