# -*- coding: utf-8 -*-

from collections import deque
import getopt
import sys
import codecs

class BufferList:
    def __init__(self, size):
        self.size = size
        self.curr_size = 0
        self._q = deque([])
        
    def add(self, val):
        self.curr_size += 1
        self._q.append(val)
        if self.curr_size > self.size:
            return self.pop()
        return None

    def pop(self):
        self.curr_size -= 1
        return self._q.popleft()

    @property
    def is_full(self):
        return self.size == self.curr_size

    def __iter__(self):
        return iter(self._q)


class ContextBuffer:
    def __init__(self, string_reader, left_len, target_len, right_len):
        self._reader = string_reader
        self._left = BufferList(left_len)
        self._target = BufferList(target_len)
        self._right = BufferList(right_len)
        self._fill_right()
                
    def _fill_right(self):
        while not self._right.is_full:
            try:
                c = next(self._reader)
                val = self._right.add(c)
            except StopIteration:
                break
    
    def next(self):
        curr_val = None
        try:
            c = next(self._reader)
            curr_val = self._right.add(c)
        except StopIteration as e:
            if self._right.curr_size == 0:
                 raise e
            curr_val = self._right.pop()
        passed_val = self._target.add(curr_val)
        if passed_val:
            self._left.add(passed_val)
        return curr_val
        
    def __next__(self):
        return self.next()

    def __iter__(self):
        return self

    def get_context(self):
        return ''.join(self._left), ''.join(self._right)


class ContextedStringFinder:
    def __init__(self, pattern, alphabet, left_ctx_len, right_ctx_len):
        self.pattern = pattern
        self.alphabet = alphabet
        self.left_ctx_len = left_ctx_len
        self.right_ctx_len = right_ctx_len

        self._prefix = []
        self.compute_prefix()

    def compute_prefix(self):
        self._prefix = [0] * len(self.pattern)
        k = 0
        for pos in range(1, len(self.pattern)):
            while k > 0 and self.pattern[k] != self.pattern[pos]:
                k = self._prefix[k]
            if self.pattern[k] == self.pattern[pos]:
                k += 1
            self._prefix[pos] = k

    def findall(self, string_reader):
        match = 0
        reader_w_ctx = ContextBuffer(string_reader, self.left_ctx_len, len(self.pattern), self.right_ctx_len)
        for char in reader_w_ctx:
            if char not in self.alphabet:
                raise RuntimeError('encountered character not in alphabet: {}'.format(char))
            while match > 0 and self.pattern[match] != char:
                match = self._prefix[match-1]
            if self.pattern[match] == char:
                match += 1
            if match == len(self.pattern):
                match = self._prefix[match-1]
                left, right = reader_w_ctx.get_context()
                yield "{} {} {}".format(left, self.pattern, right)


def parse_args(alphabet):
    args = {'-x': ':0', '-y': ':0'}
    optlist, _ = getopt.getopt(sys.argv[1:], 'T:x:y:')
    args.update(optlist)
    vars = {'-T': str, '-x': int, '-y': int}
    for a, t in vars.items():
        try:
            args[a] = t(args[a][1:])
        except (ValueError, KeyError):
            raise Exception('{} {} is required in the form of {}:val'.format(a, t, a))
    target = left_ctx_len = right_ctx_len = None
    target = args['-T']
    for c in target:
        if c not in alphabet:
            raise Exception('illegal character {} in target subsequence'.format(c))
    left_ctx_len = args['-x']
    right_ctx_len = args['-y']
    return target, left_ctx_len, right_ctx_len


def stdin_reader(stop_chars):
    sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    while True:
        c = sys.stdin.read(1)
        if c in stop_chars:
            break
        yield c


def main():
    alphabet = set(u'ACGT')
    stop_chars = set([u'ε', u'\n', u''])
    r = stdin_reader(stop_chars)
    target, left_ctx_len, right_ctx_len = parse_args(alphabet)
    finder = ContextedStringFinder(target, alphabet, left_ctx_len, right_ctx_len)
    for match in finder.findall(r):
        print(match)


if __name__ == "__main__":
    main()

# echo "AAGTACGTGCAGTGAGTAGTAGACCTGACGTAGACCGATATAAGTAGCTAε" | python main.py -T:AGTA -x:5 -y:7