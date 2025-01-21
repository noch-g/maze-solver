import time
import random
from cell import Cell


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        if seed is not None:
            random.seed(seed)
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.cells = []
        self.animation_delay = 0.01
        self.create_cells()

        self.animation_delay = 0.2
        self.break_entrance_and_exit()

        self.animation_delay = 0.01
        self.break_walls_r(0, 0)
        self.reset_cells_visited()
        self.animation_delay = 0.12

    def create_cells(self):
        for col in range(self.num_cols):
            col_cells = []
            for row in range(self.num_rows):
                col_cells.append(Cell(self.win))
            self.cells.append(col_cells)
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.draw_cell(i, j)

    def break_entrance_and_exit(self):
        self.cells[0][0].has_top_wall = False
        self.draw_cell(0, 0)
        self.cells[-1][-1].has_bottom_wall = False
        self.draw_cell(len(self.cells)-1, len(self.cells[0])-1)

    def are_coords_valid(self, i, j):
        return 0 <= i < self.num_cols and 0 <= j < self.num_rows

    def break_walls_r(self, i, j):
        self.cells[i][j].visited = True
        while True:
            directions = []
            if self.are_coords_valid(i+1, j) and not self.cells[i+1][j].visited:
                directions.append((i+1, j))
            if self.are_coords_valid(i-1, j) and not self.cells[i-1][j].visited:
                directions.append((i-1, j))
            if self.are_coords_valid(i, j+1) and not self.cells[i][j+1].visited:
                directions.append((i, j+1))
            if self.are_coords_valid(i, j-1) and not self.cells[i][j-1].visited:
                directions.append((i, j-1))
            if not directions:
                self.draw_cell(i, j)
                return

            # dir = random.choice(directions)
            dir_index = random.randrange(len(directions))
            direction = directions[dir_index]
            dir_i, dir_j = direction
            if direction == (i+1, j):
                self.cells[i][j].has_right_wall = False
                self.cells[dir_i][dir_j].has_left_wall = False
            if direction == (i-1, j):
                self.cells[i][j].has_left_wall = False
                self.cells[dir_i][dir_j].has_right_wall = False
            if direction == (i, j+1):
                self.cells[i][j].has_bottom_wall = False
                self.cells[dir_i][dir_j].has_top_wall = False
            if direction == (i, j-1):
                self.cells[i][j].has_top_wall = False
                self.cells[dir_i][dir_j].has_bottom_wall = False
            self.break_walls_r(dir_i, dir_j)

    def reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.cells[i][j].visited = False

    def solve(self):
        return self.solve_r(0, 0)

    def solve_r(self, i, j):
        self.animate()
        self.cells[i][j].visited = True
        if (i, j) == (self.num_cols-1, self.num_rows-1):
            return True
        if self.are_coords_valid(i+1, j) and not self.cells[i][j].has_right_wall and not self.cells[i+1][j].visited:
            self.cells[i][j].draw_move(self.cells[i+1][j])
            if self.solve_r(i+1, j):
                return True
            self.cells[i][j].draw_move(self.cells[i+1][j], undo=True)
        if self.are_coords_valid(i, j+1) and not self.cells[i][j].has_bottom_wall and not self.cells[i][j+1].visited:
            self.cells[i][j].draw_move(self.cells[i][j+1])
            if self.solve_r(i, j+1):
                return True
            self.cells[i][j].draw_move(self.cells[i][j+1], undo=True)
        if self.are_coords_valid(i-1, j) and not self.cells[i][j].has_left_wall and not self.cells[i-1][j].visited:
            self.cells[i][j].draw_move(self.cells[i-1][j])
            if self.solve_r(i-1, j):
                return True
            self.cells[i][j].draw_move(self.cells[i-1][j], undo=True)
        if self.are_coords_valid(i, j-1) and not self.cells[i][j].has_top_wall and not self.cells[i][j-1].visited:
            self.cells[i][j].draw_move(self.cells[i][j-1])
            if self.solve_r(i, j-1):
                return True
            self.cells[i][j].draw_move(self.cells[i][j-1], undo=True)
        return False

    def draw_cell(self, i, j):
        if self.win is None:
            return
        cell_x1 = self.x1 + i * self.cell_size_x
        cell_x2 = cell_x1 + self.cell_size_x
        cell_y1 = self.y1 + j * self.cell_size_y
        cell_y2 = cell_y1 + self.cell_size_y

        self.cells[i][j].draw(cell_x1, cell_y1, cell_x2, cell_y2)
        self.animate()

    def animate(self):
        self.win.redraw()
        time.sleep(self.animation_delay)
