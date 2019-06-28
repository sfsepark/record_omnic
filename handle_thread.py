import time, image, os, signal
import cv2
import threading
import Queue

from imageManager import imageManager
from element import ElementManager
from statManager import StatManager
from print_log import print_log

# handle video data
class Handle_Thread(threading.Thread):
    def __init__(self, stream_buffer, isTest = True) :
        threading.Thread.__init__(self)
        self.matcher = pubg_match.Pubg()
        self.cooldown = False
        self.cooldowntime = time.time()
        self.element_manager= ElementManager.__call__()
        self.stat_manager = StatManager.__call__()
        self.isTest = isTest
        self.stream_buffer = stream_buffer
        self.HandleStreamOn = True
 
    def stream_ON(self) :
        self.HandleStreamOn = True
    def stream_OFF(self) :
        self.HandleStreamOn = False

    def run(self) :
        # print_log("Start Handle") 
        sharp_count = -1
        sharp_pt = -1
        search_count = -1

        while self.HandleStreamOn or (not stream_buffer.empty()):
            if not stream_buffer.empty() :
                video_name = stream_buffer.get()
                print_log("grade searching start  : " + video_name)
                vidcap = cv2.VideoCapture(video_name)

                count = 0

                while vidcap.isOpened() and self.cooldown < time.time():
                    success, cap_image = vidcap.read()
                    if success:
                        # not found sharp
                        if sharp_pt == -1  and count % 15 == 0 :
                            #self.matcher.image_process(cap_image)
                            #sharp_pt = self.matcher.sharp_search(count)
                            if sharp_pt == -1 and sharp_count > 0:
                                sharp_count = sharp_count -1 ;

                        # after searching sharp
                        if(sharp_pt != -1) :
                            sharp_count = 10
                            search_count += 1

                            self.matcher.image_process(cap_image)
                            sharp_pt = self.matcher.sharp_search(count)
                            if sharp_pt != -1 :
                                self.matcher.grade_search(sharp_pt, count)

                        # clear triggers
                        if sharp_count == 0 or search_count >= 30 :
                            search_count = 0
                            sharp_count = -1
                            sharp_pt = -1

                            grade = self.element_manager.get_number(0)
                            total = self.element_manager.get_number(1)

                            self.stat_manager.send_log(grade, total, isTest)

                            self.cooldown = time.time() + 60

                            self.element_manager.clear()
                            print_log('element_manager_clear()')
                            break
                        count += 1
                    else:
                        break
                cv2.destroyAllWindows()
                vidcap.release()

                os.remove(video_name)
                #print_log("Done : " + video_name)

