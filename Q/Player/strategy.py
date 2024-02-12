import copy
import sys
sys.path.insert(0, '../')
from public_game_state import PublicState
from turn import Turn

# List of strategies for playing the
# Q game. Two strategies for optimal
# play implemented. The get_next_turn
# function is called to get the next 
# turn to complete.
class Strategy:

    def positions_in_row_or_column(first_position, valid_positions):
        if first_position is not None:
            for i in range(len(valid_positions)-1, -1, -1):
                if valid_positions[i].row != first_position.row\
                    and valid_positions[i].column != first_position.column:
                    valid_positions.pop(i)
        return valid_positions

    # Implements the ldasg strategy
    # to find the next tile and position
    # for a move
    def ldasg(state: PublicState, player_tiles, first_position=None):
        sorted_tiles = sorted(player_tiles)
        if len(sorted_tiles) == 0:
            return None
        
        best_tile = sorted_tiles.pop(0)
        valid_locations = state.board.get_valid_locations(best_tile)
        while len(valid_locations) == 0:
            if len(sorted_tiles) == 0:
                return None
            best_tile = sorted_tiles.pop(0)
            valid_locations = state.board.get_valid_locations(best_tile)
        #for prev_try in tried_tiles:
        if first_position is not None:
            valid_locations = Strategy.positions_in_row_or_column(first_position, valid_locations)
        if len(valid_locations) == 0:
            return None
        location_neighbor_count = {}
        for location in valid_locations:
            location_neighbor_count[location] = state.board.get_num_neighbors(location)
        location_preference = sorted(location_neighbor_count.keys(), key= lambda a: location_neighbor_count[a], reverse=True)
        return (best_tile, location_preference.pop(0))

    # Implements the dag strategy for
    # finding the next piece and position
    # for a place move
    def dag(state: PublicState, player_tiles, first_position=None):
        sorted_tiles = sorted(player_tiles)
        if len(sorted_tiles) == 0:
            return None
        best_tile = sorted_tiles.pop(0)
        valid_locations = state.board.get_valid_locations(best_tile)
        while len(valid_locations) == 0:
            if len(sorted_tiles) == 0:
                return None
            best_tile = sorted_tiles.pop(0)
            valid_locations = state.board.get_valid_locations(best_tile)
        if first_position is not None:
            valid_locations = Strategy.positions_in_row_or_column(first_position, valid_locations)
        if len(valid_locations) == 0:
            return None
        sorted_positions = sorted(valid_locations)
        best_position = sorted_positions[0]
        return (best_tile, best_position)
    
    # allows for players to place not in the same row/col
    def dag_cheat(state: PublicState, player_tiles, first_position=None):
        sorted_tiles = sorted(player_tiles)
        if len(sorted_tiles) == 0:
            return None
        best_tile = sorted_tiles.pop(0)
        valid_locations = state.board.get_valid_locations(best_tile)
        while len(valid_locations) == 0:
            if len(sorted_tiles) == 0:
                return None
            best_tile = sorted_tiles.pop(0)
            valid_locations = state.board.get_valid_locations(best_tile)
        sorted_positions = sorted(valid_locations)
        best_position = sorted_positions[0]
        return (best_tile, best_position)

    # Takes the current board state, current
    # player, and the strategy function for
    # finding the next move to take, and returns
    # the turn that should be taken by the player.
    def get_next_turn(state: PublicState, player_tiles, strategy):
        state_copy = copy.deepcopy(state)
        player_tiles_copy = copy.deepcopy(player_tiles)
        # Get the next recommended move by the strategy
        move_list = []
        result = strategy(state_copy, player_tiles_copy)
        if result == None:
            if state.num_of_ref_tiles < 6:
                return (Turn.pass_turn, [])
            return (Turn.exchange, [])
        first_piece, first_position = result
        next_move = (first_piece, first_position) 
        
        # Iterate through and mutate the copy board
        # and player tiles to get all possible placements
        # for this turn.
        while next_move != None:
            move_list.append(next_move)
            move_tile, move_position = next_move
            state_copy.board.raw_place(move_tile, move_position)
            player_tiles_copy.remove(move_tile)
            next_move = strategy(state_copy, player_tiles_copy, first_position=first_position)
        
        return (Turn.place, move_list)
