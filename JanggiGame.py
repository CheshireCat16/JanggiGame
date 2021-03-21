# Author: John Cheshire
# Date: March 9, 2021
# Description: This file contains classes to implement the game Janggi. No
#               user interface is provided, but the game can be played from the
#               command line. Basic rules for the way pieces can move and when
#               the general is in check are enforced.
#
# Future Plans -    Complete rules for draws
#                   Add AI implementation
#                   Improve AI by having learning by playing another AI
from copy import deepcopy


class JanggiPiece:
    """
    This is a super class for all Janggi pieces. The JanggiPiece class and its
    subclasses interact with the JanggiBoard to assist in determining whether or
    not moves are valid.
    """

    def __init__(self, color: str):
        """
        Initializes a JanggiPiece with color
        :param color: The "color" or side of the piece that is being initialized
        """
        self._row = None
        self._column = None
        self._piece_type = None
        self._on_board = False
        self._color = color

    def __str__(self):
        """
        Returns the color and type of the piece
        :return: Piece color and type
        """
        return self._color + " " + self._piece_type

    def __repr__(self):
        """
        Returns the color and type of the piece
        :return: Piece color and type
        """
        return "JanggiPiece(color=" + self._color + ")"

    def set_location(self, row: int, column: int):
        """
        Sets the piece on a location on the board
        :param row: The row where the piece is, 0 to 9.
        :param column: The column where the piece is, 0 to 8
        :return: Nothing
        """
        self._row = row
        self._column = column
        self._on_board = True

    def remove(self):
        """
        Updates the pieces info after its been removed from the board
        :return: Nothing
        """
        self._row = None
        self._column = None
        self._on_board = False

    def check_piece_on_board(self) -> bool:
        """
        Checks whether a piece is currently on the board
        :return: True or False
        """
        return self._on_board

    def get_color(self) -> str:
        """
        Returns the color of the piece
        :return: string for color of piece
        """
        return self._color

    def get_location(self) -> (int, int):
        """
        Gets the current location of a piece
        :return: Tuple of row, column integers
        """
        return self._row, self._column

    def check_move(self, row, column, board: "JanggiBoard") -> bool:
        """
        Determine whether or not the requested move is valid
        :param row: Row of move destination
        :param column: Column of move destination
        :param board: Board that move is happening on
        :return: True or False
        """
        valid_moves = self.find_valid_moves(board)
        for move in valid_moves:
            if (row, column) == move:
                return True
        return False


class General(JanggiPiece):
    """This is the class for the general piece. It inherits from JanggiPiece"""

    def __init__(self, color: str):
        """Initializes the General piece with color"""
        super().__init__(color)
        self._piece_type = "General"

    def __repr__(self):
        """
        Returns the color and type of the piece"
        :return: Piece color and type
        """""
        return "General(color=" + self._color + ")"

    def find_valid_moves(self, board: "JanggiBoard") -> list:
        """
        Creates a list of all valid . Note: does not check for check
        :param board: The JanggiBoard object to find moves on
        :return: list of moves that are valid
        """
        valid_move_list = []
        current_position = self.get_location()
        current_side = self.get_color()

        # Set up the palace row range for either red or blue side
        if current_side == "red":
            palace_range = [0, 3]
        else:
            palace_range = [7, 10]

        # The king can only move diagonally if not in the North / South / East / West spot in castle
        if board.check_special_palace_move(current_position[0], current_position[1]):
            # Iterate over the palace spaces
            for row in range(palace_range[0], palace_range[1]):
                for column in range(3, 6):
                    # Check if the space in question is only a move of 1 away
                    if abs(row - current_position[0]) < 2 and abs(column - current_position[1]) < 2:
                        # Make sure the space is empty or an enemy piece
                        if board.check_empty_or_enemy_or_off_board(row, column, current_side):
                            valid_move_list.append((row, column))
        # Check moves in standard four directions
        else:
            move_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for move_row, move_column in move_directions:
                if board.check_empty_or_enemy_or_off_board(current_position[0] + move_row, current_position[1] +
                                                                                           move_column, current_side):
                    if board.check_space_in_palace(current_position[0] + move_row, current_position[1] + move_column):
                        valid_move_list.append((current_position[0] + move_row, current_position[1] + move_column))

        return valid_move_list

    def get_piece_type(self) -> str:
        """Returns a string for the piece type"""
        return self._piece_type


