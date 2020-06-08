from z3 import *

class Cell:
    def __init__(self, pos, value, size):
        # Position number
        self._id = pos

        # Cell position
        self._x, self._y, self._block = self.get_pos(pos, size)

        # Set initial value
        self._value = value if value in range(1, size+1) else None

        # Set initial candidates
        self._candidates = {i for i in range(1, size+1) if i != value}


    def __repr__(self):
        return 'Cell({:d})'.format(self.cell_id())


    def cell_id(self):
        return self._id


    def col(self):
        """ Return col number of cell """
        return self._x


    def row(self):
        """ Return row number of cell """
        return self._y


    def block(self):
        """ Return block number of cell """
        return self._block


    def value(self):
        """ Return cell value """
        return self._value


    def candidates(self):
        """ Return cell candidates """
        return set(self._candidates)


    def get_pos(self, pos, size):
        """ Get cell position """
        x = pos%size
        y = pos//size
        size_root = int(size**0.5)
        blk = size_root * (y // size_root) + (x // size_root)
        return x, y, blk


    def decide(self):
        """ Decide cell value if it has only one candidate """
        if self._value is not None:
            return

        if len(self._candidates) == 1:
            self._value = self._candidates.pop()


    def valid(self):
        """ Check cell validation """
        if self._value is None:
            return len(self._candidates) != 0
        else:
            return len(self._candidates) == 0


    def remove_candidates(self, candidates):
        """ Remove candidates """
        self._candidates -= candidates


    def update_cell(self, remove_candidates):
        """ Update cell """
        self.remove_candidates(remove_candidates)
        self.decide()



class Board:
    def __init__(self, cells, size):
        # Check input cells
        if len(cells) != size**2:
            err = 'Size {:d} board requires {:d} cells (but {:d} given)'
            raise ValueError(err.format(size, size**2, len(cells)))

        #self.cells = [Cell(i, v, size) for i, v in enumerate(cells)] # list
        self._cells = {Cell(i, v, size) for i, v in enumerate(cells)} # set
        self._size = size


    def __repr__(self):
        return 'Board({:d}x{:d})'.format(self._size, self._size)


    def get_size(self):
        return self._size


    def get_cells(self):
        return self._cells


    def get_col(self, col_num):
        """ Get cells of the column """
        # TODO: setを返すようにする？
        #return self.cells[col_num::size]
        return filter(lambda c: c.col() == col_num, self._cells)


    def get_row(self, row_num):
        """ Get cells of the row """
        #return self.cells[size*row_num:size*(row_num+1)-1]
        return filter(lambda c: c.row() == row_num, self._cells)


    def get_block(self, block_num):
        """ Get cells of the block """
        return filter(lambda c: c.block() == block_num, self._cells)


    def get_cell(self, cell_id):
        """ Get cells of the id """
        return list(filter(lambda c: c.cell_id() == cell_id, self._cells))[0]


    def valid(self):
        """ Check validation of current board """
        gen_funcs = [self.get_col, self.get_row, self.get_block]
        def check(target):
            values = map(lambda c: c.value(), target)
            filtered = list(filter(lambda v: v is not None, values))
            #print(list(filtered), set(filtered))
            return len(filtered) == len(set(filtered))

        return all(check(f(i)) for f in gen_funcs for i in range(self._size))


    def fill(self):
        return all(cell.value() is not None for i in range(self._size) for cell in self.get_row(i))


    def is_solved(self):
        """ Return this board is solved """
        return self.fill() and self.valid()


    def show(self):
        """ Show current board """
        """ - print the cell value if it is not None """
        """ - print 0 if the cell value is None """

        def get_value_list(l):
            return list(map(lambda c: 0 if c.value() is None else c.value(), l))

        for i in range(self._size):
            l = sorted(self.get_row(i), key=lambda c: c.cell_id())
            print(get_value_list(l))


    def update_one_cell(self, cell):
        """ Update one cell candidates """
        remove_candidates = \
            set(map(lambda c: c.value(), self.get_col(cell.col()))) | \
            set(map(lambda c: c.value(), self.get_row(cell.row()))) | \
            set(map(lambda c: c.value(), self.get_block(cell.block())))
        # Deep Copy
        before_candidates = set(cell.candidates())
        # Update candidates
        cell.update_cell(remove_candidates)
        # Return if cell updated or not
        return before_candidates != cell.candidates()


    def update_all_cell(self):
        """ Update all cells candidates """
        update = False
        while True:
            for cell in self._cells:
                if self.update_one_cell(cell):
                    update = True
                    print('Update {}'.format(cell))

            if not update:
                break

            update = False



class Z3Solver:
    def __init__(self, board):
        self._board = board
        self._solver = Solver()
        self._size = board.get_size()
        self._vals = \
            [Int('cell_{:d}'.format(i)) for i in range(int(board.get_size()**2))]


    def cell_value_restrict(self):
        """ All cell have a value between 1 to {size} """
        for val in self._vals:
            self._solver.add(1 <= val, val <= self._size)


    def add_unique_restrict(self, l):
        self._solver.add(Distinct(l))


    def row_unique_restrict(self):
        """ Distinct cell values in the same row """
        for i in range(self._size):
            self.add_unique_restrict(self._vals[self._size*i:self._size*(i+1)])


    def col_unique_restrict(self):
        """ Distinct cell values in the same col """
        for i in range(self._size):
            self.add_unique_restrict(self._vals[i::self._size])


    def block_unique_restrict(self):
        """ Distinct cell values in the same block """
        for i in range(self._size):
            target_cells = map(lambda c: c.cell_id(), self._board.get_block(i))
            # TODO: 一応リストにしてるけどいてらぶるでも良いかも
            self.add_unique_restrict([self._vals[i] for i in target_cells])


    def init_values(self):
        """ Add initial value restricts """
        for cell in filter(lambda c: c.value() is not None, self._board.get_cells()):
            self._solver.add(self._vals[cell.cell_id()] == cell.value())


    def solve(self):
        self.cell_value_restrict()
        self.row_unique_restrict()
        self.col_unique_restrict()
        self.block_unique_restrict()
        self.init_values()

        if self._solver.check() == sat:
            print('Solved sudoku!')
            m = self._solver.model()
            for i in range(self._size):
                print([m[self._vals[i*self._size+j]] for j in range(self._size)])

        else:
            print('Can\'t solve...')


if __name__ == '__main__':
    l = [int(i) for i in list('000009806306810000080002070030070402070604050502080010020100060000095308804700000')]
    b = Board(l, 9)
    solver = Z3Solver(b)
