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
        
    def close(self):
        self.__is_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)


class Point():
    def __init__(self):
        self.x = 0
        self.y = 0

class Line():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, canvas, )


def main():
    win = Window(800, 600)
    win.wait_for_close()

main()