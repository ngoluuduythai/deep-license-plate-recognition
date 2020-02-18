#!/usr/bin/env python
from __future__ import absolute_import, division, print_function

import argparse
import csv
import io
import os
from datetime import datetime
from threading import Thread

import cv2
import requests
from PIL import Image

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

def parse_arguments():
    parser = argparse.ArgumentParser(
        description=
        'Read backend request',
        epilog=
        'For example: python petro_backend.py --camera rtsp://admin:123abc456@minhtuanvt2019.ddns.net:554/Streaming/channels/101 --api-key 61f6ac27c3d2584e6d0ffd33a98de4a94fcb33ed --regions vn --output /path/to/output.csv'
    )
    parser.add_argument('--url', help='Petro Backend Url.', required=True)
    parser.add_argument('--plate_number', help='plate number.', required=True)
    parser.add_argument('--accurate', help='Accurrate percent', required=False)
    
    return parser.parse_args()

def camera_request(cameraId, url, plateNumber, Accurate):
    
    print("Requesting to petro backend url: %s" % url)
    reqData = {
     'camera_id' : cameraId,
     'plate_number': plateNumber, 
     'accurate_percent' : Accurate
    }

    response = requests.put(url, json = reqData)

    # response = requests.post(
    #             'https://dev.petroapi.zensmartcity.com/api/v1',
    #             files=dict(upload=imgByteArr),
    #             data=dict(regions=args.regions or ''),
    #             headers={'Authorization': 'Token ' + args.api_key})  
    res = response.json()
    print(res)
    print("Status %s" % res["status"])
    if (res["status"] == 'error'):

          print("response: error code: %s, Message: %s" % (res["error"], res["message"]))
    else:
        print("response: success")

def fetch_camera():
    url = 'https://dev.petroapi.zensmartcity.com/api/v1/cameras'
    requests.get(url, json = reqData)

def main():
   #args = parse_arguments()
   cameraId = 'camerab44c7eca627a292c4091d5418d2df132'
   url = 'https://dev.petroapi.zensmartcity.com/api/v1/camera_requests'
   plateNumber = '51F1-4567'
   Accurate = 90

   camera_request(cameraId, url, plateNumber, Accurate)
   


if __name__ == "__main__":
    main()
