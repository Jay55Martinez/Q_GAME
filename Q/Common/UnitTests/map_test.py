#!/usr/bin/env python3
# Jay Martinez -- 10/13/2023
# Tests for the map class
import pytest
import sys
sys.path.insert(0, '../')
from map import *

def init_board():
    # create list of boards
    l_boards = []
    
    # board with the starting tile as red square
    board1 = Board(Piece('square', 'red'))
    l_boards.append(board1)
    
    # board with the starting tile as an empty board tile
    board2 = Board(Piece('board', 'board'))
    l_boards.append(board2)
    
    # board with a bunch of valid tiles placed
    board3 = Board(Piece('square', 'red'))
    board3.raw_place(Piece('clover', 'red'), Position(1, 0))
    board3.raw_place(Piece('square', 'blue'), Position(0, -1))
    board3.raw_place(Piece('8star', 'red'), Position(-1, 0))
    board3.raw_place(Piece('clover', 'blue'), Position(1, -1))
    board3.raw_place(Piece('square', 'purple'), Position(0, 1))
    l_boards.append(board3)
    
    return l_boards

def test_grow():
    boards = init_board()
    board2 = boards[1]
    
    board2._grow(-1, -1)
    assert len(board2.pieces) == 2
    assert len(board2.pieces[0]) == 2
    
    board2._grow(1, 0)
    assert len(board2.pieces) == 3
    assert len(board2.pieces[0]) == 2
    
    board2._grow(0, 1)
    assert len(board2.pieces) == 3
    assert len(board2.pieces[0]) == 3
    
    assert board2.row_offset == -1
    assert board2.column_offset == -1

def test_get():
    boards = init_board()
    board1 = boards[0]
    board2 = boards[1] # empty board
    
    board1._grow(-1, -1) # grows the board left 1 and up 1
    assert board1.get(Position(0, 0)) == Piece('square', 'red')
    
def test_raw_place():
    boards = init_board()
    board1 = boards[0] # board with starting tile as red squarecd .
    
    board1.raw_place(Piece('circle', 'red'), Position(1, 0))
    board1.raw_place(Piece('star', 'red'), Position(-1, 0))
    board1.raw_place(Piece('star', 'blue'), Position(-1, -1))
    
    
    assert board1.get(Position(1, 0)) == Piece('circle', 'red')
    assert board1.get(Position(-1, 0)) == Piece('star', 'red')
    assert board1.get(Position(-1, -1)) == Piece('star', 'blue')
    
def test_get_adjacent():
    boards = init_board()
    board1 = boards[0]
    
    board1.raw_place(Piece('clover', 'red'), Position(1, 0))
    board1.raw_place(Piece('circle', 'blue'), Position(0, -1))
    board1.raw_place(Piece('8star', 'red'), Position(-1, 0))
    board1.raw_place(Piece('clover', 'blue'), Position(1, 1))
    board1.raw_place(Piece('diamond', 'blue'), Position(0, 1))
    
    assert board1.get_adjacent(Position(0, 0)) == [Piece('8star', 'red'), Piece('clover', 'red'),
                                     Piece('circle', 'blue'), Piece('diamond', 'blue')]
    assert board1.get_adjacent(Position(2, 0)) == [Piece('clover', 'red'), Piece('board', 'board'), 
                                                   Piece('board', 'board'),  Piece('board', 'board')]
    
def test_get_num_neighbors():
    boards = init_board()
    board1 = boards[0]
    board3 = boards[2]
    
    assert board3.get_num_neighbors(Position(0, 0)) == 4
    assert board3.get_num_neighbors(Position(-1, 0)) == 1
    assert board1.get_num_neighbors(Position(0, 0)) == 0

def test_is_adjacent():
    boards = init_board()
    board1 = boards[0]
    
    assert board1.is_adjacent(Position(1, 0)) == True
    assert board1.is_adjacent(Position(0, -1)) == True
    assert board1.is_adjacent(Position(0, 0)) == False
    assert board1.is_adjacent(Position(-2, 0)) == False
    
def test_get_all_pieces():
    boards = init_board()
    board3 = boards[2]
    
    all_pieces_for_board3 = board3.get_all_pieces()

    assert Piece('square', 'red') in all_pieces_for_board3
    assert Piece('clover', 'red') in all_pieces_for_board3
    assert Piece('square', 'blue') in all_pieces_for_board3
    assert Piece('8star', 'red') in all_pieces_for_board3
    assert Piece('clover', 'blue') in all_pieces_for_board3
    assert Piece('square', 'blue') in all_pieces_for_board3
    assert not Piece('square', 'green') in all_pieces_for_board3
    
