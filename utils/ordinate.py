
def convert(arg):
    if type(arg) is tuple:
        #convert to index
        x, y = arg
        return 15 * x + y
    elif type(arg) is int:
        r = arg / 15
        c  = arg % 15
        return (r, c)

def ok(arg):
    if type(arg) is tuple:
        x, y = arg
        return x > 0 and x < 15 and y > 0 and y < 15
    elif type(arg) is int:
        return arg < 15 * 15
if __name__ == '__main__':
    print convert((1,3))
    print convert(18)
    print convert((7,7))
