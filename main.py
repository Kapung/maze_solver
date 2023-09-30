from tkinter import Tk, BOTH, Canvas
from time import sleep

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

    def __str__(self):
        return f"Left: {self.has_left_wall}\nRight: {self.has_right_wall}\nTop: {self.has_top_wall}\nBot: {self.has_bottom_wall}\nX: {self._x1}|{self._y1}\nY: {self._x2}|{self._y2}"

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
    
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self.up_trigger = True
        self.down_trigger = True

        self._create_cells()
        self._break_entrance_and_exit()

    def _create_cells(self):
        self._cells = [[self._draw_cell(c, r) for r in range(self._num_rows)] for c in range(self._num_cols)]

    def _draw_cell(self, i, j):
        x = Point(self._x1 + i * self._cell_size_x, self._y1 + j * self._cell_size_y)
        y = Point(self._x1 + (i + 1) * self._cell_size_x, self._y1 + (j + 1) * self._cell_size_y)

        cell = Cell(x, y, self._win, True, True, self.up_trigger, self.down_trigger)
        cell.draw()

        self._animate()
        return cell

    def _animate(self):
        self._win.redraw()
        sleep(0.005)

    def _break_entrance_and_exit(self):
        self.up_trigger = False
        self._cells[0][0] = self._draw_cell(0, 0)
        self.up_trigger = True

        self.down_trigger = False
        self._cells[self._num_cols - 1][self._num_rows - 1] = self._draw_cell(self._num_cols - 1, self._num_rows - 1)
        self.down_trigger = True



def main():
    win = Window(800, 590)
    maze = Maze(10, 10, 19, 26, 30, 30, win)
    win.wait_for_close()

main()