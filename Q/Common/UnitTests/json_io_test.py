#!/usr/bin/env python3
import pytest
import sys
sys.path.insert(0, '../')
from public_game_state import PublicState
sys.path.insert(0, '../../Player/')
from player import Player, Birthday
from baddie_player import Baddie_Player
from cheating_player import Cheating_Player
from count_baddie_player import Count_Baddie_Player
sys.path.insert(0, '../')
from game_state import GameState
from map import *
sys.path.insert(0, '../')
from turn import *
from json_io import *

# _______Testing____Serialization_______#
def test_to_j_coodinate():
    assert Json_io.to_j_coordinate(Position(0, 0)) == '{"row": 0, "column": 0}'
    assert Json_io.to_j_coordinate(Position(-23, 10039)) == '{"row": -23, "column": 10039}'
    
def test_to_j_tile():
    assert Json_io.to_j_tile(Piece("clover", "green")) == '{"color": "green", "shape": "clover"}'
    assert Json_io.to_j_tile(Piece("diamond", "blue")) == '{"color": "blue", "shape": "diamond"}'
    assert Json_io.to_j_tile(Piece("triangle", "black")) == '{"color": "board", "shape": "board"}'
    
def test_to_j_tiles():
    assert Json_io.to_j_tiles([Piece("8star", "blue"), Piece("star", "green"), Piece("square", "red")]) == '[{"color": "blue", "shape": "8star"}, {"color": "green", "shape": "star"}, {"color": "red", "shape": "square"}]'

def test_to_j_action():
    assert Json_io.to_j_action(Turn.pass_turn) == '"pass"'
    assert Json_io.to_j_action(Turn.exchange) == '"replace"'
    assert Json_io.to_j_action(Turn.place) == '{"coordinate": {"row": 0, "column": 0}, "1tile": {"color": "board", "shape": "board"}}'
    
def test_j_placement():
    assert Json_io.to_j_placement((Position(0, 0), Piece("square", "red"))) == '{"coordinate": {"row": 0, "column": 0}, "1tile": {"color": "red", "shape": "square"}}'
    assert Json_io.to_j_placement((Position(-124, 493), Piece("diamond", "blue"))) == '{"coordinate": {"row": -124, "column": 493}, "1tile": {"color": "blue", "shape": "diamond"}}'
    
def test_j_placements():
    assert Json_io.to_j_placements([(Position(0, 0), Piece("square", "red")), (Position(2, 3), Piece("star", "orange"))]) == '[{"coordinate": {"row": 0, "column": 0}, "1tile": {"color": "red", "shape": "square"}}, {"coordinate": {"row": 2, "column": 3}, "1tile": {"color": "orange", "shape": "star"}}]'
    
def test_to_j_turn():
    assert Json_io.to_j_turn(Turn.pass_turn, []) == '{"turn_type": "pass", "tile*": []}'
    assert Json_io.to_j_turn(Turn.exchange, []) == '{"turn_type": "replace", "tile*": []}'
    assert Json_io.to_j_turn(Turn.place, [(Position(214, 90), Piece("square", "red")), (Position(-12, 3), Piece("clover", 'green'))]) == '{"turn_type": {"coordinate": {"row": 0, "column": 0}, "1tile": {"color": "board", "shape": "board"}}, "tile*": [{"coordinate": {"row": 214, "column": 90}, "1tile": {"color": "red", "shape": "square"}}, {"coordinate": {"row": -12, "column": 3}, "1tile": {"color": "green", "shape": "clover"}}]}'
    
def test_to_j_player():
    p1 = Player("A", 0)
    p1.score = 32
    p1.tiles = [Piece("square", "red"), Piece("star", "purple")]
    assert Json_io.to_j_player(p1) == '{"score": 32, "name": "A", "tile*": [{"color": "red", "shape": "square"}, {"color": "purple", "shape": "star"}]}'
    
