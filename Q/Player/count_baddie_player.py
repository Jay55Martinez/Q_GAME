# Player that throws an exception on the given method on a count down
# This player extends the Player class
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, '..'))
from Common.public_game_state import PublicState
from Player.player import Player

class Count_Baddie_Player(Player):
    def __init__(self, name, birthday, strategy=None, exception_method=None, count_down=None):
        super().__init__(name, birthday, strategy)
        self.exception_method = exception_method
        self.count_down = count_down

    def setup(self, m, st):
        self.count_down -= 1
        if self.exception_method == Player.setup and self.count_down <= 0:
            raise RuntimeError("Baddie_Player: Cannot call setup method")
        super().setup(m, st)

    def take_turn(self, pub_state):
        self.count_down -= 1
        if self.exception_method == Player.take_turn and self.count_down <= 0:
            raise RuntimeError("Baddie_Player: Cannot call take_turn method")
        return super().take_turn(pub_state)

    def new_tiles(self, st):
        self.count_down -= 1
        if self.exception_method == Player.new_tiles and self.count_down <= 0:
            raise RuntimeError("Baddie_Player: Cannot call new_tiles method")
        super().new_tiles(st)

    def win(self, w):
        self.count_down -= 1
        if self.exception_method == Player.win:
            raise RuntimeError("Baddie_Player: Cannot call win method")
        super().win(w)