from window import Cell
import time
import random
from collections import deque
from constants import ANIMATE_SPEED


class Maze:
    def __init__(
        self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None
    ):
        self._x1, self._y1 = x1, y1
        self._num_rows, self._num_cols = num_rows, num_cols
        self._cell_size_x, self._cell_size_y = cell_size_x, cell_size_y
        self._win = win
        self._cells = []
        if seed:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate(animate_speed=0.001)

    def _animate(self, animate_speed=ANIMATE_SPEED):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(animate_speed)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_right_wall = False
        self._cells[-1][-1].has_left_wall = False
        self._draw_cell(0, 0)
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []

            # determine which cell(s) to visit next
            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
            # right
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            # down
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))

            # if there is nowhere to go from here
            # just break out
            if len(next_index_list) == 0:
                self._draw_cell(i, j)
                return

            # randomly choose the next direction to go
            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]

            # knock out walls between this cell and the next cell(s)
            # right
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # left
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # down
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            # up
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            # recursively visit the next cell
            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for cells in self._cells:
            for cell in cells:
                cell.visited = False

    def solve(self):
        return self._solve_bfs()

    def _solve_r(self, i, j):
        self._animate()
        pass

    def _solve_bfs(self):
        if not self._cells:
            raise Exception("Maze is blank")

        queue = deque([(self._cells[0][0], (0, 0), (0, 0))])

        while queue:
            self._animate()

            cell, pos, prev = queue.popleft()
            x, y = pos
            prev_x, prev_y = prev

            cell.visited = True
            cell.draw_move(self._cells[prev_x][prev_y])

            if x == self._num_cols - 1 and y == self._num_rows - 1:
                return True

            if (
                x - 1 >= 0
                and not self._cells[x - 1][y].visited
                and not cell.has_left_wall
            ):
                queue.append((self._cells[x - 1][y], (x - 1, y), (x, y)))
            if (
                x + 1 < self._num_cols
                and not self._cells[x + 1][y].visited
                and not cell.has_right_wall
            ):
                queue.append((self._cells[x + 1][y], (x + 1, y), (x, y)))
            if (
                y + 1 < self._num_rows
                and not self._cells[x][y + 1].visited
                and not cell.has_bottom_wall
            ):
                queue.append((self._cells[x][y + 1], (x, y + 1), (x, y)))
            if (
                y - 1 >= 0
                and not self._cells[x][y - 1].visited
                and not cell.has_top_wall
            ):
                queue.append((self._cells[x][y - 1], (x, y - 1), (x, y)))

        return False
