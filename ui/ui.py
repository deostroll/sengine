from engine import Game

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
        pass

    def setPlayer(self, name, firstTurn=True):
        self.game.setupPlayer(name, firstTurn)

def main():

    game = Game.getInstance()

    def event_handler(game, evt, *args):
        if evt == Game.Events.READY:
            print 'cool'

    game.wireSink(event_handler, 'ui')

    game.setupPlayer('deostroll') #sets up as first player

if __name__ == '__main__':
    main()
