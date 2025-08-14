
# Convert LL to UTM
import numpy as np
import math
import pymap3d as pm

# Converts GPS data to poses in the ENU frame
def convert_novatel_to_pose(novatel,convert_body_frame):
  # first novatel data
  gps_msg = novatel[0];
  poses = [];
  timestamps = [];
  FIRST_RUN = True;
  origin = [];
  origin_roll= 0; 
  origin_pitch= 0;
  origin_yaw = 0;

  timestamp = float(gps_msg[0])
  lat = float(gps_msg[3])+float(gps_msg[4])/60+float(gps_msg[5])/3600;

  lon = float(gps_msg[6])+float(gps_msg[7])/60+float(gps_msg[8])/3600;
  ele = float(gps_msg[9]);
  roll = np.deg2rad(float(gps_msg[16]));
  pitch = np.deg2rad(float(gps_msg[17]));
  azimuth = float(gps_msg[18]);
  yaw = np.deg2rad(-1.0 * azimuth);

  c_phi = math.cos(roll);
  s_phi = math.sin(roll);
  c_theta = math.cos(pitch);
  s_theta = math.sin(pitch);
  c_psi = math.cos(yaw);
  s_psi = math.sin(yaw);

  # The body here refers to the LiDAR frame. ENU refers to the n frame
  # Assuming the first point is the starting point of the ENU system.
  # the ENU frame and the SPANIMU frame are aligned at the origin, with only one attitude difference.
  T_SPANIMU_2_ENU = np.matrix([
      [c_psi * c_phi - s_psi * s_theta * s_phi, -s_psi * c_theta, c_psi * s_phi + s_psi * s_theta * c_phi, 0],
      [s_psi * c_phi + c_psi * s_theta * s_phi, c_psi * c_theta, s_psi * s_phi - c_psi * s_theta * c_phi, 0],
      [-c_theta * s_phi, s_theta, c_theta * c_phi, 0],
      [0.0, 0.0, 0.0, 1.0]])

  # T_body_to_SPANIMU: rotation is the unit matrix, translation is [0, 0, 0.42]; They are the sensors’ extrinsic parameters.
  # T_body_2_ENU is the pose of the LiDAR frame at time 0 in the ENU frame
  T_body_to_SPANIMU = np.eye(4)
  T_body_to_SPANIMU[2, 3] = 0.42
  T_body_2_ENU =  T_SPANIMU_2_ENU *  T_body_to_SPANIMU

  if FIRST_RUN:
    origin = [lat,lon, ele];
    origin_roll=roll;
    origin_yaw=yaw;
    origin_pitch=pitch;
    FIRST_RUN = False;

  for gps_msg in novatel:
    timestamp = float(gps_msg[0])
    timestamps.append(timestamp);
    lat = float(gps_msg[3])+float(gps_msg[4])/60+float(gps_msg[5])/3600;
    lon = float(gps_msg[6])+float(gps_msg[7])/60+float(gps_msg[8])/3600;
    ele = float(gps_msg[9]);

    # ENU based on first node
    enu_x, enu_y, enu_z = pm.geodetic2enu(lat, lon, ele, origin[0], origin[1], origin[2]);

    roll = np.deg2rad(float(gps_msg[16]));
    pitch = np.deg2rad(float(gps_msg[17]));
   # Azimuth = north at 0 degrees, east at 90 degrees, south at 180 degrees and west at 270 degrees
    azimuth = float(gps_msg[18]);
    # yaw = north at 0 deg, 90 at west and 180 at south, east at 270 deg
    yaw = np.deg2rad(-1.0 * azimuth);

    c_phi = math.cos(roll);
    s_phi = math.sin(roll);
    c_theta = math.cos(pitch);
    s_theta = math.sin(pitch);
    c_psi = math.cos(yaw);
    s_psi = math.sin(yaw);

    # This is the T_locallevel_body transform where ENU is the local level frame
    # https://hexagondownloads.blob.core.windows.net/public/Novatel/assets/Documents/Bulletins/apn037/apn037.pdf

    pose = np.matrix([
      [c_psi * c_phi - s_psi * s_theta * s_phi, -s_psi * c_theta, c_psi * s_phi + s_psi * s_theta * c_phi, enu_x],
      [s_psi * c_phi + c_psi * s_theta * s_phi, c_psi * c_theta, s_psi * s_phi - c_psi * s_theta * c_phi, enu_y],
      [-c_theta * s_phi, s_theta, c_theta * c_phi, enu_z],
      [0.0, 0.0, 0.0, 1.0]])
    if convert_body_frame:
      # The mathematical expression: T_SPANIMU_2_LiDAR0 = T_ENU_2_LiDAR0 * T_SPANIMU_2_ENU
      pose = np.linalg.inv(T_body_2_ENU) * pose
      # LiDAR0 is the first LiDAR frame at time 0; LiDAR is the moving LiDAR frame.
      # The mathematical expression: T_LiDAR_2_LiDAR0 = T_SPANIMU_2_LiDAR0 * T_LiDAR_2_SPANIMU
      pose = pose * T_body_to_SPANIMU
    poses.append(pose);

  return poses, timestamps;
