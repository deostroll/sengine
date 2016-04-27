from core import Tile
import json
from random import randrange
from ds import WUF, isValidSequence
# import pdb

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
        self.isFirstTurn = True

    def  loadTiles(self):
        res = loadTiles()
        self.tiles = res['tiles']
        self.letter_scores = res['letter_score']

    def fillRack(self, rack, default=None):

        if default is not None:

            existing = len(rack.tiles)
            remaining = rack.size - existing
            default = list(default[:remaining])
            tiles = []
            for ch in default:

                #this itself will raise a StopIteration error
                tile = next(t for t in self.tiles if t.letter == ch)

                tiles.append(tile)
                self.tiles.remove(tile)
            rack.tiles.extend(tiles)

            # TODO: write code for case when the default < remaining

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
            # check for blank tile
            idx = self.player.rack.find('_')
            if idx == -1:
                return {
                    'result' : False,
                    'msg' : 'Invalid tile:' + ch
                }
            else:
                #set the blank tile
                tile = self.player.rack.tiles[idx]
                tile.setSubstituteLetter(ch)

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
                self.position = (pos[0], pos[1] + 1)
                # #if this cell has some tile increment it
                # if self.board.getCell(self.position).hasTile():
                #     self.position = (self.position[0], self.position[1] + 1)
            else:
                self.position = (pos[0] + 1, pos[1])
        else:
            return {
                'result': False,
                'msg': 'Cannot accept letter: ' + ch + '. Row/column at its end'
            }

        # remove tile from rack at that index
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



        return {
            'result' : True,
            'msg' : 'Accepted'
        }

    def joinNeighbours(self, pos, vcells):
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

        # nodes = map(lambda x: self.board._getIndex(x), nodes)
        #
        s = self.board._getIndex(pos)
        # vcells = list(self.board.virtual_cells)
        uf = WUF(vcells)
        # for idx in nodes:
        #     if self.board.getCell(idx).hasTile():
        #         uf.join(s, idx);
        #
        # self._ucells = vcells

        for n in nodes:
            cell = self.board.getCell(n);
            if cell.hasTile():
                uf.join(s, cell.id)


        # return uf

    def endTurn(self):
        midCellIndex = self.board.size** 2 / 2
        def _sort_(a):
            if self.orientation == 'horizontal':
                return a[1]
            else:
                return a[0]

        #sort our placed array
        sorted(self._utilized, key=_sort_)
        vcells = list(self.board.virtual_cells)
        for item in self._utilized:
            self.joinNeighbours(item[1], vcells)
        uf = WUF(vcells)
        # join the entered
        for i in range(1, len(self._utilized)):
            prev = self._utilized[i - 1]
            curr = self._utilized[i]
            pidx = self.board._getIndex(prev[1])
            cidx = self.board._getIndex(curr[1])
            uf.join(pidx, cidx)

        #first index pos of placed word
        _ , p = self._utilized[0]

        idx = self.board._getIndex(p)
        # if self.isFirstTurn:
        #     if uf.isConnected(idx, midCellIndex) == False:
        #         return { 'result' : False, 'msg' : 'Must place first word to pass through the star tile' }
        #
        #     # TODO: Must commit and compute score here
        #
        #     #TODO: Fill rack
        #
        #     self.isFirstTurn = False
        #     return { 'result' : True, 'msg': 'Accepted' }
        # else:
        #     if uf.isConnected(idx, midCellIndex) == False:
        #         return { 'result': 'False', 'msg' : 'Placed word isn\'t connected to game on board'}

        if uf.isConnected(idx, midCellIndex) == False:
            if self.isFirstTurn:
                return { 'result' : False, 'msg' : 'Must place first word to pass through the star tile' }
            else:
                return { 'result' : False, 'msg' : 'Word placed must be connected words played on board' }



    def getCurrentScore(self):

        assert self.orientation is not None
        assert len(self._utilized) > 0

        # 1. Check if all letters put
        #    belong to one row or column
        # 2. identify gap. Check gap with
        #    board
        # 3. retrieve all words (horizontal and vertical)
        # 4. compute score

        """

            General strategy
            ================

            1-  If only 1 letter in queue

                1.1-    if is first turn

                            1.1.1-  throw error

                1.2-    check for neighboring joins and make word(s)

                1.3-    If there are words - compute score

        """
        #clone utilized queue
        utilized = self._utilized[:]

        if len(utilized) == 1:
            #we've to check neighbours
            if self.isFirstTurn:
                return { 'result': False, 'msg': 'First turn not valid word'}

            # we'd only be interested
            # in a case where this isn't
            # the first turn

        if self.isFirstTurn:
            # we don't really care for neighbours
            # at this point

            # join each letter
            # and try to compute

            positions = map(lambda x: x[1], utilized)

            seqRet = isValidSequence(positions)

            if seqRet['result'] == True:
                if seqRet['direction'] == 'horizontal':
                    sorted(utilized, key=lambda x: x[1][1]) # sort with y-ordinate
                    _, fpos = utilized[0]
                    lqueue = []
                    npos = -1
                    gap = False
                    for tile, pos in utilized:
                        if npos == -1:
                            npos = pos[1]
                        elif npos == pos[1]:
                            gap = False
                        else:
                            gap = True

                        npos = npos + 1

                        if gap:
                            # check against the board
                            cell = self.board.getCell(pos)
                            if not cell.hasTile():
                                return Result('False', 'invalid word formation in row')
                            lqueue.append((cell.tile, pos))
                        else:
                            # add tile to lqueue
                            lqueue.append((tile, pos))

                else:
                    sorted(utilized, key=lambda x: x[1][0]) # sort with x-ordinate
                    lqueue = []
                    npos = -1
                    gap = False
                    for tile, pos in utilized:
                        if npos == -1:
                            npos = pos[0]
                        elif npos == pos[0]:
                            gap = False
                        else:
                            gap = True

                        if gap:
                            # check against the board
                            cell = self.board.getCell(pos)
                            if not cell.hasTile():
                                return Result('False', 'invalid word formation in column')
                            lqueue.append((cell.tile, pos))
                        else:
                            # add tile to lqueue
                            lqueue.append((tile, pos))
            else:
                return Result(False, 'invalid tile placement. should be placed either all vertically or horizontally')

            assert lqueue is not None
            # pdb.set_trace()
            score = self._computeQueue(lqueue)

            return Result(True, 'computed score', { 'score': score })

    def _computeQueue(self, queue):
        score = 0
        hasWordScoreBonus = False
        for tile, pos in queue:
            cell = self.board.getCell(pos)
            ls = tile.score
            if cell.hasBonus():
                if cell.bonus == 'TL':
                    ls = ls * 3
                elif cell.bonus == 'DL':
                    ls = ls * 2
                else:
                    hasWordScoreBonus = True
                    wsType = cell.bonus

            score = score + ls
        if hasWordScoreBonus:
            factor = 3 if wsType == 'TW' else 2
            score = score * factor
        return score












def Result(res, msg, other=None):
    ret = {}
    ret['result'] = res
    ret['msg'] = msg

    if other is not None:
        for key in other:
            ret[key] = other[key]

    return ret
