from unittest import TestCase
from context import *
import pdb
import pprint

def write(l):
    w = open('debug.txt', 'a')
    w.write(str(l) + '\n')
    w.close()

def testWrap(tc, func):
    def execute(inp, expected, hasReturn=True):
        if hasReturn:
            actual = func(inp)
            tc.assertEqual(actual, expected, "fail: \n" + pprint.pformat(locals()))
        else:
            func(inp)

    return execute

class  TesteSequence(TestCase):

    def test_in_sequence_horizontal(self):
        inpSeq = [ (4,6), (4, 7), (4, 8) , (4, 9)]
        res = isValidSequence(inpSeq)
        self.assertIsNotNone(res)
        self.assertTrue(res['result'], "not a valid sequence")

    def test_out_sequence_horizontal(self):
        inpSeq = [ (4,6), (4, 7), (5, 8) , (4, 9)]
        res = isValidSequence(inpSeq)
        self.assertIsNotNone(res)
        self.assertFalse(res['result'], "not a valid sequence")

    def test_in_sequence_vertical(self):
        inpSeq = [ (5, 3), (6,3), (4,3), (2, 3), (3,3)]
        res = isValidSequence(inpSeq)
        self.assertIsNotNone(res)
        self.assertTrue(res['result'], "not a valid sequence")

    def test_out_sequence_vertical(self):
        inpSeq = [ (5, 3), (6,3), (4,4), (2, 3), (3,3)]
        res = isValidSequence(inpSeq)
        self.assertIsNotNone(res)
        self.assertFalse(res['result'], "not a valid sequence")

    def test_valid_sequence_gaps_vertical(self):
        inpSeq = [ (5, 3), (6,3), (2, 3), (3,3)]
        res = isValidSequence(inpSeq)
        self.assertIsNotNone(res)
        self.assertTrue(res['result'], "not a valid sequence")

    def test_valid_sequence_gaps_horizontal(self):
        inpSeq = [ (4,6), (4, 7), (4, 9) ]
        res = isValidSequence(inpSeq)
        self.assertIsNotNone(res)
        self.assertTrue(res['result'], "should be a valid sequence")