def test_to_j_state():
    p1 = Player("A", 0)
    p1.score = 1
    p1.tiles = [Piece("star", "purple")]
    p2 = Player("B", 0)
    p2.score = 2
    p2.tiles = [Piece("circle", "blue")]
    gs1 = GameState(referee_tiles=[], players=[p1, p2])
    gs1.referee_tiles = [Piece("square", "red"), Piece("clover", "green")]
    board1 = Board(Piece("square", "red"))
    gs1.board = board1
    assert Json_io.to_j_state(gs1) == '{"map": [[0, [0, {"color": "red", "shape": "square"}]]], "tile*": [{"color": "red", "shape": "square"}, {"color": "green", "shape": "clover"}], "players": [{"score": 1, "name": "A", "tile*": [{"color": "purple", "shape": "star"}]}, {"score": 2, "name": "B", "tile*": [{"color": "blue", "shape": "circle"}]}]}'
    
    gs2 = GameState(referee_tiles=[], players=[]) # BUG
    gs2.board = Board(Piece("board", "board"))
    gs2.referee_tiles = []
    assert Json_io.to_j_state(gs2) == '{"map": [], "tile*": [], "players": []}' 
    
def test_to_j_names():
    assert Json_io.to_j_names([Player("Jay", 0), Player("Taiga", 0)], []) == '[["Jay", "Taiga"], []]'
    assert Json_io.to_j_names([Player("Taiga", 0)], [Player("Jay", 0)]) == '[["Taiga"], ["Jay"]]'

def test_to_j_pub():
    jay = Player("Jay", 0)
    jay.score = 50
    jay.tiles = [Piece("clover", "green"), Piece("star", "purple")]
    assert Json_io.to_j_pub(PublicState(Board(Piece("square", "red")), 180, [50, 20, 10], jay)) == '{"map": [[0, [0, {"color": "red", "shape": "square"}]]], "tile*": 180, "players": [{"score": 50, "name": "Jay", "tile*": [{"color": "green", "shape": "clover"}, {"color": "purple", "shape": "star"}]}, 20, 10]}'
    assert Json_io.to_j_pub(PublicState(Board(Piece("board", "board")), 0, [0], Player("Taiga", 0))) == '{"map": [], "tile*": 0, "players": [{"score": 0, "name": "Taiga", "tile*": []}]}'
    
def test_to_j_choice():
    assert Json_io.to_j_choice((Turn.pass_turn, [])) == '"pass"'
    assert Json_io.to_j_choice((Turn.exchange, [])) == '"replace"'
    assert Json_io.to_j_choice((Turn.place, [(Position(0, 0), Piece("square", "red")), (Position(1, 0), Piece("star", "purple"))])) == '[{"coordinate": {"row": 0, "column": 0}, "1tile": {"color": "red", "shape": "square"}}, {"coordinate": {"row": 1, "column": 0}, "1tile": {"color": "purple", "shape": "star"}}]'
    
def test_to_j_won():
    assert Json_io.to_j_won(True) == '"True"'
    assert Json_io.to_j_won(False) == '"False"'
#___End_____Of____Serialization_____Tests________#



#_______Testing_____Deserialization_______#
def test_from_j_action():
    assert Json_io.from_j_action('"pass"') == Turn.pass_turn
    assert Json_io.from_j_action('"replace"') == Turn.exchange
    assert Json_io.from_j_action('{"coordinate": {"row": 0, "column": 0}, "1tile": {"color": "board", "shape": "board"}}') == Turn.place
    
def test_from_j_tile():
    assert Json_io._from_j_tile('{"color": "red", "shape": "square"}') == Piece("square", "red")
    assert Json_io._from_j_tile('{"color": "green", "shape": "clover"}') == Piece("clover", "green")
    
def test_from_j_column_index():
    assert Json_io._from_j_column_index(5) == 5
    assert Json_io._from_j_column_index(-245) == -245
    
