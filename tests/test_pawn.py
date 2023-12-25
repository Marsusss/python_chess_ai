import copy
import unittest

from modules.board import Board
from modules.pawn import Pawn


class TestChessPiece(unittest.TestCase):
    def setUp(self):
        self.pawn = Pawn((0, 0), "black", 1, "down")
        self.board = Board(["black", "white"])
        self.pawn = self.board[1, 0]

    def test_init(self):
        self.assertEqual(self.pawn.position, (1, 0))
        self.assertEqual(self.pawn.piece_type, "pawn")
        self.assertEqual(self.pawn.color, "black")
        self.assertEqual(self.pawn.id, 8)
        self.assertEqual(self.pawn.state["just_double_moved"], False)
        self.assertEqual(self.pawn.forward_direction, (1, 0))

    def test_deepcopy(self):
        deepcopy_piece = copy.deepcopy(self.pawn)
        self.assertIsNot(deepcopy_piece, self.pawn)
        self.assertEqual(deepcopy_piece.dict, self.pawn.dict)

    def test_get_allowed_moves(self):
        # Testing get single and double move
        self.assertEqual(self.pawn.get_allowed_moves(self.board), [(2, 0), (3, 0)])

        # Test has_moved
        self.pawn["state"]["has_moved"] = True
        self.assertEqual(self.pawn.get_allowed_moves(self.board), [(2, 0)])

        # Test attacking and blocking
        self.pawn["state"]["has_moved"] = False
        self.board._board[2][0] = Pawn((2, 0), "white", 40, "up")
        self.board._board[2][1] = Pawn((2, 1), "white", 41, "up")
        self.assertEqual(self.pawn.get_allowed_moves(self.board), [(2, 1)])

        # Test en passant, just use print(self.board) to see what is happening.
        self.board._board[2][1] = None
        self.board._board[1][1] = Pawn((1, 1), "white", 41, "up")
        self.board._board[1][1]["state"]["just_double_moved"] = True
        self.assertEqual(self.pawn.get_allowed_moves(self.board), [(2, 1)])

    def test_move(self):
        self.pawn.move((2, 0), self.board)
        self.assertEqual(self.pawn.position, (2, 0))

        with self.assertRaises(ValueError):
            self.pawn.move((2, 1), self.board)


if __name__ == "__main__":
    unittest.main()
