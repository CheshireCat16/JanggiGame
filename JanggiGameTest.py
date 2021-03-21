import unittest
from JanggiGame import JanggiGame, Chariot, General, Elephant, Soldier
from JanggiGame import Cannon, Guard, Horse


class JanggiGameTest(unittest.TestCase):
    """Janggi game tests"""

    def setUp(self) -> None:
        self.my_game = JanggiGame()

    def test_get_current_side(self):
        """Tests the get current side method and that sides change correctly"""
        self.assertEqual("blue", self.my_game.get_current_side().get_color())
        self.my_game.change_current_side()
        self.assertEqual("red", self.my_game.get_current_side().get_color())

    def test_get_game_state(self):
        """Tests that game state is properly reported"""
        self.assertEqual("UNFINISHED", self.my_game.get_game_state())

    def test_is_in_check(self):
        """Tests whether the game properly detects check"""
        pass

    def test_make_move(self):
        """
        Tests whether moves are properly completed, whether check is detected,
        whether check-mate is detected, whether game status is properly updated,
        and whether turn is properly changed.
        """
        # Try passing a turn
        self.my_game.make_move("a1", "a1")
        self.assertEqual("red", self.my_game.get_current_side().get_color())

        # Currently Red's move, try to move a Blue piece
        move_result = self.my_game.make_move("h4", "h5")
        self.assertFalse(move_result)

        # Try to move from a space with no piece
        move_result = self.my_game.make_move("d4", "h5")
        self.assertFalse(move_result)

        # Move a red soldier up one row
        self.my_game.make_move("a4", "a5")
        self.assertIsInstance(self.my_game._board.get_board_layout()[4][0],
                              Soldier)

        # Move a blue soldier up one row
        self.my_game.make_move("a7", "a6")
        self.assertIsInstance(self.my_game._board.get_board_layout()[5][0],
                              Soldier)

        # Move a red soldier up one row and take the blue piece
        self.my_game.make_move("a5", "a6")
        self.assertIsInstance(self.my_game._board.get_board_layout()[5][0],
                              Soldier)
        self.assertEqual(self.my_game._board.get_board_layout()[5][0].get_color(), "red")
        self.assertEqual(self.my_game._blue_side.get_pieces(False)[0].get_location(), (None, None))
        self.assertIsInstance(self.my_game._blue_side.get_pieces(False)[0], Soldier)

        # Try to move a soldier two spaces
        move_complete = self.my_game.make_move("c7", "e7")
        self.assertEqual(move_complete, False)

        # Move a blue solider one space to left
        move_complete = self.my_game.make_move("c7", "d7")
        self.assertEqual(move_complete, True)
        self.assertEqual(self.my_game._board.get_board_layout()[6][3].get_color(), "blue")
        self.assertIsInstance(self.my_game._board.get_board_layout()[6][3], Soldier)

        # Pass reds turn
        self.my_game.make_move("a1", "a1")

        # Try to move blue solider into space of other blue soldier
        move_complete = self.my_game.make_move("d7", "e7")
        self.assertEqual(move_complete, False)
        self.assertEqual(self.my_game._board.get_board_layout()[6][3].get_color(), "blue")
        self.assertIsInstance(self.my_game._board.get_board_layout()[6][3], Soldier)

        # Make sure the soldier can't move backward
        move_complete = self.my_game.make_move("d7", "d8")
        self.assertEqual(move_complete, False)
        self.assertEqual(self.my_game._board.get_board_layout()[6][3].get_color(), "blue")
        self.assertIsInstance(self.my_game._board.get_board_layout()[6][3], Soldier)

        # Move blue soldier up into palace
        self.my_game.make_move("d7", "d6")
        self.my_game.make_move("a1", "a1")
        self.my_game.make_move("d6", "d5")
        self.my_game.make_move("a1", "a1")
        self.my_game.make_move("d5", "d4")
        self.my_game.make_move("a1", "a1")
        self.my_game.make_move("d4", "d3")

        # Try an invalid move with the general
        move_complete = self.my_game.make_move("e2", "f1")
        self.assertEqual(move_complete, False)
        self.assertEqual(self.my_game._board.get_board_layout()[1][4].get_color(), "red")
        self.assertIsInstance(self.my_game._board.get_board_layout()[1][4], General)

        # Try an invalid move with the general
        move_complete = self.my_game.make_move("e2", "d1")
        self.assertEqual(move_complete, False)
        self.assertEqual(self.my_game._board.get_board_layout()[1][4].get_color(), "red")
        self.assertIsInstance(self.my_game._board.get_board_layout()[1][4], General)

        # Try an valid move with the general
        move_complete = self.my_game.make_move("e2", "f2")
        self.assertEqual(move_complete, True)
        self.assertEqual(self.my_game._board.get_board_layout()[1][5].get_color(), "red")
        self.assertIsInstance(self.my_game._board.get_board_layout()[1][5], General)

        # Check if the soldier can move forward left
        move_complete = self.my_game.make_move("d3", "c2")
        self.assertEqual(move_complete, False)
        self.assertEqual(self.my_game._board.get_board_layout()[2][3].get_color(), "blue")
        self.assertIsInstance(self.my_game._board.get_board_layout()[2][3], Soldier)

        # Check if the soldier can move forward right
        move_complete = self.my_game.make_move("d3", "e2")
        self.assertEqual(move_complete, True)
        self.assertEqual(self.my_game._board.get_board_layout()[1][4].get_color(), "blue")
        self.assertIsInstance(self.my_game._board.get_board_layout()[1][4], Soldier)

        # Check if the soldier can move forward right again
        self.my_game.make_move("f2", "f3")
        move_complete = self.my_game.make_move("e2", "f1")
        self.assertEqual(move_complete, True)
        self.assertEqual(self.my_game._board.get_board_layout()[0][5].get_color(), "blue")
        self.assertIsInstance(self.my_game._board.get_board_layout()[0][5], Soldier)

        # Check if the soldier can move forward
        self.my_game.make_move("a1", "a1")
        move_complete = self.my_game.make_move("f1", "f0")
        self.assertEqual(move_complete, False)
        self.assertEqual(self.my_game._board.get_board_layout()[0][5].get_color(), "blue")
        self.assertIsInstance(self.my_game._board.get_board_layout()[0][5], Soldier)
        self.my_game.make_move("a1", "a1")

        # Try an invalid move with the general
        move_complete = self.my_game.make_move("f3", "g3")
        self.assertEqual(move_complete, False)
        self.assertEqual(self.my_game._board.get_board_layout()[2][5].get_color(), "red")
        self.assertIsInstance(self.my_game._board.get_board_layout()[2][5], General)

        # Take the soldier on f1
        move_complete = self.my_game.make_move("f3", "f2")
        self.assertEqual(move_complete, True)
        move_complete = self.my_game.make_move("a1", "a1")
        self.assertEqual(move_complete, True)
        move_complete = self.my_game.make_move("f2", "f1")
        self.assertEqual(move_complete, True)
        self.assertEqual(self.my_game._board.get_board_layout()[0][5].get_color(), "red")
        self.assertIsInstance(self.my_game._board.get_board_layout()[0][5], General)
        self.my_game.make_move("a1", "a1")

        # Try to move out of the palace down
        move_complete = self.my_game.make_move("f1", "f2")
        self.assertEqual(move_complete, True)
        self.assertEqual(self.my_game._board.get_board_layout()[1][5].get_color(), "red")
        self.assertIsInstance(self.my_game._board.get_board_layout()[1][5], General)
        self.my_game.make_move("a1", "a1")
        move_complete = self.my_game.make_move("f2", "f3")
        self.assertEqual(move_complete, True)
        self.assertEqual(self.my_game._board.get_board_layout()[2][5].get_color(), "red")
        self.assertIsInstance(self.my_game._board.get_board_layout()[2][5], General)
        self.my_game.make_move("a1", "a1")
        move_complete = self.my_game.make_move("f3", "f4")
        self.assertEqual(move_complete, False)
        self.assertEqual(self.my_game._board.get_board_layout()[2][5].get_color(), "red")
        self.assertIsInstance(self.my_game._board.get_board_layout()[2][5], General)

        # Try to move out of the palace left
        move_complete = self.my_game.make_move("f3", "e3")
        self.assertEqual(move_complete, True)
        self.assertEqual(self.my_game._board.get_board_layout()[2][4].get_color(), "red")
        self.assertIsInstance(self.my_game._board.get_board_layout()[2][4], General)
        self.my_game.make_move("a1", "a1")
        move_complete = self.my_game.make_move("e3", "d3")
        self.assertEqual(move_complete, True)
        self.assertEqual(self.my_game._board.get_board_layout()[2][3].get_color(), "red")
        self.assertIsInstance(self.my_game._board.get_board_layout()[2][3], General)
        self.my_game.make_move("a1", "a1")
        move_complete = self.my_game.make_move("d3", "c4")
        self.assertEqual(move_complete, False)
        self.assertEqual(self.my_game._board.get_board_layout()[2][3].get_color(), "red")
        self.assertIsInstance(self.my_game._board.get_board_layout()[2][3], General)
        self.my_game.make_move("a1", "a1")

        # Try to move out of the palace upper left (blue)
        move_complete = self.my_game.make_move("e9", "f8")
        self.assertEqual(move_complete, True)
        self.assertEqual(self.my_game._board.get_board_layout()[7][5].get_color(), "blue")
        self.assertIsInstance(self.my_game._board.get_board_layout()[7][5], General)
        self.my_game.make_move("a1", "a1")
        move_complete = self.my_game.make_move("e9", "f7")
        self.assertEqual(move_complete, False)
        self.assertEqual(self.my_game._board.get_board_layout()[7][5].get_color(), "blue")
        self.assertIsInstance(self.my_game._board.get_board_layout()[7][5], General)

        # Move a guard
        move_complete = self.my_game.make_move("d10", "d9")
        self.assertEqual(move_complete, True)
        self.assertEqual(self.my_game._board.get_board_layout()[8][3].get_color(), "blue")
        self.assertIsInstance(self.my_game._board.get_board_layout()[8][3], Guard)

    def test_horse(self):
        # Move blue horse
        move_complete = self.my_game.make_move("h10", "f9")
        self.assertEqual(move_complete, False)
        move_complete = self.my_game.make_move("h10", "i8")
        self.assertEqual(move_complete, True)

        # Move horse
        move_complete = self.my_game.make_move("c1", "d3")
        self.assertEqual(move_complete, True)

    def test_cannon(self):
        # Move blue cannon
        move_complete = self.my_game.make_move("b8", "b7")
        self.assertEqual(move_complete, False)
        # Move blue general
        move_complete = self.my_game.make_move("e9", "e8")
        self.assertEqual(move_complete, True)

        # Move red cannon
        move_complete = self.my_game.make_move("b3", "d3")
        self.assertEqual(move_complete, False)
        # Move red Horse
        move_complete = self.my_game.make_move("c1", "d3")
        self.assertEqual(move_complete, True)

        # Move blue cannon
        move_complete = self.my_game.make_move("b8", "g8")
        self.assertEqual(move_complete, True)

        # Move red cannon
        move_complete = self.my_game.make_move("b3", "g3")
        self.assertEqual(move_complete, True)

        # Move blue cannon
        move_complete = self.my_game.make_move("g8", "g4")
        self.assertEqual(move_complete, True)
        self.assertEqual(self.my_game._board.get_board_layout()[3][6].get_color(), "blue")
        self.assertIsInstance(self.my_game._board.get_board_layout()[3][6], Cannon)

        # Test cannon in Palace
        # Move red cannon
        move_complete = self.my_game.make_move("g3", "g7")
        self.assertEqual(move_complete, False)
        # Move red guard
        move_complete = self.my_game.make_move("f1", "f2")
        self.assertEqual(move_complete, True)
        self.my_game.make_move("a1", "a1")
        move_complete = self.my_game.make_move("f2", "f3")
        self.assertEqual(move_complete, True)
        self.my_game.make_move("a1", "a1")
        move_complete = self.my_game.make_move("d3", "c5")
        self.assertEqual(move_complete, True)
        self.my_game.make_move("a1", "a1")
        move_complete = self.my_game.make_move("g3", "d3")
        self.assertEqual(move_complete, True)
        self.my_game.make_move("a1", "a1")
        move_complete = self.my_game.make_move("d3", "f1")
        self.assertEqual(move_complete, True)
        self.assertEqual(self.my_game._board.get_board_layout()[0][5].get_color(), "red")
        self.assertIsInstance(self.my_game._board.get_board_layout()[0][5], Cannon)
        self.my_game.make_move("a1", "a1")

    def test_cannon_palace_alternate(self):
        # Move blue cannon
        move_complete = self.my_game.make_move("b8", "b7")
        self.assertEqual(move_complete, False)
        # Move blue general
        move_complete = self.my_game.make_move("e9", "e8")
        self.assertEqual(move_complete, True)

        # Move red cannon
        move_complete = self.my_game.make_move("b3", "d3")
        self.assertEqual(move_complete, False)
        # Move red Horse
        move_complete = self.my_game.make_move("c1", "d3")
        self.assertEqual(move_complete, True)

        # Move blue cannon
        move_complete = self.my_game.make_move("b8", "g8")
        self.assertEqual(move_complete, True)

        # Move red cannon
        move_complete = self.my_game.make_move("b3", "g3")
        self.assertEqual(move_complete, True)

        # Move blue cannon
        move_complete = self.my_game.make_move("g8", "g4")
        self.assertEqual(move_complete, True)
        self.assertEqual(self.my_game._board.get_board_layout()[3][6].get_color(), "blue")
        self.assertIsInstance(self.my_game._board.get_board_layout()[3][6], Cannon)

        # Test cannon in Palace
        # Move red cannon
        move_complete = self.my_game.make_move("g3", "g7")
        self.assertEqual(move_complete, False)
        # Move red guard
        move_complete = self.my_game.make_move("f1", "f2")
        self.assertEqual(move_complete, True)
        self.my_game.make_move("a1", "a1")
        move_complete = self.my_game.make_move("f2", "f3")
        self.assertEqual(move_complete, True)
        self.my_game.make_move("a1", "a1")
        move_complete = self.my_game.make_move("d3", "c5")
        self.assertEqual(move_complete, True)
        self.my_game.make_move("a1", "a1")
        move_complete = self.my_game.make_move("g3", "e3")
        self.assertEqual(move_complete, True)
        self.my_game.make_move("a1", "a1")
        move_complete = self.my_game.make_move("e3", "f2")
        self.assertEqual(move_complete, False)
        self.assertEqual(self.my_game._board.get_board_layout()[2][4].get_color(), "red")
        self.assertIsInstance(self.my_game._board.get_board_layout()[2][4], Cannon)
        self.my_game.make_move("a1", "a1")

    def test_is_in_check(self):
        result = self.my_game.is_in_check("blue")
        self.assertEqual(result, False)

        # Move put blue general into check and confirm
        move_complete = self.my_game.make_move("e9", "f8")
        self.assertEqual(move_complete, True)
        move_complete = self.my_game.make_move("i1", "i2")
        self.assertEqual(move_complete, True)
        self.my_game.make_move("a1", "a1")
        move_complete = self.my_game.make_move("i2", "f2")
        self.assertEqual(move_complete, True)

        result = self.my_game.is_in_check("blue")
        self.assertEqual(result, True)

        # Try move when general is in check
        move_complete = self.my_game.make_move("i7", "i6")
        self.assertEqual(move_complete, False)

    def test_elephant(self):
        # Move blue elephant
        move_complete = self.my_game.make_move("b10", "d9")
        self.assertEqual(move_complete, False)
        move_complete = self.my_game.make_move("b10", "d7")
        self.assertEqual(move_complete, True)
        self.assertEqual(self.my_game._board.get_board_layout()[6][3].get_color(), "blue")
        self.assertIsInstance(self.my_game._board.get_board_layout()[6][3], Elephant)

        # Move red elephant
        move_complete = self.my_game.make_move("b1", "d4")
        self.assertEqual(move_complete, True)

    def test_chariot(self):
        # Move blue chariot
        move_complete = self.my_game.make_move("a10", "b10")
        self.assertEqual(move_complete, False)
        move_complete = self.my_game.make_move("a10", "a8")
        self.assertEqual(move_complete, True)
        self.assertEqual(self.my_game._board.get_board_layout()[7][0].get_color(), "blue")
        self.assertIsInstance(self.my_game._board.get_board_layout()[7][0], Chariot)

        # Move red chariot
        move_complete = self.my_game.make_move("i1", "i2")
        self.assertEqual(move_complete, True)

        # Move blue chariot
        move_complete = self.my_game.make_move("a8", "a6")
        self.assertEqual(move_complete, False)
        move_complete = self.my_game.make_move("a8", "a9")
        self.assertEqual(move_complete, True)

        # Move red chariot
        move_complete = self.my_game.make_move("i2", "f2")
        self.assertEqual(move_complete, True)

        # Move blue chariot
        move_complete = self.my_game.make_move("a9", "d9")
        self.assertEqual(move_complete, True)

        # Move red chariot
        move_complete = self.my_game.make_move("f2", "e1")
        self.assertEqual(move_complete, True)

        # Move blue chariot
        move_complete = self.my_game.make_move("d9", "f7")
        self.assertEqual(move_complete, False)

    def test_grade_scope_test(self):
        move_complete = self.my_game.make_move("a7", "a6")
        self.assertEqual(move_complete, True)
        move_complete = self.my_game.make_move("i4", "i5")
        self.assertEqual(move_complete, True)
        move_complete = self.my_game.make_move("i7", "i6")
        self.assertEqual(move_complete, True)

    def test_position_conv(self):
        """Tests the converter from string to index for locations"""
        i_j_location = self.my_game.translate_space("a1")
        self.assertEqual((0, 0), i_j_location)
        i_j_location = self.my_game.translate_space("b1")
        self.assertEqual((0, 1), i_j_location)
        i_j_location = self.my_game.translate_space("b6")
        self.assertEqual((5, 1), i_j_location)
        # Test for an invalid input
        i_j_location = self.my_game.translate_space("m11")
        self.assertEqual((-1, -1), i_j_location)

    def test_check_scenario_1(self):
        """Tests that check and check mate are properly captured"""
        # Move blue soldier
        move_complete = self.my_game.make_move("e7", "e6")
        self.assertEqual(move_complete, True)
        move_complete = self.my_game.make_move("a9", "a9")
        move_complete = self.my_game.make_move("e6", "e5")
        self.assertEqual(move_complete, True)
        move_complete = self.my_game.make_move("a9", "a9")
        move_complete = self.my_game.make_move("e5", "e4")
        self.assertEqual(move_complete, True)
        move_complete = self.my_game.make_move("a9", "a9")
        move_complete = self.my_game.make_move("e4", "e3")
        self.assertEqual(move_complete, True)
        # Red general in check now - confirm can only make move out of check
        move_complete = self.my_game.make_move("i4", "i5")
        self.assertEqual(move_complete, False)
        move_complete = self.my_game.make_move("f1", "f2")
        self.assertEqual(move_complete, False)
        move_complete = self.my_game.make_move("f1", "e2")
        self.assertEqual(move_complete, False)

        # Move General back
        move_complete = self.my_game.make_move("e2", "e1")
        self.assertEqual(move_complete, True)

        # Move soldier up again
        move_complete = self.my_game.make_move("e3", "e2")
        self.assertEqual(move_complete, True)

        # Capture soldier with guard
        move_complete = self.my_game.make_move("f1", "e2")
        self.assertEqual(move_complete, True)
        move_complete = self.my_game.make_move("a9", "a9")
        move_complete = self.my_game.make_move("e2", "f3")
        self.assertEqual(move_complete, True)

    def test_check_scenario_2(self):
        """Tests that check can be blocked"""
        # Move blue chariot
        move_complete = self.my_game.make_move("i10", "i9")
        self.assertEqual(move_complete, True)
        self.my_game.make_move("a9", "a9")
        move_complete = self.my_game.make_move("i9", "f9")
        self.assertEqual(move_complete, True)
        self.my_game.make_move("a9", "a9")
        move_complete = self.my_game.make_move("f9", "f4")
        self.assertEqual(move_complete, True)
        self.my_game.make_move("a9", "a9")
        move_complete = self.my_game.make_move("f4", "g4")
        self.assertEqual(move_complete, True)
        self.my_game.make_move("a9", "a9")
        move_complete = self.my_game.make_move("g4", "g2")
        self.assertEqual(move_complete, True)

        # It should not be able to pass a turn while in check
        move_complete = self.my_game.make_move("a9", "a9")
        self.assertEqual(move_complete, False)
        in_check = self.my_game.is_in_check("red")
        self.assertEqual(in_check, True)
        # Move Guard up to block Chariot
        move_complete = self.my_game.make_move("f1", "f2")
        self.assertEqual(move_complete, True)
        in_check = self.my_game.is_in_check("red")
        self.assertEqual(in_check, False)

        # Make sure cannot move into check
        move_complete = self.my_game.make_move("a9", "a9")
        self.assertEqual(move_complete, True)
        move_complete = self.my_game.make_move("f2", "f1")
        self.assertEqual(move_complete, False)

    def test_check_mate(self):
        """Tests that check can be blocked"""
        # Move blue chariot
        move_complete = self.my_game.make_move("i10", "i9")
        self.assertEqual(move_complete, True)
        self.my_game.make_move("a9", "a9")
        move_complete = self.my_game.make_move("i9", "f9")
        self.assertEqual(move_complete, True)
        self.my_game.make_move("a9", "a9")
        move_complete = self.my_game.make_move("f9", "f4")
        self.assertEqual(move_complete, True)
        self.my_game.make_move("a9", "a9")
        move_complete = self.my_game.make_move("f4", "g4")
        self.assertEqual(move_complete, True)
        self.my_game.make_move("a9", "a9")
        move_complete = self.my_game.make_move("g4", "g2")
        self.assertEqual(move_complete, True)

        # It should not be able to pass a turn while in check
        move_complete = self.my_game.make_move("a9", "a9")
        self.assertEqual(move_complete, False)
        in_check = self.my_game.is_in_check("red")
        self.assertEqual(in_check, True)
        # Move Guard up to block Chariot
        move_complete = self.my_game.make_move("f1", "f2")
        self.assertEqual(move_complete, True)
        in_check = self.my_game.is_in_check("red")
        self.assertEqual(in_check, False)

        # Make sure cannot move into check
        move_complete = self.my_game.make_move("a9", "a9")
        self.assertEqual(move_complete, True)
        move_complete = self.my_game.make_move("f2", "f1")
        self.assertEqual(move_complete, False)
        move_complete = self.my_game.make_move("e2", "e1")
        self.assertEqual(move_complete, True)
        move_complete = self.my_game.make_move("e7", "e6")
        self.assertEqual(move_complete, True)
        move_complete = self.my_game.make_move("a1", "a1")
        self.assertEqual(move_complete, True)
        move_complete = self.my_game.make_move("e6", "e5")
        self.assertEqual(move_complete, True)
        move_complete = self.my_game.make_move("a1", "a1")
        self.assertEqual(move_complete, True)
        move_complete = self.my_game.make_move("e5", "e4")
        self.assertEqual(move_complete, True)
        move_complete = self.my_game.make_move("a1", "a1")
        self.assertEqual(move_complete, True)
        move_complete = self.my_game.make_move("e4", "e3")
        self.assertEqual(move_complete, True)
        move_complete = self.my_game.make_move("a1", "a1")
        self.assertEqual(move_complete, True)
        move_complete = self.my_game.make_move("h10", "g8")
        self.assertEqual(move_complete, True)
        move_complete = self.my_game.make_move("a1", "a1")
        self.assertEqual(move_complete, True)
        move_complete = self.my_game.make_move("h8", "e8")
        self.assertEqual(move_complete, True)
        move_complete = self.my_game.make_move("e1", "f1")
        self.assertEqual(move_complete, True)
        move_complete = self.my_game.make_move("e3", "f2")
        self.assertEqual(move_complete, True)
        in_check = self.my_game.is_in_check("red")
        self.assertEqual(in_check, True)
        game_status = self.my_game.get_game_state()
        self.assertEqual(game_status, "BLUE_WON")

    def test_board_setup(self):
        """Tests that board initialization is correct"""
        # Initial board layout, note Elephant and Horse have fixed positions
        # unlike in the actual game where they can be moved
        initial_board = [[Chariot, Elephant, Horse, Guard, None, Guard, Elephant,
                          Horse, Chariot],
                         [None, None, None, None, General, None, None, None, None],
                         [None, Cannon, None, None, None, None, None, Cannon, None],
                         [Soldier, None, Soldier, None, Soldier, None, Soldier,
                          None, Soldier],
                         [None, None, None, None, None, None, None, None, None],
                         [None, None, None, None, None, None, None, None, None],
                         [Soldier, None, Soldier, None, Soldier, None, Soldier,
                          None, Soldier],
                         [None, Cannon, None, None, None, None, None, Cannon, None],
                         [None, None, None, None, General, None, None, None, None],
                         [Chariot, Elephant, Horse, Guard, None, Guard, Elephant,
                          Horse, Chariot]]

        for row in range(0, 9):
            for column in range(0, 8):
                if initial_board[row][column] is None:
                    self.assertIsNone(
                        self.my_game._board.get_board_layout()[row][column])
                else:
                    self.assertIsInstance(
                        self.my_game._board.get_board_layout()[row][column],
                        initial_board[row][column])

    def test_get_space_info(self):
        """Tests the Board class get_space_info method"""
        my_piece = self.my_game._board.get_space_info(0, 0)
        self.assertIsInstance(my_piece, Chariot)
        my_piece = self.my_game._board.get_space_info(8, 4)
        self.assertIsInstance(my_piece, General)

    def test_check_space_in_palace(self):
        """Confirm that the location within the palace is properly captured"""
        in_palace = self.my_game._board.check_space_in_palace(0, 0)
        self.assertEqual(in_palace, False)
        in_palace = self.my_game._board.check_space_in_palace(0, 2)
        self.assertEqual(in_palace, False)
        in_palace = self.my_game._board.check_space_in_palace(0, 3)
        self.assertEqual(in_palace, True)
        in_palace = self.my_game._board.check_space_in_palace(7, 3)
        self.assertEqual(in_palace, True)
        in_palace = self.my_game._board.check_space_in_palace(9, 3)
        self.assertEqual(in_palace, True)
        in_palace = self.my_game._board.check_space_in_palace(9, 5)
        self.assertEqual(in_palace, True)
        in_palace = self.my_game._board.check_space_in_palace(9, 6)
        self.assertEqual(in_palace, False)
        in_palace = self.my_game._board.check_space_in_palace(6, 4)
        self.assertEqual(in_palace, False)
        in_palace = self.my_game._board.check_space_in_palace(4, 4)
        self.assertEqual(in_palace, False)
        in_palace = self.my_game._board.check_space_in_palace(2, 6)
        self.assertEqual(in_palace, False)
        in_palace = self.my_game._board.check_space_in_palace(2, 5)
        self.assertEqual(in_palace, True)

    def test_check_2(self):
        """Test another game"""
        # Blue
        move_complete = self.my_game.make_move("g7", "g6")
        self.assertEqual(move_complete, True)
        # Red
        move_complete = self.my_game.make_move("h1", "i3")
        self.assertEqual(move_complete, True)
        # Blue
        move_complete = self.my_game.make_move("h8", "h2")
        self.assertEqual(move_complete, False)
        # Blue
        move_complete = self.my_game.make_move("g6", "h6")
        self.assertEqual(move_complete, True)
        # Red
        move_complete = self.my_game.make_move("f1", "f2")
        self.assertEqual(move_complete, True)
        # Blue
        move_complete = self.my_game.make_move("h8", "h4")
        self.assertEqual(move_complete, True)
        # Red
        move_complete = self.my_game.make_move("i3", "h5")
        self.assertEqual(move_complete, False)
        # Red
        move_complete = self.my_game.make_move("i3", "g3")
        self.assertEqual(move_complete, False)
        # Red
        move_complete = self.my_game.make_move("f2", "f3")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        # Blue
        move_complete = self.my_game.make_move("c10", "d8")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        # Red
        move_complete = self.my_game.make_move("e2", "e1")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        # Blue
        move_complete = self.my_game.make_move("h4", "c4")
        self.assertEqual(move_complete, False)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        # Blue
        move_complete = self.my_game.make_move("h4", "e4")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        # Red
        move_complete = self.my_game.make_move("f3", "e4")
        self.assertEqual(move_complete, False)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        # Red
        move_complete = self.my_game.make_move("f3", "e3")
        self.assertEqual(move_complete, False)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        # Red
        move_complete = self.my_game.make_move("f3", "f2")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        # Blue
        move_complete = self.my_game.make_move("i10", "i8")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        # Red
        move_complete = self.my_game.make_move("g1", "e4")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        # Blue
        move_complete = self.my_game.make_move("c7", "c6")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        # Red
        move_complete = self.my_game.make_move("b1", "d4")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        # Blue
        move_complete = self.my_game.make_move("a7", "b7")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        # Red
        move_complete = self.my_game.make_move("i1", "f1")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        # Blue
        move_complete = self.my_game.make_move("d10", "d9")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        # Red
        move_complete = self.my_game.make_move("f2", "e3")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        # Blue
        move_complete = self.my_game.make_move("c6", "c5")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        # Red
        move_complete = self.my_game.make_move("f1", "f10")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(True, blue_check)
        # Blue
        move_complete = self.my_game.make_move("e9", "f8")
        self.assertEqual(move_complete, False)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(True, blue_check)
        # Blue
        move_complete = self.my_game.make_move("a9", "a9")
        self.assertEqual(move_complete, False)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(True, blue_check)
        # Blue
        move_complete = self.my_game.make_move("e9", "e8")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(False, blue_check)
        # Red
        move_complete = self.my_game.make_move("h3", "h10")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(False, blue_check)
        # Blue
        move_complete = self.my_game.make_move("i8", "f8")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(False, blue_check)
        self.assertEqual(False, blue_check)
        # Red
        move_complete = self.my_game.make_move("e4", "h6")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(True, blue_check)
        # Blue
        move_complete = self.my_game.make_move("e7", "f7")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(False, blue_check)
        # Red
        move_complete = self.my_game.make_move("d4", "b7")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(False, blue_check)
        # Blue
        move_complete = self.my_game.make_move("d8", "b7")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(False, blue_check)
        # Red
        move_complete = self.my_game.make_move("b3", "f3")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(False, blue_check)
        # Blue
        move_complete = self.my_game.make_move("b8", "b1")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(False, blue_check)
        # Red
        move_complete = self.my_game.make_move("f3", "f8")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(False, blue_check)
        # Blue
        move_complete = self.my_game.make_move("e8", "f8")
        self.assertEqual(move_complete, False)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(False, blue_check)
        # Blue
        move_complete = self.my_game.make_move("b7", "a5")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(False, blue_check)
        # Red
        move_complete = self.my_game.make_move("f10", "f9")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(True, blue_check)
        # Blue
        move_complete = self.my_game.make_move("e8", "f9")
        self.assertEqual(move_complete, False)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(True, blue_check)
        # Blue
        move_complete = self.my_game.make_move("e8", "d8")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(False, blue_check)
        # Red
        move_complete = self.my_game.make_move("f8", "f7")
        self.assertEqual(move_complete, False)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(False, blue_check)
        # Red
        move_complete = self.my_game.make_move("f8", "f3")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(False, blue_check)
        # Blue
        move_complete = self.my_game.make_move("f7", "f6")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(False, blue_check)
        # Red
        move_complete = self.my_game.make_move("f3", "d3")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(False, blue_check)
        # Blue
        move_complete = self.my_game.make_move("i7", "i6")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(False, blue_check)
        # Red
        move_complete = self.my_game.make_move("c4", "d4")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(True, blue_check)
        # Blue
        move_complete = self.my_game.make_move("c5", "d5")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(False, blue_check)
        # Red
        move_complete = self.my_game.make_move("d4", "d5")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(True, blue_check)
        # Blue
        move_complete = self.my_game.make_move("b10", "d7")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(False, blue_check)
        # Red
        move_complete = self.my_game.make_move("d5", "d6")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(False, blue_check)
        # Blue
        move_complete = self.my_game.make_move("b1", "d1")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("UNFINISHED", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(False, blue_check)
        # Red
        move_complete = self.my_game.make_move("d6", "d7")
        self.assertEqual(move_complete, True)
        result = self.my_game.get_game_state()
        self.assertEqual("RED_WON", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(True, blue_check)
        # Blue
        move_complete = self.my_game.make_move("b1", "b1")
        self.assertEqual(move_complete, False)
        result = self.my_game.get_game_state()
        self.assertEqual("RED_WON", result)
        red_check = self.my_game.is_in_check("red")
        blue_check = self.my_game.is_in_check("blue")
        self.assertEqual(False, red_check)
        self.assertEqual(True, blue_check)

if __name__ == "__main__":
    """Runs the unit test"""
    unittest.main()
