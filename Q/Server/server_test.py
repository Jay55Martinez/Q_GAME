#!/usr/bin/env python3
import copy
import time
import json
import pytest
import sys
import socket
sys.path.insert(0, '../Player')
from player import Player, Birthday
sys.path.insert(0, '../Common')
from public_game_state import PublicState
from server import *


def test_connection():
    initial_state = {"map": [[0, [0, {"color": "purple", "shape": "star"}], [1, {"color": "purple", "shape": "8star"}]]], "tile*": [{"color": "blue", "shape": "diamond"}, {"color": "red", "shape": "square"}], "players": [{"score": 1, "name": "A", "tile*": [{"color": "green", "shape": "clover"}]}, {"score": 2, "name": "B", "tile*": [{"color": "red", "shape": "square"}]}]}

    scoring_config = {
        "qbo": 8,
        "fbo": 4
    }

    ref_spec = {
        "state0": initial_state,
        "quiet": False,
        "config-s": scoring_config,
        "per-turn": 10,
        "observe": False
    }
    
    config = {
        'port':2048,
        'server-tries':2,
        'server-wait':20,
        'wait-for-signup':5,
        'quiet':False,
        'ref-spec':ref_spec
    }
    
    server = Server(config)
    server.start_listening()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    client_socket.connect(('127.0.0.1', config['port']))
    assert client_socket
    server.close_sockets()

def test_starts_run():
    initial_state = {"map": [[0, [0, {"color": "purple", "shape": "star"}], [1, {"color": "purple", "shape": "8star"}]]], "tile*": [{"color": "blue", "shape": "diamond"}, {"color": "red", "shape": "square"}], "players": []}

    scoring_config = {
        "qbo": 8,
        "fbo": 4
    }

    ref_spec = {
        "state0": initial_state,
        "quiet": False,
        "config-s": scoring_config,
        "per-turn": 10,
        "observe": False
    }
    
    config = {
        'port':2048,
        'server-tries':2,
        'server-wait':1,
        'wait-for-signup':5,
        'quiet':False,
        'ref-spec':ref_spec
    }

    server = Server(config)
    assert server.ready_to_run() == json.loads("[ [], [] ]")

    initial_state = {"map": [[0, [0, {"color": "purple", "shape": "star"}], [1, {"color": "purple", "shape": "8star"}]]], "tile*": [{"color": "blue", "shape": "diamond"}, {"color": "red", "shape": "square"}], "players": [{"score": 1, "name": "A", "tile*": [{"color": "green", "shape": "clover"}]}, {"score": 2, "name": "B", "tile*": [{"color": "red", "shape": "square"}]}]}
    scoring_config = {
        "qbo": 8,
        "fbo": 4
    }

    ref_spec = {
        "state0": initial_state,
        "quiet": False,
        "config-s": scoring_config,
        "per-turn": 10,
        "observe": False
    }
    
    config = {
        'port':2048,
        'server-tries':2,
        'server-wait':1,
        'wait-for-signup':5,
        'quiet':False,
        'ref-spec':ref_spec
    }

    server = Server(config)
    server.start_listening()
    assert '[[A], []]' == server.ready_to_run()
    
def test_new():
    initial_state = {"map": [[0, [0, {"color": "purple", "shape": "star"}], [1, {"color": "purple", "shape": "8star"}]]], "tile*": [{"color": "blue", "shape": "diamond"}, {"color": "red", "shape": "square"}], "players": [{"score": 1, "name": "A", "tile*": [{"color": "green", "shape": "clover"}]}, {"score": 2, "name": "B", "tile*": [{"color": "red", "shape": "square"}]}]}
    scoring_config = {
        "qbo": 8,
        "fbo": 4
    }

    ref_spec = {
        "state0": initial_state,
        "quiet": False,
        "config-s": scoring_config,
        "per-turn": 10,
        "observe": False
    }
    
    config = {
        'port':2048,
        'server-tries':2,
        'server-wait':1,
        'wait-for-signup':5,
        'quiet':False,
        'ref-spec':ref_spec
    }

    server = Server(config)
    server.new("hi", 0)
    assert len(server.players) == 1

    
if __name__ == '__main__':
    pytest.main(['-v', 'server_test.py'])