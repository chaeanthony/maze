from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title = "Maze Solver"
        self.__canvas = Canvas(self.__root, bg="white", width=width, height=height)
        self.__canvas.pack(
            fill=BOTH, expand=1
        )  # stretch to fill x and y, expand if resized
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)


class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y


class Line:
    def __init__(self, point1: Point, point2: Point):
        self.point1, self.point2 = point1, point2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point1.x,
            self.point1.y,
            self.point2.x,
            self.point2.y,
            fill=fill_color,
            width=2,
        )


class Cell:
    def __init__(
        self,
        window: Window = None,
    ):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = self._x2 = self._y1 = self._y2 = None
        self._win = window
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        self._x1, self._y1, self._x2, self._y2 = x1, y1, x2, y2
        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line, "white")
        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line, "white")
        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line, "white")
        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line)
        else:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line, "white")

    def draw_move(self, to_cell, undo=False):
        center_x, center_y = (
            self._x1 + abs(self._x1 - self._x2) // 2,
            self._y1 + abs(self._y2 - self._y1) // 2,
        )
        to_x, to_y = (
            to_cell._x1 + abs(to_cell._x1 - to_cell._x2) // 2,
            to_cell._y1 + abs(to_cell._y2 - to_cell._y1) // 2,
        )

        fill = "red" if not undo else "gray"
        self._win.draw_line(Line(Point(center_x, center_y), Point(to_x, to_y)), fill)
