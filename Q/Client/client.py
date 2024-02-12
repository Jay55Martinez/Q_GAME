import socket
import sys
import logging
import json
import time
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, '..'))
from Player.player import *
from Player.strategy import Strategy
from Common.json_io import *
from Common.public_game_state import PublicState
from Client.referee import ProxyRef

CONNECTION_ATTEMPTS = 3
TIMEOUT = 5

# Represents a Client
# Connects a player to the server
class Client():

    def __init__(self, config):
        self.port = config['port']
        self.host = config['host']
        self.wait = config['wait']
        self.quiet = config['quiet']
        self.player = config['player']
        
        self.logger = logging.getLogger(__name__)
        if self.quiet:
            self.logger.setLevel(logging.CRITICAL)
        else:
            self.logger.setLevel(logging.DEBUG)
            
        self.server = None

    # Checks whether this message is asking for a name, if it is, a name is sent
    def sent_name(self, message):
        # TODO - This is not the right message
        if message == "Name":
            self.server.send(self.player.get_name().encoded('utf-8'))
            return True
        return False
    
    # Attempts CONNECTION_ATTEMPS times to connect to the server, returns bool about the success of connection
    def try_connect(self):

        for i in range(CONNECTION_ATTEMPTS):
            try:
                client_socket = socket.create_connection((self.host, self.port), timeout=TIMEOUT)
                self.server = client_socket
                return True
            except (socket.timeout, socket.error) as e:
                if i < CONNECTION_ATTEMPTS:
                    time.sleep(TIMEOUT)
        return False

    # Starts the socket and recieves the first message
    def start_client(self):
        #self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # TODO - NOT CONNECTING
        connected = self.try_connect()
      
        if connected:
            try:
                first_message = self.server.recv(1024).decode('utf-8')

                if self.sent_name(first_message):
                    setup_message = self.server.recv(1024).decode('utf-8')
                    self.setup(setup_message)
            except socket.error as e:
                self.logger.debug(f"{e}")
            except UnicodeDecodeError as ud:
                self.logger.debug(f"Unicode Failure: {ud}")

    # Sets up the Proxy Ref with this message
    def setup(self, message):
        proxy_ref = ProxyRef(self.server, self.player)
        proxy_ref.setup(message)