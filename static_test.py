'''
pubg.tnya.kr
    PUBG grade live tracking system

    LAST CHANGE : 2017-10-14
    developer : sfsepark@gmail.com
'''

import pubg_match
from element import ElementManager

import cv2
import time, image,os
import sys

pubg = pubg_match.Pubg()

vidcap = cv2.VideoCapture(sys.argv[1])
count = 0
sharp_pt = -1

element_manager = ElementManager.__call__()

element_manager.clear()

while vidcap.isOpened():
    success, cap_image = vidcap.read()
    if success:
        if(count % 3 == 0) :
            if(sharp_pt == -1 and count % 30 == 0) : 
                pubg.image_process(cap_image)
                sharp_pt = pubg.sharp_search(count)
            if(sharp_pt != -1) :
                pubg.image_process(cap_image)
                cv2.imwrite('./capture/cap_f_' + str(count) + '.png' , cap_image)
                sharp_pt = pubg.sharp_search(count)
                if(sharp_pt != -1) :
                    pubg.grade_search(sharp_pt,count)
        count += 1
    else:
        break
cv2.destroyAllWindows()
vidcap.release()

print('yellow'+str(element_manager.yellow_info))
print('gray' + str(element_manager.gray_info))

grade = element_manager.get_number(0)
total = element_manager.get_number(1)

print(grade, total)
      
