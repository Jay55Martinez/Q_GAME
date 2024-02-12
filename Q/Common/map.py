from enum import Enum
import itertools

#possible statuses
Status = Enum('Status_Type', ['Success','Failure','GameOver'])

#note board shape can only show up with board color
#note board always must be last
Shapes = Enum('Shape_Type', ['star','8star','square','circle','clover','diamond', 'board'])    
Colors = Enum('Color_Type', ['red','green','blue','yellow','orange','purple', 'board'])

class Piece:
    """ Represents a type of piece that has a
    particular shape and color.
    """

    def __init__(self, shape, color):
        try:
            self.shape = Shapes[shape]
            self.color = Colors[color]
        except KeyError:
            self.shape = Shapes["board"]
            self.color = Colors["board"]
    
    def __str__(self) -> str:
        return str(self.shape) + ' ' + str(self.color)
    
    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Piece):
            return False
        return self.shape == __value.shape and self.color == __value.color
    
    def __ne__(self, __value: object) -> bool:
        return not self == __value
    
    def __lt__(self, other):
        if self.shape == Shapes.board or self.color == Colors.board\
            or other.shape == Shapes.board or other.color == Colors.board:
            raise ValueError("Cannot compare board pieces")
        if not isinstance(other, Piece):
            raise ValueError("Can not compare a non tile object to a tile")
        if self.shape != other.shape:
            return self.shape.value < other.shape.value
        return self.color.value < other.color.value

    def __hash__(self):
        return hash(self.shape) + hash(self.color)

# Piece placed in the board to represent blank tiles
# instead of using null (None in Python)
BOARD_PIECE = Piece(Shapes.board.name, Colors.board.name)


#represents positions on the board
class Position:
    """ Represents a position on the board
    which is a row index and a column index.
    These indices are relative to the center
    tile, which is (0,0). Row represents the row
    index (up and down), while column represents
    the column index (left and right).
    """

    def __init__(self, row, column):
        self.row = row #int
        self.column = column #int
        
    def __repr__(self):
        return f"{self.row}: {self.column}"
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Position):
            return False
        return self.row == __value.row and self.column == __value.column
    
    def __lt__(self, other) -> bool:
        if self.row != other.row:
            return self.row < other.row
        return self.column < other.column

    def __hash__(self):
        return hash(self.row) + hash(self.column)
     
class Segment:
    """ Represents a segment in a particular
    direction (row or column) of the board.
    This does not contain and tiles, but it is
    a numeric range, and an index.
    """
    
    def __init__(self, start, stop, index):
        self.start = start
        self.stop = stop
        self.index = index
    def __hash__(self):
        return hash(self.start) + hash(self.stop) + hash(self.index)
    def __eq__(self, other):
        return self.start == other.start\
            and self.stop == other.stop\
            and self.index == other.index
    
    def __repr__(self):
        return f"Start: {self.start}, Stop: {self.stop}"
    
    def length(self):
        count = 1
        for _ in range(self.start, self.stop):
            count += 1
        return count


