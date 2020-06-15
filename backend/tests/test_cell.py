from src.main import Cell

def check_cell(c, cell_id, col, row, block, value, candidates):
    assert c.cell_id == cell_id
    assert c.col == col
    assert c.row == row
    assert c.block == block
    assert c.value == value
    assert c.candidates == candidates
    assert c.valid


def test_cell_create_01():
    c = Cell(0, None, 9)
    check_cell(c, 0, 0, 0, 0, 0, {i for i in range(1, 9+1)})


def test_cell_create_02():
    c = Cell(31, 5, 9)
    check_cell(c, 31, 4, 3, 4, 5, set())


def test_cell_create_03():
    c = Cell(80, 9, 9)
    check_cell(c, 80, 8, 8, 8, 9, set())


def test_cell_create_large_01():
    c = Cell(130, None, 16)
    check_cell(c, 130, 2, 8, 8, 0, {i for i in range(1, 16+1)})


def test_cell_set_value():
    c = Cell(0, None, 9)
    c.set_value(5)
    assert c.value == 5
    assert c.candidates == set()
    assert c.valid


def test_cell_update_01():
    c = Cell(0, None, 9)
    c.candidates = {1, 2}
    c.update_cell({1})
    assert c.value == 2
    assert c.candidates == set()


def test_cell_update_02():
    c = Cell(0, None, 9)
    c.candidates = {1, 2, 3}
    c.update_cell({1})
    assert not c.value
    assert c.candidates == {2, 3}


