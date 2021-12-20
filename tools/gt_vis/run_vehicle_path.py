#!/usr/bin/env python

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import quaternion

import matplotlib.pyplot as plt

import load_novatel_data, convert_novatel_to_pose

convert_body_frame = False;

novatel_path = 'data/UrbanNav_TST_GT.txt';
#novatel_path = 'UrbanNav_whampoa.txt';
# raw data
novatel = load_novatel_data.load_novatel_data(novatel_path);
# convert to ENU
poses, timestamps = convert_novatel_to_pose.convert_novatel_to_pose(novatel,convert_body_frame);

#output pose to files as tum format for SLAM comparison purpose
fo = open("test.txt", "w")
frame = 0;
for pose in poses:
  #following tum format
  print(pose[0:3,0:3])

  # rot = np.matrix([pose[0,0],pose[0,1],pose[0,2]],
  #              [pose[1,0],pose[1,1],pose[1,2]],
  #              [pose[2,0],pose[2,1],pose[2,2]]);
  qua = quaternion.from_rotation_matrix(pose[0:3,0:3]);
  pose_str = str(timestamps[frame])+" "+ str(pose[0,3]) +" "+ str(pose[1,3]) + " "+str(pose[2,3])+" "+str(qua.x) + " "+ str(qua.y)+ " " +str(qua.z)+" "+ str(qua.w) +"\n";
  frame = frame+1;
  fo.write( pose_str )

fo.close()

mpl.rcParams['legend.fontsize'] = 10

fig = plt.figure()
ax = fig.gca(projection='3d')
if convert_body_frame:
  ax.set_title('Vehicle path in Body Frame')
  ax.set_xlabel('x (m)')
  ax.set_ylabel('y (m)')
  ax.set_zlabel('z (m)')
else:
  ax.set_title('Vehicle path in ENU Frame')
  ax.set_xlabel('East (m)')
  ax.set_ylabel('North (m)')
  ax.set_zlabel('Up (m)')

length = 5
A = np.matrix([[0, 0, 0, 1],
               [length, 0, 0, 1],
               [0, 0, 0, 1],
               [0, length, 0, 1],
               [0, 0, 0, 1],
               [0, 0, length, 1]]).transpose();

for pose in poses:
  B = np.matmul(pose, A);
  ax.plot([B[0,0], B[0,1]], [B[1,0], B[1,1]],[B[2,0],B[2,1]], 'r-'); # x: red
  ax.plot([B[0,2], B[0,3]], [B[1,2], B[1,3]],[B[2,2],B[2,3]], 'g-'); # y: green
  ax.plot([B[0,4], B[0,5]], [B[1,4], B[1,5]],[B[2,4],B[2,5]], 'b-'); # z: blue

# Equal axis doesn't seem to work so set an arbitrary limit to the z axis
ax.set_zlim3d(-100,100)

plt.show()
