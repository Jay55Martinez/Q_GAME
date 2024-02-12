import socket
import sys
import logging
import json
import time
import pytest
from client import Client
sys.path.insert(0, '../Player')
from player import Player


class FakeSocket:
    def __init__(self) -> None:
        self.recv_data = b''
        self.send_data = b''
    
    def recv(self, size):
        return self.recv_data
    
    def send(self, data):
        self.send_data = data

def test_connection():
    fake = FakeSocket()
    client_config = {
        'port': 2000,
        'host': '127.0.0.1',
        'wait': 4,
        'quiet': False,
        'players': []
    }
    client = Client(client_config)
    client.try_connect(socket_creator=lambda: fake)
    assert fake == client.server

def test_no_connection():
    client_config = {
        'port': 2000,
        'host': '127.0.0.1',
        'wait': 4,
        'quiet': False,
        'players': []
    }
    client = Client(client_config)
    client.try_connect(socket_creator=lambda: None)
    assert None == client.server

def test_start_client_success():
    fake = FakeSocket()
    fake.recv_data = b'Name'
    test_player = Player("TestPlayer", 0)
    client_config = {
        'port': 2000,
        'host': '127.0.0.1',
        'wait': 4,
        'quiet': False,
        'players': test_player
    }
    client = Client(client_config)
    client.server = fake

    client.start_client()

    assert fake.recv_data == b'Name'
    assert fake.send_data == b'TestPlayer'

def test_setup():
    fake = FakeSocket()
    fake.recv_data = b'Name'
    test_player = Player("TestPlayer", 0)

    client_config = {
        'port': 2000,
        'host': '127.0.0.1',
        'wait': 4,
        'quiet': False,
        'players': test_player
    }
    client = Client(client_config)
    client.server = fake

    client.setup("SetupMessage")

    assert fake.recv_data == b'Name'


if __name__ == '__main__':
    pytest.main(['-v', 'client_tests.py'])