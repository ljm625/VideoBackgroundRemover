# Video Background Removal Tool base on RMBG-1.4

The Video Background Removal Tool is designed to enable users to effortlessly remove backgrounds from videos. 

It's able to run on NVIDIA CUDA / Apple Silicon / CPU environment.


<p align="center">
  <table>
    <tr>
      <td>
        <img src="assets/orig.gif" width="385" height="216" />
      </td>
      <td>
        <img src="assets/result.gif" width="385" height="216" />
      </td>
    </tr>
  </table>
</p>

## Contents

Table of contents:

- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)

## Installation

```bash
git clone https://github.com/ljm625/VideoBackgroundRemover
cd VideoBackgroundRemover
# Create virtual environment section, optional but recommended
python3 -m venv venv
source venv/bin/activate
# Create virtual environment section, optional but recommended
pip install -r requirements.txt
```

## Usage

### Command line

```bash
usage: main.py [-h] [--video VIDEO] [--tmp-dir TMP_DIR] [--output-video OUTPUT_VIDEO] [--background-color BACKGROUND_COLOR] [--skip-cleanup SKIP_CLEANUP]

options:
  -h, --help            show this help message and exit
  --video VIDEO         path to the video
  --tmp-dir TMP_DIR     path to the directory in which all input frames will be stored
  --output-video OUTPUT_VIDEO
                        path to store the output video
  --background-color BACKGROUND_COLOR
                        background color, can use white,green or #000FFF, default use white
  --skip-cleanup SKIP_CLEANUP
                        Skip cleanup process, useful if needs additional manual steps, or want to skip vid2img
```
## Example

The following command line is a working example from a video stored in the repo:

```bash
python3 main.py --video assets/example.mp4 --tmp-dir ./tmp --output-video output.mp4 --background-color green
```

