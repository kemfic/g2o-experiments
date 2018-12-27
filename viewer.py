import numpy as np
import pangolin as pango
from multiprocessing import Process, Queue
import OpenGL.GL as gl

class Viewer(object):
  '''
  3D viewer, since python bindings didn't include them
  '''
  def __init__(self):
    self.state = None
    self.q = Queue()
    self.vt = Process(target=self.viewer_thread, args=(self.q,))
    self.vt.daemon = True
    self.vt.start()

    self.vertices, self.edges = [], []

  def viewer_thread(self, q):
    self.viewer_init()

    while not pango.ShouldQuit():
      self.viewer_refresh(q)

  def viewer_init(self):
    w, h = (1024, 768)

    pango.CreateWindowAndBind("viewer", w, h)
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
