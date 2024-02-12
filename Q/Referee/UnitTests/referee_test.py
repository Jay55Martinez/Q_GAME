#!/usr/bin/env python3
import copy
import pytest
import sys
sys.path.insert(0, '../../Common')
from public_game_state import *
sys.path.insert(0, '../../Player')
from player import *
sys.path.insert(0, '../../Common')
from json_io import *
sys.path.insert(0, '../')
from referee import *


def init_referee():
    player1 = Player('Bill', Birthday(2, 21, 2003), Strategy.dag)
    player2 = Player('Jane', Birthday(8, 14, 1992), Strategy.ldasg)
    player3 = Player('Olivia', Birthday(3, 2, 2001), Strategy.dag)
    player4 = Player('James', Birthday(9, 12, 1997), Strategy.dag)
    l_player = [player1, player2, player3, player4]
    
    game_state = GameState(players=l_player, start_piece=Piece('clover', 'green'))
    
    referee = Referee(p=l_player, state=game_state)
    return referee

def test_setup_players():
    referee = init_referee()
    referee.setup_players()
    
    assert len(referee.state.players[0].tiles) == 6
    assert len(referee.state.players[1].tiles) == 6
    assert len(referee.state.players[2].tiles) == 6
    assert len(referee.state.players[3].tiles) == 6
    
def test_validate_place_turn():
    referee = init_referee()
    referee.state.players[0].tiles = [Piece('square', 'green'), Piece('clover', 'blue'), Piece('8star', 'blue')]
    referee.state.players[1].tiles = [Piece('circle', 'green'), Piece('circle', 'blue')]
    
    assert referee._validate_place_turn('Bill', [Piece('square', 'green')], [Position(-1, 0)]) == Status.Success
    
    # does not have the tiles in its hand to make this move
    assert referee._validate_place_turn('Bill', [Piece('star', 'green'), Piece('clover', 'blue')], [Position(-1, 0), Position(0, -1)]) == Status.Failure
    
    # invalid movees
    assert referee._validate_place_turn('Jane', [Piece('circle', 'green'), Piece('circle', 'blue')], [Position(-1, 0), Position(-2, 0)]) == Status.Failure
    assert referee._validate_place_turn('Olivia', [], []) == Status.Failure


def test_validate_exchange_turn():
    referee = init_referee()
    referee.setup_players()
    
    assert referee._validate_exchange_turn('Bill') == Status.Success
    assert referee._validate_exchange_turn('Jane') == Status.Success
    
    # player with no tiles in their hand
    referee.state.players[0].tiles = []
    assert referee._validate_exchange_turn('Bill') == Status.Success
    
    game_with_no_pieces = GameState(players=referee.state.players)
    game_with_no_pieces.referee_tiles = []
    referee.state = game_with_no_pieces
    
    assert referee._validate_exchange_turn('Olivia') == Status.GameOver
    
def test_validate_turn():
    referee = init_referee()
    referee.setup_players()
    referee.state.players[0].tiles = [Piece('square', 'green'), Piece('clover', 'orange'), Piece('square', 'blue'), Piece('square', 'blue'), Piece('clover', 'orange')]
    
    print(referee.state.board.pieces)
    referee.state.current_player = referee.state.players[0]
    assert referee.validate_turn(Turn.place, 'Bill', tiles=[Piece('clover', 'orange')], locations=[Position(1, 0)]) == Status.Success
    referee.state.current_player = referee.state.players[1]
    assert referee.validate_turn(Turn.pass_turn, 'Jane') == Status.Success
    referee.state.current_player = referee.state.players[2]
    assert referee.validate_turn(Turn.exchange, 'Olivia') == Status.Success
    
    # make an invalid move
    referee.state.current_player = referee.state.players[0]
    assert referee.validate_turn(Turn.place, 'Bill', [Piece('square', 'blue')], [Position(0, -1)]) == Status.Failure
    
    # take turn out of order
    assert referee.validate_turn(Turn.pass_turn, 'Jane')
    
    # make a valid move but the are no more game tiles to give back
    referee.state.referee_tiles = []
    assert referee.validate_turn(Turn.place, 'Bill', [Piece('square', 'green')],  [Position(0, -1)]) == Status.GameOver
    referee.state.current_player = referee.state.players[2]
    assert referee.validate_turn(Turn.exchange, 'Olivia') == Status.GameOver
    referee.state.current_player = referee.state.players[1]
    assert referee.validate_turn(Turn.pass_turn, 'Jane') == Status.Success
    
    referee.state.players = [referee.state.players[0]] # one player left in the game
    referee.state.current_player = referee.state.players[0]
    assert referee.validate_turn(Turn.place, 'Bill', [Piece('star', 'green'), Piece('clover', 'orange')], [Position(0, 1), Position(1, 0)]) == Status.GameOver

def test_accept_turn():
    referee = init_referee()
    referee.setup_players()
    
    referee.state.players[0].tiles = [Piece('square', 'green'), Piece('clover', 'orange'), Piece('square', 'blue'), Piece('clover', 'orange'), Piece('clover', 'blue'), Piece('star', 'green')]
    referee.accept_turn(Turn.place, 'Bill', [Piece('clover', 'orange')], [Position(1, 0)])
    assert len(referee.state.players) == 4
    assert len(referee.state.get_placed_pieces()) == 2
    assert len(referee.state.players[0].tiles) == 6
    assert referee.state.players[0].score == 3
    assert referee.state.current_player == referee.state.players[2]
    
    referee.accept_turn(Turn.pass_turn, 'Olivia')
    assert len(referee.state.players) == 4
    assert len(referee.state.get_placed_pieces()) == 2
    assert referee.state.current_player == referee.state.players[3]
    
    old_hand = copy.deepcopy(referee.state.players[3].tiles)
    referee.accept_turn(Turn.exchange, 'James')
    assert len(referee.state.players) == 4
    assert len(referee.state.get_placed_pieces()) == 2
    assert old_hand != referee.state.players[3].tiles
    assert referee.state.current_player == referee.state.players[1]
    
    # removing  player on an invalid move
    referee.accept_turn(Turn.place, 'Jane', [], [])
    assert len(referee.state.players) == 3
    assert len(referee.state.get_placed_pieces()) == 2
    assert referee.state.current_player == referee.state.players[0]

# TODO : write tests for the run game method 
def test_run_game_spec():
    game_state = {"map" : [[0, [0, {"color" : "red", "shape" : "square"}]]], 
                  "tile*" : [],
                  "players" :
                      [{"score" : 0, 
                        "name" : "A", 
                        "tile*" : [{"color" : "blue", "shape" : "square"}, {"color" : "green", "shape" : "square"}, {"color" : "orange", "shape" : "square"}, {"color" : "yellow", "shape" : "square"}, {"color" : "blue", "shape" : "star"}, {"color" : "blue", "shape" : "square"}]},
                        {"score" : 0,
                        "name" : "B",
                        "tile*" : [{"color" : "blue", "shape" : "square"}, {"color" : "green", "shape" : "square"}, {"color" : "orange", "shape" : "square"}, {"color" : "yellow", "shape" : "square"}, {"color" : "blue", "shape" : "star"}]}]}
    
    referee_state_config = {"qbo" : 8, "fbo" : 10}
    
    referee_config = { "state0": game_state, "quiet": False, "config-s" : referee_state_config, "per-turn" : 3, "observe" : False }
    
    referee = Referee(Json_io.from_j_referee_config(json.dumps(referee_config)))
    
    assert referee.run_game_spec() == [ ['A'], [] ]

if __name__ == "__main__":
    pytest.main(["-v", "referee_test.py"])