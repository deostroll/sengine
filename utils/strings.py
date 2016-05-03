
def pad(num, width, ch = ' '):
    snum = str(num)
    spaces = ch * width
    result = spaces + snum
    return result[-width:]