def test_from_j_row_index():
    assert Json_io._from_j_row_index(4) == 4
    assert Json_io._from_j_row_index(-249) == -249
    
def test_from_j_cell():
    assert Json_io._from_j_cell('[39, {"color": "red", "shape": "square"}]') == [39, Piece("square", "red")]
    assert Json_io._from_j_cell('[-9, {"color": "green", "shape": "clover"}]') == [-9, Piece("clover", "green")]
    
def test_from_j_row():
    assert Json_io._from_j_row('[3, [4, {"color": "purple", "shape": "8star"}], [6, {"color": "green", "shape": "clover"}]]') == [3, [4, Piece("8star", "purple")], [6, Piece("clover", "green")]]
    assert Json_io._from_j_row('[-2, [-1, {"color": "green", "shape": "clover"}], [43, {"color": "purple", "shape": "star"}], [6, {"color": "red", "shape": "square"}]]') == [-2, [-1, Piece("clover", "green")], [43, Piece("star", "purple")], [6, Piece("square", "red")]]
    
def test_from_j_map():
    board1 = Board(Piece("square", "red"))
    board1.raw_place(Piece("square", "blue"), Position(0, 1))
    board1.raw_place(Piece("star", "red"), Position(-1, 0))
    assert Json_io.from_j_map('[[0, [0, {"color": "red", "shape": "square"}], [1, {"color": "blue", "shape": "square"}]], [-1, [0, {"color": "red", "shape": "star"}]]]') == board1
    board2 = Board(Piece("clover", "red"))
    board2.raw_place(Piece("diamond", "red"), Position(1, 0))
    board2.raw_place(Piece("circle", "red"), Position(2, 0))
    assert Json_io.from_j_map('[[0, [0, {"color": "red", "shape": "clover"}]], [1, [0, {"color": "red", "shape": "diamond"}]], [2, [0, {"color": "red", "shape": "circle"}]]]') == board2
    
def test_from_j_tiles():
    tiles1 = [Piece("square", "red"), Piece("clover", "green"), Piece("star", "purple")]
    assert Json_io.from_j_tiles('[{"color": "red", "shape": "square"}, {"color": "green", "shape": "clover"}, {"color": "purple", "shape": "star"}]') == tiles1
    tiles2 = [Piece("8star", "purple")]
    assert Json_io.from_j_tiles('[{"color": "purple", "shape": "8star"}]') == tiles2
    tiles3 = []
    assert Json_io.from_j_tiles('[]') == tiles3
    

def test_from_j_player():
    player1 = Player("Jay", 0)
    player1.score = 67
    player1.tiles = [Piece("square", "red"), Piece("clover", "green")]
    assert Json_io.from_j_player('{"score": 67, "name": "Jay", "tile*": [{"color": "red", "shape": "square"}, {"color": "green", "shape": "clover"}]}') == player1
    player2 = Player("Taiga", 0)
    player2.score = -2
    player2.tiles = []
    assert Json_io.from_j_player('{"score": -2, "name": "Taiga", "tile*": []}') == player2
    
def test_from_j_players():
    player1 = Player("Jay", 0)
    player1.score = 4
    player1.tiles = [Piece("square", "red"), Piece("clover", "green")]
    players1 = [player1, 14, 2, 90]
    assert Json_io.from_j_players('[{"score": 4, "name": "Jay", "tile*": [{"color": "red", "shape": "square"}, {"color": "green", "shape": "clover"}]}, 14, 2, 90]') == players1
    player2 = Player("Taiga", 0)
    player2.score = 80
    player1.tiles = []
    players2 = [player2, -3, 34, 909, 9]
    assert Json_io.from_j_players('[{"score": 80, "name": "Taiga", "tile*": []}, -3, 34 , 909, 9]') == players2

