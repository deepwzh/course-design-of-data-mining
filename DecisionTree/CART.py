from base import DecisionTree
from utils import get_split_choice
import math

class CARTree(DecisionTree):
    def __init__(self):
        super().__init__()

    def attribute_selection_method(self, D, attribute_list):
        def getGini(D):
            """
            获取元组分类的熵
            """

            group = D.groupby(self.get_class_attribute())
            total = len(D)
            #     print([len(x[1]) for x in group1])
            InfoD = 1 - sum([math.pow(len(x[1]) / total, 2) for x in group])
            return InfoD

        def getGiniA(D, attribute):
            """
            获取对属性划分后的熵
            """
            min_gini = (None, tuple())
            values = list(D[attribute].drop_duplicates())
            print(values)
            choices = get_split_choice(values)
            D_size = len(choices)
            for choice in choices:
                gini = 0
                D1_size = len(choice[0])
                D2_size = len(choice[1])
                D1 = D[D[attribute].isin(choice[0])]
                D2 = D[D[attribute].isin(choice[1])]
                gini = (D1_size / D_size) * getGini(D1) + (D2_size / D_size) * getGini(D2)
                if min_gini[0] == None or gini < min_gini[0]:
                    min_gini = (gini, choice)
            return min_gini

        candidate_splitting_criterion = []
        gini_d = getGini(D)
        total = len(D.groupby(self.get_class_attribute()))
        for attribute in attribute_list:
            (gini_a, choice) = getGiniA(D, attribute)
            gain = gini_d - gini_a
            candidate_splitting_criterion.append((gain, attribute, choice))
            # print(gain, attribute)
        splitting_criterion = max(candidate_splitting_criterion, key=lambda item: item[0])[1:]
        print("chose attribute", splitting_criterion)
        return splitting_criterion

    
def main():
    tree = CARTree()
    tree.load_csv_data_set("data.csv")
    tree.build()    
    #print(decision_tree.get_json_result())

if __name__ == '__main__':
    main()