def test_place_if_adjacent():
    boards = init_board()
    board1 = boards[0]
    
    assert board1.place_if_adjacent(Piece('square', 'blue'), Position(-1, 0)) == Status.Success
    assert board1.row_offset == -1
    assert len(board1.pieces) == 2
    assert len(board1.pieces[0]) == 1
    assert Piece('square', 'blue') in board1.get_all_pieces()
    assert board1.place_if_adjacent(Piece('square', 'purple'), Position(-1, 1)) == Status.Success
    assert board1.row_offset == -1
    assert len(board1.pieces) == 2
    assert len(board1.pieces[0]) == 2
    assert board1.place_if_adjacent(Piece('star', 'blue'), Position(-2, -5)) == Status.Failure
     
def test_played():
    boards = init_board()
    board1 = boards[0]
    
    assert board1.played(Position(100, 100)) == False
    assert board1.played(Position(0, 0)) == True
    
def test_num_tiles_in_direction():
    boards = init_board()
    board3 = boards[2]
    
    assert board3._num_tiles_in_direction(Position(-1, 0), -1) == list()
    assert board3._num_tiles_in_direction(Position(-1, 0), -1, False) == list()

    # start at position (-1, 0) and iterate left
    assert Position(0, 0) in board3._num_tiles_in_direction(Position(-1, 0), 1) 
    assert Position(1, 0) in board3._num_tiles_in_direction(Position(-1, 0), 1)
    assert not Position(-1, 0) in board3._num_tiles_in_direction(Position(-1, 0), 1)
    
    # start at position (0, -1) and iterates down 
    assert Position(0, 0) in board3._num_tiles_in_direction(Position(0, -1), 1, False)
    assert Position(0, 1) in board3._num_tiles_in_direction(Position(0, -1), 1, False)

def test_same_color():
    boards = init_board()
    board3 = boards[2]
    
    # list of tiles that are all the color red
    l_tiles = []
    l_tiles.append(board3.get(Position(-1, 0))) # red 8star
    l_tiles.append(board3.get(Position(0, 0))) # red square
    l_tiles.append(board3.get(Position(1, 0))) # red clover
    
    assert board3.same_color(Piece('diamond', 'red'), l_tiles) == True
    assert board3.same_color(Piece('diamond', 'blue'), l_tiles) == False
    
    # list of tiles that have different colors should always be false
    l_tiles = []
    l_tiles.append(Piece('square', 'red'))
    l_tiles.append(Piece('square', 'blue'))
    l_tiles.append(Piece('square', 'green'))
    l_tiles.append(Piece('square', 'purple'))
    
    assert len(l_tiles) == 4
    assert board3.same_color(Piece('diamond', 'red'), l_tiles) == False
    assert board3.same_color(Piece('square', 'green'), l_tiles) == False
    
def test_same_shape():
    boards = init_board()
    board3 = boards[2]
    
    # list of tiles that have different shapes should always return false
    l_tiles = []
    l_tiles.append(board3.get(Position(-1, 0))) # red 8star
    l_tiles.append(board3.get(Position(0, 0))) # red square
    l_tiles.append(board3.get(Position(1, 0))) # red clover
    
    assert board3.same_shape(Piece('diamond', 'red'), l_tiles) == False
    assert board3.same_shape(Piece('diamond', 'blue'), l_tiles) == False
    
    # list of tiles that have the same shape
    l_tiles = []
    l_tiles.append(Piece('square', 'red'))
    l_tiles.append(Piece('square', 'blue'))
    l_tiles.append(Piece('square', 'green'))
    l_tiles.append(Piece('square', 'purple'))
    
    assert len(l_tiles) == 4
    assert board3.same_shape(Piece('diamond', 'red'), l_tiles) == False
    assert board3.same_shape(Piece('square', 'orange'), l_tiles) == True
    
def test_matches_in_row():
    boards = init_board()
    board3 = boards[2]
    
    assert board3.matches_in_row(Piece('diamond', 'red'), Position(-2, 0)) == True
    assert board3.matches_in_row(Piece('diamond', 'green'), Position(-2, 0)) == False
    assert board3.matches_in_row(Piece('clover', 'green'), Position(1, 2)) == True
    assert board3.matches_in_row(Piece('8star', 'purple'), Position(-1, 1)) == True
    assert board3.matches_in_row(Piece('diamond', 'blue'), Position(-1, 1)) == False
    