class Guard(JanggiPiece):
    """This is the class for the Guard piece. It inherits from JanggiPiece"""

    def __init__(self, color: str):
        """Initializes the Guard piece with color"""
        super().__init__(color)
        self._piece_type = "Guard"

    def __repr__(self):
        """
        Returns the color and type of the piece"
        :return: Piece color and type
        """""
        return "Guard(color=" + self._color + ")"

    def find_valid_moves(self, board: "JanggiBoard") -> list:
        """
        Creates a list of all valid moves
        :param board: The JanggiBoard object to find moves on
        :return: list of moves that are valid
        """
        valid_move_list = []
        current_position = self.get_location()
        current_side = self.get_color()

        # Set up the palace row range for either red or blue side
        if current_side == "red":
            palace_range = [0, 3]
        else:
            palace_range = [7, 10]

        # The Guard can only move diagonally if not in the North / South / East / West spot in castle
        if board.check_special_palace_move(current_position[0], current_position[1]):
            # Iterate over the palace spaces
            for row in range(palace_range[0], palace_range[1]):
                for column in range(3, 6):
                    # Check if the space in question is only a move of 1 away
                    if abs(row - current_position[0]) < 2 and abs(column - current_position[1]) < 2:
                        # Make sure the space is empty or an enemy piece
                        if board.check_empty_or_enemy_or_off_board(row, column, current_side):
                            valid_move_list.append((row, column))

        # Check moves in standard four directions
        else:
            move_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for move_row, move_column in move_directions:
                if board.check_empty_or_enemy_or_off_board(current_position[0] + move_row, current_position[1] +
                                                                                           move_column, current_side):
                    if board.check_space_in_palace(current_position[0] + move_row, current_position[1] + move_column):
                        valid_move_list.append((current_position[0] + move_row, current_position[1] + move_column))

        return valid_move_list

    def get_piece_type(self) -> str:
        """Returns a string for the piece type"""
        return self._piece_type


class Horse(JanggiPiece):
    """This is the class for the Horse piece. It inherits from JanggiPiece"""

    def __init__(self, color: str):
        """Initializes the Horse piece with color"""
        super().__init__(color)
        self._piece_type = "Horse"

    def __repr__(self):
        """
        Returns the color and type of the piece"
        :return: Piece color and type
        """""
        return "Horse(color=" + self._color + ")"

    def find_valid_moves(self, board: "JanggiBoard") -> list:
        """
        Creates a list of all valid moves
        :param board: The JanggiBoard object to find moves on
        :return: list of moves that are valid
        """
        valid_move_list = []
        current_position = self.get_location()
        current_side = self.get_color()
        moves_and_spaces = [[(1, 0), (2, 1)],  # South East
                            [(1, 0), (2, -1)],  # South West
                            [(-1, 0), (-2, 1)],  # North East
                            [(-1, 0), (-2, -1)],  # North West
                            [(0, -1), (1, -2)],  # West South
                            [(0, -1), (-1, -2)],  # West North
                            [(0, 1), (1, 2)],  # East South
                            [(0, 1), (-1, 2)]]  # East North

        # Go through each possible move
        for move_direction in moves_and_spaces:
            # This tracks whether an invalid condition has been found
            valid_move = True

            # Check each space the piece will move through
            for row_move, column_move in move_direction:
                target_position = current_position[0] + row_move, current_position[1] + column_move
                # If it's the target space of the move, check if it's empty or enemy
                if (row_move, column_move) == move_direction[-1]:
                    if not board.check_empty_or_enemy_or_off_board(target_position[0], target_position[1],
                                                                   current_side):
                        valid_move = False
                # Check if the space is empty if the piece is just moving through
                else:
                    if not board.check_empty_or_off_board(target_position[0], target_position[1], current_side):
                        valid_move = False

            if valid_move:
                valid_move_list.append((target_position[0], target_position[1]))

        return valid_move_list

    def get_piece_type(self) -> str:
        """Returns a string for the piece type"""
        return self._piece_type


