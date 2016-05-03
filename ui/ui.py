from engine import Game
from utils import strings

class ConsoleGameUI:
    def __init__(self):
        self.game = game = Game.getInstance();
        game.wireSink(self.onEvent, '_console_')

    def onEvent(self, evt, *args):
        if evt == Game.Events.READY:
            print 'cool'

    def runloop(self):
        self.game.start()
        self.game.waitForExit()

    def refresh(self):
        board = self.game.board
        result = ' \ '
        rng = range(15)
        result = result + ' '. join( map(lambda x: strings.pad(x, 2)) ) + '\n'
        for x in rng:
            result = result + strings.pad(x, 2) + ' '
            cells = board.cells[x]
            suffix = ' '.join( map(lambda x: ' ' + x.letter ))
            result = result + suffix


    def setPlayer(self, name, firstTurn=True):
        self.game.setupPlayer(name, firstTurn)

    def verify(self):
        pass

def main():

    # game = Game.getInstance()
    #
    # def event_handler(game, evt, *args):
    #     if evt == Game.Events.READY:
    #         print 'cool'
    #
    # game.wireSink(event_handler, 'ui')
    #
    # game.setupPlayer('deostroll') #sets up as first player

    cgame = ConsoleGameUI()

    cgame.setupPlayer('deostroll')

    cgame.runloop()

if __name__ == '__main__':
    main()
