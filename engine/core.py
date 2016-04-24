import json

class Board:
    def __init__(self, size):

        f = open('data/tiles.json')
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

class Cell:
    def __init__(self, index):
        self.id = index
        self.value = ''
        self.bonus = ''

    def hasBonus(self):
        return self.bonus != ''
