from unittest import TestCase
from context import *
import pdb
import pprint

def testWrap(tc, func):
    def execute(inp, expected, hasReturn=True):
        if hasReturn:
            actual = func(inp)
            tc.assertEqual(actual, expected, "fail: \n" + pprint.pformat(locals()))
        else:
            func(inp)

    return execute

class BoardTests(TestCase):
    def test_board_initialization(self):
        board = Board(15)
        # initializes a 1d array
        assert len(board) == 15 * 15

    def test_2d(self):
        board = Board(15)
        actual = board._get2d(14)
        expected = (0, 14)
        # pdb.set_trace()
        self.assertSequenceEqual(actual, expected, "2d test failed")

        actual = board._get2d(29)
        expected = (1, 14)

        self.assertSequenceEqual(actual, expected, "2d test failed")

        #get the centre
        idx = 15 * 15 / 2
        actual = board._get2d(idx)
        expected = (7,7)

        self.assertSequenceEqual(actual, expected, "2d test failed")

    def test_index(self):
        board = Board(15)
        test = (0,0)
        expected = 0
        def func(v):
            return board._getIndex(v)
        test = testWrap(self, func)

        test((0,0), 0)
        test((7,7), 15*15 / 2)
        test((14, 14), 224)

    def test_bonus(self):
        board = Board(15)
        import json
        f = open('data/tiles.json')
        tiles = json.load(f)

        assert tiles is not None

        def func(tiles):
            for r in tiles:
                for c in tiles[r]:
                    # print r, c, tiles[r][c]
                    cell = board.getCell((int(r), int(c)))
                    self.assertTrue(cell.hasBonus(), "Does not have bonus: \n")

        test = testWrap(self, func)

        test(tiles, None, False)
