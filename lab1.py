import numpy as np

data = np.array([889, 500, 607, 1656, 265, 20, 122, 1568, 58,
                805, 1177, 248, 71, 75, 1248, 502, 817, 94,
                48, 542, 1088, 216, 1496, 149, 1982, 283,
                15, 226, 241, 545, 401, 499, 673, 373, 641,
                641, 174, 1230, 1190, 203, 206, 600, 677,
                130, 15, 118, 170, 726, 349, 564, 186, 1172,
                462, 521, 285, 553, 432, 1065, 917, 203,
                1056, 63, 445, 44, 311, 639, 680, 114, 356,
                318, 2223, 104, 83, 179, 1875, 241, 404, 0,
                252, 135, 1186, 1808, 1670, 835, 253, 67,
                40, 1125, 153, 16, 718, 623, 337, 165, 957,
                2, 197, 913, 473, 650])
MALFUNCTION_PERCENTAGE = 0.63
TIME_WITHOUT_BREAKDOWN = 680
MALFUNCTION_INTENSITY_TIME = 1468
N = len(data)

sorted_data = sorted(data)

mean_value = data.mean()

max_value = sorted_data[len(sorted_data) - 1]

k = 10
h = max_value / k

intervals = [round(interval * h, 2) for interval in range(k + 1)]


def data_sort_through_intervals(arr, intervals):
    data_intervals = [[] for _ in range(k)]
    for element in arr:
        for i in range(k):
            if intervals[i] <= element <= intervals[i+1]:
                data_intervals[i].append(element)
    return data_intervals


def f_calculator(data_intervals, k):
    F = [0 for _ in range(k)]
    for i in range(k):
        F[i] = len(data_intervals[i])/(N * h)
    return F


def find_the_interval(number, intervals):
    for i in range(k):
        if intervals[i] <= number <= intervals[i+1]:
            return i


def probabilities(frequency):
    P = [0 for _ in range(k)]
    for i in range(k):
        square = 0
        for j in range(i+1):
            square += (frequency[j] * h)
        P[i] = round(1 - square, 5)
    return P


def T(percentage, probability_arr, intervals):
    new_p_arr = probability_arr.copy()
    new_p_arr.insert(0, 1)
    for i in range(len(new_p_arr)):
        if new_p_arr[i] > percentage:
            new_p_arr.insert(i + 1, percentage)
    index = new_p_arr.index(percentage)
    d = round((new_p_arr[index+1] - percentage)/(new_p_arr[index+1] - new_p_arr[index-1]), 2)
    T_value = round(intervals[index] - h * d, 2)
    return T_value


def probability_for_time(time, frequency_arr, intervals):
    number_of_interval = find_the_interval(time, intervals)
    square = 0
    for i in range(number_of_interval + 1):
        if i != number_of_interval:
            square += (frequency_arr[i] * h)
        else:
            square += (frequency_arr[i] * (time - intervals[i]))
    p = round(1 - square, 4)
    return p


def intensity_for_time(time, frequency_arr, intervals):
    number_of_interval = find_the_interval(time, intervals)
    p = probability_for_time(time, frequency_arr, intervals)
    return round(frequency_arr[number_of_interval]/p, 4)


data_intervals = data_sort_through_intervals(sorted_data, intervals)
print("Intervals: \n", intervals)

f_array = f_calculator(data_intervals, k)

p_array = probabilities(f_array)

t_value = T(MALFUNCTION_PERCENTAGE, p_array, intervals)
print("Середній наробіток до відмови: ", t_value)

p = probability_for_time(TIME_WITHOUT_BREAKDOWN, f_array, intervals)
print("Ймовірність часу до відмови: " + str(TIME_WITHOUT_BREAKDOWN) + " год" + "\n", p)

intensity = intensity_for_time(MALFUNCTION_INTENSITY_TIME, f_array, intervals)
print("Інтенсивність для " + str(MALFUNCTION_INTENSITY_TIME) + " год" + "\n", intensity)