class Elephant(JanggiPiece):
    """This is the class for the Elephant piece. It inherits from JanggiPiece"""

    def __init__(self, color: str):
        """Initializes the Elephant piece with color"""
        super().__init__(color)
        self._piece_type = "Elephant"

    def __repr__(self):
        """
        Returns the color and type of the piece"
        :return: Piece color and type
        """""
        return "Elephant(color=" + self._color + ")"

    def find_valid_moves(self, board: "JanggiBoard") -> list:
        """
        Creates a list of all valid moves
        :param board: The JanggiBoard object to find moves on
        :return: list of moves that are valid
        """
        valid_move_list = []
        current_position = self.get_location()
        current_side = self.get_color()
        moves_and_spaces = [[(1, 0), (2, 1), (3, 2)],  # South East
                            [(1, 0), (2, -1), (3, -2)],  # South West
                            [(-1, 0), (-2, 1), (-3, 2)],  # North East
                            [(-1, 0), (-2, -1), (-3, -2)],  # North West
                            [(0, -1), (1, -2), (2, -3)],  # West South
                            [(0, -1), (-1, -2), (-2, -3)],  # West North
                            [(0, 1), (1, 2), (2, 3)],  # East South
                            [(0, 1), (-1, 2), (-2, 3)]]  # East North

        # Go through each possible move
        for move_direction in moves_and_spaces:
            # This tracks whether an invalid condition has been found
            valid_move = True

            # Check each space the piece will move through
            for row_move, column_move in move_direction:
                target_position = current_position[0] + row_move, current_position[1] + column_move
                # If it's the target space of the move, check if it's empty or enemy
                if (row_move, column_move) == move_direction[-1]:
                    if not board.check_empty_or_enemy_or_off_board(target_position[0], target_position[1],
                                                                   current_side):
                        valid_move = False
                # Check if the space is empty if the piece is just moving through
                else:
                    if not board.check_empty_or_off_board(target_position[0], target_position[1], current_side):
                        valid_move = False

            if valid_move:
                valid_move_list.append(target_position)
        return valid_move_list

    def get_piece_type(self) -> str:
        """Returns a string for the piece type"""
        return self._piece_type


class Chariot(JanggiPiece):
    """This is the class for the Chariot piece. It inherits from JanggiPiece"""

    def __init__(self, color: str):
        """Initializes the Chariot piece with color"""
        super().__init__(color)
        self._piece_type = "Chariot"

    def __repr__(self):
        """
        Returns the color and type of the piece"
        :return: Piece color and type
        """""
        return "Chariot(color=" + self._color + ")"

    def find_valid_moves(self, board: "JanggiBoard") -> list:
        """
        Creates a list of all valid moves
        :param board: The JanggiBoard object to find moves on
        :return: list of moves that are valid
        """
        valid_move_list = []
        current_position = self.get_location()
        current_side = self.get_color()
        moves_directions = [(1, 0),  # South
                            (-1, 0),  # North
                            (0, 1),  # East
                            (0, -1)]  # West

        # Check each move direction
        for row_move, column_move in moves_directions:
            target_position = current_position[0] + row_move, current_position[1] + column_move
            # Continue adding moves until piece would be off the board or a piece blocks
            piece_found = False
            while board.check_empty_or_enemy_or_off_board(target_position[0], target_position[1], current_side) \
                    and not piece_found:
                if board.get_space_info(target_position[0], target_position[1]) is not None:
                    piece_found = True
                valid_move_list.append(target_position)
                target_position = target_position[0] + row_move, target_position[1] + column_move

        # Check for valid moves in the place
        if board.check_special_palace_move(current_position[0], current_position[1]):
            moves_directions = [(1, 1),  # South East
                                (-1, 1),  # North East
                                (-1, -1),  # North West
                                (1, -1)]  # South West

            for row_move, column_move in moves_directions:
                target_position = current_position[0] + row_move, current_position[1] + column_move
                # Continue adding moves until piece would be off the board or a piece blocks
                piece_found = False
                while board.check_empty_or_enemy_or_off_board(target_position[0], target_position[1], current_side) \
                        and not piece_found and board.check_space_in_palace(target_position[0], target_position[1]):
                    if board.get_space_info(target_position[0], target_position[1]) is not None:
                        piece_found = True
                    valid_move_list.append(target_position)
                    target_position = target_position[0] + row_move, target_position[1] + column_move

        return valid_move_list

    def get_piece_type(self) -> str:
        """Returns a string for the piece type"""
        return self._piece_type


