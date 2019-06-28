'''
pubg.tnya.kr
    PUBG grade live tracking system

    LAST CHANGE : 2017-10-24

    VERSION 1.0.0

    developer : sfsepark@gmail.com
'''

import pubg_match
from element import ElementManager
from statManager import StatManager

import time, image,os, signal
import threading
import Queue

import cv2
from livestreamer import Livestreamer
import sys
from stream_check import Stream_check

# change to a stream that is actually online

stream_buffer =  Queue.Queue()
#
GetStreamOn = True
HandleStreamOn = True

def print_log(log_text) :
    print('[' + time.strftime("%Y_%m_%d_%H_%M_%S") + '] : ' + str(log_text))

# handle video data
class Handle_Thread(threading.Thread):
    def __init__(self, isTest = True) :
        threading.Thread.__init__(self)
        self.matcher = pubg_match.Pubg()
        self.cooldown = False
        self.cooldowntime = time.time()
        self.element_manager= ElementManager.__call__()
        self.stat_manager = StatManager.__call__()
        self.isTest = isTest

    def run(self) :
        # print_log("Start Handle") 
        sharp_count = -1
        sharp_pt = -1
        search_count = -1

        while HandleStreamOn or (not stream_buffer.empty()):
            if not stream_buffer.empty() :
                video_name = stream_buffer.get()
                print_log("capture start  : " + video_name)
                vidcap = cv2.VideoCapture(video_name)

                count = 0

                while vidcap.isOpened() and self.cooldown < time.time():
                    success, cap_image = vidcap.read()
                    if success:
                        # not found sharp
                        if sharp_pt == -1  and count % 30 == 0 :
                            self.matcher.image_process(cap_image)
                            sharp_pt = self.matcher.sharp_search(count)
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

                #os.remove(video_name)
                #print_log("Done : " + video_name)


# get stream and put data to stream buffer

class GetStream_Thread(threading.Thread):
    def __init__(self,stream) :
        threading.Thread.__init__(self)
        self.stream = stream
#        self.stream_buffer = stream_buffer

    def run(self) :
    
        print_log("Start Get Stream")

        
        while GetStreamOn :

            fd = self.stream.open()

            data = ''
            file_name = "./buffer/" + time.strftime("%Y_%m_%d_%H_%M_%S") + "_" + streamer
 
            print_log("Open : " + time.strftime("%H_%M_%S"))

            with open(file_name,"wb") as f :
                end_time = time.time() + 3.0
                while time.time() < end_time:
                    data += fd.read(1024)

                if not data == '' :
                    f.write(data)
                    stream_buffer.put(file_name)

            print_log("Closed : " + time.strftime("%H_%M_%S"))

            fd.close()

#--------------- main -------------------

print_log('*** PUBG STAT TRACKER START - [' + sys.argv[1] + '] ***')

isTest = True

stream_check = Stream_check(sys.argv[1])

user_id = stream_check.get_user_id() 

if user_id == -2 :
    print_log('Request Error. Maybe you should change clien-id')
    exit()
elif user_id == -1 :
    print_log('WRONG STREAMER NAME')
    exit()
    
if len(sys.argv) > 2 and sys.argv[2] == 'REAL' :
    print_log("!!!!!!!!!!!!!!!!CAUTION!!!!!!!!!!!!!!!!")
    print_log("This is NOT TEST")
    isTest = False
else :
    isTest = True
handleThread = Handle_Thread(isTest)

#Handling stream is on when streamer plays pubg. 
while True :
    if stream_check.check_playing_pubg() :
        print_log('Streamer ' + sys.argv[1] + ' plays PUBG')
        GetStreamOn = True
        HandleStreamOn = True

        livestreamer = Livestreamer()
        livestreamer.set_option('http-headers','Client-ID=03uamzu42b8grbcd174vfm02ta6vv4')
        
        plugin = livestreamer.resolve_url("http://twitch.tv/" + sys.argv[1])
        streamer = sys.argv[1]
        streams = plugin.get_streams()
        stream = streams['720p60']

        gsthread = GetStream_Thread(stream)
        
        gsthread.start()
        handleThread.start()

        while stream_check.check_playing_pubg() :
            time.sleep(300)
        
        print_log('Streamer ' + sys.argv[1] + ' turn off PUBG')

        GetStreamOn = False
        HandleStreamOn = False

        gsthread.join()
        handleThread.join()
    else :
        time.sleep(300)
