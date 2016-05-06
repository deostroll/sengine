from core import Tile, Board, Player, Ai, Rack
import json
from random import randrange
from ds import WUF, isValidSequence
import threading
from utils import ordinate
# import pdb


class Events:
    READY = 0
    QUIT = 3
    ERROR = 4

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

    @staticmethod
    def getInstance():
        board = Board(15)
        game = Game(board)
        return game

    def __init__(self, board):
        self.board = board
        self.loadTiles()
        self.isFirstTurn = True
        self.sinks = []
        # self.status = Events.BUSY
        self.quitFlag = False
        self.played = False
        self.q = {}
        self.error = False
        self.reason = ''

    def resetError(self):
        self.error = False
        self.reason = ''

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


    def setPlayer(self, name):
        self.name = name

    def trigger(self, evt, *args):
        for sink, handler in self.sinks:
            handler(evt, self, *args)

    def wireSink(self, handler, source='_internal_'):
        self.sinks.append((source, handler))

    def removeSink(self, source):

        for item in self.sinks:
            x, _ = item
            if x == source:
                break

        self.sinks.remove(item)

    def setupPlayer(self, name):
        self.name = name

    def start(self):
        # self.evt = threading.Event()
        t = threading.Thread(target=self.run)
        t.daemon = True
        t.start()
        self.thread = t

    def waitForExit(self):
        self.thread.join()

    def quit(self):
        self.quit = True

    def run(self):
        # print 'run...'
        game = self
        rack = Rack(7)
        self.player = player = Player(self.name, rack)
        game.fillRack(player.rack)

        rack = Rack(7)
        ai = Ai(rack)
        ai.setup(game)
        self.ai = ai

        humanRackSize = lambda: len(player.rack.tiles)
        aiRackSize = lambda: len(ai.rack.tiles)
        remaining = lambda: len(game.tiles)

        humanRackEmpty = lambda: humanRackSize() == 0
        aiRackEmpty = lambda: aiRackSize() == 0

        passCount = 0
        round = 0

        while True:
            round = round + 1
            self.current = player
            self.trigger(Events.READY, self, round)

            if self.quit:
                break

            if self.error:
                self.trigger(Events.ERROR, self, self.reason)
                round = round - 1
                continue
            # self.current = ai
            # ai.play()

    def clear(self):
        self.q = {}

    def put(self, pos, letter):
        board = self.board
        cell = board.getCell(pos)
        if ordinate.ok(pos) and cell.hasTile() == False:
            idx = self.current.rack.find(letter)
            if idx == -1:
                self.error = True
                self.reason = 'letter not in rack: ' + letter
            self.q[pos] = letter
        else:
            self.error = True
            self.reason = 'cannot place tile at previously occupied cell: ' + str(pos)

    def putWord(self, pos, word, direction):
        board = self.board
        if direction == 'h':
            # increment y ordinate
            y = pos[1]

            counter = 0
            length = len(word)
            while counter < length:
                ch = word[counter]
                y = y + 1
                loc = (pos[0], y)
                while board.getCell(loc).hasTile():
                    y = loc[1] = loc[1] + 1
                self.put(loc, ch)
                if self.error:
                    break
                counter = counter + 1
        else:
            # increment x ordinate
            x = pos[0]

            counter = 0
            length = len(word)
            while counter < length:
                ch = word[counter]
                x = x + 1
                loc = (x, pos[1])
                while board.getCell(loc).hasTile():
                    x = loc[0] = loc[0] + 1
                self.put(loc, ch)
                if self.error:
                    break
                counter = counter + 1
