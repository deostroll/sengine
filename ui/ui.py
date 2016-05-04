from engine import Game, Events
from utils import strings

def repl(game):
    pass

class ConsoleGameUI:
    def __init__(self):
        self.game = game = Game.getInstance();
        game.wireSink(self.onEvent, '_console_')

    def onEvent(self, evt, *args):
        # print 'evt:'        , evt
        if evt == Events.READY:
            self.refresh()
            self.game.quit()

    def runloop(self):
        self.game.start()
        self.game.waitForExit()

    def refresh(self):
        board = self.game.board
        result = ' \ '
        rng = range(15)
        result = result + ' '. join( map(lambda x: strings.pad(x, 2), rng) ) + '\n'

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
            cells = []

            for y in range(board.size):
                cells.append(board.getCell((x, y)))

            suffix = ' '.join( map(lambda x: strings.pad(getCell(x), 2), cells) )
            result = result + suffix + '\n'

        print result


    def setPlayer(self, name):
        self.game.setupPlayer(name)

    def verify(self):
        pass

def main():

    cgame = ConsoleGameUI()

    cgame.setPlayer('deostroll')

    cgame.runloop()

    print 'End'

if __name__ == '__main__':
    main()
