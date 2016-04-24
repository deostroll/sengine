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
        tiles = loadTiles()['tiles']
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
        game = Game(self.board)
        game.loadTiles()
        rack = Rack(7)
        total = len(game.tiles)
        game.fillRack(rack)
        # pdb.set_trace()
        assert len(rack.tiles) == 7
        assert total - 7 == len(game.tiles)

    def test_player_rack(self):
        rack = Rack(7)
        game = Game(self.board)
        player = Player('Player 1', rack)
        game.fillRack(player.rack, 'xcwaaei')
        game.setPlayer(player)

        #place a tile not in rack
        #should error
        result = game.playLetter('k')

        self.assertTrue(result['result'] == False, 'letter cannot be played')

        #player rack tiles would have not reduced
        assert len(player.rack.tiles) == 7

        result = game.playLetter('c')
        self.assertTrue(result['result'])
        assert len(player.rack.tiles) == 6

    
