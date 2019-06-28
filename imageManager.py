'''
pubg.tnya.kr
    PUBG grade live tracking system

    LAST CHANGE : 2017-11-06
    developer : sfsepark@gmail.com
'''

import cv2
import numpy as np
import os
import time
import operator
from elementManager import ElementManager
from singleton import SingletonType

class imageManager:

    '''
    USAGE CYCLE
    Init your image using image_process(cap_image) .
    -> find sharp(#) element and get sharp_pt using sharp_search() .
    -> find each element using grade_search() .
    '''

    __metaclass__ = SingletonType

    def __init__(self) :
        self.template = {'sharp': cv2.imread('./template_720p/yellow_sharp.png',0)}
        self.template['sharp_mask'] = cv2.imread('./template_720p/yellow_sharp_mask.png',0)

        for i in range(10) :
            self.template['gray_mask_' + str(i)] = cv2.imread('./template_720p/gray_mask_' + str(i) + '.png' , 0)
            self.template['yellow_' + str(i)] = cv2.imread('./template_720p/yellow_' + str(i) +'.png',0)
            
        element_manager = ElementManager.__call__()

        for key in self.template.keys() :
            height, width = self.template[key].shape
            element_manager.template_width[key] = width

    #------------- START OF BASED FUNCTION DEFINITON -------------------------
    #template match based edged image
    def template_match(self,img_edges, template,threshold):
        res = cv2.matchTemplate(img_edges,template,cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            return zip(*loc[::-1])
        return None
    #------------- END OF BASED FUNCTION DEFINITION --------------------------

    #if you use sharp_search, and gray_search, use this function first.
    def image_process(self, cap_image) :
        #crop and edge detect with Canny edge detection
        height, width,channel  = cap_image.shape
        crop_height, crop_width = height / 6 ,width / 5
        self.crop_image = cap_image[0:crop_height, width - crop_width - 1: width - 1]
        self.end_crop_image = cap_image[height / 10:height/10*2,0:width/2]

        self.canny_image = cv2.Canny(self.crop_image,100,200)
        self.resolutions = height

    #------------- START OF ELEMENT SEARCH FUNCTION DEFINITION ---------------------------------
    
    #detect image has yellow zone.
    def end_detect(self, count = 0) :
        hsv = cv2.cvtColor(self.end_crop_image, cv2.COLOR_BGR2HSV)

        upper_bound = np.array([25 , 250, 243])
        lower_bound = np.array([23 , 244, 237])

        #cv2.imwrite('./capture/' + str(self.resolutions) + 'p_' + str(count) + '.png', self.end_crop_image)
        #print(count)
        yellow_filtered = cv2.inRange(hsv, lower_bound, upper_bound)
        
        detected = False

        for w in yellow_filtered :
            for p in w :
                if p != 0 :
                    detected = True
                    break
            if detected == True :
                break

        if detected == True :
            print('detected ' + str(count))

        return detected

    #MUST use image_process(cap_image) first.
    def sharp_search(self,count = 0) :
        #matching
        match_res = self.template_match(self.canny_image, self.template['sharp'], 0.6)
 
        if(match_res is None) :
            return -1
        else :
            return match_res[0][0]

    #search the yellow(grade) number.
    def yellow_search(self,count=0) :

        element_manager = ElementManager.__call__()

        for i in range(10) :
            res = self.template_match(self.canny_image, self.template['yellow_' + str(i)], 0.6)
            
            if res is not None :
                element_manager.add_info(0, i, res)

  #      cv2.imwrite('./capture/for_crop_' + str(count)+ '.png', self.crop_image)
 #       cv2.imwrite('./capture/for_canny_' + str(count) + '.png', self.canny_image)


    def crop_gray(self,count=0) :
        element_manager = ElementManager.__call__()
        
        start_pt = element_manager.get_gray_start_pt() - 5
        self.gray_croped_image = self.crop_image[48:108 , start_pt : 230]

    #search the gray(total) number.
    def gray_search(self,count=0) :
        element_manager = ElementManager.__call__()
 
        hsv = cv2.cvtColor(self.gray_croped_image, cv2.COLOR_BGR2HSV)

        upper_bound = np.array([179,120,250])
        lower_bound = np.array([0,0,240])

        while lower_bound[2] > 30 :
            checked = True
            lower_bound[2] -= 2

            gray_filtered = cv2.inRange(hsv, lower_bound, upper_bound)

            for i in range(10) :
                res = self.template_match(gray_filtered , self.template['gray_mask_' + str(i)], 0.7)
                if res is not None :
                    element_manager.add_info(1, i , res)
       # print(count)
       # print(upper_bound, lower_bound)

    # position of points.        
    # sharp_pt -> yellow_number -> slash_pt -> gray_number

    #--------------- END OF ELEMENT SEARCH FUNCTION -------------------------------------

    def grade_search(self, sharpt_pt, count = 0) :
        self.yellow_search(count = count)
        self.crop_gray(count = count)
        self.gray_search(count = count) 
