#!/usr/bin/env python

import argparse
import re
import commands, sys
#import fire


def bfs(graph, start, debug=False):
      """
      Breadth First Search (BFS)

      Given a node in a graph, BFS will find all nodes connected to this
      node. The distance between nodes is measured in HOPS. It will find
      all nodes at distance 'k' before finding any nodes at a further
      distance. It will return the full list of connected nodes.

      PseudoCode:

      BFS(G,s)

      for each vertex u in V[G] - {s} do
        state[u] = WHITE
        predecessor[u] = nil
      state[s] = GRAY
      predecessor[s] = nil
      QUEUE = {s}
      while QUEUE != 0 do
        u = dequeue[Q]
        process vertex u as desired
        for each v in Adjacent[u] do
          process edge (u,v) as desired (e.g. distance[v] = distance[u] + 1)
          if state[v] = WHITE then
            state[v] = GRAY
            predecessor[v] = u
            enqueue[Q,v]
        state[u] = BLACK
      """
      result = []
      for v in graph.getVertices():
          a_vertex = graph.getVertex(v)
          a_vertex.setColor(Vertex.WHITE)
          a_vertex.setDistance(0)
          a_vertex.setPred(None)

      start.setDistance(0)
      start.setPred(None)
      vertex_queue = Queue()
      vertex_queue.enqueue(start)
      while (vertex_queue.size() > 0):
          current_vertex = vertex_queue.dequeue()
          result.append(current_vertex)
          if debug:
              print current_vertex
          for v in current_vertex.getConnections():
              if v.getColor() == Vertex.WHITE:
                  v.setColor(Vertex.GRAY)
                  v.setDistance(current_vertex.getDistance() + 1)
                  v.setPred(current_vertex)
                  vertex_queue.enqueue(v)
          current_vertex.setColor(Vertex.BLACK)
      return result

# Bradley N. Miller, David L. Ranum
# Introduction to Data Structures and Algorithms in Python
# Copyright 2005
# 
#queue.py

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

#
#  adjGraph
#
#  Created by Brad Miller on 2005-02-24.
#  Copyright (c) 2005 Brad Miller, David Ranum, Luther College. All rights reserved.
#

import sys
import os

