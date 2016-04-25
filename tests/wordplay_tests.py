from unittest import TestCase
from context import *
import pdb
import pprint

def write(l):
    w = open('debug.txt', 'a')
    w.write(str(l) + '\n')
    w.close()

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

        self.assertTrue(result['result'] == True, "should fail")

    def test_first_turn_negative(self):
        game = self.game
        player = self.player
        game.fillRack(player.rack, 'cxghiji')
        game.setOrientation('horizontal')
        game.setPosition((6,5))

        game.playLetter('c')
        game.playLetter('h')
        game.playLetter('i')

        res = game.endTurn()

        self.assertTrue(res['result'] == False, "should not accept")

    def test_first_turn_positive(self):
        game = self.game
        player = self.player
        game.fillRack(player.rack, 'cxghiji')
        game.setOrientation('horizontal')
        game.setPosition((7,5))

        game.playLetter('c')
        game.playLetter('h')
        game.playLetter('i')
        # pdb.set_trace()
        res = game.endTurn()

        self.assertTrue(res['result'], "should accept turn")
