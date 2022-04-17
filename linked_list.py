### Doubly Linked List consists of a series of Node objects which hold song information


class Node:
    def __init__(self, data = None):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def append(self, data):
        if self.head == None:
            self.head = Node(data)
            self.tail = self.head
            self.count += 1
            return

        self.tail.next = Node(data)
        self.tail.next.prev = self.tail
        self.tail = self.tail.next
        self.count  += 1

    def get_count(self):
        return self.count

    def read_array(self, track_array):
        num_tracks = len(track_array)

        for i in range(0, num_tracks):
            self.append(track_array[i])

    def get_head(self):
        return self.head

    def get_tail(self):
        return self.tail

    def get_forward_array(self):
        arr = []

        temp = self.head
        while temp != None:
            arr.append(temp.data)
            temp = temp.next

        return arr

    def get_backward_array(self):
        arr = []

        temp = self.tail
        while temp != None:
            arr.append(temp.data)
            temp = temp.prev

        return arr

    def print_forward(self):
        temp = self.head
        while temp != None:
            print(temp.data)
            temp = temp.next

    def print_backward(self):
        temp = self.tail
        while temp != None:
            print(temp.data)
            temp = temp.prev
