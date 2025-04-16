import random

import numpy as np

data1 = [[1,1],[1,8],[2,2],[2,5],[3,1],[4,3],[5,2],[6,1],[6,8],[8,6]]
data2 = [[1,1],[1,2],[1,5],[2,8],[3,7],[4,2],[7,5],[8,3],[8,7],[9,3]]
data3 = [[2,1],[2,4],[3,5],[3,6],[4,1],[4,9],[5,4],[5,6],[7,2],[9,8]]
data4 = [[1,4],[2,5],[2,8],[3,4],[3,5],[4,1],[4,7],[5,6],[7,6],[8,1]]
data0 = [data1, data2, data3, data4]


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

def kmeans(data, k):
    centers = []
    clusters = []
    while len(centers) < k:
        tmp_i = random.randint(0, len(data)-1)
        if data[tmp_i] not in centers:
            centers.append(data[tmp_i])
            clusters.append([data[tmp_i]])
    for el in data:
        if el not in centers:
            min_dist = np.inf
            min_i = -1
            for i in range(k):
                cur_dist = np.linalg.norm(np.array(centers[i]) - np.array(el))
                if cur_dist < min_dist:
                    min_dist = cur_dist
                    min_i = i
            clusters[min_i].append(el)
        else:
            clusters[centers.index(el)].append(el)
    # print(clusters)
    old = clusters.copy()
    new = []
    while not compare_clusters(old, new):
        old = clusters.copy()
        centers = []
        clusters = [[] for i in range(k)]
        for cluster in old:
            center_of_mass = [sum(coords) / len(coords) for coords in zip(*cluster)]
            centers.append(center_of_mass)
        for el in data:
            min_dist = np.inf
            min_i = -1
            for i in range(k):
                cur_dist = np.linalg.norm(np.array(centers[i]) - np.array(el))
                if cur_dist < min_dist:
                    min_dist = cur_dist
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
    kmeans(el, 3)