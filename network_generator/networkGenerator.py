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

from utils import dbManager
from pyvis.network import Network
import networkx as nx
import random
import time


def generateGraph(g, n=1):
    t = {}
    for nl in g.nodes:
        t[nl] = (len(list(g.neighbors(nl))), len(list(g.predecessors(nl))))

    nt = Network(height='750px', width='100%', bgcolor='#222222', font_color='white', directed=True)
    nt.show_buttons(filter_=['physics'])
    nt.from_nx(g)
    nt.set_edge_smooth('dynamic')

    for node in nt.nodes:
        node['value'] = (t[node['id']][0] + t[node['id']][1]) * n
        node['title'] += '<br>As Input: '
        node['title'] += str(t[node['id']][0])
        node['title'] += '<br>As Output: '
        node['title'] += str(t[node['id']][1])
        node['title'] += '<br>Total transactions: '
        node['title'] += str(t[node['id']][0] + t[node['id']][1])

    return nt


class NetworkGenerator(object):
    """
        This class models the bitcoin transaction network generator.
        This is a singleton class.
    """

    __species = None
    __first_init = True

    def __new__(cls, *args, **kwargs):
        if cls.__species is None:
            cls.__species = object.__new__(cls)
        return cls.__species

    def __init__(self):
        if self.__first_init:
            self.manager = dbManager.DBManager()
            self.networkNodes = []
            self.networkEdges = []
            self.address = None
            self.layer = None
            self.__class__.__first_init = False

    def generateLocalNetwork(self, address, layer):
        """
        This method generates all of the data needed to construct a transaction graph using local database
        """
        self.address = address
        self.layer = layer
        print("Layer level:", layer)
        print('#' * 30)
        address_nodes = {address}
        address_edges = []
        address_explored = set()
        tx_explored = set()
        address_exist = True
        for i in range(0, layer):
            print("Exploring layer " + str(i) + "......")
            address_nodes_temp = address_nodes.copy()
            for an in address_nodes_temp:
                if an in address_explored:
                    continue
                else:
                    print("Exploring address " + an + "......")
                    # forward direction
                    print("Forward......")
                    input_query = """
                    SELECT O.address AS output_address, O.tx_id, T.hash
                    FROM (SELECT input.tx_id, output.address 
                    FROM input JOIN transaction JOIN output 
                    ON input.pre_tx_hash = transaction.hash AND output.tx_id = transaction.tx_id AND input.pos_index = output.pos_index
                    WHERE output.address = '%s') AS I
                    JOIN transaction AS T
                    JOIN output AS O
                    ON I.tx_id = T.tx_id AND T.tx_id = O.tx_id
                    """ % an
                    addresses = self.manager.execute_query(input_query)
                    if not addresses:
                        if i == 0:
                            address_exist = False
                    else:
                        for a in addresses:
                            address_nodes.add(a[0])
                            if (a[1], an, a[0]) not in tx_explored:
                                address_edges.append(((an, a[0]), a[2]))
                                tx_explored.add((a[1], an, a[0]))

                    # reverse direction
                    print("Reverse......")
                    input_query = """
                    SELECT I.address AS input_address, I.tx_id, T.hash
                    FROM (SELECT input.tx_id, output.address 
                    FROM input JOIN transaction JOIN output 
                    ON input.pre_tx_hash = transaction.hash AND output.tx_id = transaction.tx_id AND input.pos_index = output.pos_index) AS I
                    JOIN transaction AS T
                    JOIN output AS O
                    ON I.tx_id = T.tx_id AND T.tx_id = O.tx_id
                    WHERE O.address = '%s'
                    """ % an
                    addresses = self.manager.execute_query(input_query)
                    if not addresses:
                        if i == 0 and not address_exist:
                            address_exist = False
                    else:
                        address_exist = True
                        for a in addresses:
                            address_nodes.add(a[0])
                            if (a[1], an, a[0]) not in tx_explored:
                                address_edges.append(((a[0], an), a[2]))
                                tx_explored.add((a[1], an, a[0]))
                    if not address_exist:
                        print("The transactions of address doesn't exist in the local database.")
                        print("Network generation failed. Please try again.")
                        return False
                    address_explored.add(an)
                    print('#' * 30)
        print("Total nodes:", len(address_nodes))
        print("Total edges:", len(address_edges))
        self.networkNodes = list(address_nodes)
        self.networkEdges = address_edges

    def generateAddressCenteredGraph(self):
        """
        This method generates the address centered graph
        """
        print("Address centered graph")
        print('#' * 30)
        if self.networkNodes and self.networkEdges:
            tx_list = []
            print("Generating graph......")
            g = nx.MultiDiGraph()
            for node in self.networkNodes:
                g.add_node(node, title=node, label=node)
            for edge in self.networkEdges:
                if (edge[0][0], edge[0][1], edge[1]) not in tx_list:
                    g.add_edge(edge[0][0], edge[0][1], title='tx hash: ' + edge[1])
                    tx_list.append((edge[0][0], edge[0][1], edge[1]))

            nt = generateGraph(g)

            nt.get_node(self.address)['color'] = 'yellow'

            print("Graph generated")
            nt.show('graphs/address_centered/Address_Centered_Graph_' + self.address + '_' + str(self.layer) + '.html')
            print("Showing graph......")
            print('Graph location: ' + 'graphs/address_centered/Address_Centered_Graph_' + self.address + '_' + str(
                self.layer) + '.html')
        else:
            print("!!Warning: Transaction network not constructed. Please generate first.")

    def generateFullEntityCenteredGraph(self):
        """
        This method generates the address centered graph full version
        """
        print("Address centered graph - Full version")
        print('#' * 30)
        if self.networkNodes and self.networkEdges:
            print("Generating graph......")
            g = nx.MultiDiGraph()
            tags = set()
            node_tag = {}

            for node in self.networkNodes:
                tag_query = "SELECT tag FROM cluster WHERE address = '%s'" % node
                tag = self.manager.execute_query(tag_query)
                if tag:
                    node_tag[node] = tag[0][0]
                    tags.add(tag[0][0])
                    if node == self.address:
                        at = tag[0][0]
                else:
                    t = str(int(random.random() * 100000)) + str(int(time.time()))
                    cluster_replace_query = "INSERT INTO cluster (address, tag) VALUES ('%s', '%s')" % (node, t)
                    self.manager.execute_query(cluster_replace_query)
                    node_tag[node] = t
                    tags.add(t)
                    if node == self.address:
                        at = t

            for tag in tags:
                g.add_node(tag, title=tag, label=tag)

            tx_list = []
            for address_edge in self.networkEdges:
                if address_edge[0][0] in node_tag and address_edge[0][1] in node_tag:
                    if (node_tag[address_edge[0][0]], node_tag[address_edge[0][1]], address_edge[1]) not in tx_list:
                        g.add_edge(node_tag[address_edge[0][0]], node_tag[address_edge[0][1]],
                                   title='tx hash: ' + address_edge[1])
                        tx_list.append((node_tag[address_edge[0][0]], node_tag[address_edge[0][1]], address_edge[1]))

            nt = generateGraph(g, 3)

            for tag in tags:
                addresses_query = "SELECT address FROM cluster WHERE tag = '%s'" % tag
                addresses = self.manager.execute_query(addresses_query)
                for address in addresses:
                    nt.add_node(address[0], title=address[0], label=address[0], value=1, color='#dd4b39')
                    nt.add_edge(address[0], tag)

            nt.get_node(self.address)['color'] = 'yellow'
            nt.get_node(at)['color'] = 'yellow'

            print("Graph generated")
            nt.show(
                'graphs/entity_centered/Entity_Centered_Full_Graph_' + self.address + '_' + str(self.layer) + '.html')
            print("Showing graph......")
            print('Graph location: ' + 'graphs/entity_centered/Entity_Centered_Full_Graph_' + self.address + '_' + str(
                self.layer) + '.html')
        else:
            print("!!Warning: Transaction network not constructed. Please generate first.")

    def generateSimpleEntityCenteredGraph(self):
        """
        This method generates the address centered graph simplified version
        """
        print("Address centered graph - Simplified version")
        print('#' * 30)
        if self.networkNodes and self.networkEdges:
            print("Generating graph......")
            g = nx.MultiDiGraph()
            tags = set()
            node_tag = {}

            for node in self.networkNodes:
                tag_query = "SELECT tag FROM cluster WHERE address = '%s'" % node
                tag = self.manager.execute_query(tag_query)
                if tag:
                    node_tag[node] = tag[0][0]
                    tags.add(tag[0][0])
                    if node == self.address:
                        at = tag[0][0]
                else:
                    t = str(int(random.random() * 100000)) + str(int(time.time()))
                    cluster_replace_query = "INSERT INTO cluster (address, tag) VALUES ('%s', '%s')" % (node, t)
                    self.manager.execute_query(cluster_replace_query)
                    node_tag[node] = t
                    tags.add(t)
                    if node == self.address:
                        at = t

            for tag in tags:
                g.add_node(tag, title=tag, label=tag)

            tx_list = []
            for address_edge in self.networkEdges:
                if address_edge[0][0] in node_tag and address_edge[0][1] in node_tag:
                    if (node_tag[address_edge[0][0]], node_tag[address_edge[0][1]], address_edge[1]) not in tx_list:
                        g.add_edge(node_tag[address_edge[0][0]], node_tag[address_edge[0][1]], title='tx hash: ' + address_edge[1])
                        tx_list.append((node_tag[address_edge[0][0]], node_tag[address_edge[0][1]], address_edge[1]))

            nt = generateGraph(g, 3)

            for address in self.networkNodes:
                if address in node_tag:
                    nt.add_node(address, title=address, label=address, value=1, color='#dd4b39')
                    nt.add_edge(address, node_tag[address])

            nt.get_node(self.address)['color'] = 'yellow'
            nt.get_node(at)['color'] = 'yellow'

            print("Graph generated")
            nt.show('graphs/entity_centered/Entity_Centered_Simple_Graph_' + self.address + '_' + str(
                self.layer) + '.html')
            print("Showing graph......")
            print(
                'Graph location: ' + 'graphs/entity_centered/Entity_Centered_Simple_Graph_' + self.address + '_' + str(
                    self.layer) + '.html')
        else:
            print("!!Warning: Transaction network not constructed. Please generate first.")
