import socket
import select
import time
import json
import sys
import os
import logging
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, '..'))
from Player.player import Player
from Common.json_io import Json_io
from Referee.referee import Referee
from Server.player import ProxyPlayer
from Referee.referee_spec import RefereeSpec

#        ____                           
#       / ___|  ___ _ ____   _____ _ __ 
#       \___ \ / _ \ '__\ \ / / _ \ '__|
#        ___) |  __/ |   \ V /  __/ |   
#       |____/ \___|_|    \_/ \___|_|   

# Server class represents a server for the Q game. Allows clients to join via TCP. 
# Runs a Q game with the connected clients.

MIN_PLAYERS = 2
MAX_PLAYERS = 4

class Server():

    def __init__(self, config):
        self.port = config['port']
        self.max_attempts = config['server-tries']
        self.wait_time = config['server-wait']
        self.wait_for_name = config['wait-for-signup']
        self.quiet = config['quiet']
        self.ref_spec = config['ref-spec']
 
        self.logger = logging.getLogger(__name__)
        if self.quiet:
            self.logger.setLevel(logging.CRITICAL)
        else:
            self.logger.setLevel(logging.DEBUG)
        
        self.min_players = MIN_PLAYERS
        self.max_players = MAX_PLAYERS
        self.players = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def new_client(self, client_socket):
        """Takes the client who is connected to this server and creates a ProxyPlayer
        with the name the client sends back.

        Args:
            client_socket (socket): socket for the respective client
        """
        if len(self.players) < self.max_players:
            client_socket.sendall(b"Name: ")
            client_socket.settimeout(self.wait_for_name)
            try:
                name = client_socket.recv(1024).decode('utf-8')
                self.check_client_name(name)
                self.players.append(ProxyPlayer(name, len(self.players), client_socket))
            except socket.timeout:
                client_socket.close()
                self.logger.debug("name request timed out")
            except ValueError:
                client_socket.close()
                self.logger.debug("name was not valid")
                

    def check_client_name(self, name):
        """Helper method to check if the given client name is between 1-20 chars and doesn't contain spaces.

        Args:
            name (str): name returned from the client 

        Raises:
            ValueError: String length must be between 1 and 20 characters
            ValueError: String cannot contain spaces
        """
        if not (1 <= len(name) <= 20) or ' ' in name:
            self.logger.debug("String length muct be between 1 and 20 characters and cannot contain spaces")
            raise ValueError("String length must be between 1 and 20 characters")
      
            
    def wait_cycle(self):
        """Waits one cycle of this servers wait_time for clients to connect, and creates ProxyPlayers
        for each client that joins.
        """
        start_time = time.time()
        while time.time() - start_time <= self.wait_time:
            time_left = self.wait_time - (time.time() - start_time)
            # checks if someone is trying to connect
            client_ready,  _, _ = select.select([self.server_socket], [], [], time_left)
            try:
                if client_ready and len(self.players) < self.max_players:
                    client_socket, _ = self.server_socket.accept()
                    self.new_client(client_socket)
                elif client_ready and len(self.players) >= self.max_players:
                    client_socket.close()
                    self.logger.debug("Player can not join the game because 4 players are already signed up")
            except socket.timeout:
                self.logger.debug("socket timed out")
      
            
    def close_sockets(self):
        """Closes the sockets of all clients in this server with a ProxyPlayer.
        """
        for player in self.players:
            if isinstance(player, ProxyPlayer):
                player.socket.close()
        self.server_socket.close()


    def check_local_players(self):
        """Checks the spec to see if any players listed in it have not already connected. If there exists 
        players who are not currently connected then this server will create a local Player to take its place.
        
        Side Affect:
            Appends Player to self.players
        """
        names_list = []
        for player in self.players:
            names_list.append(player.name)
        if len(self.players) < len(self.ref_spec['state0']['players']):
            for player in self.ref_spec['state0']['players']:
                if player['name'] not in names_list:
                    names_list.append(player['name'])
                    local_player = Player(player['name'], 0)
                    self.players.append(local_player)


    def ready_to_run(self):
        """Allows clients to connect to this server during a specified amount of time. Once enough clients (2-4)
        have joined or the server is done waiting this server runs a game and returns the results.

        Returns:
            list[list]: in the formate of: [[Winners], [Eliminated]] where Winners are the names of the players
            that won and Eliminated is the names of the players that were eliminated
        """
        for i in range(self.max_attempts):
            self.wait_cycle()
            if len(self.players) >= self.min_players and len(self.players) <= self.max_players:
                break
        result = self.create_referee()
        self.close_sockets()
        return result


    def start_listening(self):
        """Binds this server_socket to '127.0.0.1' and starts listening for clients.
        """
        self.server_socket.bind(('127.0.0.1', self.port))

        self.server_socket.listen(self.max_players)   


    def create_referee(self):
        """This server creates a referee with the players in it's fields, and then runs a game using the referee.

        Returns:
            list[list]: in the formate of: [[Winners], [Eliminated]] where Winners are the names of the players
            that won and Eliminated is the names of the players that were eliminated
        """
        self.check_local_players()
        try:
            if len(self.players) >= self.min_players and len(self.players) <= self.max_players:
                self.give_players_starting_hand_by_spec()
                self.ref_spec['players'] = self.players
                server_referee = RefereeSpec(self.ref_spec)
                return server_referee.run_game()
            else:
                return json.loads("[ [], [] ]")
        except ValueError as ve:
            # runs the game with out the spec because spec was wrong
            # TODO : This is not the right logic. Should remove the player whose name is not in the spec
            self.ref_spec['players'] = self.players
            server_referee = RefereeSpec(self.ref_spec)
            return server_referee.run_game()
    
    
    def give_players_starting_hand_by_spec(self):
        """Helper method that gives signed up players their starting tiles and score based on the jstate config.
        
        Side Affects:
            mutates players in the the players field with new tiles and scores.
        """
        for jplayer in self.ref_spec['state0']['players']:
            player_from_j_state = Json_io.from_string_player(jplayer)
            update_player = self._player_with_name(player_from_j_state.name)
            update_player.set_tiles(player_from_j_state.tiles)
            update_player.set_score(player_from_j_state.score)
    
    
    def _player_with_name(self, name):
        """Helper method returns the player with this name

        Args:
            name (str): given name

        Raises:
            ValueError: no player exists with the name that is currently signed up to play

        Returns:
            Player: returns player with that name
        """        
        for player in self.players:
            if player.name == name:
                return player
        self.logger.debug(f"no player exists with the name {name} that is currently signed up to play")
        raise ValueError(f"no player exists with the name {name} that is currently signed up to play")