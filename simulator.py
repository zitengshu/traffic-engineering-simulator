import networkx as nx
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt
import json

def get_flow_labels(graph: nx.Graph, flow_dict: dict) -> dict:
  labels = {}
  flow_attributes = {}
  for from_node, adj in flow_dict.items():
    for to_node, flow in adj.items():
      if flow > 0:
        labels[(from_node,to_node)] = f"{flow}/{graph.edges[from_node, to_node]['capacity']}"
        flow_attributes[(from_node,to_node)] = flow
  nx.set_edge_attributes(G, flow_attributes, "flow")
  return labels

def draw_theoretical_traffic(graph: nx.Graph, labels: dict, image_name: str) -> None:
  pos=nx.spring_layout(graph)
  nx.draw_networkx(graph, pos=pos)
  nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
  plt.savefig(image_name)

def save_graph(graph: nx.Graph, filename: str) -> None:
  data = json_graph.adjacency_data(graph)
  s = json.dumps(data)
  with open(filename, "w") as f:
    f.write(s)


if __name__ == '__main__':
  G = nx.Graph()
  G.add_edge("x", "a", capacity=3.0)
  G.add_edge("x", "b", capacity=1.0)
  G.add_edge("a", "c", capacity=3.0)
  G.add_edge("b", "c", capacity=5.0)
  G.add_edge("b", "d", capacity=4.0)
  G.add_edge("d", "e", capacity=2.0)
  G.add_edge("c", "y", capacity=2.0)
  G.add_edge("e", "y", capacity=3.0)
  
  flow_value, flow_dict = nx.maximum_flow(G, "x", "y")

  labels = get_flow_labels(G, flow_dict)
  draw_theoretical_traffic(G, labels, "theoretical-traffic.png")
  save_graph(G, "TE-graph.json")