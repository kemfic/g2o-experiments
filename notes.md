notes
---

### [.g2o file format](https://github.com/RainerKuemmerle/g2o/wiki/File-Format)

#### vertices

3d pose
  - VERTEX_SE3:QUAT id x y z qx qy qz qw

3d point
  - VERTEX_TRACKXYZ id x y z

#### edges
  - EDGE_SE3:QUAT id1 id2
