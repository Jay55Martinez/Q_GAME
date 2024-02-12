#!/usr/bin/env python3
import pytest
import sys
sys.path.insert(0, '../../Common')
from game_state import *
from public_game_state import *
sys.path.insert(0, '../')
from player import *

def init_player():
    player1 = Player('Bill', Birthday(2, 21, 2003), Strategy.dag)
    player2 = Player('Jane', Birthday(8, 14, 1992), Strategy.ldasg)
    player3 = Player('Olivia', Birthday(3, 2, 2001), Strategy.dag)
    player4 = Player('James', Birthday(9, 12, 1997), Strategy.dag)
    l_player = [player1, player2, player3, player4]
    return l_player

def test_get_sorted_tiles():
    l_players = init_player()
    player1 = l_players[0]
    player2 = l_players[1]
    
    player1.tiles = [Piece('square', 'red'), Piece('star', 'blue'), Piece('square', 'purple'), Piece('8star', 'green'), Piece('clover', 'green'), Piece('diamond', 'orange')]
    assert player1.get_sorted_tiles() == [Piece('star', 'blue'), Piece('8star', 'green'), Piece('square', 'red'), Piece('square', 'purple'), Piece('clover', 'green'), Piece('diamond', 'orange')]
    
    player2.tiles = [Piece('diamond', 'green'), Piece('star', 'red'), Piece('star', 'purple'), Piece('star', 'green'), Piece('clover', 'red'), Piece('star', 'red')]
    assert player2.get_sorted_tiles() == [Piece('star', 'red'), Piece('star', 'red'), Piece('star', 'green'), Piece('star', 'purple'), Piece('clover', 'red'), Piece('diamond', 'green')]
    
def test_setup():
    l_players = init_player()
    player1 = l_players[0]
    player2 = l_players[1]
    player3 = l_players[2]
    player4 = l_players[3]
    
    player_scores = {player1.name:player1.score, player2.name:player2.score, player3.name:player3.score, player4.name:player4.score}
    public_state = PublicState(Board(Piece('square', 'red')), 9999, player_scores)
    
    t_hand = [BOARD_PIECE, BOARD_PIECE, BOARD_PIECE, BOARD_PIECE, BOARD_PIECE, BOARD_PIECE]
    player1.setup(public_state, t_hand)

    assert player1.tiles == t_hand
    assert player1.public_state == public_state
    
def test_get_name():
    l_players = init_player()
    player1 = l_players[0]
    
    assert player1.get_name() == 'Bill'
    
def test_win():
    l_players = init_player()
    player1 = l_players[0]
    
    assert not player1.win_game
    
    player1.win(True)
    assert player1.win_game
    
def test_new_tiles():
    l_players = init_player()
    player1 = l_players[0]
    
    player_hand = [Piece('star', 'green'), Piece('diamond', 'blue'), Piece('square', 'orange'), Piece('clover', 'blue')]
    player1.tiles = player_hand
    received_tiles = [Piece('square', 'green'), Piece('8star', 'orange')]
    player1.new_tiles(received_tiles)
    new_hand = [Piece('star', 'green'), Piece('diamond', 'blue'), Piece('square', 'orange'), Piece('clover', 'blue'), Piece('square', 'green'), Piece('8star', 'orange')]
    assert player1.tiles == new_hand
    
def test_remove_return_tiles():
    l_players = init_player()
    player1 = l_players[0]
    
    t_tiles = [BOARD_PIECE, BOARD_PIECE, BOARD_PIECE, BOARD_PIECE, BOARD_PIECE, BOARD_PIECE]
    player1.tiles = t_tiles
    
    assert player1.remove_return_tiles() == t_tiles
    assert player1.tiles == []
    
if __name__ == "__main__":
    pytest.main(["-v", "player_test.py"])