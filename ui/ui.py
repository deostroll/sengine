from engine import Game, Events
from utils import strings, help, tty
from repl import repl

class ConsoleGameUI:
    def __init__(self):
        self.game = game = Game.getInstance();
        game.wireSink(self.onEvent, '_console_')

    def onEvent(self, evt, *args):
        # print 'evt:'        , evt
        if evt == Events.READY:
            self.clear()
            self.printBoard()
            repl(self.game, self)
        elif evt == Events.ERROR:
            print '> Error: ', self.reason
            raw_input('> Press enter to continue...')
            self.game.resetError()
        elif evt == Events.PUT:
            # print args
            self.clear()
            self.printBoard()
            opt = args[1]
            if opt == 'p':
                _, __, pos, tile = args
                print '> put letter: ' + str(tile) + ' at position: ' + str(pos) + ' success...'
            elif opt == 'w':
                _, __, pos, word, direction = args
                print '> put word: ' + word + ' at position: ' + str(pos) + ' dir: ' + direction +  ' success...'

        elif evt == Events.CLEAR:
            self.clear()
            self.printBoard()
            print '> game cleared...'




    def runloop(self):
        self.game.start()
        self.game.waitForExit()

    def printBoard(self):
        game = self.game
        board = self.game.board
        q = self.game.q
        # tty.clear()
        result = ' \ '
        rng = range(15)
        result = result + ' '. join( map(lambda x: strings.pad(x, 2), rng) ) + '\n'
        # _, c = getTerminalSize()
        # for x in range(c) : print ''
        def getCell(cell):
            _2dpos = board._get2d(cell.id)

            if cell.hasTile():
                return cell.letter
            elif _2dpos in q.keys():
                tile = q[_2dpos]
                if tile.isBlank():
                    return tile.sub_letter
                return tile.letter
            elif cell.hasBonus():
                bonus = cell.bonus
                if bonus == 'TW' : ch =  '='
                if bonus == 'DW' : ch = '+'
                if bonus == 'TL' : ch = ':'
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
        print ''
        print 'Rack:', game.current.rack
        print '> board and rack printed...'


    def setPlayer(self, name):
        self.game.setupPlayer(name)

    def showBonus(self):
        # tty.clear()
        rng = range(15)
        board = self.game.board
        result = ' \ '
        result = result + ' '. join( map(lambda x: strings.pad(x, 2), rng) ) + '\n'
        def printBonus(cell):
            if cell.hasBonus():
                bonus = cell.bonus
                if bonus == 'TW' : ch =  '='
                if bonus == 'DW' : ch = '+'
                if bonus == 'TL' : ch = ':'
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

            suffix = ' '.join( map(lambda x: strings.pad(printBonus(x), 2), cells) )
            result = result + suffix + '\n'

        print result
        print ''
        print '> bonus cells printed...'
    def clear(self):
        tty.clear()



def main():

    cgame = ConsoleGameUI()

    cgame.setPlayer('deostroll')

    cgame.runloop()

    print 'End'

def getTerminalSize():
    import os
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

        ### Use get(key[, default]) instead of a try/catch
        #try:
        #    cr = (env['LINES'], env['COLUMNS'])
        #except:
        #    cr = (25, 80)
    return int(cr[1]), int(cr[0])

if __name__ == '__main__':
    main()
