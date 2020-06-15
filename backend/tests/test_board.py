from src.main import Board

def test_board_create_01():
    b = Board([1]*(9**2), 9)
    assert all([c.value == 1 for c in b])
    assert len(b) == 81
    assert all([[c.value for c in b.get_row(i)] == [1] * 9 for i in range(9)])
    assert all([[c.value for c in b.get_col(i)] == [1] * 9 for i in range(9)])
    assert all([[c.value for c in b.get_block(i)] == [1] * 9 for i in range(9)])
    assert not b.is_valid
    assert b.is_filled
    assert not b.is_solved


def test_board_create_02():
    l = [int(i) for i in list( \
        '020030008' \
        '700600540' \
        '004000090' \
        '560020900' \
        '900708004' \
        '002010053' \
        '040000200' \
        '071009005' \
        '200040060')]
    b = Board(l, 9)
    assert len(b) == 81
    assert all([[c.value for c in b.get_row(i)] == l[i*9:(i+1)*9] for i in range(9)])
    assert all([[c.value for c in b.get_col(i)] == l[i::9] for i in range(9)])
    block_list = [
        [int(s) for s in '020700004'],
        [int(s) for s in '030600000'],
        [int(s) for s in '008540090'],
        [int(s) for s in '560900002'],
        [int(s) for s in '020708010'],
        [int(s) for s in '900004053'],
        [int(s) for s in '040071200'],
        [int(s) for s in '000009040'],
        [int(s) for s in '200005060']
    ]
    assert all([[c.value for c in b.get_block(i)] == block_list[i] for i in range(9)])
    assert b.is_valid
    assert not b.is_filled
    assert not b.is_solved


def test_board_cell_update_01():
    l = [int(i) for i in list( \
        '020030008' \
        '700600540' \
        '004000090' \
        '560020900' \
        '900708004' \
        '002010053' \
        '040000200' \
        '071009005' \
        '200040060')]
    b = Board(l, 9)
    b.update_one_cell(b[0])
    assert b[0].value == 0
    assert b[0].candidates == {1, 6}
    assert b[0].valid


def test_board_cell_update_02():
    l = [int(i) for i in list( \
        '020030108' \
        '700600540' \
        '004000090' \
        '560020900' \
        '900708004' \
        '002010053' \
        '040000200' \
        '071009005' \
        '200040060')]
    b = Board(l, 9)
    b.update_one_cell(b[0])
    assert b[0].value == 6
    assert b[0].candidates == set()
    assert b[0].valid


def test_board_cell_all_update():
    l = [int(i) for i in list( \
        '020030008' \
        '700600540' \
        '004000090' \
        '560020900' \
        '900708004' \
        '002010053' \
        '040000200' \
        '071009005' \
        '200040060')]
    b = Board(l, 9)
    b.update_all_cell()
    assert b.is_valid
    assert b.is_filled
    assert b.is_solved
    res = [int(i) for i in list( \
        '629435178' \
        '738691542' \
        '154872396' \
        '567324981' \
        '913758624' \
        '482916753' \
        '346587219' \
        '871269435' \
        '295143867')]
    assert all([[c.value for c in b.get_row(i)] == res[i*9:(i+1)*9] for i in range(9)])
