import json

class Board:
    def __init__(self, size):

        f = open('data/bonus.json')
        tiles = json.load(f)
        self.size = size

        def createCell(x):
            c = Cell(x)
            x, y = self._get2d(x)
            sx = str(x)
            sy = str(y)
            try:
                b = tiles[sx][sy]
                c.bonus = b['type']
            except KeyError:
                pass
            return c

        self.cells = map(createCell, range(size * size))
        self.virtual_cells = range(size * size)
        self._place = {}

    def __len__(self):
        return len(self.cells)

    def _get2d(self, index):
        row = index / self.size
        col = index % self.size
        return row,col

    def _getIndex(self, tup):
        row, col = tup
        return row * self.size + col

    def getCell(self, arg):
        if type(arg) is tuple:
            #tuple type
            if not (type(arg[0]) is int and type(arg[1]) is int):
                raise ValueError('Tuple must contain integer indexes')
            index = self._getIndex(arg)
            return self.cells[index]
        elif type(arg) is int:
            return self.cells[arg]
        else:
            raise ValueError('Invalid argument passed into getCell call')

    def put(self, pos, tile):
        self._place[pos] = tile

    def getTile(self, pos):
        cell = self.getCell(pos)
        if cell.tile is None:
            if len(self._place) > 0:
                if type(pos) is tuple:
                    pos = self._getIndex(pos)
                return self._place[pos]
            else:
                return None

        return None


class Cell:
    def __init__(self, index):
        self.id = index
        self.value = ''
        self.bonus = ''
        self.tile = None

    def hasBonus(self):
        return self.bonus != ''

    def setTile(tile):
        self.tile = tile

class Tile:
    def __init__(self, letter, score):
        self.letter = letter
        self.score = score

class Rack:
    def __init__(self, size):
        self.size = size
        self.tiles = []

    def __repr__(self):
        return ''.join(map(lambda x: x.letter, self.tiles))
