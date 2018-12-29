import numpy as np
import g2o
import pangolin as pango
import OpenGL.GL as gl

optimizer = g2o.SparseOptimizer()
optimizer.set_verbose(True)

optimizer.load("data/sphere2500.g2o")

vertices = [i.estimate().matrix() for i in optimizer.vertices().values()]
print(np.shape(vertices))
edges = []
for edge in optimizer.edges():
  edges.append([edge.vertices()[0].estimate().matrix(), edge.vertices()[1].estimate().matrix()])
edges = np.array(edges)

rotator = np.array([[0.0, 0.0, 1.0, 0.0],
                    [1.0, 0.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 1.0]])

vertices = np.dot(vertices, rotator)

pango.CreateWindowAndBind('Main', 640, 480)
gl.glEnable(gl.GL_DEPTH_TEST)

# Define Projection and initial ModelView matrix
scam = pango.OpenGlRenderState(
  pango.ProjectionMatrix(640, 480, 420, 420, 320, 240, 0.2, 2000000),
  pango.ModelViewLookAt(-2, 2, -2, 0, 0, 0, pango.AxisDirection.AxisY))
handler = pango.Handler3D(scam)

# Create Interactive View in window
dcam = pango.CreateDisplay()
dcam.SetBounds(0.0, 1.0, 0.0, 1.0, -640.0/480.0)
dcam.SetHandler(handler)

while not pango.ShouldQuit():
  gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
  gl.glClearColor(0.15, 0.15, 0.15, 1.0)
  dcam.Activate(scam)

  gl.glPointSize(5)
  gl.glColor3f(1.0,1.0,1.0)
  pango.DrawCameras(vertices)

  gl.glColor3f(0.0, 0.7,0.4)
  pango.DrawLines(edges[:,0,:-1,-1 ], edges[:,1,:-1,-1])

  pango.FinishFrame()
