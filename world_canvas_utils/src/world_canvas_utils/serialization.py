#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2014, Yujin Robot
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Author: Jorge Santos

import genpy
import rospy
import roslib
import cStringIO as StringIO


class SerializationError(Exception):
    pass

def serializeMsg(msg):
    try:
        buffer = StringIO.StringIO()
        rospy.msg.serialize_message(buffer, 0, msg)
        ser_msg = buffer.getvalue()
    except rospy.exceptions.ROSSerializationException as e:
        raise SerializationError('Serialization failed: %s' % str(e))
    else:
        return ser_msg
    finally:
        buffer.close()

def deserializeMsg(ser_msg, msg_class):
    try:
        msg_queue = list()
        buffer = StringIO.StringIO()
        buffer.write(ser_msg)
        rospy.msg.deserialize_messages(buffer, msg_queue, msg_class)
    except genpy.DeserializationError as e:
        raise SerializationError('Deserialization failed: %s' % str(e))
    else:
        if len(msg_queue) == 0:
            # Probably deserialize_messages would had raised an exception instead
            raise SerializationError('Deserialization returned 0 messages')
        if len(msg_queue) > 1:
            # This should be impossible
            rospy.logwarn("More than one object deserialized (%d)!" % len(msg_queue))
        return msg_queue.pop()
    finally:
        buffer.close()
