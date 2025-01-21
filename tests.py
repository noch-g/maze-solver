import unittest
from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1.cells),
            num_cols,
        )
        self.assertEqual(
            len(m1.cells[0]),
            num_rows,
        )

    def test_maze_break_entrance(self):
        num_cols = 4
        num_rows = 4
        m1 = Maze(0, 0, num_rows, num_cols, 5, 5)
        self.assertEqual(m1.cells[0][0].has_top_wall,False)
        self.assertEqual(m1.cells[0][0].has_left_wall, True)
        self.assertEqual(m1.cells[0][0].has_bottom_wall, True)
        self.assertEqual(m1.cells[0][0].has_right_wall, True)

        self.assertEqual(m1.cells[3][3].has_bottom_wall, False)
        self.assertEqual(m1.cells[3][3].has_left_wall, True)
        self.assertEqual(m1.cells[3][3].has_top_wall, True)
        self.assertEqual(m1.cells[3][3].has_right_wall, True)


if __name__ == "__main__":
    unittest.main()
