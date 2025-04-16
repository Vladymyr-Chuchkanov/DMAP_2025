from abc import ABC,abstractmethod
import numpy as np

#          0     1     2     3     4     5     6     7     8     9
data1 = [[1,1],[1,8],[2,2],[2,5],[3,1],[4,3],[5,2],[6,1],[6,8],[8,6]]
data2 = [[1,1],[1,2],[1,5],[2,8],[3,7],[4,2],[7,5],[8,3],[8,7],[9,3]]
data3 = [[2,1],[2,4],[3,5],[3,6],[4,1],[4,9],[5,4],[5,6],[7,2],[9,8]]
data4 = [[1,4],[2,5],[2,8],[3,4],[3,5],[4,1],[4,7],[5,6],[7,6],[8,1]]
data0 = [data1, data2, data3, data4]


class ClusterMergeStrategy(ABC):
    @abstractmethod
    def compute_distance(self, cluster1, cluster2):
        pass


class SingleLinkage(ClusterMergeStrategy):
    def compute_distance(self, cluster1, cluster2):
        min_dist = np.inf
        for x in cluster1:
            for y in cluster2:
                dist = np.linalg.norm(np.array(x)-np.array(y))
                if dist < min_dist:
                    min_dist = dist
        return  min_dist


class CompleteLinkage(ClusterMergeStrategy):
    def compute_distance(self, cluster1, cluster2):
        max_dist = -np.inf
        for x in cluster1:
            for y in cluster2:
                dist = np.linalg.norm(np.array(x)-np.array(y))
                if dist > max_dist:
                    max_dist = dist
        return max_dist


class AverageLinkage(ClusterMergeStrategy):
    def compute_distance(self, cluster1, cluster2):
        total = 0.0
        for x in cluster1:
            for y in cluster2:
                total += np.linalg.norm(np.array(x)-np.array(y))
        return total / (len(cluster1) * len(cluster2))


class CentroidLink(ClusterMergeStrategy):
    def compute_distance(self, cluster1, cluster2):
        centroid1 = np.mean(cluster1, axis=0)
        centroid2 = np.mean(cluster2, axis=0)
        return np.linalg.norm(centroid1 - centroid2)


class MedianLinkage(ClusterMergeStrategy):
    def compute_distance(self, cluster1, cluster2):
        median1 = np.median(cluster1, axis=0)
        median2 = np.median(cluster2, axis=0)
        return np.linalg.norm(median1 - median2)


class WardsLinkage(ClusterMergeStrategy):
    def compute_distance(self, cluster1, cluster2):
        combined = np.vstack([cluster1, cluster2])
        centroid_combined = np.mean(combined, axis=0)
        ss_combined = np.sum((combined - centroid_combined) ** 2)
        ss1 = np.sum((cluster1 - np.mean(cluster1, axis=0)) ** 2) if len(cluster1) > 0 else 0
        ss2 = np.sum((cluster2 - np.mean(cluster2, axis=0)) ** 2) if len(cluster2) > 0 else 0
        delta = ss_combined - (ss1 + ss2)
        return delta if delta > 0 else 0


class HierarchicalClustering:
    def __init__(self, strategy: ClusterMergeStrategy):
        self.strategy = strategy

    def fit(self, data: np.ndarray):
        history = []
        n = len(data)
        clusters = [[i] for i in range(n)]
        distances = np.full((n, n), np.inf)
        history.append(clusters)
        for i in range(n):
            for j in range(i + 1, n):
                distances[i, j] = self.strategy.compute_distance([data[i]], [data[j]])

        while len(clusters) > 1:
            i, j = np.unravel_index(np.argmin(distances), distances.shape)
            merged_cluster = clusters[i] + clusters[j]
            new_clusters = [clusters[k] for k in range(len(clusters)) if k not in (i, j)]
            new_clusters.append(merged_cluster)
            new_size = len(new_clusters)
            new_distances = np.full((new_size, new_size), np.inf)
            for k in range(new_size - 1):
                points_k = [data[p] for p in new_clusters[k]]
                points_merged = [data[p] for p in merged_cluster]
                dist = self.strategy.compute_distance(points_k, points_merged)
                new_distances[k, -1] = dist
            for k in range(new_size - 1):
                for m in range(k + 1, new_size - 1):
                    orig_k = clusters.index(new_clusters[k])
                    orig_m = clusters.index(new_clusters[m])
                    new_distances[k, m] = distances[min(orig_k, orig_m), max(orig_k, orig_m)]
            clusters = new_clusters
            history.append(clusters)
            distances = new_distances

        return history


def print_dendrogram(clusters):
    reversed_clusters = clusters[::-1]
    for i in range(len(reversed_clusters)):
        tmp = reversed_clusters[i]
        tmp2 = []
        for el in tmp:
            tmp_el = el
            tmp_el.sort()
            tmp2.append(tmp_el)

        tmp = sorted(tmp2, key=lambda x: x[0])
        print(tmp)


def clustering(data):
    strats = [SingleLinkage(), CompleteLinkage(), AverageLinkage(), CompleteLinkage(), MedianLinkage(), WardsLinkage()]
    for strat in strats:
        hc = HierarchicalClustering(strat)
        hist = hc.fit(data)
        print(strat)
        print_dendrogram(hist)


for el in data0:
    clustering(el)
