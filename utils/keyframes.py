import json
import numpy as np
import os

def transform_and_save_keyframes(start_file, end_file, output_file):
    def load_json(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)

    def process_camera_data(camera_data, frame_prefix):
        keyframe_dict = {}
        for idx, key in enumerate(sorted(camera_data.keys())):
            if key == 'K':  # Skip the intrinsic matrix part if not needed
                continue
            matrix = camera_data[key]
            keyframe_name = f"{frame_prefix}_{str(idx).zfill(3)}"
            # Flatten the matrix from top to bottom and left to right for keyframe format
            if frame_prefix == 'frame_00001':
                time = 1
            else:
                time = 0
                
            keyframe_dict[keyframe_name] = {
                'cam_in_ob': [item for sublist in matrix for item in sublist],
                'time': time
            }
        return keyframe_dict

    # Load start and end state camera data
    start_camera_data = load_json(start_file)
    end_camera_data = load_json(end_file)

    # Process both the start and end states
    start_keyframes = process_camera_data(start_camera_data, 'frame_00000')
    end_keyframes = process_camera_data(end_camera_data, 'frame_00001')

    # Merge keyframes from both start and end into one dictionary
    all_keyframes = {**start_keyframes, **end_keyframes}

    # Save the result to the output file in YAML-like format
    with open(output_file, 'w') as f:
        for key, value in all_keyframes.items():
            f.write(f"{key}:\n")
            f.write("  cam_in_ob:\n")
            for i in range(0, 16, 4):
                f.write(f"    - {value['cam_in_ob'][i]} \n    - {value['cam_in_ob'][i+1]}\n    - {value['cam_in_ob'][i+2]}\n    - {value['cam_in_ob'][i+3]}\n")
            f.write(f"  time: {value['time']}\n")


if __name__ == "__main__":
    object_name = 'knife'
    object_id = '101217'
    root = f'/media/qil/DATA/Carter_Articulated_Objects/NeuralImplicitRepresentation/data/paris/{object_name}_{object_id}_train_set'

    # File paths for the start and end trans.json files
    start_file = os.path.join(root, 'camera_start.json')
    end_file = os.path.join(root, 'camera_end.json')
    output_file = os.path.join(root, 'init_keyframes.yml')

    # Generate keyframes
    transform_and_save_keyframes(start_file, end_file, output_file)

