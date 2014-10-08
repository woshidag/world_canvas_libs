#!/usr/bin/env python

import rospy
import copy

import world_canvas_client

from yocs_msgs.msg import *
from world_canvas_msgs.msg import *

if __name__ == '__main__':
    rospy.init_node('test_annotation_collection')
    topic_name  = rospy.get_param('~topic_name', 'annotations')
    topic_type  = rospy.get_param('~topic_type', None)
    pub_as_list = rospy.get_param('~pub_as_list', False)
    namespace   = rospy.get_param('~srv_namespace', '')
    world    = rospy.get_param('~world')
    uuids    = rospy.get_param('~uuids', [])
    names    = rospy.get_param('~names', [])
    types    = rospy.get_param('~types', [])
    keywords = rospy.get_param('~keywords', [])
    related  = rospy.get_param('~relationships', [])

    ac = world_canvas_client.AnnotationCollection(world, uuids, names, types, keywords, related, namespace)
    ac.loadData()
    walls = ac.getDataOfType(yocs_msgs.msg.Wall)
    columns = ac.getDataOfType(yocs_msgs.msg.Column)

    # Publish annotations' visual markers on client side
    ac.publishMarkers('annotation_markers')

    # Publish annotations on client side
    ac.publish(topic_name + '_client', topic_type, False, pub_as_list)

    # Request server to also publish the same annotations
    ac.publish(topic_name,             topic_type, True,  pub_as_list)

    # Add a couple of new annotation, delete one, and save the resulting collection
    annot1 = world_canvas_msgs.msg.Annotation()
    annot1.timestamp = rospy.Time.now()
    annot1.world     = world
    annot1.name      = 'New column 1'
    annot1.type      = 'yocs_msgs/Column'
    annot1.shape     = 3
    annot1.color.r   = 0.4
    annot1.color.g   = 0.7
    annot1.color.b   = 0.6
    annot1.color.a   = 0.9
    annot1.size.x    = 1.2
    annot1.size.y    = 1.2
    annot1.size.z    = 0.9
    annot1.pose.header.frame_id = '/map'
    annot1.pose.pose.pose.position.x = 2.2
    annot1.pose.pose.pose.position.y = 4.2
    annot1.pose.pose.pose.position.z = 0.45
    annot1.pose.pose.pose.orientation.w = 1
    annot1.keywords  = [ 'this', 'is', 'a', 'test', 'column' ]
    annot2 = copy.deepcopy(annot1)
    annot2.name      = 'New column 2'
    
    column1 = yocs_msgs.msg.Column()
    column1.name = annot1.name
    column1.radius = annot1.size.x
    column1.height = annot1.size.z
    column1.pose = copy.deepcopy(annot1.pose)
    column2 = copy.deepcopy(column1)

    ac.add(annot1, column1)
    ac.add(annot2, column2)
    column = ac.getData(annot1)
    ac.delete(annot2.id)
    ac.save()
    
    rospy.loginfo("Done")
    rospy.spin()
