import random

import numpy as np

data1 = [[1,1],[1,8],[2,2],[2,5],[3,1],[4,3],[5,2],[6,1],[6,8],[8,6]]
data2 = [[1,1],[1,2],[1,5],[2,8],[3,7],[4,2],[7,5],[8,3],[8,7],[9,3]]
data3 = [[2,1],[2,4],[3,5],[3,6],[4,1],[4,9],[5,4],[5,6],[7,2],[9,8]]
data4 = [[1,4],[2,5],[2,8],[3,4],[3,5],[4,1],[4,7],[5,6],[7,6],[8,1]]
data0 = [data1, data2, data3, data4]


def custom_median(arr):
    sorted_arr = sorted(arr, key=lambda x: x[0])
    n = len(sorted_arr)
    if n % 2 == 1:
        return sorted_arr[n // 2]
    else:
        return sorted_arr[n // 2 - 1]


def compare_clusters(old, new):
    if len(old)==0 or len(new)==0:
        return False
    old1 = []
    for el in old:
        old1.append(sorted(el, key=lambda x: x[0]))
    new1 = []
    for el in new:
        new1.append(sorted(el, key=lambda x: x[0]))
    new1 = sorted(new1, key=lambda x: x[0])
    old1 = sorted(old1, key=lambda x: x[0])
    return old1 == new1

def kmedians(data, k):
    centers = []
    clusters = []
    while len(centers) < k:
        tmp_i = random.randint(0, len(data)-1)
        if data[tmp_i] not in centers:
            centers.append(data[tmp_i])
            clusters.append([data[tmp_i]])
    distances = []
    for i in range(len(data)):
        distances.append([])
        for j in range(len(data)):
            cur_dist = np.linalg.norm(np.array(data[i]) - np.array(data[j]))
            distances[i].append(cur_dist)
    for el in data:
        min_dist = np.inf
        min_i = -1
        for i in range(k):
            tmp = distances[data.index(centers[i])][data.index(el)]
            if min_dist > tmp:
                min_dist = tmp
                min_i = i
        clusters[min_i].append(el)


    old = clusters.copy()
    new = []
    while not compare_clusters(old, new):
        old = clusters.copy()
        centers = []
        clusters = [[] for i in range(k)]
        for cluster in old:
            cent = custom_median(cluster)
            centers.append(cent)
        for el in data:
            min_dist = np.inf
            min_i = -1
            for i in range(k):
                tmp = distances[data.index(list(centers[i]))][data.index(el)]
                if min_dist > tmp:
                    min_dist = tmp
                    min_i = i
            clusters[min_i].append(el)
        new = clusters.copy()
    new1 = []
    for el in new:
        new1.append(sorted(el, key=lambda x: x[0]))
    new1 = sorted(new1, key=lambda x: x[0])
    for el in new1:
        print(el)
    print("--------------------------------------")








for el in data0:
    kmedians(el, 3)