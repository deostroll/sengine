from operator import itemgetter

class WUF:
    def __init__(self, array):
        self.id = array
        self.size = len(array)
        self.sz = map(lambda x: 1, range(self.size))

    def root(self, i):
        id = self.id
        while id[i] != i:
            i = id[i]
        return i

    def isConnected(self, p, q):
        return self.root(p) == self.root(q)

    def join(self, p, q):
        if self.isConnected(p, q):
            return

        rp = self.root(p)
        rq = self.root(q)

        if self.sz[rp] < self.sz[rq]:
            self.id[p] = rq
            self.sz[rq] = self.sz[rq] + self.sz[rp]
        else:
            self.id[q] = rp
            self.sz[rp] = self.sz[rp] + self.sz[rq] + 1

def isValidSequence(seq):
    assert len(seq) > 1

    # sorting with x-ordinate then y-ordinate
    sortedSeq = sorted(seq, key=itemgetter(0,1))

    xSame = sortedSeq[0][0] == sortedSeq[1][0]
    dir = 'invalid'
    if xSame:
        test_val = sortedSeq[0][0]
        res = all(map(lambda x: x[0] == test_val, sortedSeq))
        dir = 'horizontal'
    else:
        test_val = sortedSeq[0][1]
        res = all(map(lambda x: x[1] == test_val,sortedSeq))
        dir = 'vertical'

    return { 'result': res, 'direction': dir }
