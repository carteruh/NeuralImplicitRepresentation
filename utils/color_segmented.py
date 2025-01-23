import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def color_segment_image(src_dir, dst_dir, state):
    # Iterate over the images in the source directory
    for idx, filename in enumerate(sorted(os.listdir(src_dir))):
        # Filter for image files (assuming PNG, JPG, etc.)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(src_dir, filename)
            
            
            image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE) # Load the image 
            image[image > 200] = 0 # Set all pixel values over 200 to 0
            
            if state == 'start':
                depth_filename = f"00000_{str(idx).zfill(3)}.png"
            else:
                depth_filename = f"00001_{str(idx).zfill(3)}.png"
            output_path = os.path.join(dst_dir, depth_filename)
            cv2.imwrite(output_path, image)
            print(f'saved: {output_path}')
            

def main(root, states, stages):
    for state in states:
        for stage in stages:
            src_dir = os.path.join(root, 'color_segmented', state, stage)
            dst_dir = os.path.join(root, 'new_color_segmented')
            os.makedirs(dst_dir, exist_ok=True)

            
            color_segment_image(src_dir=src_dir, dst_dir=dst_dir, state=state)

if __name__ == '__main__':
    object_name = 'knife'
    object_id = '101217'
    states = ['start', 'end']
    stages = ['test']
    root = f'/media/qil/DATA/Carter_Articulated_Objects/NeuralImplicitRepresentation/data/multi_part/{object_name}_{object_id}'

    main(root, states, stages)