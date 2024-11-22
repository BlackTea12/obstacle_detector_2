cmake_minimum_required(VERSION 3.5)
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()
project(obstacle_detector)

# set(CMAKE_CXX_FLAGS "-std=c++11 -fpermissive ${CMAKE_CXX_FLAGS} -Wfatal-errors\ ")

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(visualization_msgs REQUIRED)
find_package(std_srvs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(laser_geometry REQUIRED)
find_package(builtin_interfaces REQUIRED)
find_package(rosidl_default_generators REQUIRED)

find_package(Armadillo REQUIRED)
find_package(Boost 1.54.0 REQUIRED system)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/CircleObstacle.msg"
  "msg/Obstacles.msg"
  "msg/SegmentObstacle.msg"
  DEPENDENCIES geometry_msgs std_msgs builtin_interfaces 
)

set(PROJECT_INCLUDE_DIRS include)
set(PROJECT_DEPENDS "rclcpp" "std_msgs" "nav_msgs" "std_srvs" "visualization_msgs" "geometry_msgs" "sensor_msgs" "tf2" "tf2_geometry_msgs" "tf2_ros" "laser_geometry" "rosidl_default_generators")

include_directories(include ${PROJECT_INCLUDE_DIRS} ${ARMADILLO_INCLUDE_DIRS} ${Boost_INCLUDE_DIRS})

#
# Build libs
add_library(obstacle_extractor src/obstacle_extractor.cpp)
target_link_libraries(obstacle_extractor ${ARMADILLO_LIBRARIES})
ament_target_dependencies(obstacle_extractor ${PROJECT_DEPENDS})
# allow the project to link against its own messages
rosidl_get_typesupport_target(cpp_typesupport_target "${PROJECT_NAME}" "rosidl_typesupport_cpp")
target_link_libraries(obstacle_extractor "${cpp_typesupport_target}")

add_library(obstacle_tracker src/obstacle_tracker.cpp)
target_link_libraries(obstacle_tracker ${ARMADILLO_LIBRARIES})
ament_target_dependencies(obstacle_tracker ${PROJECT_DEPENDS})
# allow the project to link against its own messages
rosidl_get_typesupport_target(cpp_typesupport_target "${PROJECT_NAME}" "rosidl_typesupport_cpp")
target_link_libraries(obstacle_tracker "${cpp_typesupport_target}")

add_library(obstacle_publisher src/obstacle_publisher.cpp)
target_link_libraries(obstacle_publisher ${ARMADILLO_LIBRARIES})
ament_target_dependencies(obstacle_publisher ${PROJECT_DEPENDS})
# allow the project to link against its own messages
rosidl_get_typesupport_target(cpp_typesupport_target "${PROJECT_NAME}" "rosidl_typesupport_cpp")
target_link_libraries(obstacle_publisher "${cpp_typesupport_target}")

add_executable(obstacle_extractor_node src/nodes/obstacle_extractor_node.cpp)
target_link_libraries(obstacle_extractor_node obstacle_extractor)

add_executable(obstacle_tracker_node src/nodes/obstacle_tracker_node.cpp)
target_link_libraries(obstacle_tracker_node obstacle_tracker)

add_executable(obstacle_publisher_node src/nodes/obstacle_publisher_node.cpp)
target_link_libraries(obstacle_publisher_node obstacle_publisher)

install(TARGETS obstacle_extractor obstacle_tracker obstacle_publisher
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

install(TARGETS obstacle_extractor_node obstacle_tracker_node obstacle_publisher_node
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

install(
  DIRECTORY
  launch config rviz
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()