from src.main import Board
from src.solvers.z3_solver import Z3Solver

def test_z3_solve_01():
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
    solver = Z3Solver(b)
    solver.solve()
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


def test_z3_solve_02():
    l = [int(i) for i in list( \
        '800000200' \
        '000056003' \
        '040900700' \
        '007500010' \
        '010000090' \
        '060004500' \
        '003009050' \
        '400760000' \
        '008000006')]
    b = Board(l, 9)
    solver = Z3Solver(b)
    solver.solve()
    assert b.is_valid
    assert b.is_filled
    assert b.is_solved
    res = [int(i) for i in list( \
        '835471269' \
        '792856143' \
        '146932785' \
        '287593614' \
        '514627398' \
        '369184527' \
        '673249851' \
        '451768932' \
        '928315476')]
    assert all([[c.value for c in b.get_row(i)] == res[i*9:(i+1)*9] for i in range(9)])
