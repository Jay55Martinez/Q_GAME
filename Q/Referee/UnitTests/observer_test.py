#!/usr/bin/env python3
import pytest
import sys
import copy
sys.path.insert(0, '../../Common')
from public_game_state import *
sys.path.insert(0, '../../Player')
from player import *
sys.path.insert(0, '../../Common')
from game_state import *
from json_io import *
sys.path.insert(0, '../')
from referee import *
from observer import *

def init_gs():
    game_state = GameState(referee_tiles=get_starting_tiles(4), players=[Player('Jay', Birthday(4, 21, 2004), Strategy.dag), Player('Matt', Birthday(2, 21, 2003))], start_piece=Piece('clover', 'green'))
    return game_state

def init_obs():
    observer = Observer(init_gs())
    return observer

def test_show_next():
    observer = init_obs()
    game_state = init_gs()
    next_game = copy.deepcopy(game_state)
    next_game.board.raw_place(Piece('star', 'green'), Position(1, 0))
    observer.update_state(next_game)
    observer.show_next()
    assert observer.curr_spot == 1
    assert observer.get_current() == next_game
    
def test_show_previous():
    observer = init_obs()
    game_state = init_gs()
    next_game = copy.deepcopy(game_state)
    next_game.board.raw_place(Piece('star', 'green'), Position(1, 0))
    observer.update_state(next_game)
    observer.show_next()
    assert observer.curr_spot == 1
    observer.show_previous()
    assert observer.curr_spot == 0
    assert observer.get_current() == observer.l_of_state[0]
    observer.show_previous()
    assert observer.curr_spot == 0
    assert observer.get_current() == observer.l_of_state[0]

def test_update_state():
    observer = init_obs()
    game_state = init_gs()
    game_state.board.raw_place(Piece('star', 'green'), Position(1, 0))
    observer.update_state(game_state)
    assert len(observer.l_of_state) == 2
    assert len(observer.l_of_state[0].get_placed_pieces()) == 1
    assert len(observer.l_of_state[1].get_placed_pieces()) == 2
    assert len(observer.l_of_state[0].get_placed_pieces()) != len(observer.l_of_state[1].get_placed_pieces())

if __name__ == "__main__":
    pytest.main(["-v", "observer_test.py"])