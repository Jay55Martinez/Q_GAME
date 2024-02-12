import sys
import logging
import os
import copy

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, '..'))
from Referee.referee import Referee
from Common.game_state import GameState
from Common.game_state_spec import GameStateSpec
from Common.turn import Turn
from Referee.observer import Observer

#        ____                      ____       __                    
#       |  _ \ _ __ _____  ___   _|  _ \ ___ / _| ___ _ __ ___  ___ 
#       | |_) | '__/ _ \ \/ / | | | |_) / _ \ |_ / _ \ '__/ _ \/ _ \
#       |  __/| | | (_) >  <| |_| |  _ <  __/  _|  __/ | |  __/  __/
#       |_|   |_|  \___/_/\_\\__, |_| \_\___|_|  \___|_|  \___|\___|
#                            |___/                                  

# RefereeSpec represents a Referee that takes in a spec and runs a Q game based on that spec.
# RefereeSpec inherits the Referee class

class RefereeSpec(Referee):
    
    def __init__(self, config):
        self.state = GameStateSpec(config['state0'], config['config-s'])
        self.quiet = config['quiet']
        self.per_turn = config['per-turn']
        self.display_observer = config['observe']
        # NOTE - Just here for testing
        self.observers = [Observer()]
        self._update_observers_states(copy.deepcopy(self.state))
        self.logger = logging.getLogger(__name__)
        if self.quiet:
            self.logger.setLevel(logging.CRITICAL)
        else:
            self.logger.setLevel(logging.DEBUG)