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

def calculate_probabilities(data, laplas_smoothing_coef):
    friction_tables = {}
    class_table = {}
    all_third_level_keys = {}
    for row in data:
        for i in range(len(row) - 1):
            if i not in all_third_level_keys.keys():
                all_third_level_keys[i]=set()
            all_third_level_keys[i].add(row[i])
    for row in data:
        target = row[-1]
        if target not in class_table.keys():
            class_table[target] = 0
        class_table[target] += 1

        for i in range(len(row) - 1):

            if i not in friction_tables.keys():
                friction_tables[i] = {}

            if target not in friction_tables[i].keys():
                friction_tables[i][target] = {}

            for el in all_third_level_keys[i]:
                if el not in friction_tables[i][target]:
                    friction_tables[i][target][el] = 0
            friction_tables[i][target][row[i]] += 1
    for feature_name, class_feature_val_table in friction_tables.items():
        for class_name, feature_val_table in class_feature_val_table.items():
            check = False
            if min(feature_val_table.values()) != 0:
                check = True
            for key in feature_val_table.keys():
                if check:
                    feature_val_table[key] /= class_table[class_name]
                else:
                    feature_val_table[key] += laplas_smoothing_coef
                    feature_val_table[key] /= (class_table[class_name]+laplas_smoothing_coef*len(friction_tables.keys()))

    print(friction_tables)
    return friction_tables, class_table


def use_naive_bayes(probability_table, class_table, test):
    classes_prob = {}
    for class_name in class_table.keys():
        current_prob = class_table[class_name]/sum(class_table.values())
        for i in range(len(test)):
            current_prob*=probability_table[i][class_name][test[i]]
        classes_prob[class_name]=(current_prob)
    return classes_prob


def naive_bayes(data, test, laplas_smoothing_coef = 0.1):
    print(" ",end="")
    for i in range(len(test)):
        print(str(i), end=", ")
    print("S")
    for row in data:
        print(row)
    probability_table,classes = calculate_probabilities(data, laplas_smoothing_coef)
    class_probabilities = use_naive_bayes(probability_table, classes, test)
    print(class_probabilities)
    print("sample "+str(test)+" class = "+str(max(class_probabilities, key=class_probabilities.get)))
    print("-------------------------------------")


for i in range(len(data_variants)):
    naive_bayes(data_variants[i],test_variants[i])