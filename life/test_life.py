from io import StringIO
import itertools
import random
import unittest
from unittest import mock
import pytest
from life import CellList, Life
from parameterized import parameterized


class TestCellList(unittest.TestCase):
    def test_empty(self):
        c = CellList()
        assert list(c) == []

    def test_set_true(self):
        c = CellList()
        c.set(1, 2, True)
        assert c.has(1, 2)
        assert list(c) == [(1, 2)]
        c.set(500, 600, True)
        assert c.has(1, 2) and c.has(500, 600)
        assert list(c) == [(1, 2), (500, 600)]
        c.set(1, 2, True)
        assert c.has(1, 2) and c.has(500, 600)
        assert list(c) == [(1, 2), (500, 600)]

    def test_set_false(self):
        c = CellList()
        c.set(1, 2, False)
        assert not c.has(1, 2)
        assert list(c) == []
        c.set(1, 2, True)
        c.set(1, 2, False)
        assert not c.has(1, 2)
        assert list(c) == []
        c.set(1, 2, True)
        c.set(3, 2, True)
        c.set(1, 2, False)
        assert not c.has(1, 2)
        assert c.has(3, 2)
        assert list(c) == [(3, 2)]

    def test_set_default(self):
        c = CellList()
        c.set(1, 2)
        assert c.has(1, 2)
        assert list(c) == [(1, 2)]
        c.set(1, 2)
        assert not c.has(1, 2)
        assert list(c) == []


class TestLife(unittest.TestCase):
    def test_new(self):
        life = Life()
        assert life.survival == [2, 3]
        assert life.birth == [3]
        assert list(life.living_cells()) == []
        assert life.rules_str() == '23/3'

    def test_new_custom(self):
        life = Life([3, 4], [4, 7, 8])
        assert life.survival == [3, 4]
        assert life.birth == [4, 7, 8]
        assert list(life.living_cells()) == []
        assert life.rules_str() == '34/478'

    @parameterized.expand([('pattern1.txt',), ('pattern2.txt',)])
    def test_load(self, pattern):
        life = Life()
        life.load(pattern)
        assert life.survival == [2, 3]
        assert life.birth == [3]
        assert set(life.living_cells()) == {
            (10, 10), (11, 11), (15, 10), (17, 10)}
        assert life.bounding_box() == (10, 10, 17, 11)

    def test_load_life_custom_rules(self):
        life = Life()
        life.load('pattern3.txt')
        assert life.survival == [3, 4]
        assert life.birth == [4, 5]
        assert list(life.living_cells()) == [(10, 10), (11, 11), (10, 12)]
        assert life.bounding_box() == (10, 10, 11, 12)

    def test_load_invalid(self):
        life = Life()
        with pytest.raises(RuntimeError):
            life.load('pattern4.txt')

    def test_toggle(self):
        life = Life()
        life.toggle(5, 5)
        assert list(life.living_cells()) == [(5, 5)]
        life.toggle(5, 6)
        life.toggle(5, 5)
        assert list(life.living_cells()) == [(5, 6)]

    @parameterized.expand(itertools.product(
        [[2, 3], [4]],  # two different survival rules
        [[3], [3, 4]],  # two different birth rules
        [True, False],  # two possible states for the cell
        range(0, 9),    # nine number of possible neighbors
    ))
    def test_advance_cell(self, survival, birth, alive, num_neighbors):
        life = Life(survival, birth)
        if alive:
            life.toggle(0, 0)
        neighbors = [(-1, -1), (0, -1), (1, -1),
                     (-1, 0), (1, 0),
                     (-1, 1), (0, 1), (1, 1)]
        for i in range(num_neighbors):
            n = random.choice(neighbors)
            neighbors.remove(n)
            life.toggle(*n)

        new_state = life._advance_cell(0, 0)
        if alive:
            # survival rule
            if num_neighbors in survival:
                assert new_state is True
            else:
                assert new_state is False
        else:
            # birth rule
            if num_neighbors in birth:
                assert new_state is True
            else:
                assert new_state is False

    @mock.patch.object(Life, '_advance_cell')
    def test_advance_false(self, mock_advance_cell):
        mock_advance_cell.return_value = False
        life = Life()
        life.toggle(10, 10)
        life.toggle(12, 10)
        life.toggle(20, 20)
        life.advance()

        # there should be exactly 24 calls to _advance_cell:
        # - 9 around the (10, 10) cell
        # - 6 around the (12, 10) cell (3 were already processed by (10, 10))
        # - 9 around the (20, 20) cell
        assert mock_advance_cell.call_count == 24
        assert list(life.living_cells()) == []

    @mock.patch.object(Life, '_advance_cell')
    def test_advance_true(self, mock_advance_cell):
        mock_advance_cell.return_value = True
        life = Life()
        life.toggle(10, 10)
        life.toggle(11, 10)
        life.toggle(20, 20)
        life.advance()

        # there should be exactly 24 calls to _advance_cell:
        # - 9 around the (10, 10) cell
        # - 3 around the (11, 10) cell (3 were already processed by (10, 10))
        # - 9 around the (20, 20) cell
        assert mock_advance_cell.call_count == 21

        # since the mocked advance_cell returns True in all cases, all 24
        # cells must be alive
        assert set(life.living_cells()) == {
            (9, 9), (10, 9), (11, 9), (12, 9),
            (9, 10), (10, 10), (11, 10), (12, 10),
            (9, 11), (10, 11), (11, 11), (12, 11),
            (19, 19), (20, 19), (21, 19),
            (19, 20), (20, 20), (21, 20),
            (19, 21), (20, 21), (21, 21),
        }
