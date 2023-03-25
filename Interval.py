class Interval:
    def __init__(self, start, end, countA, countB, countC):
        self.start = start
        self.end = end
        self.countA = countA
        self.countB = countB
        self.countC = countC

    def __str__(self):
        return "Interval: [{}, {}]. Count: [{}, {}, {}]".format(self.start, self.end, self.countA, self.countB, self.countC)
