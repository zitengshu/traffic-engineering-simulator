import networkx as nx
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt
import json
import random
import argparse
from yaml import load, Loader
import os
from datetime import datetime

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
  data = json_graph.cytoscape_data(graph)
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

def prefix_sum(i:int)->float:
  sum = 0.0
  for j in range(i):
    sum += j*0.1*(1 - 2 * (j%2))
  return sum

def gen_direct_connect(graph: nx.Graph, num_server: int, num_leaf: int, num_spine: int, num_server_per_leaf: int, capacity_list: list, block2block_capacity_list: list, num_source: int, num_sink: int):
  server_list = [f"server{i}" for i in range(num_server)]
  leaf_list = [f"leaf{i}" for i in range(num_leaf)]
  spine_list = [f"spine{i}" for i in range(num_spine)]

  for i in range(num_server):
    graph.add_node(server_list[i], pos=(2*i, 2))

  for i in range(num_leaf):
    graph.add_node(leaf_list[i], pos=(4*i+1, 6+i*prefix_sum(i)))
  
  for i in range(num_spine):
    graph.add_node(spine_list[i], pos=(8*i+2, 15))

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
  
  for i in range(num_leaf-1):
    for j in range(i+1, num_leaf):
      graph.add_edge(leaf_list[i], leaf_list[j], capacity=random.sample(block2block_capacity_list, 1)[0])

  sample_list = random.sample(server_list, num_source + num_sink)
  for source in sample_list[:num_source]:
    graph.add_edge("source", source, capacity=float('inf'))
  for sink in sample_list[num_source:]:
    graph.add_edge(sink, "sink", capacity=float('inf'))


def clos_example() -> None:
  graph = nx.Graph()
  gen_clos(graph, 16, 8, 4, 2, [5, 10, 20, 40, 100, 200], 3, 2)
  
  flow_value, flow_dict = nx.maximum_flow(graph, "source", "sink")

  labels = get_flow_labels(graph, flow_dict)
  draw_theoretical_traffic(graph, labels, "theoretical-traffic-clos.png")
  save_graph(graph, "TE-graph-clos.json")
  print(f"Theoretical maximum flow is {flow_value}")

def block2block_example() -> None:
  graph = nx.Graph()
  gen_direct_connect(graph, 16, 8, 4, 2, [5, 10, 20, 40, 100, 200], [0, 128, 256, 384], 5, 5)
  
  flow_value, flow_dict = nx.maximum_flow(graph, "source", "sink")

  labels = get_flow_labels(graph, flow_dict)
  draw_theoretical_traffic(graph, labels, "theoretical-traffic-block2block.png")
  save_graph(graph, "TE-graph-block2block.json")
  print(f"Theoretical maximum flow is {flow_value}")

def cmd() -> None:
  parser = argparse.ArgumentParser(
                    prog = 'Traffic-Engineering-Simulator',
                    description = 'This simulator generates demand data center network topology and traffic allocation.')
  parser.add_argument('-e', '--example')
  parser.add_argument('-f', '--filepath')
  args = parser.parse_args()
  if args.example == "clos":
    clos_example()
    exit(0)
  elif args.example == "block2block":
    block2block_example()
    exit(0)
  elif args.example == None:
    pass
  else:
    print(f"[ERROR] No such example: {args.example}")
    exit(0)
  
  filepath = args.filepath
  if not os.path.isfile(filepath):
    print(f"[ERROR] Cannot find: {filepath}")

  graph = nx.Graph()
  
  file = open(filepath, 'r')
  stream = file.read()
  file.close()
  data = load(stream, Loader=Loader)
  topo = data['topology']
  num_server = data['numberOfServer']
  num_leaf = data['numberOfLeaf']
  num_spine = data['numberOfSpine']
  num_server_per_leaf = data['numberOfServersPerLeaf']
  capacity_list = data['capacityList']
  b2b_cap_list = data['block2blockCapacityList']
  num_source = data['numberOfSource']
  num_sink = data['numberofSink']
  draw_graph = data['drawGraph']
  if topo == 'clos':
    gen_clos(graph, num_server, num_leaf, num_spine, num_server_per_leaf, capacity_list, num_source, num_sink)
  elif topo == 'block2block':
    gen_direct_connect(graph, num_server, num_leaf, num_spine, num_server_per_leaf, capacity_list, b2b_cap_list, num_source, num_sink)
  
  flow_value, flow_dict = nx.maximum_flow(graph, "source", "sink")
  labels = get_flow_labels(graph, flow_dict)
  if draw_graph == True:
    draw_theoretical_traffic(graph, labels, f"theoretical-traffic-{topo}.png")
  save_graph(graph, f"TE-graph-{topo}.json")
  print(f"Theoretical maximum flow is {flow_value}")

def benchmark_func(num_server: int) -> float:
  start = datetime.now()
  graph = nx.Graph()
  half = num_server//2
  gen_clos(graph, num_server, half, half//2, 2, [0, 10, 20, 40, 80, 100, 200, 400], half, half)
  flow_value, flow_dict = nx.maximum_flow(graph, "source", "sink")
  labels = get_flow_labels(graph, flow_dict)
  end = datetime.now()
  return (end - start).total_seconds()

def benchmark() -> None:
  num_server_list = [2**n for n in range(2, 15)]
  time_list = []
  for num_server in num_server_list:
    t = benchmark_func(num_server)
    time_list.append(t)
    print(num_server, t)
  plt.plot(num_server_list, time_list)
  plt.title('Benchmark Test(Runing Time)')
  plt.xlabel('Number of Servers')
  plt.ylabel('Second')
  plt.savefig("Benchmark.png")

if __name__ == '__main__':
  cmd()