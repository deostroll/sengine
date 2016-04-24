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

class GamePlayTests(TestCase):
    def setUp(self):
        self.board = Board(15)

    def test_tile_load(self):
        tiles = loadTiles()
        assert tiles is not None
        assert len(tiles) == 100

    def test_cell_put(self):
        assert self.board is not None
        board = self.board
        tile = Tile('P', 3)
        board.put(112, tile)

        result = board.getTile(112)
        assert tile == result

    def test_rack(self):
        game = Game()
        game.loadTiles()
        rack = Rack(7)
        total = len(game.tiles)
        game.fillRack(rack)
        # pdb.set_trace()
        assert len(rack.tiles) == 7
        assert total - 7 == len(game.tiles)
