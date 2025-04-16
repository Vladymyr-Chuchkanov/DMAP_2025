
data1 = [[ 'a', 'b', 'c', 'd'], [ 'b', 'c', 'd'], [ 'a', 'e', 'f', 'g', 'h'], [ 'b', 'c', 'd', 'e', 'g', 'j'], [ 'b', 'c', 'd', 'e', 'f'], [ 'a', 'f', 'g'], [ 'a', 'i', 'j'],
[ 'a', 'b', 'e', 'h'], [ 'f', 'g', 'h', 'i', 'j'], [ 'e', 'f', 'h']]

data2 = [[ 'a', 'b', 'c', 'f'], [ 'b', 'c', 'f'], [ 'b', 'd', 'e', 'g', 'h'], [ 'b', 'c', 'e', 'f', 'g', 'j'], [ 'b', 'c', 'd', 'e', 'f'], [ 'a', 'd', 'g'], [ 'a', 'i', 'j'],[ 'a', 'b', 'e', 'h'],
[ 'd', 'g', 'h', 'i', 'j'], [ 'd', 'e', 'h']]

data3 = [[ 'a', 'b', 'c', 'd', 'e', 'f'], [ 'b', 'c', 'd'], [ 'b', 'e', 'g', 'h'], [ 'b', 'c', 'g', 'j'], [ 'b', 'c', 'd', 'e', 'f'], [ 'a', 'e', 'f'], [ 'a', 'i', 'j'], [ 'a', 'b', 'c', 'e', 'h'],
[ 'e', 'b' , 'h', 'i', 'j'], [ 'b', 'f', 'h']]

data0 = [data1,data2,data3]



def calc_sup(element, data):
    sup = 0
    for el in data:
        if element & el == element:
            sup+=1
    return sup/len(data)


def generate_n_els(current_els, data, min_sup, sup_dict):
    next_n = []
    for i in range(len(current_els)):
        for j in range(i+1, len(current_els)):
            if (len(current_els[i] & current_els[j]) == len(current_els[i]) - 1) or len(current_els[i]) == 1:
                tmp = current_els[i] | current_els[j]
                tmp2 = calc_sup(tmp, data)
                print(str(tmp) + " " + str(tmp2 * 100) + "%")
                if tmp2 >= min_sup and tmp not in next_n:
                    next_n.append(tmp)
                    sup_dict[str(tmp)]=tmp2

    return next_n






def apriori(data2, min_sup, min_conf):
    data = []
    sup_dict = {}
    for el in data2:
        print(el)
        data.append(set(el))
    sets = set()
    for el in data:
        for char in el:
            sets.add(char)
    sets = list(sets)
    lst2 = []
    for el in sets:
        el_sup = calc_sup(set(el), data)
        print(str(set(el))+" "+str(el_sup*100)+"%")
        if el_sup >= min_sup:
            lst2.append(set(el))
            sup_dict[str(set(el))]=el_sup
    result = [lst2]
    next_n = generate_n_els(lst2, data, min_sup,sup_dict)
    while len(next_n) > 1:
        result.append(next_n)
        next_n = generate_n_els(result[-1], data, min_sup,sup_dict)
    if len(next_n) > 0:
        result.append(next_n)
    result2 = []
    print(result)
    for el in result[-1]:
        for i in range(len(result)-1):
            for element in result[i]:
                if element & el == element:
                    tmp = sup_dict[str(el)]/sup_dict[str(element)]
                    if tmp >= min_conf:
                        result2.append(str(element)+" => "+str(el-element))
                    print("conf("+str(element)+" => "+str(el-element)+") = "+str(tmp))
    print(result)
    print(result2)


    print("----------------------------------------------------------------------------")


for el in data0:
    apriori(el, 0.4, 0.75)