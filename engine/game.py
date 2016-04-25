from core import Tile
import json
from random import randrange
from ds import WUF

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
        assert self.position is not None
        assert self.orientation is not None

        idx = self.player.rack.find(ch)

        if idx == -1:
            return {
                'result' : False,
                'msg' : 'Invalid tile:' + ch
            }

        # TODO: add implementation of adding to board here

        pos = self.position
        if pos[0] < self.board.size and pos[1] < self.board.size:

            cell = self.board.getCell(pos)
            #push into queue
            if cell.tile is not None:
                return {
                    'result': False,
                    'msg': 'Cannot accept: ' + ch + '. Already a tile in ' + str(pos)
                }
            self._utilized.append((self.player.rack.tiles[idx], pos))
            if self.orientation == 'horizontal':
                self.position = (pos[0] + 1, pos[1])
            else:
                self.posotion = (pos[0], pos[1] + 1)
        else:
            return {
                'result': False,
                'msg': 'Cannot accept letter: ' + ch + '. Row/column at its end'
            }


        del self.player.rack.tiles[idx]

        return {
            'result' : True,
            'msg' : 'Accepted'
        }

    def setOrientation(self, orientation):
        self.orientation = orientation

    def setPosition(self, pos):
        self.position = pos

    def playWord(self, word):
        assert self.orientation is not None
        assert self.position is not None
        for letter in word:
            res = self.playLetter(letter)
            if res['result'] == False:
                return res

        #todo check for connection

        return {
            'result' : True,
            'msg' : 'Accepted'
        }

    def isValid(self):
        #clone virtual cells
        vcells = list(self.board.virtual_cells)
        uf = WUF(vcells)


        for i in range(1, len(self._utilized)):
            pass
    def joinNeighbours(self, pos):
        nodes = []
        size = self.board.size

        #top  (0, 1 - 13)
        #botton (14, 1 - 13)
        #left (1 - 13, 0)
        #right (1-13, 14)
        #topLeft (0,0)
        #topRight (0,14)
        #bottomLeft (14, 0)
        #bottomRight (14,14)

        if pos[0] == 0 and (pos[1] > 0 and pos[1] < size): #top
            nodes.append((pos[0] - 1, pos[1])) #left
            nodes.append((pos[0] + 1, pos[1])) #right
            # nodes.append((pos[0], pos[1] - 1)) #top
            nodes.append((pos[0], pos[1] + 1)) #bottom
        elif pos[0] == size - 1 and (pos[1] > 0 and pos[1] < size): #bottom
            nodes.append((pos[0] - 1, pos[1])) #left
            nodes.append((pos[0] + 1, pos[1])) #right
            nodes.append((pos[0], pos[1] - 1)) #top
            # nodes.append((pos[0], pos[1] + 1)) #bottom
        elif (pos[0] > 0 and pos[0] < size) and pos[1] == 0: #left
            # nodes.append((pos[0] - 1, pos[1])) #left
            nodes.append((pos[0] + 1, pos[1])) #right
            nodes.append((pos[0], pos[1] - 1)) #top
            nodes.append((pos[0], pos[1] + 1)) #bottom
        elif (pos[0] > 0 and pos[0] < size) and pos[1] == size - 1: #right
            nodes.append((pos[0] - 1, pos[1])) #left
            # nodes.append((pos[0] + 1, pos[1])) #right
            nodes.append((pos[0], pos[1] - 1)) #top
            nodes.append((pos[0], pos[1] + 1)) #bottom
        elif pos[0] == pos[1] == 0: #topLeft
            # nodes.append((pos[0] - 1, pos[1])) #left
            nodes.append((pos[0] + 1, pos[1])) #right
            # nodes.append((pos[0], pos[1] - 1)) #top
            nodes.append((pos[0], pos[1] + 1)) #bottom
        elif pos[0] == 0 and pos[1] == size - 1: #topRight
            nodes.append((pos[0] - 1, pos[1])) #left
            # nodes.append((pos[0] + 1, pos[1])) #right
            # nodes.append((pos[0], pos[1] - 1)) #top
            nodes.append((pos[0], pos[1] + 1)) #bottom
        elif pos[0] == size - 1 and pos[1] == 0: #bottomLeft
            # nodes.append((pos[0] - 1, pos[1])) #left
            nodes.append((pos[0] + 1, pos[1])) #right
            nodes.append((pos[0], pos[1] - 1)) #top
            # nodes.append((pos[0], pos[1] + 1)) #bottom
        else:
            nodes.append((pos[0] - 1, pos[1])) #left
            # nodes.append((pos[0] + 1, pos[1])) #right
            nodes.append((pos[0], pos[1] - 1)) #top
            # nodes.append((pos[0], pos[1] + 1)) #bottom

        nodes = map(lambda x: self.board._getIndex(x), nodes)

        s = self.board._getIndex(pos)
