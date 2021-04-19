# VisualBit - A tool to facilitate the analyses of Bitcoin transactions
# Copyright (C) <2021>  <Zhang Yixing>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Email: u3544946@connect.hku.hk

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
