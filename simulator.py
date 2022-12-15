import networkx as nx
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt
import json
import random

def get_flow_labels(graph: nx.Graph, flow_dict: dict) -> dict:
  labels = {}
  flow_attributes = {}
  for from_node, adj in flow_dict.items():
    for to_node, flow in adj.items():
      if flow > 0:
        labels[(from_node,to_node)] = f"{flow}/{graph.edges[from_node, to_node]['capacity']}"
        flow_attributes[(from_node,to_node)] = flow
  nx.set_edge_attributes(graph, flow_attributes, "flow")
  return labels

def draw_theoretical_traffic(graph: nx.Graph, labels: dict, image_name: str) -> None:
  plt.figure(0, figsize=(20,20))
  pos=nx.get_node_attributes(graph, 'pos')
  nx.draw_networkx(graph, pos=pos, node_size=600, font_size=8)
  nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
  plt.savefig(image_name)

def save_graph(graph: nx.Graph, filename: str) -> None:
  data = json_graph.adjacency_data(graph)
  s = json.dumps(data)
  with open(filename, "w") as f:
    f.write(s)

def gen_clos(graph: nx.Graph, num_server: int, num_leaf: int, num_spine: int, num_server_per_leaf: int, capacity_list: list, num_source: int, num_sink: int) -> None:
  server_list = [f"server{i}" for i in range(num_server)]
  leaf_list = [f"leaf{i}" for i in range(num_leaf)]
  spine_list = [f"spine{i}" for i in range(num_spine)]

  for i in range(num_server):
    graph.add_node(server_list[i], pos=(2*i, 3))

  for i in range(num_leaf):
    graph.add_node(leaf_list[i], pos=(4*i+1, 6))
  
  for i in range(num_spine):
    graph.add_node(spine_list[i], pos=(8*i+2, 9))

  graph.add_node("source", pos=(0,0))
  graph.add_node("sink", pos=(2*num_server,0))
  for spine in spine_list:
    for leaf in leaf_list:
      graph.add_edge(leaf, spine, capacity=random.sample(capacity_list, 1)[0])
  i = 0
  j = 0
  while i < num_server:
    graph.add_edge(server_list[i], leaf_list[j], capacity=random.sample(capacity_list, 1)[0])
    i += 1
    if i % num_server_per_leaf == 0:
      j += 1
  
  sample_list = random.sample(server_list, num_source + num_sink)
  for source in sample_list[:num_source]:
    graph.add_edge("source", source, capacity=float('inf'))
  for sink in sample_list[num_source:]:
    graph.add_edge(sink, "sink", capacity=float('inf'))
  return

def clos_example() -> None:
  graph = nx.Graph()
  gen_clos(graph, 16, 8, 4, 2, [5, 10, 20, 40, 100, 200], 3, 2)
  
  flow_value, flow_dict = nx.maximum_flow(graph, "source", "sink")

  labels = get_flow_labels(graph, flow_dict)
  draw_theoretical_traffic(graph, labels, "theoretical-traffic-clos.png")
  save_graph(graph, "TE-graph-clos.json")
  print(f"theoretical maximum flow is {flow_value}")

if __name__ == '__main__':
  print("main")