def test_matches_in_column():
    boards = init_board()
    board3 = boards[2]
    
    assert board3.matches_in_column(Piece('circle', 'red'), Position(2, 0)) == True
    assert board3.matches_in_column(Piece('clover', 'green'), Position(1, 2)) == True
    assert board3.matches_in_column(Piece('diamond', 'green'), Position(-2, 0)) == True
    assert board3.matches_in_column(Piece('diamond', 'red'), Position(-2, 0)) == True
    assert board3.matches_in_column(Piece('diamond', 'blue'), Position(-1, 1)) == False
    
def test_can_play_piece_here():
    boards = init_board()
    board3 = boards[2]
    
    assert board3.can_play_piece_here(Piece('circle', 'red'), Position(2, 0)) == True
    assert board3.can_play_piece_here(Piece('clover', 'green'), Position(1, 2)) == False
    assert board3.can_play_piece_here(Piece('diamond', 'green'), Position(-2, 0)) == False
    assert board3.can_play_piece_here(Piece('diamond', 'red'), Position(-2, 0)) == True
    assert board3.can_play_piece_here(Piece('diamond', 'blue'), Position(-1, 1)) == False
    
def test_get_valid_locations():
    boards = init_board()
    board1 = boards[0]
    board3 = boards[2]
    
    # tests on board1
    valid_location_for_blue_square = board1.get_valid_locations(Piece('square', 'blue'))
    assert len(valid_location_for_blue_square) == 4
    assert Position(1, 0) in valid_location_for_blue_square
    assert Position(-1, 0) in valid_location_for_blue_square
    assert Position(0, 1) in valid_location_for_blue_square
    assert Position(0, -1) in valid_location_for_blue_square

    valid_location_for_blue_circle = board1.get_valid_locations(Piece('circle', 'blue'))
    assert len(valid_location_for_blue_circle) == 0
    
    # tests on board3
    valid_location_for_red_diamond = board3.get_valid_locations(Piece('diamond', 'red'))
    assert len(valid_location_for_red_diamond) == 2
    assert Position(-2, 0) in valid_location_for_red_diamond
    assert Position(2, 0) in valid_location_for_red_diamond
    
    valid_location_for_purple_diamond = board3.get_valid_locations(Piece('diamond', 'purple'))
    assert len(valid_location_for_purple_diamond) == 0
    
def test_get_contiguous_pieces():
    boards = init_board()
    board3 = boards[2]
    
    assert board3.get_contiguous_pieces([Position(-2, 0)]) == 4
    
    assert board3.get_contiguous_pieces([Position(1, 1)]) == 5

def test_q_color_completed():
    boards = init_board()
    board1 = boards[0] # contains red at 0, 0
    
    # add every color to the board
    board1.raw_place(Piece('square', 'blue'), Position(0, -1))
    board1.raw_place(Piece('square', 'green'), Position(0, -2))
    board1.raw_place(Piece('square', 'purple'), Position(0, -3))
    board1.raw_place(Piece('square', 'yellow'), Position(0, -4))
    board1.raw_place(Piece('square', 'orange'), Position(0, -5))
    
    l_every_color_position = [Position(0, 0), Position(0, -1), Position(0, -2), Position(0, -3), Position(0, -4), Position(0, -5)]
    assert board1.q_color_completed(l_every_color_position) == True
    
    l_every_color_position.remove(Position(0, 0))
    assert board1.q_color_completed(l_every_color_position) == False
    
def test_shape_completed():
    boards = init_board()
    board1 = boards[0] # contains square at 0, 0
    
    # add every shape to the board
    board1.raw_place(Piece('star', 'red'), Position(0, -1))
    board1.raw_place(Piece('diamond', 'red'), Position(0, -2))
    board1.raw_place(Piece('8star', 'red'), Position(0, -3))
    board1.raw_place(Piece('clover', 'red'), Position(0, -4))
    board1.raw_place(Piece('circle', 'red'), Position(0, -5))
    
    l_every_shape_position = [Position(0, 0), Position(0, -1), Position(0, -2), Position(0, -3), Position(0, -4), Position(0, -5)]
    assert board1.q_shape_completed(l_every_shape_position) == True
    
    l_every_shape_position.remove(Position(0, 0))
    assert board1.q_shape_completed(l_every_shape_position) == False

