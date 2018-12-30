import pangolin as pango
import numpy as np
import OpenGL.GL as gl
from multiprocessing import Process, Queue

class Viewer(object):
  '''
  3d viewer for g2o maps
    - based off ficiciSLAM's viewer
       - github.com/kemfic/ficiciSLAM
  '''
  is_optim = False
  tform = np.array([[0.0, 0.0, 1.0, 0.0],
                    [1.0, 0.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 1.0]])
  def __init__(self, vertices, pts):
    self.nodes = vertices
    self.pts = pts
    self.init()

    while not pango.ShouldQuit():
      self.refresh()


  def init(self):
    w, h = (1024,768)
    f = 2000 #420

    pango.CreateWindowAndBind("g2o_stuff", w, h)
    gl.glEnable(gl.GL_DEPTH_TEST)

    # Projection and ModelView Matrices
    self.scam = pango.OpenGlRenderState(
        pango.ProjectionMatrix(w, h, f, f, w //2, h//2, 0.1, 100000),
        pango.ModelViewLookAt(0, -50.0, -10.0,
                              0.0, 0.0, 0.0,
                              0.0, -1.0, 0.0))#pango.AxisDirection.AxisY))
    self.handler = pango.Handler3D(self.scam)

    # Interactive View in Window
    self.dcam = pango.CreateDisplay()
    self.dcam.SetBounds(0.0, 1.0, 0.0, 1.0, -w/h)
    self.dcam.SetHandler(self.handler)
    self.dcam.Activate()

  def refresh(self):
    #clear and activate screen
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glClearColor(0.15, 0.15, 0.15, 0.0)
    #gl.glClearColor(1.0, 1.0, 1.0, 0.0)

    self.dcam.Activate(self.scam)

    # render
    gl.glLineWidth(1)
    # render cameras
    if len(self.nodes) > 1:
      gl.glColor3f(1.0, 1.0, 1.0)
      pango.DrawCameras(self.nodes)
    # render edges
    gl.glColor3f(0.0, 0.8, 0.5)
    if len(self.pts) > 1:
      pango.DrawPoints(self.pts)
    pango.FinishFrame()
