import threading
import Queue

from livestreamer import Livestreamer
import sys
from stream_check import Stream_check

#get stream and put data to stream buffer

class GetStream_Thread(threading.Thread):
    def __init__(self,stream, stream_buffer) :
        threading.Thread.__init__(self)
        self.stream_buffer = stream_buffer
        self.GetStreamOn = False
        self.stream = stream

    def stream_ON(self):
        self.GetStreamOn = True
    def stream_OFF(self) :
        self.GetStreamOn = False

    def run(self) :
    
        print_log("Start Get Stream")

        
        while self.GetStreamOn :

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