def test_from_j_pub():
    tiaga = Player("Taiga", 0)
    tiaga.score = 43
    public_state = PublicState(Board(Piece("square", "red")), 1080, [43, 2], tiaga)
    assert Json_io.from_j_pub('{"map": [[0, [0, {"color": "red", "shape": "square"}]]], "tile*": 1080, "players": [{"score": 43, "name": "Taiga", "tile*": []}, 2]}') == public_state
    jay = Player("Jay", 0)
    jay.score = 23
    jay.tiles = [Piece("star", "purple"), Piece("8star", "purple")]
    board = Board(Piece("clover", "green"))
    board.raw_place(Piece("clover", "red"), Position(1, 0))
    board.raw_place(Piece("square", "red"), Position(1, 1))
    public_state2 = PublicState(board, 40, [23, 1, -5], jay)
    assert Json_io.from_j_pub('{"map": [[0, [0, {"color": "green", "shape": "clover"}]], [1, [0, {"color": "red", "shape": "clover"}], [1, {"color": "red", "shape": "square"}]]], "tile*": 40, "players": [{"score": 23, "name": "Jay", "tile*": [{"color": "purple", "shape": "star"}, {"color": "purple", "shape": "8star"}]}, 1, -5]}') == public_state2
    
def test_from_j_state():
    player1 = Player("A", 0)
    player1.score = 1
    player1.tiles = [Piece("clover", "green")]
    player2 = Player("B", 0)
    player2.score = 2 
    player2.tiles = [Piece("square", "red")]
    board = Board(Piece("star", "purple"))
    board.raw_place(Piece("8star", "purple"), Position(0, 1))
    tiles = [Piece("diamond", "blue"), Piece("square", "red")]
    game_state = GameState(referee_tiles=tiles, players=[player1, player2])
    game_state.board = board
    assert Json_io.from_j_state('{"map": [[0, [0, {"color": "purple", "shape": "star"}], [1, {"color": "purple", "shape": "8star"}]]], "tile*": [{"color": "blue", "shape": "diamond"}, {"color": "red", "shape": "square"}], "players": [{"score": 1, "name": "A", "tile*": [{"color": "green", "shape": "clover"}]}, {"score": 2, "name": "B", "tile*": [{"color": "red", "shape": "square"}]}]}') == game_state
    
def test_from_j_placement():
    assert Json_io.from_j_placement('{"coordinate": {"row": 0, "column": 0}, "1tile": {"color": "red", "shape": "square"}}') == (Position(0, 0), Piece("square", "red"))
    assert Json_io.from_j_placement('{"coordinate": {"row": -24, "column": 10}, "1tile": {"color": "purple", "shape": "star"}}') == (Position(-24, 10), Piece("star", "purple"))
    
def test_from_j_placements():
    assert Json_io.from_j_placements('[{"coordinate": {"row": 0, "column": 0}, "1tile": {"color": "red", "shape": "square"}}, {"coordinate": {"row": -24, "column": 10}, "1tile": {"color": "purple", "shape": "star"}}]') == [(Position(0, 0), Piece("square", "red")), (Position(-24, 10), Piece("star", "purple"))]
    assert Json_io.from_j_placements('[{"coordinate": {"row": 120, "column": -32}, "1tile": {"color": "blue", "shape": "circle"}}, {"coordinate": {"row": 0, "column": 0}, "1tile": {"color": "purple", "shape": "8star"}}]') == [(Position(120, -32), Piece("circle", "blue")), (Position(0, 0), Piece("8star", "purple"))]
    
def test_from_j_strategy():
    assert Json_io.from_j_strategy('"dag"') == Strategy.dag
    assert Json_io.from_j_strategy('"ldasg"') == Strategy.ldasg
    
