from Interval import Interval
import numpy as np
from scipy.stats import chi2_contingency


def parseCSV(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            data.append(line.strip().split(','))
    return data


def getIntervals(data, index):
    ans = []
    sorted_data = sorted(data, key=lambda x: x[index])
    uniqe_value = [x[index] for x in sorted_data]
    for value in uniqe_value:
        countA = sum([1 for x in sorted_data if x[index]
                     == value and x[-1] == 'Iris-setosa'])
        countB = sum([1 for x in sorted_data if x[index] ==
                     value and x[-1] == 'Iris-versicolor'])
        countC = sum([1 for x in sorted_data if x[index] ==
                     value and x[-1] == 'Iris-virginica'])
        ans.append(Interval(value, value, countA, countB, countC))
    return ans


def chiMerge(intervals):
    # 创建函数来计算卡方值
    def get_chi_square(interval1, interval2):
        compareList = [[interval1.countA, interval1.countB, interval1.countC], [
            interval2.countA, interval2.countB, interval2.countC]]
        expected = [[0, 0, 0], [0, 0, 0]]
        sumOfRow = []
        sumOfCol = []
        for i in range(2):
            sumOfRow.append(sum(compareList[i]))
        for i in range(3):
            sumOfCol.append(sum([x[i] for x in compareList]))
        all = sum(sumOfRow)
        # 计算期望值
        for i in range(2):
            for j in range(3):
                expected[i][j] = sumOfRow[i] * sumOfCol[j] / all
        # 计算卡方值
        chi2_value = 0
        for i in range(2):
            for j in range(3):
                if expected[i][j] != 0:
                    chi2_value += (compareList[i][j] -
                                   expected[i][j]) ** 2 / expected[i][j]
        return chi2_value

    def merge_interval(interval1, interval2):
        interval1.end = interval2.end
        interval1.countA += interval2.countA
        interval1.countB += interval2.countB
        interval1.countC += interval2.countC

    # 循环合并区间直到达到停止条件
    while len(intervals) > 6:
        min_chi = float('inf')
        merge_indices = None
        for i in range(len(intervals) - 1):
            interval1 = intervals[i]
            interval2 = intervals[i + 1]
            chi = get_chi_square(interval1, interval2)
            if chi < min_chi:
                min_chi = chi
                merge_indices = (i, i+1)
        merge_interval(intervals[merge_indices[0]],
                       intervals[merge_indices[1]])
        del intervals[merge_indices[1]]

    # 返回结果
    return intervals


def outPutIntervals(intervals):
    for interval in intervals:
        print(interval.__str__())
    print("")


# 加载数据
data = parseCSV('iris.data')
for i in range(0, 4):
    intervals = []
    intervals = getIntervals(data, i)
    outPutIntervals(chiMerge(intervals))
