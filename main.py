from tkinter import Tk, BOTH, Canvas

class Window():
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas()
        self.__canvas.pack()
        self.__is_running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__is_running = True
        while self.__is_running:
            self.redraw()
        self.__root.destroy()
        
    def close(self):
        self.__is_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
    
    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, canvas, fill_color):
        canvas.create_line(self.x.x, self.x.y, self.y.x, self.y.y, fill=fill_color, width=2)
        canvas.pack()

class Cell():
    def __init__(self, win, has_left_wall=True, has_right_wall=True, has_top_wall=True, has_bottom_wall=True):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self._x1 = 0
        self._x2 = 0
        self._y1 = 0
        self._y2 = 0
        self._win = win

    def draw(self):
        if self.has_left_wall:
            self.win.draw_line()
        if self.has_right_wall:
            self.win.draw_line()
        if self.has_top_wall:
            self.win.draw_line()
        if self.has_bottom_wall:
            self.win.draw_line()

def main():
    win = Window(800, 600)
    win.draw_line(Line(Point(15, 25), Point(200, 25)), "red")
    win.wait_for_close()

main()