#represents the physical board
class Board:
    """ Stores all the information about where
    tiles are placed on the board. Uses a list of
    columns to store the pieces in a 2-dimensional
    array.
    """

    def __init__(self, starting_piece):
        self.pieces = [[starting_piece]] #list of list of piece
        self.row_offset = 0
        self.column_offset = 0
        
    def __eq__(self, __value=object) -> bool:
        if not isinstance(__value, Board):
            return False
        return self.pieces == __value.pieces and\
            self.row_offset == __value.row_offset and\
                self.column_offset == __value.column_offset
        
    def __repr__(self):
        return f'board: {self.pieces}, row offset: {self.row_offset}, column offset: {self.column_offset}'
        

    def _grow(self, increase_columns=0, increase_rows=0):
        """   negative increase adds to the left or bottom respectively
        
        Args:
            increase_columns (int) - direction and magnitude to increase number of columns
            increase_row (int) - direction and magnitude to increase number of rows
        
        Returns: 
            Void
            
        Side Affects:
            increase_columns or increase_rows is negative then 
            column_offset/ row_offset will be increased respectively 
        """

        #grow the rows, if 0 does nothing
        if increase_rows < 0:
            self.row_offset += increase_rows
            self.pieces = [([BOARD_PIECE] * abs(increase_rows)) + column for column in self.pieces]
        else:
            self.pieces = [column + ([BOARD_PIECE]*increase_rows) for column in self.pieces]

        #grow the columns, if 0 does nothing
        if increase_columns < 0:
            self.column_offset += increase_columns
            new_columns = []
            for i in range(0,abs(increase_columns)):
                new_columns.append([BOARD_PIECE]*(len(self.pieces[0])))
            new_columns.extend(self.pieces)
            self.pieces = new_columns
        else:
            new_columns = []
            for i in range(0,increase_columns):
                new_columns.append([BOARD_PIECE]*(len(self.pieces[0])))
            self.pieces.extend(new_columns)

    def get(self, position):
        """   determines if the given position has a tiled played there or not

        Args:
            position (Position): position that will 

        Returns:
            bool: true if there is not a piece played in that position
        """
        if position.row >= self.row_offset and position.row < len(self.pieces[0]) + self.row_offset and \
           position.column >= self.column_offset and position.column < len(self.pieces) + self.column_offset:
            return self.pieces[position.column - self.column_offset][position.row - self.row_offset]
        else:
            return BOARD_PIECE

    def played(self, position):
        """checks the given position to see if the spot contains a non board piece

        Args:
            position (Position): the Position that will be check

        Returns:
            bool: true if the location contains a non board piece
        """
        return self.get(position) != BOARD_PIECE
        
    def raw_place(self, tile, position):
        """places a tile without checking whether it is valid to do so.

        Args:
            tile (Piece): Piece that will be placed
            position (Position): Position where the Piece will be placed
            
        Returns:
            Void
            
        Side Affects:
            adds new Piece to self.pieces and grows self.pieces if needed
        """
        self.grow_board(position.row, position.column)
        self.pieces[position.column - self.column_offset][position.row - self.row_offset] = tile

    def get_adjacent(self, location):
        """get the adjacet pieces to a location

        Args:
            location (Position): Position where the neighbor check happens

        Returns:
            Pieces[]: list of 4 pieces can include board pieces
        """
        return [self.get(x) for x in
                [Position(location.row-1, location.column), Position(location.row+1, location.column),
                Position(location.row, location.column-1), Position(location.row, location.column+1)]]

    def get_num_neighbors(self, location):
        """Returns the number of neighboring

        Args:
            location (Position): Position where the neighbor check happens

        Returns:
            int: the number of neighbors that are not board Pieces
        """
        adjacent_pieces = self.get_adjacent(location)
        neighbor_count = 0
        for neighbor in adjacent_pieces:
            if neighbor.color != Colors.board and neighbor.shape != Shapes.board:
                neighbor_count += 1
        return neighbor_count

    def is_adjacent(self, location):
        """determines if the location is adjacent to at least one player piece

        Args:
            location (Position): Position to check

        Returns:
            bool: true if the location has a adjacent player piece i.e piece that is not a board piece
        """
        return self.get_num_neighbors(location) > 0

    def place_if_adjacent(self, tile, location):
        """place a piece if it is adjacent to a piece does not check for validness

        Args:
            tile (Piece): Piece that is trying to be placed
            location (Position):  Position where the Piece is trying to be placed

        Returns:
            Enum Status: Success if the Piece is placed or Failure if the Piece is not placed
            
        Side Affects:
            can grows self.pieces and add new Piece to self.pieces
        """
        if self.is_adjacent(location):
            self.raw_place(tile, location)
            return Status.Success
        return Status.Failure
        
    def same_color(self, piece, tiles):
        """hecks if the given piece is the same color of all the pieces in tiles

        Args:
            piece (Piece): Piece that will be check to see if it is the same color as the tiles
            tiles (Pieces{}): list of Pieces that should all be the same color if they are not then return false

        Returns:
            bool: True if the given piece is the same color as all the tiles and all the tiles are same color as well. False otherwise
        """
        # if tiles has nothing in it then True
        if len(tiles) == 0:
            return True
        # if tiles has pieces that are different colors then False
        if any(tiles[0].color != same_color.color for same_color in tiles):
            return False
        # if piece is the same color as all of the tiles
        if piece.color != tiles[0].color:
            return False
        return True

    def same_shape(self, piece, tiles):
        """checks if the given piece is the same shape of all the pieces in tiles and that a piece already exists in the row or column

        Args:
            piece (Piece): Piece that will be check to see if it is the same shape as the tiles
            tiles (Piece[]): list of Pieces that should all be the same shape if they are not then return false

        Returns:
            bool: True if the given piece is the same shape as all the tiles and all the tiles are same shape as well. False otherwise
        """
        # if tiles has nothing in it then True
        if len(tiles) == 0:
            return True
        # if tiles has pieces that are different shapes then False
        if any(tiles[0].shape != tile.shape for tile in tiles):
            return False
        # if piece is the same color as all of the tiles
        if piece.shape != tiles[0].shape:
            return False
        return True
    
    def piece_already_exists(self, piece, tiles):
        """Checks if the given is piece already exists in the set of tiles

        Args:
            piece (Piece): Piece that will be checked to see if it already exists in the set of Pieces
            tiles (Piece[]): The set of Pieces that should all be unique
            
        Returns:
            bool: True if the piece does not exist false if it alread does 
        """
        return not any(piece == tile for tile in tiles)

    def matches_in_row(self, piece, location):
        """eturns if the given piece follows the q game rules at the given position for the row

        Args:
            piece (Piece): Piece to check
            location (Position): location of piece to check

        Returns:
            bool: true if it follows the rules for all other peices in the row it is either the same color or same shape. false if it does not match.
        """
        position_in_row = self._num_tiles_in_direction(location, -1)\
            + (self._num_tiles_in_direction(location, 1))
        pieces_in_row = [self.get(position) for position in position_in_row]
        return (self.same_color(piece, pieces_in_row) or self.same_shape(piece, pieces_in_row)) and self.piece_already_exists(piece, pieces_in_row)

    def matches_in_column(self, piece, location):
        """returns if the given piece follows the q game rules at the given position for the column

        Args:
            piece (Piece): Piece to check
            location (Position): Position to check

        Returns:
            bool: bool - true if it follows the rules for all other peices in the column it is either the same color or same shape. false if it does not match.
        """
        position_in_column = self._num_tiles_in_direction(location, -1, row_scan=False)\
            + (self._num_tiles_in_direction(location, 1, row_scan=False))
        pieces_in_column = [self.get(position) for position in position_in_column]
        return (self.same_color(piece, pieces_in_column) or self.same_shape(piece, pieces_in_column)) and self.piece_already_exists(piece, pieces_in_column)

    def can_play_piece_here(self, piece, location):
        """can a piece be played at a location and it follows the q game rules

        Args:
            piece (Piece): Piece to check
            location (Position): Position to check

        Returns:
            bool: true if the given piece and location is a valid placement. false otherwise
        """
        if not self.played(location):
            adjacent_positions = self.get_adjacent(location)
            has_adjacent = False
            for tile in adjacent_positions:
                if tile != Piece(Shapes.board.name, Colors.board.name):
                    has_adjacent = True
            return has_adjacent and self.matches_in_row(piece, location) and self.matches_in_column(piece, location)
        return False

    def get_valid_locations(self, piece):
        """returns the possible valid locations to place pieces

        Args:
            piece (Piece): Piece that is getting all valid locations for

        Returns:
            Position[]: all valid locations that the given Piece can be placed at
        """
        valid_locations = list()
        for row in range(self.row_offset - 1, len(self.pieces[0])+self.row_offset + 1):
            for column in range(self.column_offset - 1, len(self.pieces)+self.column_offset + 1):
                cur_position = Position(row, column)
                if self.can_play_piece_here(piece, cur_position):
                    valid_locations.append(cur_position)
        return valid_locations

    def _num_tiles_in_direction(self, location, iter, row_scan=True):
        """Helper method used to iterate in a directiony_

        Args:
            location (Postion): the starting position for the search does not include it self in the search
            iter (int): can be -1 to search left and up or 1 to search right and down
            row_scan (bool): is true to search the row and false to search the column

        Returns:
            Position[]: the positions in the row/column that contatain a piece that is not a board piece
        """
        pieces_set = list()
        step = iter
        if row_scan:
            while self.get(Position(location.row, location.column+iter)) != BOARD_PIECE:
                pieces_set.append(Position(location.row, location.column+iter))
                iter += step
        else:
            while self.get(Position(location.row+iter, location.column)) != BOARD_PIECE:
                pieces_set.append(Position(location.row+iter, location.column))
                iter += step
        
        return pieces_set

    def get_row_from_location(self, location):
        """creates a row object representing all of the pieces in the row of the given location

        Args:
            location (Position): creates the row from the other tiles next to this position

        Returns:
            Segment: The row containing this location
        """
        prev_positions = self._num_tiles_in_direction(location, -1)
        prev_positions.reverse()
        next_positions = self._num_tiles_in_direction(location, 1)
        start = 0
        stop = 0
        if len(prev_positions) == 0 and len(next_positions) == 0:
            return Segment(location.column, location.column, location.row)
        elif len(prev_positions) == 0:
            start = location.column
            stop = next_positions[len(next_positions)-1].column
        elif len(next_positions) == 0:
            start = prev_positions[0].column
            stop = location.column
        else:
            start = prev_positions[0].column
            stop = next_positions[len(next_positions)-1].column
        return Segment(start, stop, location.row)
    
    def get_column_from_location(self, location):
        """creates a column object that conatians the piece at the pieces in the column of the given location

        Args:
            location (Position): creates the column from the finding the other tiles also in column

        Returns:
            Segment: the column containing this location
        """
        prev_positions = self._num_tiles_in_direction(location, -1, row_scan=False)
        prev_positions.reverse()
        next_positions = self._num_tiles_in_direction(location, 1, row_scan=False)
        start = 0
        stop = 0
        if len(prev_positions) == 0 and len(next_positions) == 0:
            return Segment(location.row, location.row, location.column)
        elif len(prev_positions) == 0:
            start = location.row
            stop = next_positions[len(next_positions)-1].row
        elif len(next_positions) == 0:
            start = prev_positions[0].row
            stop = location.row
        else:
            start = prev_positions[0].row
            stop = next_positions[len(next_positions)-1].row
        return Segment(start, stop, location.column)

    def get_contiguous_pieces(self, locations):
        """helper method for the getting all of the contiguous pieces at a given location

        Args:
            locations (Postion[]): list of Positions to check

        Returns:
            Postion[]: all the Positions that the piece at the given location is contiguous to
        """
        rows = set()
        columns = set()
        for location in locations:
            cur_row = self.get_row_from_location(location)
            cur_column = self.get_column_from_location(location)
            if cur_row.stop - cur_row.start != 0:
                rows.add(cur_row)
            if cur_column.stop - cur_column.start != 0:
                columns.add(cur_column)

           
        total_piece_num = 0
        for r in rows:
            total_piece_num += r.length()
        for c in columns:
            total_piece_num += c.length()
        return total_piece_num

    def q_color_completed(self, locations):
        """Determine if the group of locations provided have one piece for each possible color, and no more.

        Args:
            locations (Positions[]): list of Positions to check for q color completeness

        Returns:
            bool: true if the all the locations contain every color in Colors
        """
        if len(locations) < 6:
            return False
        possible_colors = list(x for x in list(Colors))
        possible_colors.remove(Colors.board) # removes the board piece from the possible_colors
        for p in locations:
            piece_color = self.get(p).color
            if not piece_color in possible_colors:
                return False
            else:
                possible_colors.remove(piece_color)
        return len(possible_colors) == 0

    def q_shape_completed(self, locations):
        """Determine if the group of locations provided have one piece for each shape, and no more.

        Args:
            locations (Position[]): list of Positions to check for q shape completeness

        Returns:
            bool: true if the all the locations contain every color in Shapes
        """
        possible_shapes = list(x for x in list(Shapes))
        possible_shapes.remove(Shapes.board)
        for p in locations:
            piece_shape = self.get(p).shape
            if not piece_shape in possible_shapes:
                return False
            else:
                possible_shapes.remove(piece_shape)
        return len(possible_shapes) == 0

    def q_completed(self, locations):
        """When given a list of positions, this method determines if a "Q" has been completed, meaning a contigous row or column has been created with each possible shape or color, and nothing else.

        Args:
            locations (Postion[]): list of Positions where a piece was played

        Returns:
            int: the score returned after checking for completeness
        """
        q_row_completed = False
        q_column_completed = False
        for location in locations:
            if not q_row_completed:
                contiguous_row_set = self._num_tiles_in_direction(location, -1)\
                    + (self._num_tiles_in_direction(location, 1))
                contiguous_row_set.append(location)
                if self.q_color_completed(contiguous_row_set)\
                    or self.q_shape_completed(contiguous_row_set):
                    q_row_completed = True
            if not q_column_completed:
                contiguous_column_set = self._num_tiles_in_direction(location, -1, row_scan=False)\
                    + (self._num_tiles_in_direction(location, 1, row_scan=False))
                contiguous_column_set.append(location)
                if self.q_color_completed(contiguous_column_set)\
                    or self.q_shape_completed(contiguous_column_set):
                    q_column_completed = True           

        score = 0
        if q_row_completed:
            score += 1
        if q_column_completed:
            score += 1
        return score

    def num_contiguous_pieces(self, locations):
        """Returns the number of pieces that are in the same row or column as the provided position. This is used for scoring moves.

        Args:
            locations (Postion[]): list of Positions to ckeck

        Returns:
            int: the length of all of the contiguous pieces
        """
        return self.get_contiguous_pieces(locations)

    def get_all_pieces(self):
        """gets all the player pieces on the board

        Returns:
            Piece[]: list of all the Pieces on the board that are not board Pieces
        """
        l_pieces = []
        for col in self.pieces:
            for row in col:
                if row.color != Colors.board and row.shape != Shapes.board:
                    l_pieces.append(row)
        return l_pieces

    def grow_board(self, increase_row, increase_column):
        """grows the board by increasing the row and or column to specified length in both the positive or negative direction. Makes calls to the grow method to achive this

        Args:
            increase_row (int): int (+/-) direction and magnitiude to grow the row
            increase_column (int): int (+/-) direction and magnitiude to grow the column
            
        Side Affects:
            grows self.pieces 2d array by appending board pieces or lists of board pieces
        """

        absolute_row = increase_row - self.row_offset
        absolute_column = increase_column - self.column_offset
        
        if absolute_row < 0:
            self._grow(0, absolute_row)
        elif absolute_row > 0:
            if absolute_row < len(self.pieces[0]) - 1:
                if absolute_column < 0:
                    self._grow(absolute_column, 0)
                elif absolute_column > 0:
                    if absolute_column < len(self.pieces) - 1:
                        return
                    positive_column_addition = absolute_column - len(self.pieces) + 1
                    self._grow(positive_column_addition, 0)
                return
            positive_row_addition = absolute_row - len(self.pieces[0]) + 1
            self._grow(0, positive_row_addition)
        
        if absolute_column < 0:
            self._grow(absolute_column, 0)
        elif absolute_column > 0:
            if absolute_column < len(self.pieces) - 1:
                return
            positive_column_addition = absolute_column - len(self.pieces) + 1
            self._grow(positive_column_addition, 0)
