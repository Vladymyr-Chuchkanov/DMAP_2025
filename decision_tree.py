import copy
import math

data1 = [[0,1,2,1], [1,0,1,1], [0,1,1,0], [0,0,1,1], [0,0,2,1], [1,1,2,0], [1,0,2,1],
[1,0,0,0], [0,0,0,0], [0,0,1,1]]
test1 = [1,1,1]

data2 = [[0,1,2,1], [1,0,1,0], [0,1,1,1], [0,0,1,1], [0,0,2,1], [1,1,2,1], [1,0,2,0],
[1,0,0,1], [0,0,0,0], [0,0,1,0]]
test2 = [1,1,1]

data3 = [[0,1,2,0], [1,0,1,0], [0,1,1,0], [0,0,1,0], [0,0,2,1], [1,1,2,1], [1,0,2,1],
[1,0,0,1], [0,0,0,0], [0,0,1,1]]
test3 = [1,1,1]

data4 = [[0,1,2,0], [1,0,1,1], [0,1,1,0], [0,0,1,1], [0,0,2,0], [1,1,2,1], [1,0,2,1],
[1,0,0,1], [0,0,0,0], [0,0,1,1]]
test4 = [1,1,1]

data_variants = [data1,data2,data3,data4]
test_variants = [test1, test2, test3, test4]


def entropy(class_counts):
    total = sum(class_counts.values())
    return -sum((count / total) * math.log2(count / total) if count != 0 else 0 for count in class_counts.values())


def information_gain(data, feature_name):
    class_counts = {}
    subset_counts = {}
    for row in data:
        cls = row[-1]
        class_counts[cls] = class_counts.get(cls, 0) + 1
    total_entropy = entropy(class_counts)
    for row in data:
        val = row[feature_name]
        subset = subset_counts.setdefault(val, {})
        subset[row[-1]] = subset.get(row[-1], 0) + 1
    weighted_sum = 0
    total = len(data)
    for val, counts in subset_counts.items():
        subset_size = sum(counts.values())
        weighted_sum += (subset_size / total) * entropy(counts)
    return total_entropy - weighted_sum


def majority_class(data):
    class_counts = {}
    for row in data:
        cls = row[-1]
        class_counts[cls] = class_counts.get(cls, 0) + 1
    return max(class_counts, key=class_counts.get)


def build_tree(A, Q):
    if len(Q) == 0:
        max_s = {}
        for el in A:
            if el[-1] not in max_s.keys():
                max_s[el[-1]] = 0
            max_s[el[-1]] += 1
        return {"type": "leaf", "class": max(max_s, key=max_s.get), "branches": {}}

    if len(set([el[-1] for el in A])) == 1:
        return {"type": "leaf", "class": A[0][-1], "branches": {}}

    qi = max(Q, key=lambda a: information_gain(A, a))
    tree = {"type": "node", "feature": qi, "branches": {}}
    feature_values = {row[qi] for row in A}
    for value in feature_values:
        subset = [row for row in A if row[qi] == value]
        if not subset:
            tree["branches"][value] = {"type": "leaf", "class": majority_class(A)}
        else:
            remaining_attrs = [q for q in Q if q != qi]
            tree["branches"][value] = build_tree(subset, remaining_attrs)
    return tree


def use_tree(tree, test):
    current_node = copy.deepcopy(tree)
    while len(current_node["branches"].items()) != 0:
        current_node = current_node["branches"][test[current_node["feature"]]]
    return current_node["class"]

def print_tree(node, padding=0):
    if node['type'] == 'leaf':
        print(' ' * padding + 'class:', node['class'])
    else:
        print(' ' * padding + 'feature:', node['feature'])
        for value, branch in node['branches'].items():
            print(' ' * (padding+2) + 'value:', value)
            print_tree(branch, padding+4)


def decision_tree(data, test):
    Q = [i for i in range(len(test))]
    tree = build_tree(data, Q)
    print_tree(tree)
    result = use_tree(tree, test)
    print("sample "+str(test)+" class: "+str(result))
    print("-------------------------------------------")


for i in range(len(data_variants)):
    decision_tree(data_variants[i],test_variants[i])

