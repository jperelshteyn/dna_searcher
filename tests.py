# -*- coding: utf-8 -*-

import unittest
from matchseq.matchseq import *

class TestBufferList(unittest.TestCase):

    def test(self):
        bl = BufferList(5)
        bl.add('1')
        bl.add('2')
        bl.add('3')
        bl.add('4')
        ret = bl.add('5')
        self.assertIsNone(ret, 'expected to get None while buffer is not full')
        self.assertTrue(bl.is_full, 'expected buffer to be full')
        ret = bl.add('6')
        self.assertEqual(ret, '1', "expected to get oldest element out of full buffer")


class TestContextBuffer(unittest.TestCase):

    def test(self):
        ctx = ContextBuffer(reader(STRING), 2, 2, 2)
        front, back = ctx.get_context()
        self.assertEqual(front, '', 'expected front context to be initially empty')
        self.assertEqual(back, STRING[:2], 'expected back context to fill up on initialization')
        c = next(ctx)
        self.assertEqual(c, STRING[0], 'expected to get the first char from string')
        next(ctx)
        next(ctx)
        front, _ = ctx.get_context()
        self.assertEqual(front, STRING[0], 'expected front context to have first char')

class TestContextedStringFinder(unittest.TestCase):

    def test(self):
        finder = ContextedStringFinder(PATTERN, u'ACGT', 5, 7)
        results = list(finder.findall(reader(STRING)))
        expected = [
            'A AGTA CGTGCAG',
            'CAGTG AGTA GTAGACC',
            'TGAGT AGTA GACCTGA',
            'ATATA AGTA GCTA',
        ]
        self.assertListEqual(results, expected, 'string finder results do not match expected')


STRING = 'AAGTACGTGCAGTGAGTAGTAGACCTGACGTAGACCGATATAAGTAGCTA'
PATTERN = 'AGTA'
def reader(string):
    for c in string:
        yield c


if __name__ == '__main__':
    unittest.main()