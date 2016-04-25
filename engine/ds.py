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

    def isConneced(self, p, q):
        return self.root(p) == self.root(q)

    def join(self, p, q):
        if self.isConneced(p, q):
            return

        rp = self.root(p)
        rq = self.root(q)

        if self.sz[rp] < self.sz[rq]:
            self.id[p] = rq
            self.sz[rq] = self.sz[rq] + self.sz[rp]
        else:
            self.id[q] = rp
            self.sz[rp] = self.sz[rp] + self.sz[rq] + 1
