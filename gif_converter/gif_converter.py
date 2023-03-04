"""Gif Converter

This tool convert from video file (ex. mp4) to gif file.
"""

import argparse
from PIL import Image
import cv2


def ArgParser():
    """Parse Arguments
    
    This function parses arguments and return argparse object.
    """
    parser = argparse.ArgumentParser(description='This tool convert from video file (ex. mp4) to gif file.',
                formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--input_file', dest='input_file', type=str, default=None, required=True, \
            help='Input file path')
    parser.add_argument('--output_file', dest='output_file', type=str, default=None, required=True, \
            help='Output file path')

    args = parser.parse_args()

    return args

def Video2Frame(video_path):
    """Video to Frame
    
    This function convert to frame data from video file
    
    Args:
        video_path (str): specify input video file path
    
    Returns:
        list of frame data and video frame rate
    """
    
    cap = cv2.VideoCapture(video_path)
    if (not cap.isOpened()):
        return None, None
    
    frame_data = []
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    
    while (True):
        ret, frame = cap.read()
        if (ret):
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_pillow = Image.fromarray(frame_rgb)
            frame_data.append(frame_pillow)
        else:
            break
    
    print('[Video file info]')
    print(f'  - frame rate: {frame_rate}')
    print(f'  - frame num: {len(frame_data)}')
    print(f'  - duration of video file: {frame_rate * len(frame_data):.02f}[sec]')
    
    return frame_data, frame_rate

def CreateGif(frame_data, frame_rate, output_file):
    """Create GIF
    
    This function creates GIF file from frame data.
    
    Args:
        frame_data (list): frame data
        frame_rate (float): frame rate of input video file
        output_file (str): output gif file path
    """
    
    duration = int(1000.0 / frame_rate)
    frame_data[0].save(output_file, save_all=True, append_images=frame_data[1:], duration=duration, loop=0)

def main():
    """Main function
    
    This function is main function.
    """
    args = ArgParser()
    print('args.input_file : {}'.format(args.input_file))
    print('args.output_file : {}'.format(args.output_file))

    frame_data, frame_rate = Video2Frame(args.input_file)
    CreateGif(frame_data, frame_rate, args.output_file)
    
    return

if __name__ == '__main__':
    main()

