# from pyvis.network import Network
# import networkx as nx
#
# networkNodes = ["a", "b", "c", "d", "e"]
# networkEdges = [("a", "a"), ("a", "b"), ("a", "c"), ("a", "d"), ("a", "e"), ("a", "f"), ("a", "c"), ("b", "c"), ("c", "d"),
#                 ("d", "e"), ("e", "a")]
#
# g = nx.MultiGraph()
# for node in networkNodes:
#     g.add_node(node, title=node, label=node)
# g.add_edges_from(networkEdges)
#
# nt = Network(height='750px', width='100%', bgcolor='#222222', font_color='white', directed=True)
# nt.show_buttons(filter_=['physics'])
# nt.from_nx(g)
# nt.set_edge_smooth('dynamic')
#
# neighbor_map = nt.get_adj_list()
# for node in nt.nodes:
#     node['value'] = len(neighbor_map[node['id']])
#
# nt.show('graphs/foo.html')
