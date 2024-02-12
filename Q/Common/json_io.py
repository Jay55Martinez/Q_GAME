import re
import sys
import json
import os
from json import JSONDecoder, JSONDecodeError
from turn import Turn
import ipaddress
import socket
from map import *
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, '..'))
from Player.strategy import Strategy
from Player.player import Player
from Player.baddie_player import Baddie_Player
from Player.cheating_player import Cheating_Player
from Player.count_baddie_player import Count_Baddie_Player

#               _                   _       
#              | |___  ___  _ __   (_) ___  
#           _  | / __|/ _ \| '_ \  | |/ _ \ 
#          | |_| \__ \ (_) | | | | | | (_) |
#           \___/|___/\___/|_| |_| |_|\___/ 

# Json parsing class
class Json_io:
    def __init__(self):
        pass
    
    #converts a json JMap to a board
    #input: j_map - type(str) - a json string of the JMap format
    #output: type(Board) - the board represented by j_map
    #side-effects: None
    # TESTED
    @staticmethod
    def from_j_map(j_map):
        json_map = json.loads(j_map)
        rows = [Json_io._from_j_row(json.dumps(x)) for x in json_map]
        board = Board(BOARD_PIECE) #board_piece gets overwritten
        for row in rows:
            row_index = row[0]
            for (column_index,tile) in row[1:]:
                board.raw_place(tile,Position(row_index,column_index))
        return board

    # converts a json action to a player move
    # input: j_action - type(str) - a json string of the JAction format
    # JAction is "pass", "replace", or a 1Placement.
    # TESTED
    @staticmethod
    def from_j_action(j_action):
        if j_action == '"pass"':
            return Turn.pass_turn
        elif j_action == '"replace"':
            return Turn.exchange
        else:
            return Turn.place
    
     # TESTED
    @staticmethod
    def to_j_action(turn_type):
        if turn_type == Turn.pass_turn:
            return json.dumps("pass")
        elif turn_type == Turn.exchange:
            return json.dumps("replace")
        else:
            return json.dumps({"coordinate" : json.loads(Json_io.to_j_coordinate(Position(0, 0))), "1tile" : json.loads(Json_io.to_j_tile(Piece("board", "board")))})
    
    # TESTED
    @staticmethod
    def to_j_turn(turn_type, placements):
        j_action = Json_io.to_j_action(turn_type)
        j_placements = Json_io.to_j_placements(placements)
        return json.dumps({"turn_type" : json.loads(j_action), "tile*" : json.loads(j_placements)})
    
    # TESTED
    @staticmethod
    def to_j_placements(placements):
        j_placements = []
        for p in placements:
            j_placements.append(json.loads(Json_io.to_j_placement(p)))
        return json.dumps(j_placements)
    
    #TESTED
    @staticmethod
    def to_j_placement(placement):
        j_placement = {}
        j_placement["coordinate"] = json.loads(Json_io.to_j_coordinate(placement[0]))
        j_placement["1tile"] = json.loads(Json_io.to_j_tile(placement[1]))
        return json.dumps(j_placement)
    
    #TESTED
    @staticmethod
    def to_j_tiles(tiles):
        return json.dumps([json.loads(Json_io.to_j_tile(tile)) for tile in tiles])
    # Convert the provided Board into a Jmap 
    # column represents a Jrow and row represents a Jcolumn
    @staticmethod
    def to_j_map(board_state):
        jmap = []
        for column in range(board_state.column_offset, len(board_state.pieces) - abs(board_state.column_offset)):
            jrow = [column]
            for row in range(board_state.row_offset, len(board_state.pieces[0]) - abs(board_state.row_offset)):
                cur_piece = board_state.get(Position(column, row))
                if cur_piece != Piece('board', 'board'):
                    jcell = [row, {"color": cur_piece.color.name, "shape": cur_piece.shape.name}]
                    jrow.append(jcell)
            if len(jrow) != 1:
                jmap.append(jrow)
            jrow = []
        return jmap
    
    @staticmethod
    def from_string_player(s_player):
        score = s_player["score"]
        name = s_player["name"]
        tiles = Json_io.from_j_tiles(json.dumps(s_player["tile*"]))
        player = Player(name, 0)
        player.score = score
        player.tiles = tiles
        player.strategy = Strategy.dag
        return player
    

    #TESTED
    @staticmethod
    def from_j_player(j_player):
        json_player = json.loads(j_player)
        return Json_io.from_string_player(json_player)

    # Takes a list that starts with a
    # JPlayer and then a group of integers
    # representing scores, and returns a list
    # of Players.
    # TESTED
    @staticmethod
    def from_j_players(j_players):
        json_players = json.loads(j_players)
        player = Json_io.from_j_player(json.dumps(json_players[0]))
        players = [player]
        for player_scores in json_players[1:]:
            players += [player_scores]
        return players
    
    # Creates a JState from a GameState object
    # returns a JState
    # TESTED
    @staticmethod
    def to_j_state(gamestate):
        jmap = Json_io.to_j_map(gamestate.board)
        l_j_tiles = json.loads(Json_io.to_j_tiles(gamestate.referee_tiles))
        l_j_players = [json.loads(Json_io.to_j_player(p)) for p in gamestate.players]
        return json.dumps({'map' : jmap, 'tile*' : l_j_tiles, 'players' : l_j_players})
            
    # TESTED
    @staticmethod
    def to_j_player(player):
        score = player.score
        name = player.name
        tiles = json.loads(Json_io.to_j_tiles(player.tiles))
        return json.dumps({'score' : score, 'name' : name, 'tile*' : tiles})

    # Takes in the list of winning players
    # and kicked players, and returns the
    # two lists of names.
    # TESTED
    @staticmethod
    def to_j_names(winners, kicked_players):
        output_names = [[], []]
        for w in winners:
            output_names[0].append(w.name)
        output_names[0] = sorted(output_names[0])
        for k in kicked_players:
            output_names[1].append(k.name)

        return json.dumps(output_names)

    # Parses JPlacement into a Position object.
    # TESTED
    @staticmethod
    def from_j_placements(placements_dict):
        json_placements = json.loads(placements_dict)
        placements = []
        for p in json_placements:
            placements.append(Json_io.from_j_placement(json.dumps(p)))
        return placements
    
    # TESTED
    @staticmethod
    def from_j_placement(j_placement):
        json_placement = json.loads(j_placement)
        jcoordinate = json_placement["coordinate"]
        jtile = json_placement["1tile"]
        pos = Position(jcoordinate["row"], jcoordinate["column"])
        tile = Json_io._from_j_tile(json.dumps(jtile))
        return (pos, tile)

    # Returns the correct Strategy function
    # pointer given the JStrategy string given.
    # TESTED
    @staticmethod
    def from_j_strategy(strategy):
        if strategy == '"dag"':
            return Strategy.dag
        elif strategy == '"ldasg"':
            return Strategy.ldasg

    # Convers the provided JState dictionary
    # into
    # TESTED
    @staticmethod
    def from_j_state(j_state):
        json_state = json.loads(j_state)
        map = Json_io.from_j_map(json.dumps(json_state['map']))
        ref_tiles = Json_io.from_j_tiles(json.dumps(json_state['tile*']))
        ps = [Json_io.from_j_player(json.dumps(p)) for p in json_state['players']]
        game_state = GameState(referee_tiles=ref_tiles, players=ps)
        game_state.board = map
        return game_state

    # Converts a board to j_map and list of tiles to j_tiles
    # TESTED
    @staticmethod
    def to_j_pub(public_state):
        jmap = Json_io.to_j_map(public_state.board)
        l_of_player_scores = [score for score in public_state.player_scores[1:]]
        return json.dumps({'map' : jmap, 'tile*' : public_state.num_of_ref_tiles, 'players' : [json.loads(Json_io.to_j_player(public_state.current_player))] + l_of_player_scores})

    # TESTED
    @staticmethod
    def from_j_pub(j_pub):
        json_public_state = json.loads(j_pub)
        map = Json_io.from_j_map(json.dumps(json_public_state["map"]))
        ref_tiles = int(json_public_state['tile*'])
        players = Json_io.from_j_players(json.dumps(json_public_state['players']))
        player_scores = [players[0].score]
        player_scores += [player_scores for player_scores in players[1:]]
        public_state = PublicState(map, ref_tiles, player_scores, players[0])
        return public_state

    # TESTED
    @staticmethod
    def from_j_setup(j_setup):
        input_objects = Json_io.decode_stacked(j_setup)
        parsed_objects = [elem for elem in input_objects]

        json_pub = json.dumps(parsed_objects[0])
        json_tiles = json.dumps(parsed_objects[1])
        
        public_state = Json_io.from_j_pub(json_pub)
        player_tiles = Json_io.from_j_tiles(json_tiles)

        return [public_state, player_tiles]

    #TESTED
    @staticmethod
    def from_j_tiles(j_tiles):
        json_tiles = json.loads(j_tiles)
        tiles = [Json_io._from_j_tile(json.dumps(t)) for t in json_tiles]
        return tiles
    
    # TESTED
    @staticmethod
    def to_j_choice(choice):
        move = ""
        if choice[0] == Turn.pass_turn:
            move = "pass"
        elif choice[0] == Turn.exchange:
            move = "replace"
        elif choice[0] == Turn.place:
            move = json.loads(Json_io.to_j_placements(choice[1]))
        json_move = json.dumps(move)
        return json_move
    
    # TESTED
    @staticmethod
    def from_j_won(jwon):
        return json.loads(jwon).upper() == 'TRUE'
    
    # TESTED
    @staticmethod
    def to_j_won(won):
        if won:
            j_won = '"True"'
        else:
            j_won = '"False"'
        return j_won
    
    @staticmethod
    def from_j_state_and_actors(j_state, j_actor_list):
        json_state = json.loads(j_state)
        json_actor_list = json.loads(j_actor_list)
        j_actor_players = Json_io.from_j_actors(json.dumps(json_actor_list))
        j_state_players = [Json_io.from_j_player(json.dumps(player)) for player in json_state["players"]]
        players = []
        if len(j_actor_players) == len(j_state_players):
            for x in range(0, len(j_actor_players)):
                player = j_actor_players[x]
                player.tiles = j_state_players[x].tiles
                player.score = j_state_players[x].score
                players.append(player)
        else:
            raise ValueError("j_actors and players in game state are not the same size")
        board = Json_io.from_j_map(json.dumps(json_state["map"]))
        game_state = GameState(referee_tiles=Json_io.from_j_tiles(json.dumps(json_state["tile*"])), players=players)
        game_state.board = board
        return game_state

    # Called with the list of JActors and
    # the list of players in the JState to
    # returns a list of players for the game.
    # TESTING
    @staticmethod
    def from_j_actors(j_actor_list):
        json_actor_list = json.loads(j_actor_list)
        players = []
        for j_actor in json_actor_list:
            players.append(Json_io.from_j_actor_spec(json.dumps(j_actor)))
        return players

    # TESTED
    @staticmethod
    def from_j_actor_spec(j_actor_spec):
        json_actor_spec = json.loads(j_actor_spec)
        if len(json_actor_spec) == 2:
            return Player(Json_io._from_j_name(json.dumps(json_actor_spec[0])), 0, strategy=Json_io.from_j_strategy(json.dumps(json_actor_spec[1])))
        elif len(json_actor_spec) == 3:
            return Baddie_Player(Json_io._from_j_name(json.dumps(json_actor_spec[0])), 0, strategy=Json_io.from_j_strategy(json.dumps(json_actor_spec[1])), exception_method=Json_io._from_j_exn(json.dumps(json_actor_spec[2])))
        elif len(json_actor_spec) == 4:
            if json_actor_spec[2] == "a cheat":
                return Cheating_Player(Json_io._from_j_name(json.dumps(json_actor_spec[0])), 0, strategy=Json_io.from_j_strategy(json.dumps(json_actor_spec[1])), cheat=Json_io._from_j_cheat(json.dumps(json_actor_spec[3])))
            else:
                return Count_Baddie_Player(Json_io._from_j_name(json.dumps(json_actor_spec[0])), 0, strategy=Json_io.from_j_strategy(json.dumps(json_actor_spec[1])), exception_method=Json_io._from_j_exn(json.dumps(json_actor_spec[2])), count_down=json_actor_spec[3])
    
    # TESTED
    @staticmethod
    def _from_j_name(j_name):
        json_name = json.loads(j_name)
        return json_name
    
    # TESTED
    @staticmethod
    def _from_j_cheat(j_cheat):
        json_cheat = json.loads(j_cheat)
        if json_cheat == "non-adjacent-coordinate":
            return "non-adjacent-coordinate"
        elif json_cheat == "tile-not-owned":
            return "tile-not-owned"
        elif json_cheat == "not-a-line":
            return "not-a-line"
        elif json_cheat == "bad-ask-for-tiles":
            return "bad-ask-for-tiles"
        elif json_cheat == "no-fit":
            return "no-fit"
        raise ValueError("not a j_cheat")
    
    # TESTED
    @staticmethod
    def _from_j_exn(j_exn):
        json_exn = json.loads(j_exn)
        if json_exn == "setup":
            return Player.setup
        elif json_exn == "take-turn":
            return Player.take_turn
        elif json_exn == "new-tiles":
            return Player.new_tiles
        elif json_exn == "win":
            return Player.win
        raise ValueError(f"not a j_exn: {j_exn}")

    #converts a json JRow to a list
    #input: j_row - type(str) - a json string of the JRow format
    #output: type(str)
    #side-effects: None
    @staticmethod
    # TESTED
    def _from_j_row(j_row):
        json_row = json.loads(j_row)
        j_row = [Json_io._from_j_row_index(json_row[0])]
        for x in json_row[1:]:
            j_row += [Json_io._from_j_cell(json.dumps(x))]
        return j_row

    #converts a json JCell to a tuple of (int, Piece)
    #input: j_cell - type(str) - a json string of the
    #output: type(list)
    #side-effects: None
    # TESTED
    @staticmethod
    def _from_j_cell(j_cell):
        json_cell = json.loads(j_cell)
        return [Json_io._from_j_column_index(json_cell[0]), Json_io._from_j_tile(json.dumps(json_cell[1]))]

    #converts an integer and a Piece to a json JCell
    #input: column_pos - type(int)
    #       cell - type(list)
    #output: type(list)
    #side-effects: None
    @staticmethod
    def _to_j_cell(column_pos, cell):
        return [column_pos, Json_io.to_j_tile(cell)]

    #converts a json JTile to a piece
    #input: j_tile  - type(str) - a json string of the
    #output: type(Tile)
    #side-effects: None
    # TESTED
    @staticmethod
    def _from_j_tile(j_tile):
        json_tile = json.loads(j_tile)
        return Piece(json_tile["shape"], json_tile["color"])

    #converts a piece to a Json JTile
    #input: tile - type(Tile)
    #output: type(dict)
    #side-effects: None
    # TESTED
    @staticmethod
    def to_j_tile(tile):
        return json.dumps({"color": tile.color.name, "shape": tile.shape.name})

    #converts a Position to a json JCoordinate
    #input: coordinate - type(Position)
    #output: type(dict)
    #side-effects: None
    # TESTED
    @staticmethod
    def to_j_coordinate(coordinate):
        return json.dumps({"row": coordinate.row, "column": coordinate.column})

    #converts a json RowIndex to an integer
    #input: j_row_index - type(str) - a json string of the
    #output: type(int)
    #side-effects: None
    @staticmethod
    def _from_j_row_index(j_row_index):
        return int(j_row_index)

    #converts an integer to a json RowIndex
    #input: row_index - type(int)
    #output: type(int)
    #side-effects: None
    # TESTED
    @staticmethod
    def _to_j_row_index(row_index):
        return row_index

    #converts a json ColumnIndex to an integer
    #input: j_column_index - type(str) - a json string of the
    #output: type(int)
    #side-effects: None
    # TESTED
    @staticmethod
    def _from_j_column_index(j_column_index):
        return int(j_column_index)

    #converts an integer to a json ColumnIndex
    #input: column_index - type(int) - 
    #output: type(int)
    #side-effects: None
    @staticmethod
    def _to_j_column_index(column_index):
        return column_index

    #converts a json Shape to a Shape
    #input: j_shape - type(str) - a json string of the
    #output: type(str)
    #side-effects: None
    @staticmethod
    def _from_j_shape(j_shape):
        return j_shape

    #converts a Shape to a json Shape
    #input: shape - type(Shape) - 
    #output: type(str)
    #side-effects: None
    @staticmethod
    def _to_j_shape(shape):
        return shape

    #converts a json Color to a Color
    #input: j_color - type(str) - a json string of the
    #output: type(str)
    #side-effects: None
    @staticmethod
    def _from_j_color(j_color):
        return j_color

    #converts a Color to a json Color
    #input: color - type(Color) - a Color to convert to a json Color string
    #output: type(str)
    #side-effects: None
    @staticmethod
    def _to_j_color(color):
        return color
    
    """
    A ClientConfig is an object with 5 fields:,
       { "port"  : Natural (between 10000 and 60000),
         "host"   : String (either an IP address or a domain name),
         "wait"  : Natural (less than 10s),
         "quiet" : Boolean,
         "players" : JActorsB }
    """
    # TESTED
    @staticmethod
    def from_j_client_config(j_client_config):
        json_client_config = json.loads(j_client_config)
        if json_client_config["port"] > 60000 or json_client_config["port"] < 10000:
            raise ValueError("port number is not valid")
        if json_client_config["wait"] < 0 or json_client_config["wait"] > 10:
            raise ValueError("wait time is not valid")
        if not isinstance(json_client_config["quiet"], bool):
            raise ValueError("quiet is not a bool")
        players = Json_io.from_j_actors(json.dumps(json_client_config["players"]))
        json_client_config["players"] = players 
        return json_client_config
    
    # check that the given address is a valid ip address
    def is_valid_ip(address):
        try:
            ipaddress.ip_address(address)
            return True
        except ValueError:
            return False
        
    # checks that the given domain is a valid domain 
    def is_valid_domain(domain):
        try:
            socket.gethostbyname(domain)
            return True
        except ValueError:
            return False
    
    # TODO - from_j_ServerConfig, should return 
    """
    { "port" : Natural (between 10000 and 60000),
      "server-tries" : Natural (less than 10),
      "server-wait" : Natural (less than 30[s]),
      "wait-for-signup" : Natural (less than 10),
      "quiet" : Boolean,
      "ref-spec" : RefereeConfig }
    """
    # TESTING
    @staticmethod
    def from_j_server_config(j_server_config):
        json_server_config = json.loads(j_server_config)
        if json_server_config["port"] < 10000 or json_server_config["port"] > 60000:
            raise ValueError("invalid port number")
        elif json_server_config["server-tries"] > 10 or json_server_config["server-tries"] < 0:
            raise ValueError("invalid server tries time")
        elif json_server_config["server-wait"] > 30 or json_server_config["server-wait"] < 0:
            raise ValueError("invalid server wait time")
        elif json_server_config["wait-for-signup"] > 10 or json_server_config["wait-for-signup"] < 0:
            raise ValueError("invalid wait for sign up time")
        elif not isinstance(json_server_config["quiet"], bool):
            raise ValueError("quiet is not a bool")
        referee_config = Json_io.from_j_referee_config(json.dumps(json_server_config["ref-spec"]))
        json_server_config["ref-spec"] = referee_config
        return json_server_config
    
    """
    { "qbo" : Natural (less or equal to 10),
      "fbo" : Natural (less or equal to 10) }
    """
    # TESTED
    def from_j_referee_state_config(j_referee_state_config):
        json_referee_state_config = json.loads(j_referee_state_config)
        if json_referee_state_config["qbo"] > 10 or json_referee_state_config["qbo"] < 0:
            raise ValueError("qbo is invalid")
        if json_referee_state_config["fbo"] > 10 or json_referee_state_config["fbo"] < 0:
            raise ValueError("fbo is invalid")
        return json_referee_state_config
            
    
    """
    { "state0" : JState,
      "quiet" : Boolean,
      "config-s" : RefereeStateConfig,
      "per-turn" : Natural (less than or equal to 6),
      "observe" : Boolean }
    """
    # TESTED
    @staticmethod
    def from_j_referee_config(j_referee_config):
        json_referee_config = json.loads(j_referee_config)
        json_ref_state_config = Json_io.from_j_referee_state_config(json.dumps(json_referee_config["config-s"]))
        json_referee_config["config-s"] = json_ref_state_config
        if not isinstance(json_referee_config["quiet"], bool):
            raise ValueError("quiet is not a bool")
        elif not isinstance(json_referee_config["observe"], bool):
            raise ValueError("observer is not a bool")
        elif json_referee_config["per-turn"] > 6 or json_referee_config["per-turn"] < 0:
            raise ValueError("per-turn is not valid")
        return json_referee_config
    
    #loads all jsons from a file into json objects
    #input: 
    def decode_stacked(document, pos=0, decoder=JSONDecoder()):
        while True:
            match = NOT_WHITESPACE.search(document, pos)
            if not match:
                return
            pos = match.start()
        
            try:
                obj, pos = decoder.raw_decode(document, pos)
            except JSONDecodeError:
            # do something sensible if there's some error
                raise
            yield obj

NOT_WHITESPACE = re.compile(r'\S') # finds any non white space character