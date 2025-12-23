import pandas as pd
import time
import IN450_Unit7_Stephen_Brock_sortingAlgorithm as s

data = pd.read_excel('IN450_Unit7_Stephen_Brock_datasource.xlsx', usecols=('B'), header=None, skiprows=1, nrows=10)
data10 = data.to_numpy()

data10_arr = []
for i in data10:
    data10_arr.append(float(i[0]))

data = pd.read_excel('IN450_Unit7_Stephen_Brock_datasource.xlsx', usecols=('B'), header=None, skiprows=1, nrows=1000)
data1000 = data.to_numpy()

data1000_arr = []
for i in data1000:
    data1000_arr.append(float(i[0]))

data = pd.read_excel('IN450_Unit7_Stephen_Brock_datasource.xlsx', usecols=('B'), header=None, skiprows=1, nrows=10000)
data10_000 = data.to_numpy()

data10_000_arr = []
for i in data10_000:
    data10_000_arr.append(float(i[0]))

def selection_sort_comparison(array):
    size = len(array)
    start = time.time()
    s.selectionSort(array, size)
    end = time.time()
    elapsed_time = end - start
    return elapsed_time

def merge_sort_comparison(array):
    size = len(array)
    start = time.time()
    s.mergeSort(array, 0, size - 1)
    end = time.time()
    elapsed_time = end - start
    return elapsed_time

selection_time = selection_sort_comparison(data10_arr)
merge_time = merge_sort_comparison(data10_arr)

print('\nDataset of 10 values')
print(f'Selection Sort time is {(selection_time * 1000):.8f} miliseconds.')
print(f'Merge Sort time is {(merge_time * 1000):.8f} miliseconds.')

selection_time = selection_sort_comparison(data1000_arr)
merge_time = merge_sort_comparison(data1000_arr)

print('\nDataset of 1,000 values')
print(f'Selection Sort time is {(selection_time * 1000):.8f} miliseconds.')
print(f'Merge Sort time is {(merge_time * 1000):.8f} miliseconds.')

selection_time = selection_sort_comparison(data10_000_arr)
merge_time = merge_sort_comparison(data10_000_arr)

print('\nDataset of 10,000 values')
print(f'Selection Sort time is {(selection_time * 1000):.8f} miliseconds.')
print(f'Merge Sort time is {(merge_time * 1000):.8f} miliseconds.')