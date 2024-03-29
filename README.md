# object-grasping-pattern-recognition

Object Recognition using the Object's Grasping Pattern

## Installation Guide

1. Install [ROS Noetic](https://wiki.ros.org/noetic/Installation/Ubuntu).

2. Follow the instructions in the [larcc_drivers repository](https://github.com/lardemua/larcc_drivers).

3. Next clone this repository into your catkin workspace:

    ```
    cd ~/catkin_ws/src
    git clone https://github.com/lardemua/object_grasping_pattern_recognition.git
    ```

4. Compile the catkin workspace:

    ```
    cd ~/catkin_ws && catkin_make
    ```

5. Install python requirements:

    ```
    cd ~/catkin_ws/src/object_grasping_pattern_recognition
    pip install -r requirements.txt
    ```

6. Download MediaPipe task models:
    
    ```
    cd ~/catkin_ws/src/object_grasping_pattern_recognition/pamaral_object_grasping_pattern_recognition/models
    wget https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/latest/pose_landmarker_lite.task
    wget https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_full/float16/latest/pose_landmarker_full.task
    wget https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/latest/pose_landmarker_heavy.task
    wget https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task
    ```

## Usage Guide

### Record Data as Bag Files

```
roslaunch pamaral_object_grasping_pattern_recognition dataset_recording.launch
```

### Extract MediaPipe Data from Bag Files

```
roslaunch pamaral_object_grasping_pattern_recognition dataset_mediapipe_preprocessing.launch
```

### Data Preprocessing

```
roslaunch pamaral_object_grasping_pattern_recognition dataset_keypoints_preprocessing.launch
```

### Train Model

```
cd model_training
python3 cnn_main.py
```

or 

```
cd model_training
python3 transformer_main.py
```
