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
            return None   
        self.end.next = node
        self.end = node
        if self.curr_size > self.size:
            ret = self.front.val
            self.front.next.prev = None
            self.front = self.front.next
            self.curr_size -= 1
            return ret
        return None

    @property
    def is_full(self):
        return self.curr_size == self.size

    def reader(self):
        node = self.front
        while node:
            yield node.val
            node = node.next


class ContextBuffer:
    def __init__(self, string_reader, front_len, data_len, back_len):
        self.string_reader = string_reader
        self.front = BufferList(front_len)
        self.data = BufferList(data_len)
        self.back = BufferList(back_len)
        while not self.back.is_full:
            c = next(self.string_reader)
            val = self.back.add(c)
            
    def __iter__(self):
        return self
                
    def next(self):
        c = next(self.string_reader)
        curr_val = self.back.add(c)
        prev_val = self.data.add(curr_val)
        if prev_val:
            self.front.add(prev_val)
        return curr_val
    
    def __next__(self):
        return self.next()

    def __str__(self):
        return ''.join(self.front.reader()) + ' ' + ''.join(self.data.reader()) + ' ' + ''.join(self.back.reader())


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
        reader_ctx = ContextBuffer(string_reader, 2, len(self.pattern), 7)
        
        try:
            while True:
                char = next(reader_ctx)

                #Next character is not a match
                while match > 0 and self.pattern[match] != char:
                    match = self.prefix[match-1]
                #A character match has been found
                if self.pattern[match] == char:
                    match += 1
                #Motif found
                if match == len(self.pattern):
                    print(reader_ctx)
                    match = self.prefix[match-1]
            
        except StopIteration:
            pass