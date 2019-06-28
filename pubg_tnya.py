'''
pubg.tnya.kr
    PUBG grade live tracking system

    LAST CHANGE : 2017-11-04

    VERSION 1.1.0
    SEE ./PATCHNOTE for patch.

    developer : sfsepark@gmail.com
'''

import pubg_match
from handle_thread import Handle_Thread
from get_stream_thread import GetStream_Thread
from end_check_trhead import End_Check_Thread
from element import ElementManager
from statManager import StatManager
from print_log import print_log

import time, image,os, signal
import threading
import Queue

import cv2
from livestreamer import Livestreamer
import sys
from stream_check import Stream_check

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
#Handling stream is on when streamer plays pubg. 
while True :
    if stream_check.check_playing_pubg() :
        print_log('Streamer ' + sys.argv[1] + ' plays PUBG')
        livestreamer = Livestreamer()
        livestreamer.set_option('http-headers','Client-ID=03uamzu42b8grbcd174vfm02ta6vv4')
        
        plugin = livestreamer.resolve_url("http://twitch.tv/" + sys.argv[1])
        streamer = sys.argv[1]
        streams = plugin.get_streams()
        worst_stream = streams['160p']
        best_stream = streams['best']
        
        worst_stream_buffer =  Queue.Queue()
        best_stream_buffer = Queue.Queue()

        getWorstThread = GetStream_Thread(worst_stream, worst_stream_buffer)
        getBestThread = GetStream_Thread(best_stream, best_stream_buffer)
        endcheckThread = End_Check_Thread(worst_stream_buffer)
        
        handleThread

        getWorstThread.stream_ON()
        getBestThread.stream_OFF()
        getWorstThread.start()
        endcheckThread.start()

        while True :
             if endcheckThread.status == False :
                getWorstThread.stream_OFF()

                getBestThread.stream_ON()
                getBestThread.start()

                endcheckThread.join()
                getWorstThread.join()
                endcheckThread.start()

             if  playing_check_time + 300 <  time.time():
                if stream_check.check_playing_pubg() :
                    break
                else :
                    playing_check_time = time.time()

            time.sleep(1)
        
        print_log('Streamer ' + sys.argv[1] + ' turn off PUBG')

        gsthread.stream_OFF()
        endcheckThread.stream_OFF()

        gsthread.join()
        endcheckThread.join()
    else :
        time.sleep(300)