class Graph:
    """
    An adjaciency representation of a graph.

    Internally nodes are store in a dictionary with:
    - Key: the key associated to the vertex
    - Value: the Vertex object itself
    """

    def __init__(self):
        self.vertices = {}
        self.numVertices = 0
        self.time = 0

    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertices[key] = newVertex
        return newVertex

    def getVertex(self,n):
        if n in self.vertices:
            return self.vertices[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertices

    def addEdge(self,f,t,cost=0):
            if f not in self.vertices:
                nv = self.addVertex(f)
            if t not in self.vertices:
                nv = self.addVertex(t)
            self.vertices[f].addNeighbor(self.vertices[t],cost)

    def getVertices(self):
        """
        Returns the list of keys stored in the internal dictionary
        that holds the vertices.
        """
        return list(self.vertices.keys())

    def __iter__(self):
        return iter(self.vertices.values())

    def getTime(self):
        return self.time

    def incrementTime(self):
        self.time = self.time + 1

    def __repr__(self):
        return '\n'.join(['%r' % self.vertices[v] for v in self.vertices])

class Vertex:
    WHITE = 0
    GRAY = 1
    BLACK = 2
    def __init__(self,num):
        self.id = num
        self.connectedTo = {}
        self.color = Vertex.WHITE
        self.dist = sys.maxsize
        self.pred = None
        self.disc = 0
        self.fin = 0

    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight

    def setColor(self,color):
        self.color = color

    def setDistance(self,d):
        self.dist = d

    def setPred(self,p):
        self.pred = p

    def setDiscovery(self,dtime):
        self.disc = dtime

    def setFinish(self,ftime):
        self.fin = ftime

    def getFinish(self):
        return self.fin

    def getDiscovery(self):
        return self.disc

    def getPred(self):
        return self.pred

    def getDistance(self):
        return self.dist

    def getColor(self):
        return self.color

    def getConnections(self):
        return self.connectedTo.keys()

    def getWeight(self,nbr):
        return self.connectedTo[nbr]

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        result = str(self.id) + ":color " + str(self.color) + ":disc " + str(self.disc) + ":fin " + str(self.fin) + ":dist " + str(self.dist)
        if self.pred:
            result += " :pred \t[" + str(self.pred.getId())+ "]"
        if len(self.connectedTo.keys()):
            result += " Connections: " \
                   + " ".join([("(%s,%3.2f)") % (v.getId(), self.connectedTo[v]) for v in self.connectedTo.keys()])
        return result

    def getId(self):
        return self.id


    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return id(self)


vertices = []
consumes = Graph()
is_consumed = Graph()

def createGraph(dependency_file):
    with open('%s' % dependency_file, 'r') as f:
        for line in f:
            m = re.match('(\d+).*label=(\w+),.*tooltip=(\w+)', line)
            if m:
                vertices.append(Vertex(int(m.group(1))))
                vertices[-1].label = m.group(2)
                vertices[-1].tooltip = m.group(3)
            m = re.match('(\d+) -> (\d+);', line)
            if m:
                consumes.addEdge(int(m.group(1)), int(m.group(2)))
                is_consumed.addEdge(int(m.group(2)), int(m.group(1)))

def toDotOutput(root_label,
                graph,
                outputFormat,
                append,
                maxNodes,
                exclude_from_node):
    root_nodes = [v for v in vertices if v.label == root_label]
    exclude_node = [v for v in vertices if v.label in exclude_from_node]
    assert(len(root_nodes)<=1)
    print("Generating the '%s' graph..." % append)
    nodes = bfs(graph, graph.getVertex(root_nodes[0].getId()))
    exclude_nodes = []
    for exclude_root_node in exclude_node:
        tmp = bfs(graph, graph.getVertex(exclude_root_node.getId()))
        exclude_nodes.extend(tmp[1:])
    with open('%s_%s.gv' % (root_label, append), 'w') as output:
        used_nodes = []
        output.write('digraph RECO { graph [label = "%s", labelloc=top];\n' % root_label)
        for n in nodes:
            if (maxNodes is not None and len(used_nodes) >= int(maxNodes)) or n in exclude_nodes:
                continue
            index = n.getId()
            if index not in used_nodes:
                used_nodes.append(index)
                output.write('%d[label=%s, tooltip=%s];\n' % (index, vertices[index].label, vertices[index].tooltip))
            for child in n.getConnections():
                if child.getId() not in used_nodes:
                    if (len(exclude_from_node) != 0 and child in exclude_nodes):
                        continue
                    used_nodes.append(child.getId())
                    output.write('%d[label=%s, tooltip=%s];\n' % (child.getId(),
                                                                  vertices[child.getId()].label,
                                                                  vertices[child.getId()].tooltip))
                output.write('%d -> %d;\n' % (n.getId(), child.getId()))
                
        output.write('}\n')
        print("Graph processed.")
    (status, _) = commands.getstatusoutput('dot -Grankdir=LR -Gmindist=4.0 -Gsplines=ortho -v -T{outputFormat} {filename}_{append}.gv -o {filename}_{append}.{outputFormat}'.format(filename='%s' % root_label,
                                                                                                                                                                                    outputFormat=outputFormat,
                                                                                                                                                                                    append=append))
    if status != 0:
        print _
        sys.exit(1)
    print("Done.")

def searchAndPrintNode(dependency_file, label, outputFormat='pdf', maxNodes=None, exclude_from_node=[]):
    createGraph(dependency_file)
    toDotOutput(label, consumes, outputFormat, 'consumes', maxNodes, exclude_from_node)
    toDotOutput(label, is_consumed, outputFormat, 'is_consumed_by', maxNodes, exclude_from_node)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Explore CMSSW FWK dependency graph.')
  parser.add_argument('-f', '--filename',
                     default = None,
                     help = 'Dependency file to use to extract information.',
                     type = str,
                     required=True)
  parser.add_argument('-l', '--label',
                     default = '',
                     help = 'Label of the python module to use as the main vertex of the Graph.',
                     type = str,
                     required=False)
  parser.add_argument('-o', '--output',
                     default = 'pdf',
                     help = 'Output extension of the generated plots.',
                     type = str,
                     required=False)
  parser.add_argument('-m', '--maxNodes',
                     default = None,
                     help = 'Maximum number of nodes to plot (using BFS exploration of the graph).',
                     type = str,
                     required=False)
  parser.add_argument('--exclude_from_nodes', 
         	     nargs='*',
                     default = '',
	             help = 'List of python labels starting from which nodes will be pruned while exploring the graph.',
                     required=False,
                     type=str)
  args = parser.parse_args()
  print args
  searchAndPrintNode(args.filename, args.label, args.output, args.maxNodes, args.exclude_from_nodes)
#    fire.Fire(searchAndPrintNode)
