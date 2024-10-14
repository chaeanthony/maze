from window import Window, Line, Point, Cell
from maze import Maze


def main():
    screen_x, screen_y = 800, 600
    margin = 50
    num_rows, num_cols = 15, 15
    cell_size_x = (screen_x - 2 * margin) // num_cols
    cell_size_y = (screen_y - 2 * margin) // num_rows
    win = Window(screen_x, screen_y)
    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win)
    maze.solve()
    win.wait_for_close()


if __name__ == "__main__":
    main()
