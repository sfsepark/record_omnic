import numpy as np
import cv2
import os
import sys

template = {}

for i in range(0,10) :
    template[i] = cv2.imread('./template_720p/gray_mask_' +str( i) + '.png',0)

test_744 = cv2.imread(sys.argv[1],-1)
hsv = cv2.cvtColor(test_744, cv2.COLOR_BGR2HSV)

upper_bound = np.array([179,120,250])
lower_bound = np.array([0,0,240])
"""
while upper_bound[2] > 70 :
    finded = False
    gf = cv2.inRange(hsv, lower_bound, upper_bound)

    for i in range(len(gf)) : 
        for j in range(len(gf[i])) :
            if gf[i][j] !=  0 :
                finded = True
                break

    if finded :
        break

    upper_bound[2] -= 10
    lower_bound[2] -= 10

lower_bound[2] = upper_bound[2] 
"""

print(hsv[0][len(hsv[0]) - 1])

while lower_bound[2] > 0 :

    lower_bound[2] -= 2

    gf = cv2.inRange(hsv, lower_bound, upper_bound)

    cv2.imwrite('./test_capture/gf_'+ str(lower_bound[2])+ '.png',gf)

    print('v : ' + str(lower_bound[2]))
    for j in range(10) :
        print('number : ' + str(j))
        res = cv2.matchTemplate(gf, template[j], cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.7)
        print(zip(*loc[::-1]))
