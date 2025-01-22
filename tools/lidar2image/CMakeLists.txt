cmake_minimum_required(VERSION 3.21)
project(lidar2image)

find_package(Eigen3 REQUIRED)
find_package(PCL REQUIRED)
find_package(OpenCV REQUIRED)

include_directories(
        ${EIGEN3_INCLUDE_DIR}
        ${PCL_INCLUDE_DIRS})
set(CMAKE_CXX_STANDARD 17)

link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})
add_executable(lidar2image main.cpp)

target_link_libraries(lidar2image ${PCL_LIBRARIES}  ${OpenCV_LIBS})
