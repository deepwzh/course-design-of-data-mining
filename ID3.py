import numpy as np
import pandas as pd
import uuid
import math

class Edge:
    def __init__(self):
        super().__init__()
        self.source = None,
        self.target = None
        self.value = None
    
    def get_json_data(self):
        return {
            "id": self.source.id + ":" + self.target.id,
            "source": self.source.id,
            "target": self.target.id,
            "value": self.value
        }
    
class Node:
    def __init__(self):
        super().__init__()
        self.value = None
        self.id = str(uuid.uuid1())
    
    def __str__(self):
        u = (self.label, self.value)
        return str(u)

class Tree:
    def __init__(self):
        super().__init__()
        self.edges = {
        }
        self.root_id = "id"
        self.nodes = {
           
        }
    
    def _get_child_node_json_data(self, node_id):
        if node_id not in self.edges:
            return {
                "id": node_id,
                "value": self.nodes[node_id].value,
                "is_leaf": True,
            }
        else:
            return {
                "id": node_id,
                "value": self.nodes[node_id].value,
                "children": [self._get_child_node_json_data(edge.target.id) for edge in self.edges[node_id]]
            }
    
    def get_node_json_data(self):
        return self._get_child_node_json_data(self.root_id)
    
    def get_edge_json_data(self):
        return [ edge.get_json_data() for node_edges in self.edges.values() for edge in node_edges]
    
    def get_json_data(self):
        return {
            "nodes": self.get_node_json_data(),
            "edges": self.get_edge_json_data(),
        }
    
    
    def create_node(self):
        return Node()
    
    def add_node(self, node):
        if not self.nodes:
            self.root_id = node.id
        self.nodes[node.id] = node
            
    def add_edge(self, par_node, node, edge_value):
        par_node_id = par_node.id
        if par_node_id not in self.edges:
            self.edges[par_node_id] = []
        
        edge = Edge()
        edge.source = par_node
        edge.target = node
        edge.value = edge_value
        self.edges[par_node_id].append(edge)


def attribute_selection_method(D, attribute_list):
    def getInfo(D):
        group = D.groupby('class:buys_computer')
        total = len(D)
    #     print([len(x[1]) for x in group1])
        InfoD = -sum([len(x[1])/total*math.log2(len(x[1])/total) for x in group])
        return InfoD
    
    candidate_splitting_criterion = []
    InfoD = getInfo(D)
    total = len(D.groupby('class:buys_computer'))
    for attribute in attribute_list:
        group1 = D.groupby(attribute)
        InfoageD = 0
        for x in group1:
            column_name = x[0]
            cdf = x[1]
            property_size = len(cdf)
#             print(property_size)
#             print(column_name)
#             print(cdf)
            InfoageD += property_size/(len(group1)) * getInfo(cdf)
#         print(InfoageD)
        gain = InfoD - InfoageD
        candidate_splitting_criterion.append((gain, attribute))
        print(gain, attribute)
    splitting_criterion = max(candidate_splitting_criterion, key=lambda item: item[0])[1]
    print("chose attribute", splitting_criterion)
    return splitting_criterion
    
def is_both_same_class(D):
    group_size = D.groupby("class:buys_computer").size()
    return (True, group_size.idxmax()) if group_size.size == 1 else (False, None)

def is_discrete(t):
    return True

def get_part(D, splitting_criterion):
    return D.groupby(splitting_criterion)

def get_majority_class(D):
    return str(D.groupby("class:buys_computer").size().idxmax())


tree = Tree()
def generate_decision_tree(D, attribute_list):
    N = tree.create_node()
    tree.add_node(N)
    is_same_class, C = is_both_same_class(D)
    print(attribute_list)
    print(D)
    if is_same_class:
        N.is_leaf = True
        N.value = str(C)
        print(type(N.value), N.value)
        return N # 返回N作为叶节点，类C标记
    if not attribute_list:
        N.is_leaf = True
        N.value = str(get_majority_class(D))
        print(type(N.value), N.value)
        return N #返回叶节点，多数类
    splitting_criterion = attribute_selection_method(D, attribute_list)
    N.value = str(splitting_criterion)

    # print(splitting_criterion)
    if is_discrete(splitting_criterion):
        attribute_list.remove(splitting_criterion)
    # print(attribute_list)
    for (label, Dj) in get_part(D, splitting_criterion):
        if Dj.empty:
            value = get_majority_class(D) # 为啥会是空？？？？
        else:
            child_N = generate_decision_tree(Dj, attribute_list)
            child_N.label = label
            tree.add_edge(N, child_N, label)
    return N


def main():
  df = pd.read_csv("data.csv")
  print(df)
  # df1 = df.loc[df["class:buys_computer"] == 'yes']
  
  N = generate_decision_tree(df, list(df.columns[1:-1]))
  print(tree.get_json_data())

if __name__ == '__main__':
  main()