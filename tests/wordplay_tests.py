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

    def test_first_turn_score(self):

        game = self.game
        player = self.player
        rackLetters = 'sinaete'
        game.fillRack(player.rack, rackLetters)
        game.setOrientation('horizontal')
        game.setPosition((7, 4))

        tileDb = loadTiles()

        tile_scores = tileDb['letter_score']

        word = 'tense'
        game.playWord('tense')

        actualScore = game.getCurrentScore()['score']
        expectedScore = 0
        for ch in word:
            t = next(tile for tile in tileDb['tiles'] if tile.letter == ch)
            expectedScore = expectedScore + t.score

        expectedScore = expectedScore * 2

        self.assertEqual(actualScore, expectedScore)

    def test_first_turn_score_exception(self):

        game = self.game
        player = self.player
        rackLetters = 'sinaete'
        game.fillRack(player.rack, rackLetters)
        game.setOrientation('horizontal')
        game.setPosition((6, 4))

        tileDb = loadTiles()

        tile_scores = tileDb['letter_score']

        word = 'tense'
        res = game.playWord('tense')
        self.assertFalse(res['result'], "should be false")
