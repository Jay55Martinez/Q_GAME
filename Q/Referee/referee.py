import sys
import logging
import copy
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, '..'))
from Player.player import Player, Birthday
from Server.player import ProxyPlayer
from Player.baddie_player import *
from Player.count_baddie_player import *
from Player.cheating_player import *
from Common.game_state import *
from Referee.observer import *
DISPLAY_OBSERVER = True
NUMBER_OF_EACH_TILES = 4

# Takes a sorted list of Players, and creates
# a new Referee to start a game.
def run_referee(players, referee=None):
    referee = Referee(players, display_observer=DISPLAY_OBSERVER, num_of_each_tile=NUMBER_OF_EACH_TILES, observers=[Observer(), Observer()])
    referee.setup_players()
    return referee.run_game()
        
#         ____       __                    
#        |  _ \ ___ / _| ___ _ __ ___  ___ 
#        | |_) / _ \ |_ / _ \ '__/ _ \/ _ \
#        |  _ <  __/  _|  __/ | |  __/  __/
#        |_| \_\___|_|  \___|_|  \___|\___|

# Handles turn actions from players ensuring that they follow the game rules and updates the gamestate.
class Referee:
    
    def __init__(self, p, state=None, num_of_each_tile=30, display_observer=False, observers=[], quiet=True):
        if state != None:
            self.state = state
        else:
            self.state = GameState(players=p, num_of_each_tile=num_of_each_tile)
            
        self.display_observer = display_observer
        self.observers = observers
        self._update_observers_states(copy.deepcopy(self.state))
        
        self.quiet = quiet
        if self.quiet:
            self.logger.setLevel(logging.CRITICAL)
        else:
            self.logger.setLevel(logging.DEBUG)


    def run_game(self):
        """This referee runs a complete Q game.

        Returns:
            List[List]: in the formate of: [[Winners], [Eliminated]] where Winners are the names of the players
            that won and Eliminated is the names of the players that were eliminated
        """
        try:
            self.setup_players()
        except IndexError:
            self.logger.debug("not enough players to start the game")
            self.state.game_over = True
        while not self._game_over():
            current_player = self.state.current_player
            try:
                player_turn_type, player_actions = current_player.take_turn(self._get_public_state())  # is a tuple
            except RuntimeError:
                if len(self.state.players) >= 2:
                    self.state.remove_current_player()
                else:
                    self.state.game_over = True
                    break
            placements = list(zip(*player_actions))
            if player_turn_type == Turn.place:
                self.accept_turn(player_turn_type, current_player.name, placements[0], placements[1])
            else:
                self.accept_turn(player_turn_type, current_player.name)

        if self.display_observer:
            for observer in self.observers:
                observer.render_observer()

        return [self._get_winners(), self._get_eliminated()]
    
    def setup_players(self):
        """This deals the starting 6 tiles to the players randomaly chooses tiles from the referee tiles
        
        Side Affects:
            Remove tiles from GameState referee tiles and add tiles to each players hand
        """
        if len(self.state.players) < 2:
            raise IndexError("not enough players to play")
        
        for player in self.state.players:
            self.state.setup_player(player.name)
    
    def validate_turn(self, turn, player_name, tiles, locations):
        """Validates the turn that the player is trying to make on this referee's ruleset 
        
        Failure:
        - player takes turn out of order
        - player makes illegal place move
        - player makes illegal exchange move
        
        GameOver:
        - player is the last one in the game not eliminated
        - player makes a valid place move and there are not enough tiles for this referee to give back
        - player makes a game over place move
        - player makes a game over exchange move
        
        Success:
        - player makes a valid place move
        - player makes a valid exchange move
        - player makes a pass move and and none of the conditions are met above

        Args:
            turn (Enum Turn): the type of turn that this player is trying to take
            player_name (string): the name of the player making the turn
            tiles (Piece[], optional): if the turn is a place turn these tiles are check if they can be place. Defaults to None.
            locations (Position[], optional): it the turn is a place turn there tiles are check if they can be placed. Defaults to None.

        Returns:
            Enum Status: Status Failure if the move is not valid else it returns true
        """
        if len(self.state.players) == 1:
            self.logger.debug(f"{player_name} is the only player left game over")
            return Status.GameOver
        
        if turn == Turn.pass_turn:
            return Status.Success

        if turn == Turn.exchange:
            return self._validate_exchange_turn(player_name)
        
        if turn == Turn.place:
            turn_move = self._validate_place_turn(player_name, tiles, locations) 
            if turn_move == Status.Success:
                if self.state.number_unused() < len(tiles): 
                    return Status.GameOver
                if len(tiles) == len(self.state.current_player.tiles):
                    return Status.GameOver
            return turn_move
        
        return Status.Success
        
    def accept_turn(self, turn, player_name, tiles=None, locations=None):
        """This referee checks the turn that the player wants to make and then commits it to the gamestate

        Args:
            turn (Enum Turn): They type of turn that the the player is taking
            player_name (str): the player name of the player that is taking this turn
            tiles (Piece[], optional): if the turn is a place turn these pieces will be placed on the board if they are valid. Defaults to None.
            locations (Position[], optional): if the turn is a place turn these locations will be used to place tiles if they are valid. Defaults to None.
        """ 
        turn_move = self.validate_turn(turn, player_name, tiles, locations)
        
        if turn_move == Status.Success:
            self.state.pass_exchage_updater(turn, player_name) # if a full rotation of passes happens then end game
            if self.state.pass_exchange_counter == len(self.state.players):
                turn_move = Status.GameOver
        
        self.state.commit(turn, player_name, turn_move, tiles, locations)
        
        if self.display_observer:
            self._update_observers_states(copy.deepcopy(self.state)) # update the observer after a turn is taken
        if self._game_over():
            self._update_observers_game_over()
        
    #----------------------------------#
    #         Private Methods          #
    #----------------------------------#
        

        
    def _validate_place_turn(self, player_name, tiles, locations):
        """Helper method decides if the given tiles and locations are valid placements on this referee's rule set
        
        Failure:
        - player is making a move with no placements
        - player tries to place tiles without having that tile tile in hand
        - player makes a move that does not follow the row/column color and shape restrictions 
        - player places multiple tiles not in the same row/column
        
        GameOver:
        - player places all tiles in it's hand
        
        Success:
        - player can do place the placements on the current board

        Args:
            player_name (str): the name of the player
            tiles (Piece[]): list of Pieces are are trying to be placed
            locations (Position[]): list of Positions where the pieces are trying to be placed

        Returns:
            Enum Status: returns status Failure if the placements are not valid else the placements are valid and returns Success
        """
        player = self.state.find_player_with_name(player_name)
        

        if len(tiles) == 0 or len(locations) == 0:
            self.logger.debug(f"{player_name} is making a place move without any placements")
            return Status.Failure 
        
        # ensuring that the player has these tiles to place in their hand
        for tile in tiles:
            if tile in player.tiles:
                continue
            self.logger.debug(f"{player_name} is making a move without owning these tiles")
            return Status.Failure
        
        first_placement = locations[0]
        # makes sure the player is playing to the same row/col
        for i in range(1, len(locations)):
            if locations[i].row != first_placement.row and\
                locations[i].column != first_placement.column:
                self.logger.debug(f"{player_name} is not placing tiles in the same column or row")
                return Status.Failure
        
        board_copy = copy.deepcopy(self.state.board)
        for tile, location in zip(tiles,locations):
            if not board_copy.can_play_piece_here(tile,location): # check on valid placements
                self.logger.debug(f"{player_name} is not a make a valid placement on the board")
                return Status.Failure
            board_copy.raw_place(tile, location)
        
        if len(tiles) == 6 & len(locations) == 6:
            self.logger.debug(f"{player_name} has finished there hand")
            return Status.GameOver
        
        return Status.Success
            
            
    def _validate_exchange_turn(self, player_name):
        """Helper method validates an exchange turn for this player
        
        Failure:
        - the player tries to exchange with more than 6 tiles in hand
        
        GameOver:
        - there is not enough referee tiles to give back
        
        Success:
        - the top conditions are not met

        Args:
            player_name (str): the player making the exchange turn

        Returns:
            Enum Status: the status of the move
        """
        if len(self.state.find_player_with_name(player_name).tiles) > 6:
            self.logger.debug(f"{player_name} is trying to exchange with more than 6 tiles in their hand")
            return Status.Failure
        elif self.state.number_unused() < 6:
            self.logger.debug(f"{player_name} has end the game since there no tiles left in the referee hand")
            return Status.GameOver
        else:
            return Status.Success
        

    def _current_players_turn(self):
        return self.state.current_player
    
    def _game_over(self):
        return self.state.game_over
    
    def _get_public_state(self):
        return self.state.create_public_state()
    
    def _get_winners(self):
        return self.state.get_winners()
    
    def _get_eliminated(self):
        return sorted([player.name for player in self.state.eliminated_players])
    
    def _update_observers_states(self, state_copy):
        for observer in self.observers:
            observer.update_state(state_copy)
            
    def _update_observers_game_over(self):
        for observer in self.observers:
            observer.update_game_over(self._game_over())

# FOR DEMO #
# sorted_players = sorted([Player('Jay', Birthday(4, 21, 2004), Strategy.dag), Player('Matt', Birthday(2, 21, 2003), Strategy.dag), Player('Matthias', Birthday(11, 2, 2001), Strategy.ldasg), Player('Michael', Birthday(8, 24, 1999), Strategy.dag), Player('Bill', Birthday(3, 21, 2006), Strategy.ldasg)], key=lambda x: x.birthday)
# run_referee(sorted_players)