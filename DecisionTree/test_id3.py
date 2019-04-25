from ID3 import ID3Tree
from C45 import C45Tree
from CART import CARTree
import unittest


class TestCARTDict(unittest.TestCase):
    def setUp(self):
        self.decision_tree = CARTree()
        self.decision_tree.load_csv_data_set("data.csv")
        self.decision_tree.build()
        #print(self.decision_tree.get_json_result())

    def tearDown(self):
        pass


    def test_record(self):
        res = self.decision_tree.test([[14, 'senior', 'medium', 'no', 'excellent', 'no']])
        self.assertEqual(res, ["no"])


class TestC45Dict(unittest.TestCase):
    def setUp(self):
        self.decision_tree = C45Tree()
        self.decision_tree.load_csv_data_set("data.csv")
        self.decision_tree.build()
        #print(self.decision_tree.get_json_result())

    def tearDown(self):
        pass


    def test_record(self):
        res = self.decision_tree.test([[14, 'senior', 'medium', 'no', 'excellent', 'no']])
        self.assertEqual(res, ["no"])

class TestID3Dict(unittest.TestCase):
    def setUp(self):
        self.decision_tree = ID3Tree()
        self.decision_tree.load_csv_data_set("data.csv")
        self.decision_tree.build()
        #print(self.decision_tree.get_json_result())

    def tearDown(self):
        pass


    def test_record(self):
        res = self.decision_tree.test([[14, 'senior', 'medium', 'no', 'excellent', 'no']])
        self.assertEqual(res, ["no"])

if __name__ == '__main__':
  unittest.main()