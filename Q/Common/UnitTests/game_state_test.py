#!/usr/bin/env python3
# Jay Martinez -- 10/17/2023
# Tests for the game_state class
import pytest
import sys
import copy
sys.path.insert        (0, '../')
from public_game_state import *
sys.path.insert(0, '../../Player')
from player import *
sys.path.insert(0, 'Common')
from game_state import *


def init_game_state():
    game = GameState(players=[Player("1", 13), Player("2", 12), Player("3", 9), Player("4", 12)], start_piece=Piece('square', 'red'))
    return game

def test_init_game_state():
    game = init_game_state()
    
    assert len(game.referee_tiles) == 1079
    assert len(game.players) == 4
    assert game.board.get(Position(0, 0)) == Piece('square', 'red')
    assert game.current_player == Player("3", 9)

def test_get_player_order():
    game = init_game_state()
    
    assert game.turn_queue.qsize() == 4
    assert game.current_player == Player("3", 9)
    assert Player("2", 12) == game.turn_queue.get()
    assert Player("4", 12) == game.turn_queue.get()
    assert Player("1", 13) == game.turn_queue.get()
    assert Player("3", 9) == game.turn_queue.get()
    
def test_get_next_player():
    game = init_game_state()
    
    # gets the next player
    assert game.current_player == Player("3", 9)
    assert Player("2", 12) == game.get_next_player()    
    assert game.turn_queue.qsize() == 4
    
    assert Player("4", 12) == game.get_next_player()
    assert Player("1", 13) == game.get_next_player()
    assert Player("3", 9) == game.get_next_player()
    assert Player("2", 12) == game.get_next_player()
    
def test_get_placed_pieces():
    game = init_game_state()
    
    assert len(game.get_placed_pieces()) == 1
    
    # raw place a piece on the board 
    game.board.raw_place(Piece('square', 'green'), Position(1, 0))
    
    # check that there are two pieces on the board now
    assert len(game.get_placed_pieces()) == 2
    
def test_remove_player():
    game = init_game_state()
    
    # before the remove happens
    assert len(game.players) == 4
    assert game.current_player == Player("3", 9)
    
    # after the remove happens 
    game.remove_current_player()
    assert len(game.players) == 3
    assert game.turn_queue.qsize() == 3
    assert game.current_player == Player("2", 12)
    # assert Player(3, 9) in game.players == False
    
    # another remove is called 
    game.remove_current_player()
    assert len(game.players) == 2
    assert game.turn_queue.qsize() == 2
    assert game.current_player == Player("4", 12)
    # assert Player(2, 12) in game.players == False
    
    # another remove is called 
    game.remove_current_player()
    assert len(game.players) == 1
    assert game.turn_queue.qsize() == 1
    assert game.current_player == Player("1", 13)
    
    # try and remove the last player should throw a RuntimeWarning
    try:
        game.remove_current_player()
    except RuntimeWarning:
        assert True

def test_score_move():
    game = init_game_state()
    game.board.raw_place(Piece('8star', 'red'), Position(-1, 0))
    game.board.raw_place(Piece('clover', 'red'), Position(1, 0))
    assert game.score_move([Position(-1, 0), Position(1, 0)]) == 5
    
    game.board.raw_place(Piece('square', 'blue'), Position(0, -1))
    assert game.score_move([Position(0, -1), Position(-1,0), Position(1, 0)]) == 8
    
    game.board.raw_place(Piece('square', 'purple'), Position(0, 1))
    game.board.raw_place(Piece('clover', 'blue'), Position(1, -1))
    
    game.board.raw_place(Piece('clover', 'purple'), Position(1, 1))
    assert game.score_move([Position(1, 1)]) == 6
    
    game.board.raw_place(Piece('8star', 'purple'), Position(-1, 1))
    assert game.score_move([Position(-1, 1), Position(1, -1)]) == 12
    
    game.board.raw_place(Piece('8star', 'blue'), Position(-1, -1))
    assert game.score_move([Position(-1, -1), Position(0, 0)]) == 14
    
    game.board.raw_place(Piece('diamond', 'red'), Position(-2, 0))
    game.board.raw_place(Piece('star', 'red'), Position(2, 0))
    game.board.raw_place(Piece('circle', 'red'), Position(-3, 0))
    assert game.score_move([Position(2, 0)]) == 15
    assert game.score_move([Position(-3, 0), Position(2, 0)]) == 16

