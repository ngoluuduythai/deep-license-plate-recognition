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
import petro_backend

import time
#import datetime
 



# os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=
        'Read license plates from a RTSP stream and save the result in a CSV file.',
        epilog=
        'For example: python anpr_camera_stream.py --camera rtsp://admin:123abc456@minhtuanvt2019.ddns.net:554/Streaming/channels/101 --api-key 61f6ac27c3d2584e6d0ffd33a98de4a94fcb33ed --regions vn --output /path/to/output.csv'
    )
    parser.add_argument('--api-key', help='Your API key.', required=True)
    parser.add_argument('--camera', help='RTSP stream url.', required=True)
    parser.add_argument('--regions', help='Regions e.g vn.', required=False)
    parser.add_argument('--output', help='csv output file ', required=True)
    
    return parser.parse_args()

def startVideoCap(args):
    currentDT = datetime.now()
    print("%s Start video capture " % str(currentDT))
    cap = cv2.VideoCapture(args.camera)

    if not cap.isOpened():
        print(" @ Error: OpenCV VideoCapture is not opened : {}".format(args.camera))
        return False

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = cap.get(5)
    Codec = cap.get(6)
    NumOfFrames = cap.get(7) #CAP_PROP_FRAME_COUNT
    print('Num of frames: %d, Codec: %s' % (NumOfFrames, Codec))
   
    camera_id = args.camera.rsplit('/', 1)[1] + '_'    
    print(camera_id)
    print(" # {} : ({:d} x {:d}) @ {:5.2f} Hz".
                         format(args.camera, frame_width, frame_height, fps))
    
    with open(args.output, 'a') as output:
        fields = ['date', 'license_plate', 'score', 'dscore', 'vehicle_type']
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        if (cap.isOpened()):
        #while(cap.isOpened()):
            print('still cap.isOpened')
            ret, frame = cap.read()
            #print('ret: %s, frame: %s' % (ret, frame))
            print('ret: %s' % (ret))
            imgByteArr = io.BytesIO()
            # if (frame is None):
            #     startVideoCap(args)
            #     print("xxx None")
            #     continue
            print("xxx else")

            im = Image.fromarray(frame)
            im.save(imgByteArr, 'JPEG')
            cv2.waitKey(1)
            imgByteArr.seek(0)
            response = requests.post(
                'https://api.platerecognizer.com/v1/plate-reader/',
                files=dict(upload=imgByteArr),
                data=dict(regions=args.regions or ''),
                headers={'Authorization': 'Token ' + args.api_key})  
            res = response.json()
            print(response)
            print(res)

            if len(res['results']) > 0:
                for result in res['results']:
                        data = dict(
                            date=datetime.today().strftime('%x %X'),
                            license_plate = result['plate'],
                            score = result['score'],
                            dscore = result['dscore'],
                            vehicle_type = result['vehicle']['type']
                        )
                        print("---save data---")
                        print(data)
                        writer.writerow(data)
                        output.flush()
        
        cap.release()
        cv2.destroyAllWindows()
        print("Start sleeping 10 seconds %s" % str(datetime.now()))
        time.sleep(10)
        print("Sleeped 10 seconds %s" % str(datetime.now()))
        startVideoCap(args)

def main():
    #print("main petro_backend 2")
    #petro_backend.main()
    #petro_backend.fetch_camera()
    args = parse_arguments()
    startVideoCap(args)
   


if __name__ == "__main__":
    main()
