import pangolin as pango
import numpy as np
import OpenGl.GL as gl
from multiprocessing import Process, Queue

class Viewer(object):
  '''
  3d viewer for g2o maps
    - based off ficiciSLAM's old viewer
       - github.com/kemfic/ficiciSLAM
  '''
  def __init__(self):
    self.edges = None
    self.nodes = None
    self.q_edges = Queue()
    self.q_nodes = Queue()

    self.vt = Process(target=self.viewer_thread, args=(self.q_edges, self.q_nodes,))
    self.vt.daemon = True
    self.vt.start()

    self.nodes, self.edges = [], []

  def viewer_thread(self, q_edges, q_nodes):
    self.viewer_init()

    while not pango.ShouldQuit():
      self.viewer_refresh(q_edges, q_nodes)

  def viewer_init(self):
    w,h = (1024, 768)
    f = 2000

    pango.CreateWindowAndBind("g2o vis", w, h)
    gl.glEnable(gl.GL_DEPTH_TEST)

    #Projection and ModelView Matrices
    self.scam = pango.OpenGlRenderState(
        pango.ProjectionMatrix(w, h, f, f, w//2, h//2, 0.1, 100000),
        pango.ModelViewLookAt(0, -50.0, -10.0,
                              0.0, 0.0, 0.0,
                              0.0, -1.0, 0.0))
    self.handler = pango.Handler3D(self.scam)

    # Interactive View in Window
    self.dcam = pango.CreateDisplay()
    self.dcam.SetBounds(0.0, 1.0, 0.0, 1.0 -w/h)
    self.dcam.Activate()

  def viewer_refresh(self, q_edges, q_nodes):
    while not q_edges.empty():
      self.edges = q_edges.get()
    while not q_nodes.empty():
      self.nodes = q_nodes.get()
      #clear and activate screen
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glClearColor(0.15, 0.15, 0.15, 0.0)
    #gl.glClearColor(1.0, 1.0, 1.0, 0.0)

    self.dcam.Activate(self.scam)

    # render
    if self.edges is not None and self.nodes is not None:
      gl.glLineWidth(1)
      # render cameras
      if self.nodes.shape[0] >= 2:
        gl.glColor3f(1.0, 0.0, 1.0)
        pango.DrawCameras(self.nodes)
      # render edges
      if self.edges.shape[0] != 0:
        gl.glColor3f(0.2, 1.0, 0.2)
        pango.DrawLines(self.edges[:,0, :-1,-1], self.edges[:,1,:-1, -1])
    pango.FinishFrame()

  def update(self, nodes, edges);
    '''
    add new stuff to queues
    '''

    if self.q_edges is None or self.q_nodes is None:
      return

    tform = np.array([[0.0, 0.0, 1.0, 0.0],
                      [1.0, 0.0, 0.0, 0.0],
                      [0.0, 1.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 1.0]])

    self.nodes = np.dot(nodes, tform)
    self.edges = edges

    self.q_edges.put(self.edges)
    self.q_nodes.put(self.nodes)

  def stop(self):
    self.vt.terminate()
    self.vt.join()

    for x in self.__dict__.values():
      if isinstance(x, type(Queue())):
        while not x.empty():
          _ = x.get()

    print("viewer stopped")