def test_q_completed():
    boards = init_board()
    board1 = boards[0] # contains a red square at 0,0 should add 12
    
    # add every color to the board
    # any of these positions should add 6
    board1.raw_place(Piece('square', 'blue'), Position(0, -1))
    board1.raw_place(Piece('square', 'green'), Position(0, -2))
    board1.raw_place(Piece('square', 'purple'), Position(0, -3))
    board1.raw_place(Piece('square', 'yellow'), Position(0, -4))
    board1.raw_place(Piece('square', 'orange'), Position(0, -5))
    
    # add every shape to the board
    # any of these positions should add 6
    board1.raw_place(Piece('star', 'red'), Position(1, 0))
    board1.raw_place(Piece('diamond', 'red'), Position(2, 0))
    board1.raw_place(Piece('8star', 'red'), Position(3, 0))
    board1.raw_place(Piece('clover', 'red'), Position(4, 0))
    board1.raw_place(Piece('circle', 'red'), Position(5, 0))
    
    # adding a few other pieces
    # any of these positions should add 0
    board1.raw_place(Piece('8star', 'blue'), Position(3, -1))
    board1.raw_place(Piece('clover', 'yellow'), Position(-1, 4))
    
    assert board1.q_completed([Position(0, 0)]) == 12
    assert board1.q_completed([Position(2, 0)]) == 6
    assert board1.q_completed([Position(3, -1)]) == 0
    assert board1.q_completed([Position(0, -5), Position(-1, 4)]) == 6
    assert board1.q_completed([Position(0, -5), Position(3, -1), Position(-1, 4)]) == 6
    
def test_num_contiguous_pieces():
    boards = init_board()
    board3 = boards[2]
    
    board3.raw_place(Piece('8star', 'purple'), Position(-1, 1))
    board3.raw_place(Piece('clover', 'purple'), Position(1, 1))   
    board3.raw_place(Piece('8star', 'blue'), Position(-1, 1))
    
    assert board3.num_contiguous_pieces([Position(1, 1), Position(0, -1)]) == 11
    assert board3.num_contiguous_pieces([Position(-1, -1), Position(1, 1)]) == 12
    assert board3.num_contiguous_pieces([Position(0,0)]) == 6
    
def test_grow_board():
    boards = init_board()
    board2 = boards[1]
    
    board2.grow_board(1, 0)
    assert len(board2.pieces) == 2
    assert len(board2.pieces[0]) == 1
    assert board2.row_offset == 0
    assert board2.column_offset == 0
    
    board2.grow_board(1, 1)
    assert len(board2.pieces) == 2
    assert len(board2.pieces[0]) == 2
    assert board2.row_offset == 0
    assert board2.column_offset == 0
    
    board2.grow_board(-1, 1)
    assert len(board2.pieces) == 3
    assert len(board2.pieces[0]) == 2
    assert board2.row_offset == -1
    assert board2.column_offset == 0
    
    board2.grow_board(2, 0)
    assert len(board2.pieces) == 4
    assert len(board2.pieces[0]) == 2
    assert board2.row_offset == -1
    assert board2.column_offset == 0
    
    board2.grow_board(0, -2)
    assert len(board2.pieces) == 4
    assert len(board2.pieces[0]) == 4
    assert board2.row_offset == -1
    assert board2.column_offset == -2

def test_get_column_from_location():
    boards = init_board()
    board1 = boards[0]
    board3 = boards[2]
    
    column_0_0 = Column(0, 0, 0)
    assert board1.get_column_from_location(Position(0, 0)) == column_0_0
    
    column_neg1_1 = Column(-1, 1, 0)
    assert board3.get_column_from_location(Position(0, 0)) == column_neg1_1
    assert column_neg1_1.length() == 3
    
    column_neg1_0 = Column(-1, 0, 1)
    assert board3.get_column_from_location(Position(1, 0)) == column_neg1_0
    assert column_neg1_0.length() == 2
    
def test_get_row_from_location():
    boards = init_board()
    board1 = boards[0]
    board3 = boards[2]
    
    row_0_0 = Row(0, 0, 0)
    assert board1.get_row_from_location(Position(0, 0)) == row_0_0
    assert row_0_0.length() == 1
    
    row_neg1_1 = Row(-1, 1, 0)
    assert board3.get_row_from_location(Position(0, 0)) == row_neg1_1
    assert row_neg1_1.length() == 3
    
    row_0_neg1 = Row(0, 1, -1)
    assert board3.get_row_from_location(Position(0, -1)) == row_0_neg1
    assert row_0_neg1.length() == 2

# when the script runs it runs using pytest
if __name__ == "__main__":
    pytest.main(["-v", "map_test.py"])
