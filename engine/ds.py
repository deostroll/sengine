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

def check(seq):
    assert len(seq) > 1

    if ordinatesInRow(seq):
        _, noGaps, gaps = gapCheck(seq)
        if noGaps:
            return True, True, True, None
        else:
            return True, True, False, gaps
    elif ordinatesInColumn(seq):
        _, noGaps, gaps = gapCheck(seq, False)
        if noGaps:
            return True, False, True, None
        else:
            return True, False, False, gaps
    else:
        return False, None, None, None

def ordinatesInRow(seq):
    test_val = seq[0][0]
    return all( map(lambda x: x[0] == test_val, seq) )

def ordinatesInColumn(seq):
    test_val = seq[0][1]
    return all( map(lambda x: x[1] == test_val, seq) )

def gapCheck(seq, horizontal=True):
    if horizontal:
        selector = lambda x: x[1]
        actualRange = sorted(map(selector, seq))
        low, high = min(actualRange), max(actualRange)
        expectedRange = range(low, high + 1)
        if actualRange != expectedRange:
            lengthHigh = len(expectedRange)
            lengthLow = len(actualRange)
            assert lengthLow < lengthHigh
            missing = filter(lambda x: x not in actualRange, expectedRange)
            return True, False, missing
        else:
            return (True, True, None)
    else:
        selector = lambda x: x[0]
        actualRange = sorted(map(selector, seq))
        low, high = min(actualRange), max(actualRange)
        expectedRange = range(low, high + 1)
        if actualRange != expectedRange:
            lengthHigh = len(expectedRange)
            lengthLow = len(actualRange)
            assert lengthLow < lengthHigh
            missing = filter(lambda x: x not in actualRange, expectedRange)
            return False, False, missing
        else:
            return False, True, None
