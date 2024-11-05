import sys
import inspect
import heapq, random

from numpy import sign


class Stack:
    def __init__(self):
        self.list = []
    def push(self, item):
        return self.list.append(item)
    def pop(self):
        return self.list.pop()
    def isEmpty(self):
        return len(self.list) == 0

class Queue:
    def __init__(self):
        self.list = []
    def push(self, item):
        self.list.insert(0,item)
    def pop(self):
        return self.list.pop()
    def isEmpty(self):
        return len(self.list) == 0

class PriorityQueue:
    def __init__(self):
        self.heap = []
    def push(self,item, priority):
        pair = (priority,item)
        heapq.heappush(self.heap,pair)
    def pop(self):
        (priority, item) = heapq.heappop(self.heap)
        return item
    def isEmpty(self):
        return len(self.heap) == 0

class PriorityQueueWithFunction(PriorityQueue):
    def __init__(self, priorityFunction):
        self.priorityFuncion = priorityFunction
        PriorityQueue.__init__(self)
    def push(self, item):
        PriorityQueue.push(self,item,self.priorityFuncion(item))

def mahattanDistance(xy1, xy2):
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

class Counter(dict):
    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)
    def incrementAll(self, keys, count):
        for key in keys:
            self[key] += count
    def argMax(self):
        if len(self.keys() == 0):
            return None
        all = self.items()
        values = [x[1] for x in all]
        maxIndex = values.index(max(values))
        return all[maxIndex][0]
    def sortedKeys(self):
        sortedItems = self.items()
        compare = lambda x,y : sign(y[1] - x[1])
        sortedItems.sort(cmp = compare)
        return  [x[0] for x in sortedItems]



