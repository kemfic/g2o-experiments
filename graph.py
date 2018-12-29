import g2o
import numpy as np
from viewer import Viewer3D
import pangolin as pango


class Graph(object):
  vertices = []
  edges = []
  def __init__(self, verbose=False):
    self.solver = g2o.BlockSolverSE3(g2o.LinearSolverEigenSE3())
    self.solver=  g2o.OptimizationAlgorithmLevengerg(self.solver)

    self.optimizer = g2o.SparseOptimizer()
    self.optimizer.set_verbose(verbose)
    self.optimizer.set_algorithm(self.solver)

  def load_file(self, fname):
    self.optimizer.load(fname)
    print("vertices: ", len(self.optimizer.vertices()))
    print("edges: ", len(self.optimizer.edges()))

    for edge in self.optimizer.edges():
      self.edges.append([edge.vertices()[0].estimate().matrix(), edge.vertices()[1].estimate().matrix()])

    self.vertices = [i.estimate().matrix() for i in self.optimizer.vertices().values()]


  def optimize(self):
    return None


if __name__ == "__main__":
  if len(sys.argv)> 0:
    gfile = str(sys.argv[1])
  else:
    gfile = "data/garage.g2o"

  viewer = Viewer3D()
  graph = Graph()
  graph.load_file(gfile)

  while not pango.ShouldQuit():
    viewer.update(graph)