class Cannon(JanggiPiece):
    """This is the class for the Cannon piece. It inherits from JanggiPiece"""

    def __init__(self, color: str):
        """Initializes the Cannon piece with color"""
        super().__init__(color)
        self._piece_type = "Cannon"

    def __repr__(self):
        """
        Returns the color and type of the piece"
        :return: Piece color and type
        """""
        return "Cannon(color=" + self._color + ")"

    def find_valid_moves(self, board: "JanggiBoard") -> list:
        """
        Creates a list of all valid moves
        :param board: The JanggiBoard object to find moves on
        :return: list of moves that are valid
        """
        valid_move_list = []
        current_position = self.get_location()
        current_side = self.get_color()
        moves_directions = [(1, 0),  # South
                            (-1, 0),  # North
                            (0, 1),  # East
                            (0, -1)]  # West

        # Check each move direction
        for row_move, column_move in moves_directions:
            target_position = current_position[0] + row_move, current_position[1] + column_move

            # Check number of pieces jumped and whether or not to stop checking for moves
            pieces_jumped = 0
            end_of_direction = False
            while board.check_location_on_board(target_position[0], target_position[1]) and not end_of_direction:
                # Get the status of the space being examined (piece object or None)
                target_space_info = board.get_space_info(target_position[0], target_position[1])
                # If the space is not empty
                if target_space_info is not None:
                    # A cannon cannot be jumped over
                    if isinstance(target_space_info, Cannon):
                        end_of_direction = True
                    # If we've already jumped a piece and encounter a friendly piece, no more valid moves
                    elif pieces_jumped > 0 and target_space_info.get_color() == current_side:
                        end_of_direction = True
                    # This is an enemy piece and not a cannon
                    else:
                        # If we've jumped a piece we can take the piece
                        if pieces_jumped == 1:
                            valid_move_list.append(target_position)
                            end_of_direction = True
                    # Set the piece as jumped
                    pieces_jumped += 1

                    # Cannot jump more than one piece
                    if pieces_jumped > 1:
                        end_of_direction = True
                # Handles the case of an empty space
                else:
                    # Add this as a valid move space if one piece has been jumped
                    if pieces_jumped == 1:
                        valid_move_list.append(target_position)

                # Move target to next position
                target_position = target_position[0] + row_move, target_position[1] + column_move

        # Check for valid moves in the palace
        if board.check_space_in_palace(current_position[0], current_position[1]):
            moves_directions = [(1, 1),  # South East
                                (-1, 1),  # North East
                                (-1, -1),  # North West
                                (1, -1)]  # South West
            # Check each move direction
            for row_move, column_move in moves_directions:
                target_position = current_position[0] + row_move, current_position[1] + column_move

                # Check number of pieces jumped and whether or not to stop checking for moves
                pieces_jumped = 0
                end_of_direction = False
                while board.check_space_in_palace(target_position[0], target_position[1]) and not end_of_direction:
                    # Get the status of the space being examined (piece object or None)
                    target_space_info = board.get_space_info(target_position[0], target_position[1])
                    # If the space is not empty
                    if target_space_info is not None:
                        # A cannon cannot be jumped over
                        if isinstance(target_space_info, Cannon):
                            end_of_direction = True
                        # If we've already jumped a piece and encounter a friendly piece, no more valid mores
                        elif pieces_jumped > 0 and target_space_info.get_color() == current_side:
                            end_of_direction = True
                        # This is an enemy piece and no a cannon
                        else:
                            # If we've jumped a piece we can take the piece
                            if pieces_jumped == 1:
                                valid_move_list.append(target_position)
                                end_of_direction = True
                        # Set the piece as jumped
                        pieces_jumped += 1

                        # Cannot jump more than one piece
                        if pieces_jumped > 1:
                            end_of_direction = True
                    # Handles the case of an empty space
                    else:
                        # Add this as a valid move space if one piece has been jumped
                        if pieces_jumped == 1:
                            valid_move_list.append(target_position)

                    # Move target to next position
                    target_position = target_position[0] + row_move, target_position[1] + column_move

        return valid_move_list

    def get_piece_type(self) -> str:
        """Returns a string for the piece type"""
        return self._piece_type


class Soldier(JanggiPiece):
    """This is the class for the Soldier piece. It inherits from JanggiPiece"""

    def __init__(self, color: str):
        """Initializes the Soldier piece with color"""
        super().__init__(color)
        self._piece_type = "Soldier"

    def __repr__(self):
        """
        Returns the color and type of the piece"
        :return: Piece color and type
        """""
        return "Soldier(color=" + self._color + ")"

    def find_valid_moves(self, board: "JanggiBoard") -> list:
        """
        Creates a list of all valid moves
        :param board: The JanggiBoard object to find moves on
        :return: list of moves that are valid
        """
        valid_move_list = []
        current_position = self.get_location()
        move_direction = -1
        current_side = self.get_color()

        # Red soldier can only move "down" the board, or increasing row
        if self.get_color() == "red":
            move_direction = 1

        # Check moves in basic three directions
        move_list = [(0, -1), (0, 1), (move_direction, 0)]
        for move_row, move_column in move_list:
            target_position = current_position[0] + move_row, current_position[1] + move_column
            # Confirm the space is empty or contains an enemy piece
            if board.check_empty_or_enemy_or_off_board(target_position[0], target_position[1], current_side):
                valid_move_list.append(target_position)

        # Check for valid moves in the palace
        if board.check_special_palace_move(current_position[0], current_position[1]):
            move_list = [(move_direction, -1), (move_direction, 1)]
            for move_row, move_column in move_list:
                target_position = current_position[0] + move_row, current_position[1] + move_column
                # Check if the space to be moved to is in the palace
                if board.check_space_in_palace(target_position[0], target_position[1]):
                    # Confirm the space is empty or contains an enemy piece
                    if board.check_empty_or_enemy_or_off_board(target_position[0], target_position[1], current_side):
                        valid_move_list.append(target_position)

        # All valid moves listed, return the list
        return valid_move_list

    def get_piece_type(self) -> str:
        """Returns a string for the piece type"""
        return self._piece_type


