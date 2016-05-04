from engine import Game
from utils import strings

class ConsoleGameUI:
    def __init__(self):
        self.game = game = Game.getInstance();
        game.wireSink(self.onEvent, '_console_')

    def onEvent(self, evt, *args):
        if evt == Game.Events.READY:
            self.refresh()
            args(0).quit()

    def runloop(self):
        self.game.start()
        self.game.waitForExit()

    def refresh(self):
        board = self.game.board
        result = ' \ '
        rng = range(15)
        result = result + ' '. join( map(lambda x: strings.pad(x, 2)) ) + '\n'

        def getCell(cell):
            if cell.hasTile():
                return cell.letter
            elif cell.hasBonus():
                bonus = cell.bonus
                if bonus == 'TW' : ch =  '='
                if bonus == 'DW' : ch = '+'
                if bonus == 'TL' : ch = '\''
                if bonus == 'DL' : ch = '-'
                if bonus == 'ST' : ch = '*'
                return ch
            else:
                return ' '

        for x in rng:
            result = result + strings.pad(x, 2) + ' '
            cells = board.cells[x]
            suffix = ' '.join( map(lambda x: strings.pad(getCell(x), 2), cells) )
            result = result + suffix + '\n'

        print result


    def setPlayer(self, name, firstTurn=True):
        self.game.setupPlayer(name, firstTurn)

    def verify(self):
        pass

def main():

    cgame = ConsoleGameUI()

    cgame.setupPlayer('deostroll')

    cgame.runloop()

    print 'End'

if __name__ == '__main__':
    main()
