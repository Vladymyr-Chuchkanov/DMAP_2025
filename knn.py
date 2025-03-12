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


def euclidean_distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def build_distance_table(data, test):
    data_modified = []
    for row in data:
        ed_temp = euclidean_distance(row[0:-1],test)
        tmp = copy.deepcopy(row)
        tmp.append(ed_temp)
        tmp.append(1/(ed_temp**2))
        data_modified.append(tmp)
    return data_modified


def knn(data, test, k=2):
    if k > len(data):
        return
    data_modified = build_distance_table(data, test)
    sorted_data = sorted(data_modified, key=lambda x: x[-2])
    print(" ", end="")
    for i in range(len(test)):
        print(str(i), end=", ")
    print("S")
    for row in data_modified:
        print(row)
    print("---")
    print(" ", end="")
    for i in range(len(test)):
        print(str(i), end=", ")
    print("S")
    for row in sorted_data:
        print(row)

    classes = {}
    for i in range(k):
        target = sorted_data[i][-3]
        if target not in classes.keys():
            classes[target]=0
        classes[target]+=sorted_data[i][-1]

    print(classes)
    print("sample "+str(test)+" class: "+str(max(classes,key=classes.get)))
    print("----------------------------------------------")

for i in range(len(data_variants)):
    knn(data_variants[i],test_variants[i],5)