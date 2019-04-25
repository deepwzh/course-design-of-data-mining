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
    def __init__(self, tree):
        super().__init__()
        self.value = None
        self._tree = tree
        self.id = str(uuid.uuid1())

    def has_child(self):
        return self.id in self._tree.edges

    def __str__(self):
        u = (self.label, self.value)
        return str(u)

    def get_child_by_value(self, value):
        edges = self._tree.edges[self.id]
        for edge in edges:
            if edge.value == value:
                return edge.target
        return None


class Tree:
    def __init__(self):
        super().__init__()
        self.edges = {
        }
        self.root_id = "id"
        self.nodes = {

        }

    def get_root(self):
        return self.nodes[self.root_id]

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
        return [edge.get_json_data() for node_edges in self.edges.values() for edge in node_edges]

    def get_json_data(self):
        return {
            "nodes": self.get_node_json_data(),
            "edges": self.get_edge_json_data(),
        }

    def create_node(self):
        return Node(tree=self)

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


class DecisionTree:
    def __init__(self):
        self.df = None
        self.tree = Tree()

    def load_csv_data_set(self, filename):
        self.df = pd.read_csv(filename)

    def load_data_set(self, data):
        self.df = None

    def get_class_attribute(self):
        return self.df.columns[-1]

    def get_json_result(self):
        return self.tree.get_json_data()

    def attribute_selection_method(self, D, attribute_list):
        raise Exception("unimplemented method")

    def is_both_same_class(self, D):
        group_size = D.groupby(self.get_class_attribute()).size()
        return (True, group_size.idxmax()) if group_size.size == 1 else (False, None)

    def is_discrete(self, t):
        return True

    def get_part(self, D, splitting_criterion):
        return D.groupby(splitting_criterion)

    def get_majority_class(self, D):
        return str(D.groupby(self.get_class_attribute()).size().idxmax())

    def _generate_decision_tree(self, D, attribute_list):
        tree = self.tree
        N = tree.create_node()
        tree.add_node(N)
        is_same_class, C = self.is_both_same_class(D)
        print(attribute_list)
        print(D)
        if is_same_class:
            N.is_leaf = True
            N.value = str(C)
            print(type(N.value), N.value)
            return N  # 返回N作为叶节点，类C标记
        if not attribute_list:
            N.is_leaf = True
            N.value = str(self.get_majority_class(D))
            print(type(N.value), N.value)
            return N  # 返回叶节点，多数类
        splitting_criterion = self.attribute_selection_method(D, attribute_list)
        N.value = str(splitting_criterion)

        # print(splitting_criterion)
        if self.is_discrete(splitting_criterion):
            attribute_list.remove(splitting_criterion)
        # print(attribute_list)
        for (label, Dj) in self.get_part(D, splitting_criterion):
            if Dj.empty:
                value = self.get_majority_class(D)  # 为啥会是空？？？？
            else:
                child_N = self._generate_decision_tree(Dj, attribute_list)
                child_N.label = label
                tree.add_edge(N, child_N, label)
        return N

    def build(self):
        self._generate_decision_tree(self.df, list(self.df.columns[1:-1]))

    def test_one_record(self, record):
        tree = self.tree
        node = tree.get_root()
        while node.has_child():
            value = record[node.value]
            node = node.get_child_by_value(value)
        return node.value

    def test(self, test_records):
        res = []
        for record in test_records:
            series = pd.Series(record, index=self.df.columns)
            value = self.test_one_record(series)
            res.append(value)
        return res