def test_commit():
    game = init_game_state()
    
    cur_player = game.current_player
    # player passes the turn
    game.commit(Turn.pass_turn, cur_player.name, Status.Success, None)
    assert len(game.get_placed_pieces()) == 1 # just the starting piece
    assert cur_player.score == 0
    
    # player places some tiles
    cur_player = game.current_player
    cur_player.tiles = [Piece('square', 'blue'), Piece('star', 'red')]
    assert cur_player.score == 0
    game.commit(Turn.place, cur_player.name, Status.Success, [Piece('square', 'blue'), Piece('star', 'red')], [Position(-1, 0), Position(0, -1)])
    assert len(game.get_placed_pieces()) == 3
    assert cur_player.score == 6
    
    # exchange turn
    cur_player = game.current_player
    cur_player.setup(game.create_public_state(), game._get_tiles_to_deal(6))
    prev_tiles = copy.deepcopy(cur_player.tiles)
    game.commit(Turn.exchange, cur_player.name, Status.Success, cur_player.tiles)
    assert prev_tiles != cur_player.tiles
    assert cur_player.score == 0
    
def test_number_unused():
    game = init_game_state()
    assert game.number_unused() == 1079
    
def test_deal_tiles_to_player():
    game = init_game_state()
    
    assert len(game._get_tiles_to_deal(4)) == 4
    assert game.number_unused() == 1075
    
    assert len(game._get_tiles_to_deal(6)) == 6
    assert game.number_unused() == 1069
    
def test_create_public_state():
    game = init_game_state()
    
    player_scores = [0, 0, 0, 0]
    assert game.create_public_state().board == Board(Piece('square', 'red'))
    assert game.create_public_state().num_of_ref_tiles == 1079
    assert game.create_public_state().player_scores == player_scores
    assert game.create_public_state().current_player == game.current_player
    assert game.create_public_state() == PublicState(Board(Piece('square', 'red')), 1079, player_scores, game.current_player)
    
def test_setup_player():
    game = init_game_state()
    player_scores = [0, 0, 0, 0]
    
    game.setup_player("1")
    assert len(game.players[0].tiles) == 6
    assert game.players[0].public_state == PublicState(Board(Piece('square', 'red')), 1073, player_scores, game.current_player)
    
    game.players[1].tiles = [Piece("square", "red"), Piece("star", "blue")]
    game.setup_player("2")
    assert len(game.players[1].tiles) == 2
    assert game.players[1].public_state == PublicState(Board(Piece('square', 'red')), 1073, player_scores, game.current_player)
    
def test_swap_pieces():
    game = init_game_state()
    
    game.setup_player("1")
    assert game.number_unused() == 1073
    
    old_tiles = copy.deepcopy(game.players[0].tiles)
    game.swap_pieces("1")
    assert game.players[0].tiles != old_tiles
    assert len(game.players[0].tiles) == 6
    assert len(game.players[0].tiles) == len(old_tiles)

def test_find_player_with_id():
    game = init_game_state() 
    
    assert game.find_player_with_name("1") == game.players[0]
    assert game.find_player_with_name("2") == game.players[1]
    assert game.find_player_with_name("3") == game.players[2]
    assert game.find_player_with_name("4") == game.players[3]
    
    with pytest.raises(ValueError) as e:
        game.find_player_with_name("5")
    assert str(e.value) == "player_name:5 does not match any of the current player names"
    
# when the script runs it runs using pytest
if __name__ == "__main__":
    pytest.main(["-v", "game_state_test.py"])