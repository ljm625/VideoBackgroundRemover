
import argparse

import glob
import time
import torch
import os
import shutil
import numpy as np
from tqdm import tqdm
import traceback
from PIL import Image
import cv2
from transformers import AutoModelForImageSegmentation
from pathlib import Path
from utilities import preprocess_image, postprocess_image 
from ImageCreator import ImageCreator
from VideoCreator import VideoCreator

def run(source_video,output_video,background_color=(255,255,255),work_dir="tmp",disable_cleanup=False):

    if not os.path.exists(Path(source_video)):
        print(f"{source_video} not found, please check")
        return
    vid = cv2.VideoCapture(Path(source_video))
    fps = vid.get(cv2.CAP_PROP_FPS)
    vid.release()

    net = AutoModelForImageSegmentation.from_pretrained("briaai/RMBG-1.4", trust_remote_code=True)
    device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Using device {device}")
    torch_device = torch.device(device)
    net.to(device)
    if not disable_cleanup:
        if os.path.exists(Path(work_dir)/"input"):
            shutil.rmtree(Path(work_dir)/"input")
        if os.path.exists(Path(work_dir)/"output"):
            shutil.rmtree(Path(work_dir)/"output")

    os.makedirs(Path(work_dir)/"input",exist_ok=True)
    folder_path = os.path.join(Path(work_dir),"input")
    image_files_png = glob.glob(os.path.join(folder_path, "frame*.png"))
    if not image_files_png:
        creator = ImageCreator(Path(source_video),folder_path)
        creator.get_images()
    image_files_png = glob.glob(os.path.join(folder_path, "frame*.png"))
    output_dir = os.path.join(Path(work_dir),"output")
    os.makedirs(output_dir, exist_ok=True)
    image_files_png =sorted(image_files_png)
    for im_path in tqdm(image_files_png):
        try:
            filename = os.path.basename(im_path)
            op_path = os.path.join(output_dir,filename)
            if os.path.exists(op_path):
                continue
            orig_im_file = Image.open(im_path).convert("RGB")
            model_input_size = [1024, 1024]
            orig_im = np.array(orig_im_file)
            orig_im_size = orig_im.shape[0:2]
            image = preprocess_image(orig_im, model_input_size)
            image = image.to(torch_device)
            result = net(image)
            result_image = postprocess_image(result[0][0], orig_im_size)
            pil_im = Image.fromarray(result_image)
            no_bg_image = Image.new("RGBA", pil_im.size, (0, 0, 0, 0))
            no_bg_image.paste(orig_im_file, mask=pil_im)
            color_background = Image.new("RGB", no_bg_image.size, background_color)
            color_background.paste(no_bg_image, (0, 0), no_bg_image)
            output_path = os.path.join(output_dir, filename)
            color_background.save(output_path)
        except Exception as e:
            print(f"Failed processing {im_path}: {e}")
            traceback.print_exc()
            continue
    v= VideoCreator(output_dir,Path(output_video))
    v.create_video(fps)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--video",
        default="video.mp4",
        type=str,
        help="path to the video",
    )
    parser.add_argument(
        "--tmp-dir",
        type=str,
        default="tmp",
        help="path to the directory in which all input frames will be stored",
    )
    parser.add_argument(
        "--output-video",
        type=str,
        default="output.mp4",
        help="path to store the output video",
    )
    parser.add_argument(
        "--background-color",
        type=str,
        default="white",
        help="background color, can use white,green or #000FFF, default use white",
    )

    parser.add_argument(
        "--skip-cleanup",
        type=bool,
        default=False,
        help="Skip cleanup process, useful if needs additional manual steps, or want to skip vid2img",
    )

    args = parser.parse_args()
    run(args.video,args.output_video,args.background_color,args.tmp_dir,args.skip_cleanup)
