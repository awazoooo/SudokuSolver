from z3 import *

class Z3Solver:
    def __init__(self, board):
        self.board = board
        self.solver = Solver()
        self.size = board.size
        self.z3_vars = \
            [Int('cell_{:d}'.format(i)) for i in range(board.size**2)]


    def cell_value_restrict(self):
        """ All cell have a value between 1 to {size} """
        for val in self.z3_vars:
            self.solver.add(1 <= val, val <= self.size)


    def add_unique_restrict(self, l):
        self.solver.add(Distinct(l))


    def row_unique_restrict(self):
        """ Distinct cell values in the same row """
        for i in range(self.size):
            self.solver.add(Distinct([self.z3_vars[c.cell_id] for c in self.board.get_row(i)]))


    def col_unique_restrict(self):
        """ Distinct cell values in the same col """
        for i in range(self.size):
            self.solver.add(Distinct([self.z3_vars[c.cell_id] for c in self.board.get_col(i)]))
            #self.add_unique_restrict(self.vals[i::self.size])


    def block_unique_restrict(self):
        """ Distinct cell values in the same block """
        for i in range(self.size):
            self.solver.add(Distinct([self.z3_vars[c.cell_id] for c in self.board.get_block(i)]))
            #target_cells = map(lambda c: c.cell_id(), self._board.get_block(i))
            # TODO: 一応リストにしてるけどいてらぶるでも良いかも
            #self.add_unique_restrict([self._vals[i] for i in target_cells])


    def init_values(self):
        """ Add initial value restricts """
        for cell in filter(lambda c: c.value, self.board):
            self.solver.add(self.z3_vars[cell.cell_id] == cell.value)


    def solve(self):
        self.cell_value_restrict()
        self.row_unique_restrict()
        self.col_unique_restrict()
        self.block_unique_restrict()
        self.init_values()

        if self.solver.check() == sat:
            print('Solved sudoku!')
            m = self.solver.model()
            for i, var in enumerate(self.z3_vars):
                # Update board
                self.board[i].set_value(m[var].as_long())

        else:
            print('Can\'t solve...')