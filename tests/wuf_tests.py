from unittest import TestCase
from context import *
import pdb
import pprint

def testWrap(tc, func):
    def execute(inp, expected, hasReturn=True):
        if hasReturn:
            actual = func(inp)
            tc.assertEqual(actual, expected, "fail: \n" + pprint.pformat(locals()))
        else:
            func(inp)

    return execute

class WUFTests(TestCase):
    def test_wuf(self):
        arr = range(10)
        uf = WUF(arr)
        # taken from
        # https://www.cs.princeton.edu/~rs/AlgsDS07/01UnionFind.pdf
        def intify(s):
            a = list(s)
            return map(lambda x: int(x), a)

        uf.join(3,4)
        e = '0123356789'
        e = intify(e)
        self.assertSequenceEqual(e, uf.id)
        self.assertSequenceEqual(e, arr)

        uf.join(4,9)
        e = '0123356783'
        e = intify(e)
        self.assertSequenceEqual(e, uf.id)

        uf.join(8,0)
        e = '8123356783'
        e = intify(e)
        self.assertSequenceEqual(e, uf.id)

        uf.join(2,3)
        e = '8133356783'
        e = intify(e)
        self.assertSequenceEqual(e, uf.id)

        uf.join(5,6)
        e = '8133355783'
        e = intify(e)
        self.assertSequenceEqual(e, uf.id)

        uf.join(5, 9)
        e = '8133335783'
        e = intify(e)
        self.assertSequenceEqual(e, uf.id)

        uf.join(7,3)
        e = '8133335383'
        e = intify(e)
        self.assertSequenceEqual(e, uf.id)

        uf.join(4,8)
        e = '8133335333'
        e = intify(e)
        self.assertSequenceEqual(e, uf.id)

        uf.join(6,1)
        e = '8333335333'
        e = intify(e)
        self.assertSequenceEqual(e, uf.id)
