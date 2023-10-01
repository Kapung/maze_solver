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
        self.assertEqual(
            maze._cells[0][0].has_top_wall,
            False
        )
        self.assertEqual(
            maze._cells[maze._num_cols - 1][maze._num_rows - 1].has_bottom_wall,
            False
        )
        for i in range(maze._num_cols):
            for j in range(maze._num_rows):
                self.assertEqual(
                    maze._cells[i][j].visited,
                    False
                )


if __name__ == "__main__":
    unittest.main()
