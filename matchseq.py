class BufferNode:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None

        
class BufferList:
    def __init__(self, size):
        self.size = size
        self.curr_size = 0
        self.front = None
        self.end = None
        
    def add(self, val):
        self.curr_size += 1
        node = BufferNode(val)
        node.prev = self.end
        if self.curr_size == 1:
            self.end = node
            self.front = node
            return        
        self.end.next = node
        self.end = node
        if self.curr_size > self.size:
            self.front.next.prev = None
            self.front = self.front.next
            self.curr_size -= 1

    def reader(self):
        node = self.front
        while node:
            yield node.val
            node = node.next
        

class ContextBuffer:
    def __init__(self, string_reader, x, y):
        self.string_reader = string_reader
        self.x = x
        self.y = y
        
    def __next__(self)
        
class KmpMatcher(object):
    def __init__(self, pattern, x, y):
        self.pattern = pattern.upper()
        self.prefix = []
        self.computePrefix()
        self.x = x
        self.y = y

    #Matches the motif pattern against itself.
    def computePrefix(self):
        #Initialize prefix array
        self.prefix = [0] * len(self.pattern)
        k = 0

        for pos in range(1, len(self.pattern)):
            #Unique base in motif
            while(k > 0 and self.pattern[k] != self.pattern[pos]):
                k = self.prefix[k]
            #repeat in motif
            if(self.pattern[k] == self.pattern[pos]):
                k += 1

            self.prefix[pos] = k

    #An implementation of the Knuth-Morris-Pratt algorithm for linear time string matching
    def kmpSearch(self, string_reader):
        #Number of characters matched
        match = 0
        pos = 0
        
        try:
            while True:
                char = next(string_reader)

                #Next character is not a match
                while match > 0 and self.pattern[match] != char:
                    match = self.prefix[match-1]
                #A character match has been found
                if self.pattern[match] == char:
                    match += 1
                #Motif found
                if match == len(self.pattern):
                    yield self.pattern
                    print("Match found at position: " + str(pos-match+2) + ':' + str(pos+1))
                    match = self.prefix[match-1]
                pos += 1
            
        except StopIteration:
            pass