def test_from_j_setup():
    tiaga = Player("Taiga", 0)
    tiaga.score = 43
    public_state = PublicState(Board(Piece("square", "red")), 1080, [43, 2], tiaga)
    tiles1 = [Piece("square", "red"), Piece("clover", "green"), Piece("star", "purple")]
    assert Json_io.from_j_setup('{"map": [[0, [0, {"color": "red", "shape": "square"}]]], "tile*": 1080, "players": [{"score": 43, "name": "Taiga", "tile*": []}, 2]} [{"color": "red", "shape": "square"}, {"color": "green", "shape": "clover"}, {"color": "purple", "shape": "star"}]') == [public_state, tiles1]
    
def test_from_j_won():
    assert Json_io.from_j_won('"False"') == False
    assert Json_io.from_j_won('"True"') == True
    assert Json_io.from_j_won('"true"') == True
    
def test_from_j_name():
    assert Json_io._from_j_name('"Jay"') == "Jay"
    assert Json_io._from_j_name('"Taiga"') == "Taiga"
    
def test_from_j_exn():
    assert Json_io._from_j_exn('"setup"') == Player.setup
    assert Json_io._from_j_exn('"take-turn"') == Player.take_turn
    assert Json_io._from_j_exn('"new-tiles"') == Player.new_tiles
    assert Json_io._from_j_exn('"win"') == Player.win
    try:
        Json_io._from_j_exn('"nothing"')
    except ValueError:
        assert True
    
def test_from_j_actor_spec():
    assert Json_io.from_j_actor_spec('["Jay", "dag"]') == Player("Jay", 0, Strategy.dag)
    assert Json_io.from_j_actor_spec('["Taiga", "ldasg", "setup"]') == Baddie_Player("Taiga", 0, Strategy.ldasg, Player.setup)
    assert Json_io.from_j_actor_spec('["Bob", "dag", "a cheat", "no-fit"]') == Cheating_Player("Bob", 0, Strategy.dag, "no-fit")
    assert Json_io.from_j_actor_spec('["Mike", "dag", "take-turn", 2]') == Count_Baddie_Player("Mike", 0, Strategy.dag, Player.take_turn, 2)
    
def test_from_j_cheat():
    assert Json_io._from_j_cheat('"non-adjacent-coordinate"') == "non-adjacent-coordinate"
    assert Json_io._from_j_cheat('"tile-not-owned"') == "tile-not-owned"
    assert Json_io._from_j_cheat('"not-a-line"') == "not-a-line"
    assert Json_io._from_j_cheat('"bad-ask-for-tiles"') == "bad-ask-for-tiles"
    assert Json_io._from_j_cheat('"no-fit"') == "no-fit"
    try:
        Json_io._from_j_cheat('"not-a-cheat"')
        assert False
    except ValueError:
        assert True
        
def test_from_j_actors():
    assert Json_io.from_j_actors('[["Jay", "dag"], ["Taiga", "ldasg", "setup"], ["Bob", "dag", "a cheat", "no-fit"]]') == [Player("Jay", 0, Strategy.dag), Baddie_Player("Taiga", 0, Strategy.ldasg, Player.setup), Cheating_Player("Bob", 0, Strategy.dag, "no-fit")]
    
def test_from_j_client_config():
    config1 = {}
    config1["port"] = 51000
    config1["host"] = "192.168.1.1"
    config1["wait"] = 8
    config1["quiet"] = True
    config1["players"] = [Player("A", 0, Strategy.dag), Cheating_Player("B", 0, Strategy.dag, "tile-not-owned"), Count_Baddie_Player("C", 0, Strategy.dag, Player.win, 2)]
    assert Json_io.from_j_client_config('{"port": 51000, "host": "192.168.1.1", "wait": 8, "quiet": true, "players": [["A", "ldasg"], ["B", "dag", "a cheat", "tile-not-owned"], ["C", "dag", "win", 2]]}') == config1
    
    # invalid port number 
    try:
        Json_io.from_j_client_config('{"port": 90000, "host": "www.game.com", "wait": 3, "quiet": false, "players": [["A", "dag"], ["B", "ldasg"]]}')
        assert False
    except ValueError:
        assert True
        
    # invalid wait time
    try:
        Json_io.from_j_client_config('{"port": 51000, "host": "192.168.1.1", "wait": -1, "quiet": true, "players": [["A", "ldasg"], ["B", "dag", "a cheat", "tile-not-owned"], ["C", "dag", "win", 2]]}')
        assert False
    except ValueError:
        assert True
        
    # invalid quiet
    try:
        Json_io.from_j_client_config('{"port": 51000, "host": "192.168.1.1", "wait": 8, "quiet": "something wrong", "players": [["A", "ldasg"], ["B", "dag", "a cheat", "tile-not-owned"], ["C", "dag", "win", 2]]}')
        assert False
    except ValueError:
        assert True
        
