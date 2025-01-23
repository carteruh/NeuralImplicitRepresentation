import os
import shutil

'''
The script changes PARIS data format to appropriate format
'''

def organize_images(object_name, object_id, states, data_types, root):
    # Set the directory paths based on the object_name and object_id
    for data_type in data_types:
        stage_dir = os.path.join(root, data_type)
        for state in states:
            state_dir = os.path.join(stage_dir, state)
            
            if not os.path.exists(state_dir):
                print(f"Directory does not exist: {state_dir}")
                continue

            # Define parent folder (mask folder in your case)
            data_folder = stage_dir
            if not os.path.exists(data_folder):
                os.makedirs(data_folder)
            
            # Iterate over the images and rename them according to the state
            for idx, file_name in enumerate(sorted(os.listdir(state_dir))):
                # Make sure we only handle files with .png extension
                if not file_name.endswith('.png'):
                    continue

                # Set the new file name based on the state (00000 or 00001)
                if state == 'start':
                    new_file_name = f"00000_{str(idx).zfill(3)}.png"
                elif state == 'end':
                    new_file_name = f"00001_{str(idx).zfill(3)}.png"
                else:
                    continue

                # Full path to the original file
                old_file_path = os.path.join(state_dir, file_name)
                # Full path to the new file location in the mask folder
                new_file_path = os.path.join(data_folder, new_file_name)

                # Move and rename the file
                print(f"Moving {old_file_path} to {new_file_path}")
                shutil.move(old_file_path, new_file_path)

if __name__ == "__main__":
    object_name = 'knife'
    object_id = '101217'
    states = ['start', 'end']
    data_type = ['color_segmented', 'mask','depth_filtered']
    root = f'/media/qil/DATA/Carter_Articulated_Objects/NeuralImplicitRepresentation/data/paris/{object_name}_{object_id}_train_set'
    
    organize_images(object_name, object_id, states, data_type, root)
