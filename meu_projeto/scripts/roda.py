#! /usr/bin/env python
# -*- coding:utf-8 -*-

import rospy
from geometry_msgs.msg import Twist, Vector3

v = 10  # Velocidade linear
w = 5  # Velocidade angular

if __name__ == "__main__":
    rospy.init_node("roda_exemplo")
    velocidade_saida = rospy.Publisher("cmd_vel", Twist, queue_size=3)

    try:
        while not rospy.is_shutdown():
            # vel = Twist(Vector3(v,0,0), Vector3(0,0,w))
            # pub.publish(vel)
            vel = Twist(Vector3(0.3, 0, 0), Vector3(0, 0, 0))
            velocidade_saida.publish(vel)
            rospy.sleep(3)

            
            vel = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0.61))            
            velocidade_saida.publish(vel)            
            rospy.sleep(2.75)

    except rospy.ROSInterruptException:
        print("Ocorreu uma exceção com o rospy")
