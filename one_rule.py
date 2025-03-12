
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

def fill_friction_table(data):
    friction_tables = {}

    for row in data:
        for i in range(len(row) - 1):
            target = row[-1]
            if i not in friction_tables.keys():
                friction_tables[i] = {}

            if row[i] not in friction_tables[i].keys():
                friction_tables[i][row[i]] = {}

            if target not in friction_tables[i][row[i]].keys():
                friction_tables[i][row[i]][target] = 0

            friction_tables[i][row[i]][target] += 1
    return friction_tables


def one_rule_select_rule(friction_table):
    error = {}
    for rule_num, tables in friction_table.items():
        feature_error_sum = 0
        feature_correct_sum = 0
        for feature_value, class_value_table in tables.items():
            max_value_key = max(class_value_table, key=class_value_table.get)
            error_feature_value = sum(class_value_table.values()) - class_value_table.get(max_value_key, 0)
            feature_error_sum += error_feature_value
            feature_correct_sum += class_value_table.get(max_value_key, 0)
        error[rule_num]=(feature_error_sum / (feature_correct_sum+feature_error_sum))
    print(error)
    return min(error, key=error.get)


def use_one_rule(friction_table, rule, test):
    return max(friction_table[rule][test[rule]], key=friction_table[rule][test[rule]].get)


def one_rule(data, test):
    friction_tables = fill_friction_table(data)
    print(friction_tables)
    rule = one_rule_select_rule(friction_tables)
    result = use_one_rule(friction_tables,rule,test)
    print(" ",end="")
    for i in range(len(test)):
        print(str(i), end=", ")
    print("S")
    for row in data:
        print(row)
    print("best rule = " + str(rule))
    print(str(test) + " : " + str(result))
    print("------------------------------------------------------------")


for i in range(len(data_variants)):
    one_rule(data_variants[i],test_variants[i])





