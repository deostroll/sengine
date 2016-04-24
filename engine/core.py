
class Board:
    def __init__(self, size):
        self.cells = map(lambda x: Cell(x), range(size * size))
        self.virtual_cells = range(size * size)
        self.size = size

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
