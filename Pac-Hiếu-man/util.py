import sys
import inspect
import heapq, random
import signal
from numpy import sign

class Stack:
    def __init__(self):
        self.list = []

    def push(self, item):
        self.list.append(item)

    def pop(self):
        return self.list.pop()

    def isEmpty(self):
        return len(self.list) == 0


class Queue:
    def __init__(self):
        self.list = []

    def push(self, item):
        self.list.insert(0, item)

    def pop(self):
        return self.list.pop()

    def isEmpty(self):
        return len(self.list) == 0


class PriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, item, priority):
        pair = (priority, item)
        heapq.heappush(self.heap, pair)

    def pop(self):
        (priority, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0


class PriorityQueueWithFunction(PriorityQueue):
    def __init__(self, priorityFunction):
        self.priorityFunction = priorityFunction
        super().__init__()

    def push(self, item):
        super().push(item, self.priorityFunction(item))


def manhattanDistance(xy1, xy2):
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


class Counter(dict):
    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)

    def incrementAll(self, keys, count):
        for key in keys:
            self[key] += count

    def argMax(self):
        if len(self) == 0:
            return None
        return max(self.items(), key=lambda x: x[1])[0]

    def sortedKeys(self):
        sortedItems = sorted(self.items(), key=lambda x: -x[1])
        return [x[0] for x in sortedItems]

    def totalCount(self):
        return sum(self.values())

    def normalize(self):
        total = float(self.totalCount())
        if total == 0:
            return
        for key in self.keys():
            self[key] = self[key] / total

    def divideAll(self, divisor):
        divisor = float(divisor)
        for key in self:
            self[key] /= divisor

    def copy(self):
        return Counter(super().copy())

    def __mul__(self, y):
        sum = 0
        x = self
        if len(x) > len(y):
            x, y = y, x
        for key in x:
            if key not in y:
                continue
            sum += x[key] * y[key]
        return sum

    def __radd__(self, y):
        for key, value in y.items():
            self[key] += value

    def __add__(self, y):
        addend = Counter()
        for key in self:
            addend[key] = self[key] + y.get(key, 0)
        for key in y:
            if key not in self:
                addend[key] = y[key]
        return addend

    def __sub__(self, y):
        addend = Counter()
        for key in self:
            addend[key] = self[key] - y.get(key, 0)
        for key in y:
            if key not in self:
                addend[key] = -y[key]
        return addend


def raiseNotDefined():
    print("Method not implemented: %s" % inspect.stack()[1][3])
    sys.exit(1)


def normalize(vectorOrCounter):
    normalizedCounter = Counter()
    if isinstance(vectorOrCounter, Counter):
        counter = vectorOrCounter
        total = float(counter.totalCount())
        if total == 0:
            return counter
        for key in counter.keys():
            value = counter[key]
            normalizedCounter[key] = value / total
        return normalizedCounter
    else:
        vector = vectorOrCounter
        s = float(sum(vector))
        if s == 0:
            return vector
        return [el / s for el in vector]


def nSample(distribution, values, n):
    if sum(distribution) != 1:
        distribution = normalize(distribution)
    rand = [random.random() for _ in range(n)]
    rand.sort()
    samples = []
    samplePos, distPos, cdf = 0, 0, distribution[0]
    while samplePos < n:
        if rand[samplePos] < cdf:
            samples.append(values[distPos])
            samplePos += 1
        else:
            distPos += 1
            cdf += distribution[distPos]
    return samples


def sample(distribution, values=None):
    if isinstance(distribution, Counter):
        items = list(distribution.items())
        distribution = [i[1] for i in items]
        values = [i[0] for i in items]
    if sum(distribution) != 1:
        distribution = normalize(distribution)
    choice = random.random()
    i, total = 0, distribution[0]
    while choice > total:
        i += 1
        total += distribution[i]
    return values[i]


def sampleFromCounter(ctr):
    items = list(ctr.items())
    return sample([v for k, v in items], [k for k, v in items])


def getProbability(value, distribution, values):
    total = 0.0
    for prob, val in zip(distribution, values):
        if val == value:
            total += prob
    return total


def flipCoin(p):
    return random.random() < p


def chooseFromDistribution(distribution):
    if isinstance(distribution, (dict, Counter)):
        return sample(distribution)
    r = random.random()
    base = 0.0
    for prob, element in distribution:
        base += prob
        if r <= base:
            return element


def nearestPoint(pos):
    (current_row, current_col) = pos
    grid_row = int(current_row + 0.5)
    grid_col = int(current_col + 0.5)
    return (grid_row, grid_col)


def sign(x):
    return 1 if x >= 0 else -1


def arrayInvert(array):
    result = [[] for _ in array]
    for outer in array:
        for inner in range(len(outer)):
            result[inner].append(outer[inner])
    return result


def matrixAsList(matrix, value=True):
    rows, cols = len(matrix), len(matrix[0])
    cells = []
    for row in range(rows):
        for col in range(cols):
            if matrix[row][col] == value:
                cells.append((row, col))
    return cells


def lookup(name, namespace):
    dots = name.count('.')
    if dots > 0:
        moduleName, objName = '.'.join(name.split('.')[:-1]), name.split('.')[-1]
        module = __import__(moduleName)
        return getattr(module, objName)
    else:
        modules = [obj for obj in namespace.values() if isinstance(obj, type(sys))]
        options = [getattr(module, name) for module in modules if hasattr(module, name)]
        options += [obj[1] for obj in namespace.items() if obj[0] == name]
        if len(options) == 1:
            return options[0]
        if len(options) > 1:
            raise Exception('Name conflict for %s' % name)
        raise Exception('%s not found as a method or class' % name)


def pause():
    input("<Press enter/return to continue>")


class TimeoutFunctionException(Exception):
    pass


class TimeoutFunction:
    def __init__(self, function, timeout):
        self.timeout = timeout
        self.function = function

    def handle_timeout(self, signum, frame):
        raise TimeoutFunctionException()

    def __call__(self, *args):
        if not hasattr(signal, 'SIGALRM'):
            return self.function(*args)
        old = signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.timeout)
        try:
            result = self.function(*args)
        finally:
            signal.signal(signal.SIGALRM, old)
        signal.alarm(0)
        return result


