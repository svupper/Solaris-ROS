#!/usr/bin/env python
import rospy
from geometry_msgs.msg  import Twist
from sensor_msgs.msg import MagneticField


class turtlebot():

	def __init__(self):
	#Creating our node,publisher and subscriber
		rospy.init_node('turtlebot_controller', anonymous=True)
		self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
		self.mgf_subscriber = rospy.Subscriber('/imu/mag', MagneticField, self.callback, queue_size = 100)
		self.rate = rospy.Rate(10)

	#Callback function implementing the mgf value received
	def callback(self, data):
		self.mgf = data.magnetic_field
		self.mgf_v.x = round(self.mgf.x, 4)
		self.mgf_v.y = round(self.mgf.y, 4)

	def oriente_equator(self):
		vel_msg = Twist()

		vel_msg.linear.x = 0
		vel_msg.linear.y = 0
		vel_msg.linear.z = 0

		#angular velocity in the z-axis:
		vel_msg.angular.x = 0
		vel_msg.angular.y = 0
		vel_msg.angular.z = 0

		while self.mgf_v.x<0:

			vel_msg.angular.z = 8

			#Publishing our vel_msg
			self.velocity_publisher.publish(vel_msg)
			self.rate.sleep()
		#Stopping our robot after the movement is over
		
		vel_msg.angular.z =0
		self.velocity_publisher.publish(vel_msg)

		rospy.spin()

	def keep_oriented(self):
		tolerance = input("Set your orientation tolerance:")
		vel_msg = Twist()

		vel_msg.linear.x = 0
		vel_msg.linear.y = 0
		vel_msg.linear.z = 0

		#angular velocity in the z-axis:
		vel_msg.angular.x = 0
		vel_msg.angular.y = 0
		vel_msg.angular.z = 0

		while True::
			if (self.mgf_v.y > (0.01 * tolerance)) :

				vel_msg.angular.z = 4

				self.velocity_publisher.publish(vel_msg)

				rospy.spin()

			elif (self.mgf_v.y < (-0.01 * tolerance)):

				vel_msg.angular.z = -4

				self.velocity_publisher.publish(vel_msg)

				rospy.spin()
			else :
				vel_msg.angular.z = 0

				self.velocity_publisher.publish(vel_msg)

				rospy.spin()



if __name__ == '__main__':
    try:
        
        x = turtlebot()
        x.oriente_equator()	#This function make sure the orientation is good even in south equator
	x.keep_oriented()	#Processing function

    except rospy.ROSInterruptException: 
	pass