class JanggiBoard:
    """The class that represents the board of the game"""

    def __init__(self, spaces: list = None):
        """Initializes the board with a blank slate"""
        if spaces is None:
            self._spaces = [[None for x in range(0, 9)] for x in range(0, 10)]
        else:
            self._spaces = spaces

    def update_location(self, row: int, column: int, piece: JanggiPiece):
        """
        Updates the location of a piece
        :param row: The row of the target location
        :param column: The column of the target location
        :param piece: The piece to be moved
        :return: None
        """
        # Take the piece off the board from its current location
        if piece.check_piece_on_board():
            from_location = piece.get_location()
            self.clear_space(from_location[0], from_location[1])
        piece.remove()

        # Remove the taken piece currently in the location if necessary
        taken_piece = self.get_space_info(row, column)
        if taken_piece is not None:
            taken_piece.remove()

        # Put the piece back on the board
        self.set_space_info(row, column, piece)
        piece.set_location(row, column)

    def get_board_layout(self) -> list:
        """
        Returns the matrix of the board's spaces and piece locations
        :return: 10 x 9 matrix of spaces
        """
        return self._spaces

    @staticmethod
    def check_special_palace_move(row: int, column: int) -> bool:
        """
        Checks whether the piece is in a space that will require checking for diagnol moves
        :param row: Row of space to check
        :param column: Column of space to check
        :return: True if a special move is possible
        """
        current_position = row, column
        if current_position != (1, 3) and current_position != (1, 5) and current_position != (0, 4) and \
                current_position != (2, 4) and current_position != (8, 3) and current_position != (8, 5) and \
                current_position != (9, 4) and current_position != (7, 4):
            return True
        else:
            return False

    def get_space_info(self, row: int, column: int) -> JanggiPiece:
        """
        Returns the current piece at the specified location, or None
        :param row: Row of space to check
        :param column: Column of space to check
        :return: Piece at that location, or None
        """
        return self._spaces[row][column]

    def set_space_info(self, row: int, column: int, piece: JanggiPiece):
        """
        Sets the piece on a specific board space
        :param row: Row to set
        :param column: Column to set
        :param piece: Piece to set in space
        :return: Nothing
        """
        self._spaces[row][column] = piece

    def clear_space(self, row: int, column: int):
        """
        Sets the specified space to be empty
        :param row: row of space to clear
        :param column: column of space to clear
        :return: nothing
        """
        self._spaces[row][column] = None

    @staticmethod
    def check_space_in_palace(row, column) -> bool:
        """
        Checks whether a space is located in the palace
        :param row: row of space to check
        :param column: column of space to check
        :return: True or False
        """
        # Columns 0 - 2 and 6 to 8 are not in the palace
        if column < 3 or column > 5:
            return False
        # Rows less than 0 and greater than 9 are off the board
        elif row < -1 or row > 9:
            return False
        # Only rows less than 3 or greater than 6 are in the palace
        elif row < 3 or row > 6:
            return True
        else:
            return False

    def check_empty_or_enemy_or_off_board(self, row: int, column: int, side: str) -> bool:
        """
        Check whether the specified space is empty or has an enemy piece
        or is not on the board
        :param row: row of space to check
        :param column: column of space to check
        :param side: Side of current player
        :return: True if empty or enemy, otherwise False
        """
        if not self.check_location_on_board(row, column):
            return False
        target_space_piece = self.get_space_info(row, column)
        if target_space_piece is None:
            return True
        elif target_space_piece.get_color() != side:
            return True
        else:
            return False

    def check_empty_or_off_board(self, row: int, column: int, side: str) -> bool:
        """
        Check whether the specified space is empty or is not on the board
        :param row: row of space to check
        :param column: column of space to check
        :param side: Side of current player
        :return: True if empty otherwise False
        """
        if not self.check_location_on_board(row, column):
            return False
        target_space_piece = self.get_space_info(row, column)
        if target_space_piece is None:
            return True
        else:
            return False

    @staticmethod
    def check_location_on_board(row: int, column: int) -> bool:
        """
        Checks whether a location in on the board or not
        :param row: Row of location to check
        :param column: Column of location to check
        :return: True or False
        """
        if column < 0 or column > 8 or row < 0 or \
                row > 9:
            return False
        else:
            return True


