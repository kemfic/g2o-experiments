notes
---

[.g2o file format](https://github.com/RainerKuemmerle/g2o/wiki/File-Format)
---

### vertices

3d pose
  - ```VERTEX_SE3:QUAT id x y z qx qy qz qw```

3d point
  - ```VERTEX_TRACKXYZ id x y z```

### edges
  - ```EDGE_SE3:QUAT id1 id2 measurement information_matrix```


**getting Rt matrix from vertex**
 - ```optimizer.vertex(index).estimate().matrix()```
 - ```matrices = [vertex.estimate().matrix() for vertex in optimizer.vertices.values()]```

**getting vertices from edge**
 - ```edges``` is a SET of ```edge``` elements?
 - ```edge.vertices()``` returns a list of vertex objects, shape: [n, 2]
