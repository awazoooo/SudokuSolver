class Cell:
    """ Sudoku cell class

    Attributes:
        cell_id (int): Cell id number
            col (int): Cell column number
            row (int): Cell row number
          block (int): Cell block number
         values (int): Cell fixed value. The value is 0 if the value is not fixed
     candidates (set): Cell candidate values
    """


    def __init__(self, pos, value, size):
        self._cell_id = pos
        self._col, self._row, self._block = self._get_pos(pos, size)
        self._value = value if value in range(1, size+1) else 0
        self._candidates = set() if self.value else {i for i in range(1, size+1) if i != value}
        self._size = size


    def __repr__(self):
        return 'Cell({:d})'.format(self._cell_id)


    @staticmethod
    def _get_pos(pos, size):
        """ Get cell col, row, and block number """
        x = pos % size
        y = pos // size
        size_root = int(size ** 0.5)
        blk = size_root * (y // size_root) + (x // size_root)
        return x, y, blk


    @property
    def cell_id(self):
        return self._cell_id


    @cell_id.setter
    def cell_id(self, val):
        self._cell_id = val


    @property
    def value(self):
        return self._value


    @value.setter
    def value(self, val):
        self._value = val
        self._candidates = set()


    @property
    def col(self):
        return self._col


    @property
    def row(self):
        return self._row


    @property
    def block(self):
        return self._block


    @property
    def candidates(self):
        return self._candidates


    @property
    def valid(self):
        """ Check cell validation """
        if not self.value:
            # If cell value is not fixed, the candidates must not be empty
            return len(self.candidates) != 0
        else:
            # If cell value is fixed, the candidates must be empty
            return len(self.candidates) == 0


    def _decide(self):
        """ Decide cell value if it has only one candidate

        Returns:
            bool: True if the cell value or candidates are updated
        """
        if len(self.candidates) == 1:
            self.value = self.candidates.pop()
            return True

        return False


    def _remove_candidates(self, rm_candidates):
        """ Remove candidates """
        before = len(set(self.candidates))
        self.candidates -= rm_candidates
        return before != len(self.candidates)


    def update_cell(self, rm_candidates):
        """ Update cell value and candidates

        Args:
            rm_candidates (set): Candidates will be removed

        Returns:
            bool: True if the cell value or candidates are updated
        """

        res = self._remove_candidates(rm_candidates)
        res2 = self._decide()
        return res or res2



class Board:
    """ Sudoku board class

    Attributes:
        cells (Cell list): List of Cell objects
              size (int): Board size
    """

    def __init__(self, cells, size):
        # Check input cells
        if len(cells) != size**2:
            err = 'Size {:d} board requires {:d} cells (but {:d} given)'
            raise ValueError(err.format(size, size**2, len(cells)))

        self.cells = [Cell(i, v, size) for i, v in enumerate(cells)]
        self.size = size


    def __getitem__(self, index):
        return self.cells[index]


    def __len__(self):
        return self.size**2


    def __repr__(self):
        return 'Board({:d}x{:d})'.format(self.size, self.size)


    def show(self):
        """ Print current board

        Sample: Of course, this board is invalid :-)
        +---+---+---+---+---+---+---+---+---+
        | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
        +---+---+---+---+---+---+---+---+---+
        | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
        +---+---+---+---+---+---+---+---+---+
        | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
        +---+---+---+---+---+---+---+---+---+
        | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
        +---+---+---+---+---+---+---+---+---+
        | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
        +---+---+---+---+---+---+---+---+---+
        | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
        +---+---+---+---+---+---+---+---+---+
        | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
        +---+---+---+---+---+---+---+---+---+
        | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
        +---+---+---+---+---+---+---+---+---+
        | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
        +---+---+---+---+---+---+---+---+---+
        """

        def _make_separator():
            return ('-'*((len(str(self.size)) + 2))).join(['+']*(self.size+1))

        sep = _make_separator()
        print(sep)
        for i in range(self.size):
            # TODO: Fits if board.size > 9
            values = [' {:d} '.format(c.value) for c in self.get_row(i)]
            print('|', '|'.join(values), '|', sep='')
            print(sep)


    def get_cell_values(self):
        """
        Get all values of cells

        Returns:
            Array(Int)
        """

        return [cell.value for cell in self.cells]


    def get_col(self, col):
        """ Get cells of the column """
        if col >= self.size:
            return []
        return self.cells[col::self.size]


    def get_row(self, row):
        """ Get cells of the row """
        return self.cells[row*self.size:(row+1)*self.size]


    def get_block(self, block):
        """ Get cells of the block """
        return [c for c in self.cells if c.block == block]


    @property
    def is_valid(self):
        """ Check validation of current board

        Returns:
            bool: True if the board is valid
        """
        def check(target):
            values = map(lambda c: c.value, target)
            # Copy iterator
            filtered = list(filter(lambda v: v, values))
            return len(filtered) == len(set(filtered))

        return all(check(f(i)) \
                   for f in [self.get_col, self.get_row, self.get_block] \
                   for i in range(self.size))


    @property
    def is_filled(self):
        """ Check current board is filled """
        return all(cell.value \
                   for i in range(self.size) \
                   for cell in self.get_row(i))


    @property
    def is_solved(self):
        """ Return this board is solved """
        return self.is_filled and self.is_valid


    def update_one_cell(self, cell):
        """ Update one cell candidates

        Args:
            cell (Cell): Cell object

        Returns:
            bool: True if the cell updated
        """
        rm_candidates = \
            {c.value for c in self.get_col(cell.col)} | \
            {c.value for c in self.get_row(cell.row)} | \
            {c.value for c in self.get_block(cell.block)}

        # Update candidates
        return cell.update_cell(rm_candidates)


    def update_all_cell(self):
        """ Repeat update all cells candidates """
        update = False
        while True:
            for cell in self.cells:
                if self.update_one_cell(cell):
                    update = True
                    print('Update {}'.format(cell))

            if not update:
                break

            update = False



if __name__ == '__main__':
    from solvers.z3_solver import Z3Solver
    l = [int(i) for i in list('000009806306810000080002070030070402070604050502080010020100060000095308804700000')]
    b = Board(l, 9)
    solver = Z3Solver(b)
    solver.solve()
    b.show()
