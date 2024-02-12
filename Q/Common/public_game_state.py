#                 ____        _     _ _      ____  _        _       
#                |  _ \ _   _| |__ | (_) ___/ ___|| |_ __ _| |_ ___ 
#                | |_) | | | | '_ \| | |/ __\___ \| __/ _` | __/ _ \
#                |  __/| |_| | |_) | | | (__ ___) | || (_| | ||  __/
#                |_|    \__,_|_.__/|_|_|\___|____/ \__\__,_|\__\___|
  
# the public knowledge of the GameState
# contains the current state of the board and the scores fo all of the players
# the player scores will be a list with the first element in the list being the current player's score
class PublicState:
    def __init__(self, board, num_ref_tiles, player_scores, current_player):
        self.board = board
        self.num_of_ref_tiles = num_ref_tiles
        self.player_scores = player_scores
        self.current_player = current_player 
        
    def __repr__(self):
        return f'Board: {self.board}, num_tiles: {self.num_of_ref_tiles}, player_scores: {self.player_scores}, cur_player: {self.current_player}'
        
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, PublicState):
            return False
        return self.board == __value.board and\
            self.num_of_ref_tiles == __value.num_of_ref_tiles and\
                self.player_scores == __value.player_scores and\
                    self.current_player == __value.current_player