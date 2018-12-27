import numpy as np
import g2o

optimizer = g2o.SparseOptimizer()
optimizer.set_verbose(True)

optimizer.load("test.g2o")

print(optimizer.vertices()[0].get_estimate_data())
