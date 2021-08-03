# Data Usage
## GNSS 
Data preparation
- Download the RINEX observation &lt;Date&gt;\.&lt;scenario&gt;\.&lt;place&gt;\.&lt;receiver&gt;\.obs
- Download the Ephemeris data, e.g. [SatRef](https://www.geodetic.gov.hk/en/rinex/downv.aspx) from Hong Kong Lands Department 

![Data preparation](img/gnss_1.png)

Using GNSS library for post-processing and evaluation
- Opensource GNSS evaluation tools: GUI, C++: RTKLIB, MATLAB: goGPS

![Processing](img/gnss_2.png)


## Visual Inertial Odometry 
Data preparation,
- Download the bag file;
- Clone the [VINS-Fusion](https://github.com/HKUST-Aerial-Robotics/VINS-Fusion) repository from GitHub;
- Update camera intrinsics and extrinsics in the yaml file;
- Run the framework of VINS-Fusion:
```
roslaunch vins vins_rviz.launch
rosrun vins vins_node ~/catkin_ws/src/VINS-Fusion/config/vi_car/vi_car.yaml
rosbag play DATASET.bag
```

## LiDAR Inertial Odometry
- Take scenario (a) as an example
Download the rosbag [UrbanNav-HK-TST-20210517](https://www.dropbox.com/s/mit5v1yo8pzh9xq/UrbanNav-HK_TST-20210517_sensors.bag?dl=0)
- Prepared the [fine-tune LIO-SAM](https://www.dropbox.com/s/g514ra8zm6nfz9r/LIO-SAM_for_urban.zip?dl=0) base on the intrinsic and extrinsic. 
```
roslaunch lio_sam run_velodyne.launch
```
- Replay the Rosbag
```
rosbag play UrbanNav-HK_TST-20210517_sensors.bag
```
![Processing](img/lidar_1.png)
