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

class WordPlayTests(TestCase):

    def setUp(self):
        self.board = Board(15)
        self.game = Game(self.board)
        rack = Rack(7)
        self.player = Player('dumy', rack)
        self.game.setPlayer(self.player)

    def test_word_play(self):
        game = self.game
        player = self.player
        game.fillRack(player.rack, 'cxghiji')
        game.setOrientation('horizontal')
        game.setPosition((7,5))
        result = game.playWord('chi')

        self.assertTrue(result['result'] == False, "should fail")
