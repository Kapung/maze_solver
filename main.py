from tkinter import Tk, BOTH, Canvas
from time import sleep
import random

COLOR = "black"
BGCOLOR = "white"

class Window():

    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        self.__canvas = Canvas(self.__root, {"width": width, "height": height, "bg": BGCOLOR})
        self.__canvas.pack()

        self.__is_running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__is_running = True
        while self.__is_running:
            self.redraw()
        
    def close(self):
        self.__is_running = False
    
    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)


class Point():

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line():

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def draw(self, canvas, fill_color):
        canvas.create_line(self.__x.x, self.__x.y, self.__y.x, self.__y.y, fill=fill_color, width=2)
        canvas.pack()

class Cell():

    def __init__(self, x, y, win, has_left_wall=True, has_right_wall=True, has_top_wall=True, has_bottom_wall=True):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self._x1 = x.x
        self._x2 = y.x
        self._y1 = x.y
        self._y2 = y.y
        self._win = win
        self.c_left = COLOR
        self.c_right = COLOR
        self.c_top = COLOR
        self.c_bot = COLOR
        self.visited = False

    def __str__(self):
        return f"Left: {self.has_left_wall}\nRight: {self.has_right_wall}\nTop: {self.has_top_wall}\nBot: {self.has_bottom_wall}\nX: {self._x1}|{self._y1}\nY: {self._x2}|{self._y2}\nVisited: {self.visited}"

    def draw(self):

        if not self.has_left_wall:
            self.c_left = BGCOLOR
        if not self.has_right_wall:
            self.c_right = BGCOLOR
        if not self.has_top_wall:
            self.c_top = BGCOLOR
        if not self.has_bottom_wall:
            self.c_bot = BGCOLOR

        self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)), self.c_left)
        self._win.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)), self.c_right)
        self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)), self.c_top)
        self._win.draw_line(Line(Point(self._x1, self._y2), Point(self._x2, self._y2)), self.c_bot)

    def draw_move(self, to_cell, undo=False):
        color = "red"
        if undo:
            color = "gray"

        left_cell = Point(self._x1 + abs(self._x1 - self._x2) // 2, self._y1 + abs(self._y1 - self._y2) // 2)
        right_cell = Point(to_cell._x1 + abs(to_cell._x1 - to_cell._x2) // 2, to_cell._y1 + abs(to_cell._y1 - to_cell._y2) // 2)

        self._win.draw_line(Line(left_cell, right_cell), color)

class Maze():
    
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        if seed:
            random.seed(seed)
        else:
            random.seed(0)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells = []
        for i in range(self._x1, self._y1 + self._cell_size_x * self._num_cols, self._cell_size_x):
            cells = []
            for j in range(self._y1, self._y1 + self._cell_size_y * self._num_rows, self._cell_size_y):
                cl = Cell (Point(i, j), Point(i + self._cell_size_x, j + self._cell_size_y), self._win)
                cells.append(cl)
            self._cells.append(cells)
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):

        cell = self._cells[i][j]
        cell.draw()
        self._animate()

    def _animate(self):
        self._win.redraw()
        sleep(0.005)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(-1, -1)

    def _break_walls_r(self, i, j):

        if not 0 <= i < self._num_cols or not 0 <= j < self._num_rows:
            return

        self._cells[i][j].visited = True
        while True:
            visit = []
            #Up
            if i - 1 >= 0 and not self._cells[i - 1][j].visited:
                visit.append((i - 1, j))
            #Down
            if i + 1 < self._num_cols and not self._cells[i + 1][j].visited:
                visit.append((i + 1, j))
            #Left
            if j - 1 >= 0 and not self._cells[i][j - 1].visited:
                visit.append((i, j - 1))
            #Right
            if j + 1 < self._num_rows and not self._cells[i][j + 1].visited:
                visit.append((i, j + 1))

            if not visit:
                self._cells[i][j].draw()
                return

            #Picks random direction to go
            random_height, random_width = visit.pop(random.randrange(len(visit)))

            if random_height == i and random_width < j:
                self._cells[i][j].has_top_wall = False
                self._cells[i][random_width].has_bottom_wall = False

            elif random_height == i and random_width > j:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][random_width].has_top_wall = False

            elif random_height < i and random_width == j:
                self._cells[i][j].has_left_wall = False
                self._cells[random_height][j].has_right_wall = False

            elif random_height > i and random_width == j:
                self._cells[i][j].has_right_wall = False
                self._cells[random_height][j].has_left_wall = False

            self._break_walls_r(random_height, random_width)

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True

        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        for next_direction_y, next_direction_x, direction in [(i - 1, j, "Left"), (i + 1, j, "Right"), (i, j - 1, "Up"), (i, j + 1, "Down")]:
            
            if not (0 <= next_direction_y < self._num_cols and 0 <= next_direction_x < self._num_rows):
                continue
            if self._cells[next_direction_y][next_direction_x].visited:
                continue
            if direction == "Left" and self._cells[next_direction_y][next_direction_x].has_right_wall:
                continue
            if direction == "Right" and self._cells[next_direction_y][next_direction_x].has_left_wall:
                continue
            if direction == "Up" and self._cells[next_direction_y][next_direction_x].has_bottom_wall:
                continue
            if direction == "Down" and self._cells[next_direction_y][next_direction_x].has_top_wall:
                continue

            self._cells[i][j].draw_move(self._cells[next_direction_y][next_direction_x])

            if self._solve_r(next_direction_y, next_direction_x):
                return True
            
            self._cells[i][j].draw_move(self._cells[next_direction_y][next_direction_x], undo=True)

        return False
    
def main():
    win = Window(800, 800)
    maze = Maze(10, 10, 19, 26, 30, 30, win, True)
    maze.solve()
    win.wait_for_close()

main()