class Min_Heap:

    def __init__(self, cap):
        self.cap = cap
        self.size = 0
        self.Heap = [0, 0]*(self.cap + 1)
        self.Heap[0] = [-1, -1]
        self.FRONT = 1

    # find parent from the position of the children

    def parent(self, pos):
        return pos//2

    # find position of the left child given the parent's position
    def leftChild(self, pos):
        return pos * 2

     # find position of the right child given the parent's position
    def rightChild(self, pos):
        return (pos * 2) + 1

    # Determine if the node at the position is a leaf node
    def is_leaf(self, pos):
        return (pos * 2) > self.size

    # Swap node
    def swap(self, fpos, spos):
        tmp = self.Heap[fpos]
        self.Heap[fpos] = self.Heap[spos]
        self.Heap[spos] = tmp

    def heapify(self, pos):

        if not self.is_leaf(pos):
            # check if a parent contains higher values than its children
            if (self.Heap[pos][0] > self.Heap[self.leftChild(pos)][0] or
               self.Heap[pos][0] > self.Heap[self.rightChild(pos)][0]):

                # Left swap case
                if self.Heap[self.leftChild(pos)][0] < self.Heap[self.rightChild(pos)][0]:
                    self.swap(pos, self.leftChild(pos))
                    self.heapify(self.leftChild(pos))
                # Right swap case
                else:
                    self.swap(pos, self.rightChild(pos))
                    self.heapify(self.rightChild(pos))

    # Insert function
    def insert(self, node):

        if self.size >= self.cap:
            return
        self.size = self.size + 1
        self.Heap[self.size] = node

        curr = self.size
        while self.Heap[curr][0] < self.Heap[self.parent(curr)][0]:
            self.swap(curr, self.parent(curr))
            curr = self.parent(curr)

    def print(self):
        for i in range(1, (self.size//2)+1):
            print(" parent : " + str(self.Heap[i])+" left baby => " +
                  str(self.Heap[2 * i])+" right baby => : " +
                  str(self.Heap[2 * i + 1]))
    # pop min index

    def pop(self):
        popped_val = self.Heap[self.FRONT][0]
        popped_index = self.Heap[self.FRONT][1]
        self.Heap[self.FRONT] = self.Heap[self.size]
        self.size = self.size - 1
        self.heapify(self.FRONT)
        return popped_val, popped_index