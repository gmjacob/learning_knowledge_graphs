from relation import Relation
import networkx as nx

import matplotlib
import matplotlib.pyplot as plt

class KnowledgeGraph:

    __relations: [Relation]
    __graph: nx.Graph
    __colors: {}

    def __init__(self, relations):
        self.__relations = relations
        self.__graph = nx.Graph()
        self.__colors = {}

    def build(self):
        for relation in self.__relations:
            hypernym = relation.getHypernym()
            hyponym = relation.getHyponym()
            
            self.__graph.add_node(hypernym)
            self.__colors[hypernym] = '#e34234'
            self.__graph.add_node(hyponym)
            self.__colors[hyponym] = '#009966'
            self.__graph.add_edge(
                hypernym,
                hyponym
            )
    
    def show(self):
        pos = nx.spring_layout(self.__graph)
        plt.figure()
        colorMap = []

        for node in self.__graph.nodes:
            colorMap.append(self.__colors[node])
        
        nx.draw(
            self.__graph,
            pos,
            edge_color='black',
            width=10,
            linewidths=1,
            node_size=100,
            node_color=colorMap,
            alpha=0.7,
            labels={node: node for node in self.__graph.nodes()}
        )
        # nx.draw_networkx_edge_labels(self.__graph, pos)
        plt.axis('off')
        # plt.show()
        plt.savefig('demo.png', bbox_inches='tight')
