import os

import cv2
from tqdm import tqdm


class VideoCreator:
    def __init__(self, imgs_dir, vid_name, pbar=True):
        """
        :param str imgs_dir: The directory where the image files are stored.
        :param str vid_name: The name of the video's filename.
        :param bool pbar: Whether to display a progress bar.
        """

        self.imgs_dir = imgs_dir
        self.video_filename = vid_name
        self.pbar = pbar

    def create_video(self, fps=30):
        filenames = sorted(os.listdir(self.imgs_dir))
        height, width, _ = cv2.imread(self.imgs_dir + "/" + filenames[0]).shape
        size = (width, height)
        out = cv2.VideoWriter(
            self.video_filename, cv2.VideoWriter_fourcc(*"MJPG"), fps, size
        )
        print("Recording video...")
        if self.pbar:
            pb = tqdm(range(len(filenames)))
        else:
            pb = range(len(filenames))
        for i in pb:
            complete_filename = self.imgs_dir + "/" + filenames[i]
            img = cv2.imread(complete_filename)
            out.write(img)
        out.release()
        print("Done.")
