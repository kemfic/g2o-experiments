import g2o
import numpy as np
from viewer import *
import sys
class Graph3D(object):
  nodes = []
  edges = []
  def __init__(self, verbose=False):
    self.solver = g2o.BlockSolverSE3(g2o.LinearSolverEigenSE3())
    self.solver=  g2o.OptimizationAlgorithmLevenberg(self.solver)

    self.optimizer = g2o.SparseOptimizer()
    self.optimizer.set_verbose(verbose)
    self.optimizer.set_algorithm(self.solver)

  def load_file(self, fname):
    self.optimizer.load(fname)
    print("vertices: ", len(self.optimizer.vertices()))
    print("edges: ", len(self.optimizer.edges()))

    for edge in self.optimizer.edges():
      self.edges.append([edge.vertices()[0].estimate().matrix(), edge.vertices()[1].estimate().matrix()])

    self.nodes = np.array([i.estimate().matrix() for i in self.optimizer.vertices().values()])
    self.nodes = np.array(self.nodes)
    self.edges = np.array(self.edges)

  def optimize(self):
    return None


if __name__ == "__main__":
  if len(sys.argv) > 1:
    gfile = str(sys.argv[1])
  else:
    gfile = "data/garage.g2o"

  graph = Graph3D()
  graph.load_file(gfile)
  print("loaded")
  viewer = Viewer3D(graph.nodes, graph.edges)
  print("viewer instantiated")




