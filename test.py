import numpy as np
import g2o

optimizer = g2o.SparseOptimizer()
optimizer.set_verbose(True)

optimizer.load("data/sphere2500.g2o")

vertices = [i.estimate().matrix() for i in optimizer.vertices().values()]