class Side:
    """This class represents one of the two sides of the game"""

    def __init__(self, color: str):
        """
        Sets the sides color and creates the piece objects for that side
        :param color: Color of the side, Blue or Red
        """
        self._color = color
        self._pieces = []
        self._pieces.append(General(color))
        self._pieces.append(Guard(color))
        self._pieces.append(Guard(color))
        self._pieces.append(Horse(color))
        self._pieces.append(Horse(color))
        self._pieces.append(Elephant(color))
        self._pieces.append(Elephant(color))
        self._pieces.append(Chariot(color))
        self._pieces.append(Chariot(color))
        self._pieces.append(Cannon(color))
        self._pieces.append(Cannon(color))
        self._pieces.append(Soldier(color))
        self._pieces.append(Soldier(color))
        self._pieces.append(Soldier(color))
        self._pieces.append(Soldier(color))
        self._pieces.append(Soldier(color))

    def get_pieces(self, on_board: bool) -> list:
        """
        Returns a list of pieces either on or off the board
        :param on_board: Specifies whether the function returns pieces on the
                            board (True) or off the board (False)
        :return: a list of JanggiPiece objects
        """
        return_list = []

        for piece in self._pieces:
            if piece.check_piece_on_board() == on_board:
                return_list.append(piece)

        return return_list

    def get_general(self) -> General:
        """
        Returns the general of that side
        :return: General piece
        """
        return self._pieces[0]

    def get_color(self) -> str:
        """
        Returns the sides color
        :return: string for color fo side
        """
        return self._color

    @staticmethod
    def move_piece(board: JanggiBoard, location: (int, int), piece: JanggiPiece):
        """
        Places a piece on the board during game initialization
        :param board: The game board
        :param location: The location to place the piece row, column
        :param piece: The JanggiPiece object to place on the board
        """
        board.update_location(location[0], location[1], piece)


