# Copyright (c) 2024 HD Hyundai Robotics
#
# Licensed under the BSD 3-Clause License;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://opensource.org/licenses/BSD-3-Clause
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, PushRosNamespace
from launch.conditions import IfCondition
from launch_ros.descriptions import ParameterFile
from nav2_common.launch import RewrittenYaml, ReplaceString


def generate_launch_description():
  # Get the launch directory
  launch_dir = get_package_share_directory('obstacle_detector')

  # Create the launch configuration variables
  use_namespace = LaunchConfiguration('use_namespace')
  namespace = LaunchConfiguration('namespace')
  params_file = LaunchConfiguration('params_file')
  
  # Declare the launch arguments
  declare_use_namespace_cmd = DeclareLaunchArgument(
    'use_namespace',
    default_value='False',
    description='Wheter to use namespace or not')
  declare_namespace_cmd = DeclareLaunchArgument(
    'namespace',
    default_value='',
    description='Top-level namespace')
  declare_params_file_cmd = DeclareLaunchArgument(
    'params_file',
    default_value=os.path.join(launch_dir, 'config', 'tracker.yaml'),
    description='obstacle extractor parameter')
  
  param_substitutions = {}
  
  configured_params = ParameterFile(
    RewrittenYaml(
      source_file=params_file,
      root_key=namespace,
      param_rewrites=param_substitutions,
      convert_types=True),
    allow_substs=True)
  
  bringup_node_group = GroupAction([
    PushRosNamespace(
      condition=IfCondition(use_namespace),
      namespace=namespace),
      Node(
      name='obstacle_tracker',
      package='obstacle_detector',
      executable='obstacle_tracker_node',
      output='screen',
      respawn_delay=2.0,
      parameters=[configured_params],
      arguments=['--ros-args', '--log-level', "info"],
    )
  ])
  
  # Create the launch description and populate
  ld = LaunchDescription()

  ld.add_action(declare_use_namespace_cmd)
  ld.add_action(declare_namespace_cmd)
  ld.add_action(declare_params_file_cmd)

  ld.add_action(bringup_node_group)

  return ld
