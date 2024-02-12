import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, '..'))
from Common.public_game_state import PublicState
from Player.strategy import Strategy

#         ____  _                       
#        |  _ \| | __ _ _   _  ___ _ __ 
#        | |_) | |/ _` | | | |/ _ \ '__|
#        |  __/| | (_| | |_| |  __/ |   
#        |_|   |_|\__,_|\__, |\___|_|   
#                       |___/           

# represents an ai player 
class Player:
    def __init__(self, name, birthday, strategy=None):
        self.name = name
        self.score = 0
        self.birthday = birthday
        self.tiles = []
        self.strategy = strategy
        self.public_state = None
        self.won_game = False
        self.game_complete = False
    
    def __repr__(self):
        return f"Name: {self.name}, Score: {self.score}, Birthday: {self.birthday}, Num Tiles: {len(self.tiles)}"
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Player):
            return False
        return self.birthday == __value.birthday and self.score == __value.score and\
            self.name == __value.name and self.tiles == __value.tiles
    
    def set_tiles(self, tiles):
        self.tiles = tiles
    
    def set_score(self, score):
        self.score = score

    def take_turn(self, pub_state):
        """the turn actions that a player can do
        - Pass
        - Replace : ask the referee to replace a set of tiles
        - Extention : request the extension of the map in given state with some tile placements

        Args:
            pub_state (PublicState): The general knowelge of the game which is the current tiles placed and the scores of the other players
            
        Returns:
            (Turn, ([Tile], [Position]))
            
        Side Affects:
            Makes changes to the game state based on the action that the player preforms
        """
        self.public_state = pub_state
        return Strategy.get_next_turn(pub_state, self.tiles, self.strategy)

    def get_sorted_tiles(self):
        """Returns the smallest tile that the player owns using the lexographic ordering defined in Piece.

        Returns:
            Piece[]: _descrireturns a sorted list of piecesption_
        """
        return sorted(self.tiles)
    
    def setup(self, m, st):
        """deals the player their hand and gives them the most current map information

        Args:
            m (PublicState): the public knowledge of the gamestate
            st (Piece[]): the players starting hand
            
        Side Affects:
            adds 6 new tiles to tiles ie the hand. The player now has informaion on the board
        """
        self.public_state = m
        self.tiles = st
    
    def remove_tile(self, tile):
        """removes the given tile from this players hand

        Args:
            tile (Piece): the piece to be removed form this players hand
            
        Side Affect:
            removes a tile from self.tiles
        """
        self.tiles.remove(tile)
    
    def get_name(self):
        """returns the name of the player
        
        Returns:
            The player id
        """
        return self.name
    
    def win(self, w):
        """updates the players win clause true if they won false if they lost
        
        Args:
            w (bool): true if player has won false if the player has not won
        """
        self.win_game = w
        
    def new_tiles(self, st):
        """gives the player a new hand of 6 tiles

        Args:
            st (Piece[]): the list of new pieces that the player recieves
        
        Side Affects:
            appends st to tiles giving the player new tiles in their hand
        """
        self.tiles += st

    def remove_return_tiles(self):
        """Removes and returns this players tiles

        Returns:
            Piece[]: the tiles were in the players hand
            
        Side Affects:
            removes all tiles in players hand
        """
        removed_tiles = self.tiles
        self.tiles = []
        return removed_tiles
    
    def recieve_current_public_state(self, pub_state):
        """gives this player the public state of the game

        Args:
            pub_state (PublicState): a public state of the game
        
        Side Affects:
            player gets a new public state
        """
        self.public_state = pub_state
        
    def game_over(self):
        """lets the player know that the game is over
        """
        self.game_complete = True
    
    
# represents a valid birthday
class Birthday:
    def __init__(self, month, day, year):
        if not self.is_valid_date(month, day, year):
            raise ValueError("Invalid date")
        self.month = month
        self.day = day
        self.year = year

    def is_valid_date(self, month, day, year):
        """ Returns True if the provided month,
        day and year is a valid month
        
        Args:
            month: numeric month
            day: numeric day
            year: numeric year

        Returns:
            bool: True if month is valid, False otherwise
        """

        if not (0 < month <= 12) or not (0 < day <= 30) or not (0 < year <= 2023):
            return False

        if month == 2:
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                if day > 29:
                    return False
            else:
                if day > 28:
                    return False
        elif month in [4, 6, 9, 11]:
            if day > 30:
                return False

        return True

    def __eq__(self, other):
        if not isinstance(other, Birthday):
            raise TypeError("Can't compare a Birthday object to a non-Birthday object")
        return self.year == other.year and self.month == other.month and self.day == other.day
    
    def __lt__(self, other):
        if not isinstance(other, Birthday):
            raise TypeError("Can't compare a Birthday object to a non-Birthday object")
        # Compare based on the year, if years are different
        if self.year != other.year:
            return self.year > other.year
        # If years are the same, compare based on month
        if self.month != other.month:
            return self.month > other.month
        # If years and months are the same, compare based on day
        return self.day > other.day
    
    def __repr__(self) -> str:
        return f'{self.month}/{self.day}/{self.year}'