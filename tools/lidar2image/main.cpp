#include <Eigen/Core>
#include <vector>
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>
#include <pcl/common/transforms.h>
#include <opencv2/opencv.hpp>

using namespace pcl;
using namespace std;
using namespace Eigen;


int main() {
    Eigen::Matrix4d cam_to_imu;
    cam_to_imu.setIdentity();
    cam_to_imu.block<3,3>(0,0)<< 0.9999930,  0.0013607,  0.0034907,
            -0.0034799, -0.0078487,  0.9999632,
            0.0013880, -0.9999683, -0.0078439;

    cam_to_imu.block<3,1>(0,3)<<-0.1,0.11,0.11;

    Eigen::Matrix4d imu_to_cam;
    imu_to_cam.setIdentity();
    imu_to_cam.block<3,3>(0,0)=cam_to_imu.block<3,3>(0,0).transpose();
    imu_to_cam.block<3,1>(0,3)=-cam_to_imu.block<3,3>(0,0).transpose()*cam_to_imu.block<3,1>(0,3);

    Eigen::Matrix4d lidar_to_imu;
    lidar_to_imu<<1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0.28,
            0, 0, 0, 1;

    Eigen::Matrix<double,3,4> P;
    P<<264.9425, 0.0, 334.3975, 0.0,
            0.0, 264.79, 183.162, 0.0,
            0.0, 0.0, 1.0, 0.0;

    int W=672;
    int H=376;

    cv::Mat image=cv::imread("3.png",cv::IMREAD_COLOR);
    pcl::PointCloud<pcl::PointXYZ>::Ptr mls(new pcl::PointCloud<pcl::PointXYZ>());
    pcl::io::loadPCDFile<pcl::PointXYZ>("2.pcd", *mls);//2_pillar_car.pcd

    for (size_t i = 0; i < mls->points.size(); ++i) {
        Matrix<double,4,1> p_mls;
        p_mls<<mls->points[i].x,mls->points[i].y,mls->points[i].z,1;

        Vector3d p_homo=P*imu_to_cam*lidar_to_imu*p_mls;

        double px=p_homo(0)/p_homo(2);
        double py=p_homo(1)/p_homo(2);

        int px_round=int(round(px));
        int py_round=int(round(py));
        if(p_homo(2)>0.1&&px_round>=0&&px_round<=W-1&&py_round>=0&&py_round<=H-1)
        {
            cv::Point pp=cv::Point(px_round,py_round);

            //select ground roughly
            if(mls->points[i].z>-2.2&&mls->points[i].z<-1.9)
            {
                cv::circle(image,pp,0.1, cv::Scalar(0, 0, 255), -1);
            }
            else
            {
                cv::circle(image,pp,0.1, cv::Scalar(255, 0, 0), -1);
            }
        }
    }

    cv::imshow("Image with Points", image);

    cv::imwrite("proj2.png",image);


    cv::waitKey(0);
    return 1;
}
