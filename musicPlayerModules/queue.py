class Queue(object):
    def __init__(self):
        self.Queue = []

    def __str__(self):
        return str(self.Queue)

    def __repr__(self):
        return self.Queue
    
    def __len__(self):
        return len(self.Queue)

    def add(self, entry):
        self.Queue.append(entry)

    def popInsertFront(self, entry):
        self.Queue.pop(0)
        self.Queue.insert(0, entry)

    def popFront(self):
        return self.Queue.pop(0)

    def remove(self, data):
        self.Queue.remove(data)

    def isEmpty(self):
        if len(self.Queue) > 0:
            return False
        return True

    def getFront(self):
        return self.Queue[0]

    def getNext(self):
        try:
            return self.Queue[1]
        except:
            return None
        
    def get(self, pos):
        return self.Queue[pos]
    
    def empty(self):
        self.Queue = []