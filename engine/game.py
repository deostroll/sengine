from core import Tile
import json
from random import randrange

def loadTiles():
    f = open('data/tiles.json')
    tiles = json.load(f)
    tileArr = []
    # print tiles['freq']
    for (l, f) in tiles['freq'].iteritems():
        score = tiles['scores'][l]
        for x in range(f):
            tileArr.append(Tile(l, score))

    return {
        'tiles': tileArr,
        'letter_score': tiles['scores']
    }

class Game:

    def __init__(self, board):
        self.board = board
        self.loadTiles()

    def  loadTiles(self):
        res = loadTiles()
        self.tiles = res['tiles']
        self.letter_scores = res['letter_score']

    def fillRack(self, rack, default=None):

        if default is not None:
            tiles = map(lambda x: Tile(x, self.letter_scores[x]) , list(default))
            rack.tiles = tiles
            return

        existing = len(rack.tiles)
        remaining = rack.size - existing
        self.shuffle()
        i = remaining
        while i > 0:
            rack.tiles.append(self.tiles.pop())
            i = i - 1


    def shuffle(self):
        for i in range(len(self.tiles) - 1, 0, -1):
            j = randrange(i + 1)
            self.tiles[i], self.tiles[j] = self.tiles[j], self.tiles[i]

    # def putWord(self, pos, word, orientation='horizontal'):
    #     for ch in word:

    def setPlayer(self, player):
        self.player = player
        self._utilized = []

    def playLetter(self, ch):
        assert self.player is not None

        idx = self.player.rack.find(ch)

        if idx == -1:
            return {
                'result' : False,
                'msg' : 'Invalid tile'
            }

        self._utilized.append(self.player.rack.tiles[idx])
        del self.player.rack.tiles[idx]

        return {
            'result' : True,
            'msg' : 'Accepted'
        }