def test_from_j_referee_state_config():
    assert Json_io.from_j_referee_state_config('{"qbo" : 9, "fbo" : 10}') == {"qbo" : 9, "fbo" : 10}
    
    # invalid qbo
    try:
        Json_io.from_j_referee_state_config('{"qbo" : 89, "fbo" : 2}')
        assert False
    except ValueError:
        assert True
        
    # invalid fbo
    try:
        Json_io.from_j_referee_state_config('{"qbo" : 2, "fbo" : -1}') 
        assert False
    except:
        assert True

def test_from_j_referee_config():
    player1 = Player("A", 0)
    player1.score = 1
    player1.tiles = [Piece("clover", "green")]
    player2 = Player("B", 0)
    player2.score = 2 
    player2.tiles = [Piece("circle", "blue")]
    board = Board(Piece("star", "purple"))
    tiles = [Piece("square", "red")]
    game_state = GameState(referee_tiles=tiles, players=[player1, player2])
    game_state.board = board
    assert Json_io.from_j_referee_config('{"state0" : {"map": [[0, [0, {"color": "purple", "shape": "star"}]]], "tile*": [{"color": "red", "shape": "square"}], "players": [{"score": 1, "name": "A", "tile*": [{"color": "green", "shape": "clover"}]}, {"score": 2, "name": "B", "tile*": [{"color": "blue", "shape": "circle"}]}]}, "quiet": true, "config-s": {"qbo": 9, "fbo": 10}, "per-turn": 4, "observe": true}') ==  {"state0" : game_state, "quiet" : True, "config-s" : {"qbo" : 9, "fbo" : 10}, "per-turn" : 4, "observe" : True}
    
def test_j_server_config():
    player1 = Player("A", 0)
    player1.score = 1
    player1.tiles = [Piece("clover", "green")]
    player2 = Player("B", 0)
    player2.score = 2 
    player2.tiles = [Piece("circle", "blue")]
    board = Board(Piece("star", "purple"))
    tiles = [Piece("square", "red")]
    game_state = GameState(referee_tiles=tiles, players=[player1, player2])
    game_state.board = board
    assert Json_io.from_j_server_config('{"port" : 10030, "server-tries" : 8, "server-wait" : 25, "wait-for-signup" : 5, "quiet" : true, "ref-spec" : {"state0" : {"map": [[0, [0, {"color": "purple", "shape": "star"}]]], "tile*": [{"color": "red", "shape": "square"}], "players": [{"score": 1, "name": "A", "tile*": [{"color": "green", "shape": "clover"}]}, {"score": 2, "name": "B", "tile*": [{"color": "blue", "shape": "circle"}]}]}, "quiet": true, "config-s": {"qbo": 9, "fbo": 10}, "per-turn": 4, "observe": true}}') == {"port" : 10030, "server-tries" : 8, "server-wait" : 25, "wait-for-signup" : 5, "quiet" : True, "ref-spec" : {"state0" : game_state, "quiet" : True, "config-s" : {"qbo" : 9, "fbo" : 10}, "per-turn" : 4, "observe" : True}}
        
if __name__ == '__main__':
    pytest.main(['-vv', 'json_io_test.py'])