import copy

import utils.check_utils as check_utils
import utils.utils as utils
from modules.chess_piece import ChessPiece
from modules.king import King
from modules.pawn import Pawn


class Board:
    def __init__(self, player_colors, board=None):
        check_utils.check_is_iterable_of_unique_elements_with_length(
            "player_colors", player_colors, list, min_length=2
        )
        self.player_colors = player_colors

        if board is None:
            self._board = [[None for _ in range(8)] for _ in range(8)]
            self._board[0][4] = King((0, 4), player_colors[0], 4)
            self._board[7][4] = King((7, 4), player_colors[1], 3 * 8 + 4)
            self._board[1] = [
                Pawn((1, i), player_colors[0], 8 + i, "down") for i in range(8)
            ]
            self._board[6] = [
                Pawn((6, i), player_colors[1], 2 * 8 + i, "up") for i in range(8)
            ]
        else:
            self._board = board

        check_utils.check_is_iterable_of_length(
            "board", self._board, list, min_length=3, max_length=20
        )
        check_utils.check_is_iterable_of_length(
            "row_0", self._board[0], list, min_length=3, max_length=20
        )
        row_length = len(self._board[0])
        for i, row in enumerate(self._board[1:]):
            check_utils.check_is_iterable_of_length(f"row_{i}", row, list, row_length)

        self.piece_dict = self.construct_piece_dict()
        for player_color in self.player_colors:
            try:
                check_utils.check_is_iterable_of_length(
                    "King_list", self.piece_dict[(player_color, "king")], list, 1
                )
            except KeyError:
                raise ValueError(f"{player_color} player doesn't have a king")

        self.board_shape = (len(self._board), row_length)

        alphabet = [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
        ]
        self.letter_to_column = {
            letter: i for i, letter in enumerate(alphabet[: self.board_shape[1]])
        }
        self.letters = list(self.letter_to_column.keys())

    def __copy__(self):
        new_copy = Board(player_colors=self.player_colors, board=self._board)
        return new_copy

    def __deepcopy__(self, memodict={}):
        new_copy = Board(
            player_colors=copy.deepcopy(self.player_colors),
            board=copy.deepcopy(self._board),
        )
        return new_copy

    def __len__(self):
        return len(self._board)

    def __getitem__(self, coordinates):
        check_utils.check_is_instance_of_types("coordinates", coordinates, (tuple, str))
        if isinstance(coordinates, str):
            return self.get_piece_by_string(coordinates)

        for coordinate in coordinates:
            check_utils.check_is_instance_of_types(
                "coordinates", coordinate, (int, slice)
            )

        if isinstance(coordinates[0], slice):
            return [row[coordinates[1]] for row in self._board[coordinates[0]]]

        check_utils.check_is_non_negative("row_coordinate", coordinates[0])

        return self._board[coordinates[0]][coordinates[1]]

    def __setitem__(self, coordinates, piece):
        if piece is not None:
            check_utils.check_is_instance("ChessPiece", piece, ChessPiece)

        check_utils.check_is_instance_of_types("coordinates", coordinates, (tuple, str))
        if isinstance(coordinates, str):
            coordinates = self.string_to_coordinate(coordinates)

        for coordinate in coordinates:
            check_utils.check_is_instance_of_types(
                "coordinates", coordinate, (int, slice)
            )

        if isinstance(coordinates[0], slice):
            coordinate_0_list = utils.slice_to_list(coordinates[0], len(self))
        else:
            coordinate_0_list = [coordinates[0]]

        if isinstance(coordinates[1], slice):
            coordinate_1_list = utils.slice_to_list(coordinates[1], self.board_shape[1])
        else:
            coordinate_1_list = [coordinates[1]]

        for row in coordinate_0_list:
            for column in coordinate_1_list:
                self._board[row][column] = piece

    def __iter__(self):
        return iter(self._board)

    def __str__(self):
        return self.board_as_string()

    def __repr__(self):
        return str(self)

    def construct_piece_dict(self):
        piece_dict = {}
        for i, row in enumerate(self._board):
            for j, piece in enumerate(row):
                if piece is not None:
                    key = (piece["color"], piece["type"])
                    if key not in piece_dict:
                        piece_dict[key] = []
                    piece_dict[key].append((i, j))
        return piece_dict

    def string_to_coordinate(self, coordinate_string):
        if (
            len(coordinate_string) != 2
            or not coordinate_string[0].isalpha()
            or not coordinate_string[1].isdigit()
        ):
            raise TypeError(
                f"String coordinates must be in the format '<letter><int>', got "
                f"{coordinate_string}"
            )

        column_letter = coordinate_string[0]
        if column_letter not in self.letters:
            raise KeyError(f"Letter must be in {self.letters}, got {column_letter}")

        coordinate = (
            int(coordinate_string[1]) - 1,
            self.letter_to_column[column_letter],
        )

        return coordinate

    def board_as_string(self):
        board_string = "\n"  # Start with a newline
        for row in self._board:
            for piece in row:
                if piece is None:
                    board_string += "O "  # Add an 'O' and a space for empty squares
                else:
                    board_string += (
                        piece.symbol + " "
                    )  # Add the piece's symbol and a space
            board_string += "\n"  # Add a newline at the end of each row
        return board_string

    def display(self):
        print(self.board_as_string())

    def piece_as_string(
        self, piece_position
    ):  # THIS SHOULD RETURN STRING REPR OF PIECE
        check_utils.check_is_iterable_of_length(
            "piece_position", piece_position, tuple, 2
        )
        return "MOCKED"

    def get_board(self):
        return self._board

    def get_piece(self, coordinate):
        return self[coordinate]

    def get_piece_by_string(self, coordinate_string):
        coordinate = self.string_to_coordinate(coordinate_string)
        return self.get_piece(coordinate)

    def is_occupied(self, coordinate):
        check_utils.check_is_2d_coordinate(coordinate, self.board_shape)
        return isinstance(self[coordinate], ChessPiece)

    def is_on_board(self, coordinate):
        return utils.is_2d_coordinate(coordinate, self.board_shape)

    def move_piece(self, old_coordinate, new_coordinate):
        for coordinate in [old_coordinate, new_coordinate]:
            check_utils.check_is_2d_coordinate(coordinate, self.board_shape)

        if not self.is_occupied(old_coordinate):
            raise ValueError(
                f"expected old coordinate {old_coordinate} to be"
                f" occupied, got {self[old_coordinate]}"
            )

        self[old_coordinate].move(new_coordinate, self)
        if (
            isinstance(self[old_coordinate], Pawn)
            and new_coordinate[1] != old_coordinate[1]
            and not self.is_occupied(new_coordinate)
        ):
            self._board[old_coordinate[0]][new_coordinate[1]] = None

        self._board[new_coordinate[0]][new_coordinate[1]] = self[old_coordinate]
        self._board[old_coordinate[0]][old_coordinate[1]] = None

    def is_similar_to(self, other):
        check_utils.check_is_instance("Other_board", other, Board)
        if self.player_colors != other.player_colors:
            return False
        if self.board_shape != other.board_shape:
            return False
        return True
