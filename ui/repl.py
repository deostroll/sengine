def repl(game, console):

    while True:
        cmd = raw_input('> Command (type h for help): ').lower()

        op = cmd[0]

        if op == 'h':
            print help.text
        elif op == 'p':
            _, x, y, l = cmd.split(' ')
            x, y = int(x), int(y)
            game.put((x,y), l)
        elif op == 'c':
            game.clear()
        elif op == 'q':
            game.quit()
            break
        elif op == 'b':
            console.clear()
            console.showBonus()
        elif op == 'r':
            console.clear()
            console.refresh()
        elif op == 'w':
            tokens = cmd.split(' ')

            if len(tokens) == 4:
                _, x, y, word = tokens
                ori = 'h'
            else:
                _, x, y, word, ori = tokens

            x, y = int(x), int(y)
            game.putWord((x,y), word, ori)
