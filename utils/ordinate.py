
def convert(arg):
    if type(arg) is tuple:
        #convert to index
        x, y = arg
        return 15 * x + y
    elif type(arg) is int:
        r = arg / 15
        c  = arg % 15
        return (r, c)


if __name__ == '__main__':
    print convert((1,3))
    print convert(18)
    print convert((7,7))