class JanggiGame:
    """
    The JanggiGame class implements the game Janggi. It allows users to get the
    game status, check for whether or not a side is in check, and for pieces to
    be moved.
    It's private member variables contain other related classes like JanggiPiece,
    JanggiBoard, and Side. JangiPiece and it's subclasses have methods that
    check for valid moves. The JanggiBoard keeps track of where the pieces are
    and tells the game where pieces are on the board. The Side class is used to
    get a list of pieces on each side and test when a move can be made by the
    side.
    """

    def __init__(self):
        """
        Initializes the Janggi game board, sets up the board, and sets up
        variables for the two generals
        """
        self._board = JanggiBoard()
        self._red_side = Side("red")
        self._blue_side = Side("blue")
        self._red_general = self._red_side.get_general()
        self._blue_general = self._blue_side.get_general()
        self.set_up_board(self._blue_side)
        self.set_up_board(self._red_side)
        self._current_side = self._blue_side
        self._game_state = "UNFINISHED"

    def get_game_state(self) -> str:
        """
        Returns the state of the game: UNFINISHED, RED_WON, BLUE_WON
        :return: State of game - UNFINISHED, RED_WON, BLUE_WON
        """
        return self._game_state

    def set_game_state(self, new_state: str):
        """
        Sets the current game state with a new state
        :param new_state: New state to update
        :return: Nothing
        """
        self._game_state = new_state

    def is_in_check(self, side: str, board: JanggiBoard = None):
        """
        Determines whether or not the specified side is in check.
        :param side: The side to check for check status ("red" or "blue"
        :param board: The JanggiBoard to use to test for check
        :return: True if in check, False if not in check
        """
        # get general and position for side being checked
        target_general = self.get_side(side).get_general()
        general_position = target_general.get_location()
        general_in_check = False

        # Use the passed board or the current game board
        if board is None:
            board = self.get_board()

        # Get other side
        if side == "red":
            other_side = self.get_side("blue")
        else:
            other_side = self.get_side("red")

        # Get all the pieces on the board for the other side
        pieces_on_board = other_side.get_pieces(True)

        # This will hold all moves on the other side
        all_moves = []

        # Find all valid moves for the other side
        for piece in pieces_on_board:
            all_moves.append((piece, piece.find_valid_moves(board)))

        # Compare Generals location with valid moves

        for piece, moves in all_moves:
            for move in moves:
                if general_position == move:
                    general_in_check = True

        return general_in_check

    def make_move(self, from_location: (int, int), to_location: (int, int)) -> bool:
        """
        Moves a piece from the specified location to the specified location
        if the move is valid. Passing the same to and from space will result in
        a passed turn.
        :param from_space: The column, row reference of the from space
                            for example "a2"
        :param to_space: The column, row reference of the to space
                            for example "a2"
        :return: True if the move is successful, False if the move is
                        invalid.
        """
        # Get the current board state
        current_board = self.get_board()

        # Get the current side
        current_side = self.get_current_side()

        # Determine whether the General is currently in check
        general_in_check = self.is_in_check(current_side.get_color(), current_board)

        # Check if the to and from spaces and not in check are the same and pass turn if so.
        if from_location == to_location and not general_in_check:
            self.change_current_side()
            return True
        elif from_location == to_location and general_in_check:
            return False

        # This is the peice that is going to move
        moving_piece = current_board.get_space_info(from_location[0], from_location[1])

        # If there was no piece in the specified space return False
        if moving_piece is None:
            return False

        # Check if the piece is on the current side
        if moving_piece.get_color() != current_side.get_color():
            return False

        # Make sure the game isn't over already
        if self.get_game_state() != "UNFINISHED":
            return False

        # Make sure the specified space was on the board
        if to_location[0] == -1:
            return False

        # Confirm that the move is valid, move the piece, and update the side
        if moving_piece.check_move(to_location[0], to_location[1], current_board):
            # Create a test board and test the move for check
            test_board = deepcopy(current_board)
            target_piece = current_board.get_space_info(to_location[0], to_location[1])
            if target_piece is not None:
                target_piece.remove()
            test_board.clear_space(from_location[0], from_location[1])
            test_board.set_space_info(to_location[0], to_location[1], moving_piece)

            # Save the pieces old location and update it's new location to check for check
            old_location = moving_piece.get_location()
            moving_piece.set_location(to_location[0], to_location[1])

            # Test that the move doesn't move into check on the test board
            if not self.is_in_check(current_side.get_color(), test_board):
                # Restore old location
                moving_piece.set_location(old_location[0], old_location[1])
                if target_piece is not None:
                    target_piece.set_location(to_location[0], to_location[1])
                current_side.move_piece(current_board, (to_location[0], to_location[1]), moving_piece)
                self.change_current_side()

                # Check for check mate by first checking for check
                current_side = self.get_current_side()
                if self.is_in_check(current_side.get_color()):
                    possible_moves = []
                    pieces_on_board = current_side.get_pieces(True)
                    check_mate = True

                    # Get all valid moves on the checked side
                    for piece in pieces_on_board:
                        possible_moves.append((piece, piece.find_valid_moves(current_board)))

                    # Check if any moves can be taken where the general is not in check
                    for piece, moves in possible_moves:
                        # Ends the loop if a valid move is found
                        if not check_mate:
                            break

                        # Loop through all the valid moves for the piece and see if any resolve the check
                        from_location = piece.get_location()
                        for move in moves:
                            test_board = deepcopy(current_board)
                            test_board.clear_space(from_location[0], from_location[1])
                            # Get info on move to location and remove piece if required
                            target_piece = test_board.get_space_info(move[0], move[1])
                            if target_piece is not None:
                                target_piece.remove()
                            test_board.set_space_info(move[0], move[1], piece)

                            # Save the pieces old location and update it's new location to check for check
                            old_location = piece.get_location()
                            piece.set_location(move[0], move[1])

                            # Test for check in the test board
                            if not self.is_in_check(current_side.get_color(), test_board):
                                # Restore old location
                                piece.set_location(old_location[0], old_location[1])
                                if target_piece is not None:
                                    target_piece.set_location(move[0], move[1])
                                check_mate = False
                                # No need to search farther so break out of this for loop
                                break

                            # Restore old location
                            piece.set_location(old_location[0], old_location[1])
                            if target_piece is not None:
                                target_piece.set_location(move[0], move[1])

                    # Test for checkmate and declare a winner as required
                    if check_mate:
                        if current_side.get_color() == "red":
                            self.set_game_state("BLUE_WON")
                        else:
                            self.set_game_state("RED_WON")

                # The move did not result in moving into check, return True
                return True

            # Reset the pieces location after testing for move into check
            moving_piece.set_location(old_location[0], old_location[1])
            if target_piece is not None:
                target_piece.set_location(to_location[0], to_location[1])

        # If the move isn't valid, return false
        return False

    def get_board(self) -> JanggiBoard:
        """
        Returns the game board.
        :return: JanggiBoard in current state
        """
        return self._board

    def set_up_board(self, side: Side):
        """
        Sets up the initial board for one side of the game
        :param side: The Side object for the side to set up.
        :return: Nothing
        """
        list_of_pieces = side.get_pieces(False)
        if side.get_color() == "red":
            side.move_piece(self._board, (1, 4), list_of_pieces[0])  # General
            side.move_piece(self._board, (0, 3), list_of_pieces[1])  # Guards
            side.move_piece(self._board, (0, 5), list_of_pieces[2])
            side.move_piece(self._board, (0, 2), list_of_pieces[3])  # Horses
            side.move_piece(self._board, (0, 7), list_of_pieces[4])
            side.move_piece(self._board, (0, 1), list_of_pieces[5])  # Elephants
            side.move_piece(self._board, (0, 6), list_of_pieces[6])
            side.move_piece(self._board, (0, 0), list_of_pieces[7])  # Chariots
            side.move_piece(self._board, (0, 8), list_of_pieces[8])
            side.move_piece(self._board, (2, 1), list_of_pieces[9])  # Cannons
            side.move_piece(self._board, (2, 7), list_of_pieces[10])
            side.move_piece(self._board, (3, 0), list_of_pieces[11])  # Soldiers
            side.move_piece(self._board, (3, 2), list_of_pieces[12])
            side.move_piece(self._board, (3, 4), list_of_pieces[13])
            side.move_piece(self._board, (3, 6), list_of_pieces[14])
            side.move_piece(self._board, (3, 8), list_of_pieces[15])
        else:
            side.move_piece(self._board, (8, 4), list_of_pieces[0])  # General
            side.move_piece(self._board, (9, 3), list_of_pieces[1])  # Guards
            side.move_piece(self._board, (9, 5), list_of_pieces[2])
            side.move_piece(self._board, (9, 2), list_of_pieces[3])  # Horses
            side.move_piece(self._board, (9, 7), list_of_pieces[4])
            side.move_piece(self._board, (9, 1), list_of_pieces[5])  # Elephants
            side.move_piece(self._board, (9, 6), list_of_pieces[6])
            side.move_piece(self._board, (9, 0), list_of_pieces[7])  # Chariots
            side.move_piece(self._board, (9, 8), list_of_pieces[8])
            side.move_piece(self._board, (7, 1), list_of_pieces[9])  # Cannons
            side.move_piece(self._board, (7, 7), list_of_pieces[10])
            side.move_piece(self._board, (6, 0), list_of_pieces[11])  # Soldiers
            side.move_piece(self._board, (6, 2), list_of_pieces[12])
            side.move_piece(self._board, (6, 4), list_of_pieces[13])
            side.move_piece(self._board, (6, 6), list_of_pieces[14])
            side.move_piece(self._board, (6, 8), list_of_pieces[15])

    def translate_space(self, location: str) -> (int, int):
        """
        This method translates the passed board location from the form of
        "letter number" to (number, number) for use internally in the matrix
        of positions on the board.
        :param location: String of location in form "a1" for the top left
                         location on the board.
        :return: Returns a tuple of the row, column location. If an invalid input
                is provided, the method will return (-1, -1).
        """
        # Reduce "a1" row by one to start at 0
        row_location = int(location[1:]) - 1
        # subtract off the ASCII value of 'a' 97

        col_location = ord(location[0]) - 97
        # Check that the locations are on the board
        if not self.get_board().check_location_on_board(row_location, col_location):
            row_location = -1
            col_location = -1

        return row_location, col_location

    def get_current_side(self) -> Side:
        """
        Gets the side whose turn it is currently.
        :return: Side object current taking turn
        """
        return self._current_side

    def set_current_side(self, color: str):
        """
        Sets the current side to the specified side
        :param color: Color of the side to set
        :return: Nothing
        """
        if color == "blue":
            self._current_side = self._blue_side
        elif color == "red":
            self._current_side = self._red_side

    def change_current_side(self):
        """
        Updates the current side to the next side
        :return: Nothing
        """
        if self.get_current_side().get_color() == "blue":
            self.set_current_side("red")
        else:
            self.set_current_side("blue")

    def get_side(self, color: str) -> Side:
        """
        Returns the Side object of the specified color
        :param color: Color of the side to return
        :return: Side object
        """
        if color == "blue":
            return self._blue_side
        else:
            return self._red_side
