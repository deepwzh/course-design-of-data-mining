data = [
  [1,2,5],
  [2,4],
  [2,3],
  [1,2,4],
  [1,3],
  [2,3],
  [1,3],
  [1,2,3,5],
  [1,2,3]
]
class Counter:
  """
  辅助类：计数器类
  """
  def __init__(self):
    self.data = {}

  def increase(self, name):
    if name not in self.data:
      self.data[name] = 1
    else:
      self.data[name] += 1
  
  def __iter__(self):
      return iter(sorted(self.data.keys()))

  def __getitem__(self, name):
    try:
      return self.data[name]
    except KeyError:
      return 0

  def __str__(self):
    return str(dict(sorted((k,self.data[k]) for k in sorted(self.data.keys()))))

def find_frequent_1_itemsets(D, min_sup):
  """
  find frequent 1 itemsets
  """
  count = Counter()
  for t in D:
    for item in t:
      count.increase(item)
  print(count)
  res = []
  for item in count:
    if count[item] >= min_sup:
      res.append([item])
  return res

class Node():
  def __init__(self, identify, v, cnt, tree):
    self._tree = tree
    self.v = v
    self.cnt = cnt
    self.identify = identify

  def get_child(self):
    if self.identify not in self._tree.edges:
      return []
    return self._tree.edges[self.identify]

  def append_child(self, node):
    if self.identify not in self._tree.edges:
      self._tree.edges[self.identify] = []
    self._tree.edges[self.identify].append(node)

  def __str__(self):
    return "%s:%d" % (self.v, self.cnt)
class Edge():
  def __init__(self):
    self.source = None
    self.target = None

class FPTree():
  """
  FP树的数据结构，0代表根节点
  """
  def __init__(self, *, min_sup):
    self._rank = {}

    self.min_sup = min_sup
    self.D = []
    self.nodes = []
    self.edges = {}
    self.node_link_list = {}
    self.init() # 初始化null根节点

  def loads(self, D):
    self.D = D

  def create_node(self, value, cnt):
    nodes_length = len(self.nodes)
    node = Node(nodes_length, value, cnt, self)
    self.nodes.append(node)
    return node

  def init(self):
    node = self.create_node('null', 0)
    self.nodes.append(node)
  
  def insert(self, record):
    pass

  def get_inital_frequent_itemset(self, D, min_sup):
    count = Counter()
    for t in D:
      for item in t:
        count.increase(item)
    # print(count)
    res = {}
    for item in count:
      if count[item] >= min_sup:
        res[item] = count[item]
    sorted_items = sorted(res.items(), key=lambda x: -x[1])
    for i in range(len(sorted_items)):
      self._rank[sorted_items[i][0]] = i
    return {key: value for key, value in sorted_items}
    # return itemset

  def init_node_list(self, itemset):
    # 初始化节点链
    self.node_link_list = {}
    for item in itemset:
      self.node_link_list[item] = { "item": item, "count": 0, "nodes": []}

  def update_node_list(self, node):
    # 更新节点链及其支持度计数
    self.node_link_list[node.v]["count"] += node.cnt
    self.node_link_list[node.v]["nodes"].append(node)

  def get_sorted_record(self, record):
    return sorted(record, key=lambda x: self._rank[x])

  def get_root(self):
    return self.nodes[0]

  def insert_node(self, item):
    pass
    
  def insert_affair(self, affair):
    items = affair
    root = self.get_root()
    cur_node = root
    common_prefix = True
    for item in items:
      if common_prefix:
        print(str(cur_node),[str(item) for item in cur_node.get_child()])
        if len(cur_node.get_child()) == 0:
          common_prefix = False
        update_flag = False
        for node in cur_node.get_child():
          if str(node.v) == str(item):
            node.cnt += 1
            print("Update %s" % (str(node),))
            cur_node = node
            update_flag = True
            break
      if not update_flag:
        common_prefix = False
      if not common_prefix:        
        node = self.create_node(item, 1)
        print("CREATE %d" % (item, ))
        cur_node.append_child(node)
        cur_node = node
        self.update_node_list(node)

  def build(self):
    itemset = self.get_inital_frequent_itemset(self.D, self.min_sup)
    self.init_node_list(itemset)
    # print(itemset)
    # print(self.node_link_list)
    for record in self.D:
      sorted_record = self.get_sorted_record(record)
      print(sorted_record)
      self.insert_affair(sorted_record)
  
  def has_unique_branch(self):
    """
    判断是否只有一个分支
    """
    # 根节点度数为一，即为只有一条边
    return len(self.edges[0]) == 1

def fpGrowth(tree, suffix):
  if tree.has_unique_branch():
    pass
  else:
    
    pass

def main():
  fptree = FPTree(min_sup=2)
  fptree.loads(data)
  fptree.build()
  print(fptree.node_link_list)
  fpGrowth(fptree, None)
if __name__ == '__main__':
  main()