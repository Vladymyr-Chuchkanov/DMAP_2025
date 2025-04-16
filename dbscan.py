import numpy as np

data1 = [[1,1],[1,8],[2,2],[2,5],[3,1],[4,3],[5,2],[6,1],[6,8],[8,6]]
data2 = [[1,1],[1,2],[1,5],[2,8],[3,7],[4,2],[7,5],[8,3],[8,7],[9,3]]
data3 = [[2,1],[2,4],[3,5],[3,6],[4,1],[4,9],[5,4],[5,6],[7,2],[9,8]]
data4 = [[1,4],[2,5],[2,8],[3,4],[3,5],[4,1],[4,7],[5,6],[7,6],[8,1]]
data0 = [data1, data2, data3, data4]


def recurrent_check(point, data, belongs_to_cluster, eps, min_pts, cluster):
    tmp = []
    for el in data:
        if el != point:
            cur_dist = np.linalg.norm(np.array(el) - np.array(point))
            if cur_dist <= eps:
                tmp.append(el)
    if not belongs_to_cluster and len(tmp) >= min_pts:
        cluster = tmp.copy()
        cluster.append(point)
        for el in tmp:
            cluster = (recurrent_check(el, data, True, eps, min_pts, cluster))
    elif len(tmp) >= min_pts:
        for el in tmp:
            if el not in cluster:
                cluster.append(el)
                cluster = (recurrent_check(el, data, True, eps, min_pts, cluster))
    return cluster


def dbscan(data, eps, min_pts):
    clusters = []
    for el in data:
        cluster = recurrent_check(el, data, False, eps, min_pts, [])
        if len(cluster) > 0:
            clusters.append(cluster)
        print(el,end=" : ")
        print(cluster)
    #print(clusters)

    print("---------------------------------------")






for el in data0:
    dbscan(el, 2.5, 2)