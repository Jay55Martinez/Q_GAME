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
from map import *
from turn import Turn
from Player.player import Player, Birthday
from Player.strategy import Strategy

# public method for initializing the starting tiles
def get_starting_tiles(num_each):
    
    shape_list = [s for s in Shapes]
    color_list = [c for c in Colors]
    piece_list = []
    for i in range(0, len(shape_list)-1):
        for j in range(0, len(color_list)-1):
            for _ in range(num_each):
                piece_list.append(Piece(shape_list[i].name, color_list[j].name))
    return piece_list

STARTING_TILES = get_starting_tiles(30)
POINTS_FROM_Q = 8
POINTS_FROM_FINISH = 4

#          ____                      ____  _        _       
#         / ___| __ _ _ __ ___   ___/ ___|| |_ __ _| |_ ___ 
#        | |  _ / _` | '_ ` _ \ / _ \___ \| __/ _` | __/ _ \
#        | |_| | (_| | | | | | |  __/___) | || (_| | ||  __/
#         \____|\__,_|_| |_| |_|\___|____/ \__\__,_|\__\___|

# Represents the information that the referee knows. i.e the private knowledge of the game


class GameState:

    def __init__(self, referee_tiles=None, num_of_each_tile=30, players=None, start_piece=None):
        self.points_from_q = POINTS_FROM_Q
        self.points_from_finish = POINTS_FROM_FINISH
        
        if referee_tiles: # set list of referee tiles
            self.referee_tiles = referee_tiles
        else: # create referee tiles
            self.referee_tiles = []
            self.referee_tiles = get_starting_tiles(num_of_each_tile) # makes 30 of each tile by default
            random.shuffle(self.referee_tiles)
    
        self.players = players 

        

        if start_piece:
            self.board = Board(start_piece)
            self.referee_tiles.remove(start_piece)
        else:
            self.board = Board(self.referee_tiles.pop())

        if players == None:
            self.players = []
            self.game_over = True
        if len(self.players) != 0:
            # turn order
            self.turn_queue = self.get_player_order()
            self.current_player = self.get_next_player()
            self.starting_player = self.current_player
        
            self.game_over = False
        self.eliminated_players = []
        self.pass_exchange_counter = 0
        
    # creates a deepcopy of the gamestate
    def __deepcopy__(self, memo):
        new_state = GameState()
        new_state.referee_tiles = copy.deepcopy(self.referee_tiles)
        new_state.board = copy.deepcopy(self.board)
        new_state.players = copy.deepcopy(self.players)
        new_state.current_player = copy.deepcopy(self.current_player)
        new_state.game_over = copy.deepcopy(self.game_over)
        new_state.starting_player = copy.deepcopy(self.starting_player)
        new_state.pass_exchange_counter = copy.deepcopy(self.pass_exchange_counter)
        new_state.turn_queue = self.turn_queue
        return new_state
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, GameState):
            return False
        return self.board == __value.board and self.players == __value.players and\
                self.referee_tiles == __value.referee_tiles

    def get_player_order(self):
        """Sorts the players in order of youngest to oldest based on the players birthday

        Returns:
            Queue(Player): sorted queue of players from yongest to oldest
        """
        turn_order = queue.Queue(len(self.players))

        sorted_player_list = self.players #sorted(self.players, key=lambda x: x.birthday)
        for player in sorted_player_list:
            turn_order.put(player)
        return turn_order
    
    # test
    def get_winners(self):
        """returns the player with the highest score
        
        Returns:
            Player : the player with the higheset score
        """
        winner_players = []
        if self.game_over:
            winner_players = [self.players[0]]
            for player in self.players:
                if player.score > winner_players[0].score:
                    winner_players = [player]
                # Checking if the scores are the same, second condition to stop double counting
                elif player.score == winner_players[0].score and player != self.players[0]:
                    winner_players.append(player)
            winner_players = [player.name for player in winner_players]
            sorted_winner_players = sorted(winner_players)
        return sorted_winner_players


    def get_next_player(self):
        """Iterate one time over the turn_queue and append the player at the front to the back and sets that player as the current player

        Returns:
            Player: the players who turn it is
        """
        next_player = self.turn_queue.get()
        self.turn_queue.put(next_player)
        self.current_player = next_player
        return next_player
    
    def get_placed_pieces(self):
        """returns all the pieces currently on the board

        Returns:
            Piece[]: list of all the pieces currently on the board
        """
        return self.board.get_all_pieces()
    
    def remove_current_player(self):
        """removes a player from the game state and keeps the current player order

        Args:
            player (Player): the Player that will be removed from the game state
        
        Side Affects:
            appends current player to emiminated player list then removes given player from self.players and self.turn_order
            if the starting player of the turn was to be removed then the next player is now assigned as the new starting player
        """
        if len(self.players) == 1:
            raise RuntimeWarning('can not remove players the last player of the game')
        
        self.referee_tiles.append(self.current_player.remove_return_tiles()) # adds player tiles back to referee tiles
        
        self.eliminated_players.append(self.current_player)
        self.players.remove(self.current_player)
        
        if self.starting_player == self.current_player:
            cur_player = self.turn_queue.get()
            self.starting_player = cur_player
        else:
            cur_player = self.turn_queue.get()
            
        # creates the new queue with out a player
        self.turn_queue = self.get_player_order()
        
        while not cur_player == self.current_player:
            self.get_next_player()
            
    def pass_exchage_updater(self, turn_type, player_name):
        """ Used to keep track of how many passes
        or exchanges have taken place in the past
        round of turns.
        
        Args:
            turn_type (Turn): type of last turn
            player_name: name of player 
        """

        if self.starting_player == self.find_player_with_name(player_name):
            self.pass_exchange_counter = 0
        if turn_type == Turn.place:
            self.pass_exchange_counter = 0
        else:
            self.pass_exchange_counter += 1

    def commit(self, turn, player_name, turn_status, tiles=None, locations=None):
        """executes a game action updating the attributes of the game state

        Args:
            turn (Enum Turn): the action that will be taken place, pass_turn, exchange
            player_name (id): the id of the player that is taking the turn
            turn_status (Enum Status) : used to determine if a move is valid or if the game should be over
            tiles (Piece[], optional): List of Pieces for the place turn option. Defaults to None.
            locations (Position[], optional): List of Positions for the place turn option. Defaults to None.
        """
        try:
            if turn_status == Status.Success:
                if turn == Turn.place:
                    for tile, location in zip(tiles, locations):
                        self.board.raw_place(tile, location)
                    self.current_player.score += self.score_move(locations)
                    self.give_tiles_after_move(tiles)
                    self.get_next_player() # end of turn

                elif turn == Turn.exchange:
                    self.swap_pieces(player_name)
                    self.get_next_player() # end of turn 
                    
                elif turn == Turn.pass_turn:
                    self.get_next_player()
                    
            elif turn_status == Status.Failure:
                self.remove_current_player()
                
            elif turn_status == Status.GameOver:
                if turn == Turn.place: # there is not enough tile to give back player scores its last move
                    for tile, location in zip(tiles, locations):
                        self.board.raw_place(tile, location)
                    
                    self.current_player.score += self.score_move(locations)
                
                self.game_over = True
                self.player_game_over()
                    
        except RuntimeError:
            self.remove_current_player()
        except RuntimeWarning:
            self.player_game_over()
    
    def player_game_over(self):
        """Alerts the players that the game is over and assigns winners
        """
        try:
            for player in self.players:
                player.game_over()
            
            
            for player_name in self.get_winners():
                player = self.find_player_with_name(player_name)
                player.win(True)
        except RuntimeError:
            pass
    
    def give_tiles_after_move(self, tiles):
        """give the current player tiles back equal to the number of tiles that are placing

        Args:
            tiles (Pieces[]): the tiles the player uses

        Exception: 
            RuntimeError can't give the player their tiles because there are not any left to give
        """
        try:
            for tile in tiles:
                self.current_player.remove_tile(tile)
            if self.number_unused() > len(tiles):
                self.current_player.new_tiles(self._get_tiles_to_deal(len(tiles)))
        except RuntimeError:
            self.remove_current_player()
            
    def score_move(self, locations):
        """returns as a score based on the given locations on this gamestates board

        Args:
            locat"non-adjacent-coordinateions (Position[]): list of positions to score

        Returns:
            int: the result of scoring
        """
        turn_score = len(locations)
        turn_score += self.board.num_contiguous_pieces(locations)
        turn_score += self.points_from_q * self.board.q_completed(locations)
        if len(locations) == 6:
            turn_score += self.points_from_finish
        return turn_score
        
    def swap_pieces(self, player_name):
        """swaps the tiles of the current player with referee tiles

        Args:
            player_name (int): the player that is preforming the swap
        
        Side Affects:
            player recieves 6 new tiles and game state referee tiles gets the player tiles add to it then deals out 6
        """
        try:
            player = self.find_player_with_name(player_name)
            pieces_from_ref = self._get_tiles_to_deal(6)
            current_player_pieces = player.remove_return_tiles()
            self.referee_tiles += current_player_pieces
            player.new_tiles(pieces_from_ref)
        except RuntimeError:
            self.eliminate_player_name(player_name)
            
    def setup_player(self, player_name):
        """deals the player its opening hand and also passes it the public knowledge of the game

        Args:
            player_name (int): the player id
            
        Side Affects:
            player gets 6 tiles and the public knowledge of the game state
        """
        try:
            player = self.find_player_with_name(player_name)
            tiles = self._get_tiles_to_deal(6)
            player.setup(self.create_public_state(), tiles)
        except RuntimeError:
            self.eliminate_player_name(player_name)

        
    def eliminate_player_name(self, player_name):
        """Eliminates the player with the given name

        Args:
            player_name (str): name of the player to be elminated
        """
        try:
            player = self.find_player_with_name(player_name)
            self.players.remove(player)
            self.eliminated_players.append(player)
        except ValueError as e:
            print(e)
    
    def find_player_with_name(self, name):
        """returns the player that has the same id in this gamestate

        Args:
            id (str): the player name that we are searching to find a match of

        Raises:
            ValueError: if the id does not match any of the player ids in the game state

        Returns:
            Player: the player with the matching id
        """
        for player in self.players:
            if player.name == name:
                return player
        raise ValueError(f"player_name:{name} does not match any of the current player names")
    
    def number_unused(self):
        """returns the number of unused referee tiles

        Returns:
            int: the number of unused referee tiles
        """
        return len(self.referee_tiles)
        
    def _get_tiles_to_deal(self, num):
        """Private method that deals each player 6 tiles from the referee tiles method used when initializing the game_state
        
        Args:
            num (int) : number of tiles to deal out
            
        Side Effects:
            Remove 6 tiles from referee tiles and return them as a list.
        """
        if num < 0:
            raise ValueError("Can not deal a negative number of tiles")
        random.shuffle(self.referee_tiles)
        tiles = []
        if num > 0:
            for x in range(0, num):
                tile = self.referee_tiles.pop()
                tiles.append(tile)      
            return tiles
    
    def create_public_state(self):
        """creates a public game state based on the current state

        Returns:
            PublicState: the public game state representation
        """
        player_scores = [self.current_player.score]
        copy_of_players = copy.deepcopy(self.players)
        copy_of_players.remove(self.current_player)
        for player in copy_of_players:
            player_scores.append(player.score)
        return PublicState(self.board, self.number_unused(), player_scores, self.current_player)
    
    def _player_eliminated(self, player_name):
        """Checks if the given player is eliminated in this game state

        Args:
            player_name (str): the name of the player

        Returns:
            Bool: true if the player is eliminated
        """
        return self.find_player_with_name(player_name) in self.eliminated_players