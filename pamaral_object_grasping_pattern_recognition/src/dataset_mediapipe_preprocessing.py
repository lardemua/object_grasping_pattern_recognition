#!/usr/bin/env python3

import json
import os
import rosbag
import rospy

from sensor_msgs.msg import Image

from pamaral_object_grasping_pattern_recognition.msg import MpResults


class DatasetMediaPipePreprocessing:

    def __init__(self, input_folder, output_image_topic, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

        # Iterate over all files in the folder
        self.filenames = []
        for filename in os.listdir(input_folder):
            # Create the absolute path to the file
            bag_path = os.path.join(input_folder, filename)

            # Check if the file path is a file (not a directory)
            if os.path.isfile(bag_path) and bag_path.endswith(".bag"):
                self.filenames.append(filename)
        
        # Create the Image Publisher        
        self.image_publisher = rospy.Publisher(output_image_topic, Image, queue_size=1)
        self.preprocessed_points_sub = rospy.Subscriber("mediapipe_results", MpResults, self.mediapipe_results_callback)

    def mediapipe_results_callback(self, msg):
        # Extract the data from the message
        hands = [{
            'handedness': h.handedness.data,
            "hand_landmarks": [[p.x, p.y, p.z] for p in h.hand_landmarks],
            "hand_world_landmarks": [[p.x, p.y, p.z] for p in h.hand_world_landmarks]
        } for h in msg.hands]

        if msg.pose is not None:
            pose = {
                "pose_landmarks": [[p.x, p.y, p.z] for p in msg.pose.pose_landmarks],
                "pose_world_landmarks": [[p.x, p.y, p.z] for p in msg.pose.pose_world_landmarks]
            }
        else:
            pose = None

        self.data.append({
            'hands': hands,
            'pose': pose
        })

        if len(self.messages) > 0:
            self.image_publisher.publish(self.messages.pop(0))
        
        else:
            # Save the data to a JSON file
            rospy.loginfo("Saving {} to a JSON file".format(self.filenames[0]))
            with open(os.path.join(self.output_folder, self.filenames.pop(0)[:-4] + ".json"), 'a+') as file:
                json.dump(self.data, file)
            
            self.read_next_bag_file()
    
    def read_next_bag_file(self):
        if len(self.filenames) > 0:
            # Reset the data
            self.data = []

            # Read the bag file
            bag = rosbag.Bag(os.path.join(self.input_folder, self.filenames[0]))
            msgs = bag.read_messages()

            # Sort the messages by publication timestamp
            msgs = sorted(msgs, key=lambda x: x[1].header.stamp.secs * 1e9 + x[1].header.stamp.nsecs)
            
            self.messages = [x[1] for x in msgs]

            # Publish 1st message
            self.image_publisher.publish(self.messages.pop(0))
        
        else:
            print("All bag files processed")


def main():
    default_node_name = 'dataset_mediapipe_processing'
    rospy.init_node(default_node_name, anonymous=False)

    input_folder = rospy.get_param(rospy.search_param('input_folder'))
    output_image_topic = rospy.get_param(rospy.search_param('output_image_topic'))
    output_folder = rospy.get_param(rospy.search_param('output_folder'))
    os.makedirs(output_folder, exist_ok=True)

    dataset_mediapipe_processing = DatasetMediaPipePreprocessing(input_folder=input_folder, output_image_topic=output_image_topic, output_folder=output_folder)

    input()

    dataset_mediapipe_processing.read_next_bag_file()

    rospy.spin()


if __name__ == '__main__':
    main()
