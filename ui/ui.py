from engine import Game

game = Game.getInstance()

def event_handler(game, evt, *args):
    if evt == Game.Events.READY:
        print 'cool'

game.wireSink(event_handler, 'ui')

game.setupPlayer('deostroll') #sets up as first player
