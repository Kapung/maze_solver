import unittest
from main import Maze

class Tests(unittest.TestCase):
    
    def test_maze_create_cells(self):
        num_cols = 19
        num_rows = 26
        maze = Maze(10, 10, num_rows, num_cols, 30, 30)
        self.assertEqual(
            len(maze._cells),
            num_cols
        )
        self.assertEqual(
            len(maze._cells[0]),
            num_rows
        )


if __name__ == "__main__":
    unittest.main()
