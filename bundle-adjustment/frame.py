import numpy as np
import cv2
import g2o
from ba import BundleAdjustment
from utils import *
from viewer import Viewer
def getCorners(img):
  gray = cv2.cvtColor(im0,cv2.COLOR_BGR2GRAY)
  corners = cv2.goodFeaturesToTrack(gray, 10000,0.01, 3)
  corners = np.int0(corners)
  return corners

class Frame(object):
  Rt = np.eye(4)
  idxs_future = []
  idxs_prev = []
  def __init__(self, img, focal=2000, K=None):
    if K is not None:
      self.K = K
    else:
      self.K = np.array([[focal, 0, img.shape[1]//2],
                        [0, focal, img.shape[0]//2],
                        [0, 0, 1]])
    self.fx = self.K[0,0]
    self.fy = self.K[1,1]
    self.cx = self.K[1,2]
    self.cy = self.K[0,2]
    self.baseline = 0.01 #meters, not real
    self.focal = focal
    self.img = cv2.resize(img, (0,0), fx=0.2, fy=0.2)
    self.corners = getCorners(self.img)
    print(len(self.corners))
    self.corners, self.des = get_features_orb(self.img,self.corners)

    #self.colors = [bgr2rgb(im1)[int(cood[0]), int(coord[1]), :] for coord in self.corners]
  def orientation(self):
    return self.Rt[0:3, 0:3]

  def position(self):
    return self.Rt[:-1, :-1]

def matchFrames(f1, f2):
  des_idxs = np.array(match_frames(f1.des, f2.des, f1.corners, f2.corners))
  idxs, E = estimate_f_matrix(des_idxs, f1.corners, f2.corners, f1.K)
  pts4d, R, t, mask = get_R_t(E, f1.corners[idxs[:,0]], f2.corners[idxs[:,1]], f1.K)
  Rt = cvt2Rt(R,t)

  f2.Rt = np.dot(f1.Rt, Rt)


  f1.idxs_future = f1.corners[[mask[:,0]]]
  f2.idxs_prev = f2.corners[mask[:,1]]

  return pts4d, mask

if __name__ == "__main__":
  '''
  this code is absolutely disgusting
  '''
  f0 = 'data/0.jpg'
  f1 = 'data/1.jpg'
  f2 = 'data/2.jpg'

  im0 = cv2.imread(f0)
  im1 = cv2.imread(f1)
  im2 = cv2.imread(f2)

  frame0 = Frame(im0)
  frame1 = Frame(im1)
  frame2 = Frame(im2)

  pt1, mask1 = matchFrames(frame0, frame1)
  pt2, mask2 = matchFrames(frame1, frame2)
  pt2 = np.dot(pt2, frame2.Rt)

  ba = BundleAdjustment()

  ba.add_pose(0, frame0, frame0)
  ba.add_pose(1, frame1, frame1)
  ba.add_pose(2, frame2, frame2)
  print('pt1: ', len(pt1))
  print('mask1: ', len(mask1))
  for i, point in enumerate(pt1):
    print(i)
    ba.add_point(i,point)
    pt_id = i
    ba.add_edge(i, 0, frame0.corners[mask1[i,0]])
    ba.add_edge(i, 1, frame1.corners[mask1[i,1]])
  pt_id += 1
  for i, point in enumerate(pt2):
    ba.add_point(i+pt_id, point)
    ba.add_edge(i+pt_id, 1, frame1.corners[mask2[i,0]])
    ba.add_edge(i+pt_id, 2, frame2.corners[mask2[i,1]])
    g = i

  ba.optimize()
  vertices = [ba.get_pose(i).matrix() for i in range(3)]
  pt1 = [ba.get_point(i) for i in range(pt_id+g+1)]

  i#pt1.extend(pt2)

  viewer = Viewer(vertices, pt1)



