from transformers import pipeline
from PIL import Image
import os

def RGB_to_depth(src_dir, dst_dir):
    # Create the destination directory if it doesn't exist
    os.makedirs(dst_dir, exist_ok=True)
    
    # Load the depth estimation pipeline
    pipe = pipeline(task="depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf")

    # Iterate over the images in the source directory
    for idx, filename in enumerate(sorted(os.listdir(src_dir))):
        # Filter for image files (assuming PNG, JPG, etc.)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(src_dir, filename)
            
            # Load the image
            image = Image.open(img_path)
            
            # Inference to get the depth image
            depth = pipe(image)["depth"]
            
            # # Construct the depth image filename
            # if state == 'start':
            #     depth_filename = f"00000_{str(idx).zfill(3)}.png"
            # else:
            #     depth_filename = f"00001_{str(idx).zfill(3)}.png"
            depth_path = os.path.join(dst_dir, filename)
            
            # Save the depth image
            depth.save(depth_path)
            print(f"Saved depth image: {depth_path}")

def main(root, states, stages): 

    src_dir = root
    dst_dir = os.path.join('/'.join(root.split('/')[:-2]), 'depth_filtered')
    os.makedirs(dst_dir, exist_ok=True)
    
    RGB_to_depth(src_dir=src_dir, dst_dir=dst_dir)

if __name__ == '__main__':
    object_name = 'knife'
    object_id = '101217'
    states = ['start', 'end']
    stages = ['test']
    root = f'/media/qil/DATA/Carter_Articulated_Objects/NeuralImplicitRepresentation/data/multi_part/{object_name}_{object_id}/new_color_segmented'

    main(root, states, stages)
