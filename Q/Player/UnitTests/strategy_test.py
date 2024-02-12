#!/usr/bin/env python3
import pytest
import sys
sys.path.insert(0, '../')
sys.path.insert(0, '../../Common')
from strategy import Strategy
from game_state import PublicState, GameState, Turn
from player import Player
from map import Piece, Shapes, Colors, Position
from strategy import *
sys.path.insert(0, '../../Referee')
from referee import Referee

p1 = Player(0, 0)
p2 = Player(1, 5)
p3 = Player(2, 17)

plist = [p1, p2, p3]

s1 = GameState(players=plist, start_piece=Piece("star", "red"))
ps = PublicState(s1.board, 30 * 36, {})

ref = Referee(s1, plist)

"""
def test_dag_move(ps, state, tiles, expected_pieces, expected_positions):
    next_player = state.current_player
    next_player.tiles = [tiles]
    next_turn, move_list = Strategy.get_next_turn(ps, next_player, Strategy.dag)
    assert next_turn == Turn.place
    for i in range(len(expected_pieces)):
        first_move_piece, first_move_position = move_list[i]
        assert first_move_position == expected_positions[i]
        assert first_move_piece == expected_pieces[i]
    assert len(move_list) == len(expected_pieces)
    ref.take_turn(Turn.place, next_player.id, expected_pieces,\
                  expected_positions)

"""
def test_dag_first_move():
    #test_dag_move(ps, s1, [Piece("square", "red"), Piece("square", "blue")],\
                 # [Piece("square", "red"), Piece("square", "blue")],\
                 # [Position(0, -1), Posit])

    next_player = s1.current_player
    next_player.tiles = [Piece("square", "red"), Piece("square", "blue")]
    next_turn, move_list = Strategy.get_next_turn(ps, next_player.tiles, Strategy.dag)
    assert next_turn == Turn.place
    first_move_piece, first_move_position = move_list[0]
    assert first_move_position == Position(-1, 0)
    assert first_move_piece == Piece("square", "red")
    second_move_piece, second_move_position = move_list[1]
    assert second_move_position == Position(-1, -1)
    assert second_move_piece == Piece("square", "blue")
    assert len(move_list) == 2
    ref.take_turn(Turn.place, next_player.id, [first_move_piece, second_move_piece],\
                  [first_move_position, second_move_position])


def test_dag_second_move():
    next_player = s1.current_player
    next_player.tiles = [Piece("circle", "red"), Piece("square", "green"), Piece("8star", "purple")]
    next_turn, move_list = Strategy.get_next_turn(ps, next_player.tiles, Strategy.dag)
    assert next_turn == Turn.place
    first_move_piece, first_move_position = move_list[0]
    assert first_move_position == Position(-2, -1)
    assert first_move_piece == Piece("square", "green")
    second_move_piece, second_move_position = move_list[1]
    assert second_move_position == Position(0, 1)
    assert second_move_piece == Piece("circle", "red")
    assert len(move_list) == 2
    ref.take_turn(Turn.place, next_player.id, [first_move_piece, second_move_piece],\
                  [first_move_position, second_move_position])


def test_dag_third_move():
    next_player = s1.current_player
    next_player.tiles = [Piece("8star", "purple")]
    next_turn, move_list = Strategy.get_next_turn(ps, next_player.tiles, Strategy.dag)
    assert next_turn == Turn.exchange
    assert move_list == []


plist2 = [Player(1, 1), Player(2, 2), Player(3, 3)]

s2 = GameState(players=plist2, start_piece=Piece("square", "green"))
ps2 = PublicState(s2.board, 30 * 36, {})
ref2 = Referee(s2, plist2)

starting_moves = [(Piece("square", "blue"), Position(0, -1)),\
                  (Piece("circle", "blue"), Position(1, -1))]
for starting_piece, starting_position in starting_moves:
    s2.board.raw_place(starting_piece, starting_position)


def test_ldasg_first_move():
    next_player = s2.current_player
    next_player.tiles = [Piece("circle", "green"), Piece("square", "blue")]
    next_turn, move_list = Strategy.get_next_turn(ps2, next_player.tiles, Strategy.ldasg)
    assert next_turn == Turn.place
    first_move_piece, first_move_position = move_list[0]
    assert first_move_piece == Piece("square", "blue")
    assert first_move_position == Position(1, 0)
    assert len(move_list) == 1

def test_ldasg_second_move():
    next_player = s2.current_player
    next_player.tiles = [Piece("square", "red")]
    next_turn, move_list = Strategy.get_next_turn(ps2, next_player.tiles, Strategy.ldasg)
    assert next_turn == Turn.place
    first_move_piece, first_move_position = move_list[0]
    assert first_move_piece == Piece("square", "red")
    assert first_move_position == Position(-1, 0)

def test_ldasg_third_move():
    next_player = s2.current_player
    next_player.tiles = [Piece("diamond", "yellow"), Piece("8star", "orange")]
    next_turn, move_list == Strategy.get_next_turn(ps2, next_player.tiles, Strategy.ldasg)
    assert next_turn == Turn.exchange
    assert len(move_list) == 0

if __name__ == '__main__':
    pytest.main(["-v", "strategy_test.py"])
