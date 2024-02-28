import rclpy
import math
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class PibDriver:
    def init(self, webots_node, properties):
        self.__robot = webots_node.robot

        self.__devices = {}

        self.__devices['tilt_sideways_motor'] = self.__robot.getDevice('head_horizontal')
        self.__devices['tilt_forward_motor'] = self.__robot.getDevice('head_vertical')
        self.__devices['shoulder_horizontal_right'] = self.__robot.getDevice('shoulder_horizontal_right')
        self.__devices['elbow_right'] = self.__robot.getDevice('ellbow_right')
        self.__devices['elbow_left'] = self.__robot.getDevice('ellbow_left')

        self.__devices['lower_arm_right'] = self.__robot.getDevice('forearm_right')
        self.__devices['lower_arm_left'] = self.__robot.getDevice('forearm_left')

        self.__target_trajectory = JointTrajectory()

        rclpy.init(args=None)
        self.__node = rclpy.create_node('pib_driver')
        self.__node.get_logger().info("nach create node")
        self.__node.create_subscription(JointTrajectory, '/joint_trajectory', self.__trajectory_callback, 1)
        self.__node.get_logger().info("nach create subscribe")

    def __cmd_vel_callback(self, twist):
        self.__target_twist = twist

    def __trajectory_callback(self, trajectory):
        self.__target_trajectory = trajectory
        self.__node.get_logger().info("trajectory callback " + trajectory.joint_names[0] + '  ' + str(trajectory.points[0].positions[0]))


    def step(self):
        rclpy.spin_once(self.__node, timeout_sec=0)

        if len(self.__target_trajectory.joint_names) > 0:
            name = self.__target_trajectory.joint_names[0]
            if not (name in self.__devices):
                rotIndex = name.find('rota')
                if rotIndex != -1 :
                    device = name[:(rotIndex-1)]
                else:
                    device = name
                self.__devices[name] = self.__robot.getDevice(device)
                self.__node.get_logger().info('created device: ' + device + '   name: ' + name)
            position = math.radians(self.__target_trajectory.points[0].positions[0]/100.0)
            if self.__devices[name] is not None:
                self.__devices[name].setPosition(position)
