from collections import defaultdict
from itertools import combinations

data1 = [[ 'a', 'b', 'c', 'd'], [ 'b', 'c', 'd'], [ 'a', 'e', 'f', 'g', 'h'], [ 'b', 'c', 'd', 'e', 'g', 'j'], [ 'b', 'c', 'd', 'e', 'f'], [ 'a', 'f', 'g'], [ 'a', 'i', 'j'],
[ 'a', 'b', 'e', 'h'], [ 'f', 'g', 'h', 'i', 'j'], [ 'e', 'f', 'h']]

data2 = [[ 'a', 'b', 'c', 'f'], [ 'b', 'c', 'f'], [ 'b', 'd', 'e', 'g', 'h'], [ 'b', 'c', 'e', 'f', 'g', 'j'], [ 'b', 'c', 'd', 'e', 'f'], [ 'a', 'd', 'g'], [ 'a', 'i', 'j'],[ 'a', 'b', 'e', 'h'],
[ 'd', 'g', 'h', 'i', 'j'], [ 'd', 'e', 'h']]

data3 = [[ 'a', 'b', 'c', 'd', 'e', 'f'], [ 'b', 'c', 'd'], [ 'b', 'e', 'g', 'h'], [ 'b', 'c', 'g', 'j'], [ 'b', 'c', 'd', 'e', 'f'], [ 'a', 'e', 'f'], [ 'a', 'i', 'j'], [ 'a', 'b', 'c', 'e', 'h'],
[ 'e', 'b' , 'h', 'i', 'j'], [ 'b', 'f', 'h']]

data0 = [data1,data2,data3]



class FPTreeNode:
    def __init__(self, data_len, els, root):
        self.root = root
        self.quantity = 0
        self.el = None
        self.data_len = data_len
        self.elements_order_count = els
        self.next_nodes = []

    def get_element(self):
        return self.el
    def add_transaction(self, trans):
        if len(trans) == 0:
            return

        if self.root:
            is_node = False
            for node in self.next_nodes:
                if node.get_element() == trans[0]:
                    node.add_transaction(trans)
                    is_node = True
            if not is_node:
                new_node = FPTreeNode(self.data_len, self.elements_order_count, False)
                new_node.add_transaction(trans)
                self.next_nodes.append(new_node)
        elif self.el is None:
            self.el = trans[0]
            self.quantity += 1
            self.elements_order_count[self.el] +=1
            if len(trans) == 1:
                return
            new_node = FPTreeNode(self.data_len, self.elements_order_count, False)
            new_node.add_transaction(trans[1:])
            self.next_nodes.append(new_node)
        elif self.el == trans[0]:
            self.quantity += 1
            self.elements_order_count[self.el] += 1
            if len(trans) == 1:
                return
            is_node = False
            for node in self.next_nodes:
                if node.get_element() == trans[1]:
                    is_node = True
                    node.add_transaction(trans[1:])
            if not is_node:
                new_node = FPTreeNode(self.data_len, self.elements_order_count, False)
                new_node.add_transaction(trans[1:])
                self.next_nodes.append(new_node)

    def print_tree(self, level=0, prefix="Root: "):

        print("    " * level + prefix + str(self.el)+":"+str(self.quantity))

        for i, node in enumerate(self.next_nodes):
            if i == len(self.next_nodes) - 1:
                node.print_tree(level + 1, "└── ")
            else:
                node.print_tree(level + 1, "├── ")



    def get_paths(self, char, result, current_path):
        if self.el == char:
            tmp = current_path.copy()
            tmp.append(char)
            result.append([tmp,self.quantity])
        else:
            if len(self.next_nodes)!=0:
                for node in self.next_nodes:
                    tmp = current_path.copy()
                    if self.el is not None:
                        tmp.append(self.el)
                    node.get_paths(char, result, tmp)
            else:
                current_path.clear()

        return


def generate_suffix_itemsets(paths):
    itemset_counts = defaultdict(int)

    for path, count in paths:
        if len(path) < 2:
            continue  

        last_element = path[-1]
        other_elements = path[:-1]

        for r in range(1, len(other_elements) + 1):
            for combo in combinations(other_elements, r):
                itemset = frozenset(combo + (last_element,))
                itemset_counts[itemset] += count

    return itemset_counts



def calc_sup(element, data):
    sup = 0
    for el in data:
        if set(element) & set(el) == set(element):
            sup+=1
    return sup/len(data)


def fpgrowth(data, min_sup, min_conf):
    chars = set()
    for el in data:
        for char in el:
            chars.add(char)
    lst2 = []
    for el in chars:
        el_sup = calc_sup(el, data)
        print(str(set(el))+" "+str(el_sup*100)+"%")
        if el_sup >= min_sup:
            lst2.append([el, el_sup])
    lst2 = sorted(lst2, key=lambda x: x[1], reverse=True)
    lst2 = [x for x,y in lst2]
    print(lst2)
    filtered_lists = [[x for x in sublist if x in lst2] for sublist in data]
    sorted_lists = [sorted(sublist, key=lambda x: lst2.index(x)) for sublist in filtered_lists]
    print(sorted_lists)
    els_dict = {}
    for el in lst2:
        els_dict[el]=0

    tree = FPTreeNode(len(sorted_lists),els_dict, True)
    for el in sorted_lists:
        tree.add_transaction(el)
    tree.print_tree()
    print(tree.elements_order_count)
    sets_all = []
    for i in range(len(lst2)-1,-1,-1):
        sets = []
        result = []
        if tree.elements_order_count[lst2[i]]/tree.data_len < min_sup:
            continue
        tree.get_paths(lst2[i], result, [])
        print(str(lst2[i]) + " " + str(result))
        frequent_itemsets = generate_suffix_itemsets(result)
        for itemset, count in sorted(frequent_itemsets.items(), key=lambda x: (-len(x[0]), -x[1])):
            if count/len(sorted_lists) >= min_sup:
                sets.append(list(itemset))
                sets_all.append(list(itemset))
            print(f"{set(itemset)}: {count}")
        print(sets)

    print(sets_all)
    print("----------------------------------------------------------------------------")


for el in data0:
    fpgrowth(el, 0.4, 0.75)