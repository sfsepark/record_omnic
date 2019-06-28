import threading
import time, image,os
import sys

import cv2
from print_log import print_log
from imageManager import imageManager

class End_Check_Thread(threading.Thread):
    def __init__(self, stream_buffer) :
        threading.Thread.__init__(self)
        self.stream_buffer = stream_buffer
        self.status = True

        self.pubg = imageManager.__call__()

    def run(self):
        while self.status == True :
            if not stream_buffer.empty() :
                video_name = stream_buffer.get()
                print_log("end searching start : " + video_name)
                vidcap = cv2.VideoCapture(video_name)

                count = 0
                detected = False

                while vidcap.isOpened() :
                    success, cap_image = vidcap.read()
                    if success :
                        if(count %3 == 0) :
                            pubg.image_process(cap_image)
                            detect = pubg.end_detect(count)
                            if detected == True :
                                break
                        count += 1
                    else:
                         break

                cv2.destroyAllWindows()
                vidcap.release()

                if detected == True :
                    self.status = False
                    

