'''
pubg.tnya.kr
    PUBG grade live tracking system

    LAST CHANGE : 2017-10-18
    developer : sfsepark@gmail.com
'''

import cv2
import numpy as np
import os
import time
import operator

class Pubg:

    def __init__(self) :
        self.template = {'sharp': cv2.imread('./template_720p/yellow_sharp.png',0)}

        for i in range(10) :
            self.template['yellow_' + str(i)] = cv2.imread('./template_720p/yellow_' + str(i) +'.png',0)
            self.template['gray_' + str(i)] = cv2.imread('./template_720p/gray_' + str(i) +'.png',0)
            self.template['gray_mask_' + str(i)] = cv2.imread('./template_720p/gray_mask_' + str(i) + '.png' , 0)
        
        self.template_width = {}

        for key in self.template.keys() :
            height, width = self.template[key].shape
            self.template_width[key] = width

            print(key + ' ' + str(width))

    #template match based edged image
    def template_match(self,img_edges, template,threshold):
        res = cv2.matchTemplate(img_edges,template,cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            return zip(*loc[::-1])
        return None

    #organize x point from each matched result
    def organize_x_points(self, pt_dic, num, matched_res) :
        for pt in matched_res :
            checked = True
            for key in pt_dic.keys():
                if (key -2 <= pt[0] and pt[0] <= key + 2) :
                    if pt_dic[key] != num :
                        pt_dic['error'] = 'error'
                        return pt_dic
                    checked = False

            if checked :
                pt_dic[pt[0]] = num

        return pt_dic

    #if you use sharp_search, and gray_search, use this function first.
    def image_process(self, cap_image) :
        #crop and edge detect with Canny edge detection
        height, width,channel  = cap_image.shape
        crop_height, crop_width = height / 6 ,width / 5
        self.crop_image = cap_image[0:crop_height, width - crop_width - 1: width - 1]
    
        self.crop_edges = cv2.Canny(self.crop_image,100,200)

    #MUST use image_process(cap_image) first.
    def sharp_search(self,count) :
               #matching
        match_res = self.template_match(self.crop_edges, self.template['sharp'], 0.6)

        cv2.imwrite('./capture/crop_edges_' + str(count) + '.png', self.crop_edges)

        if(match_res is None) :
            return -1
        else :
            return match_res[0][0]

    #search the yellow(grade) number.
    def yellow_search(self, sharp_pt) :
        pt_dic = {}
        grade = 0

        for i in range(10) :
            res = self.template_match(self.crop_edges, self.template['yellow_' + str(i)], 0.7)

            if res is not None :
                pt_dic = self.organize_x_points(pt_dic, i,  res)
                if pt_dic.get('error') is not None:
                    return Error

        sorted_ypt_tups = sorted(pt_dic.items(), key = operator.itemgetter(0))
        
        len_pt_tups = len(sorted_ypt_tups)

        if not (len_pt_tups == 1 or len_pt_tups == 2) :
            return (-1,-1)
        else :
            for pt_tup in sorted_ypt_tups :
                grade *= 10
                grade += pt_tup[1]

        print(sorted_ypt_tups)
        #check point of yellow numbers

        return (grade, 0)#slash_pt)

    #search the gray(total) number.
    def gray_search(self, slash_pt) :
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # change this code using ./test.py
        #pt_dic = {}
        #hsv = cv2.cvtColor(self.crop_image, cv2COLOR_BGR2HSV)
    
        #for V in range(70,90) :
          #  lower_bound = np.array([0,0,V])
          #  upper_bound = np.array([179,41,120])
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #gray
        total = 0
        pt_dic = {} 

        for i in range(10) :
            res = self.template_match(self.crop_edges, self.template['gray_' + str(i)] ,0.7)

            if res is not None :
                pt_dic = self.organize_x_points(pt_dic, i, res)
                if pt_dic.get('error') is not None:
                    return Error

        sorted_gpt_tups = sorted(pt_dic.items(), key = operator.itemgetter(0))

        if not len(sorted_gpt_tups) == 2:
            total = 0
        else :
            for pt_tup in sorted_gpt_tups :
                total *= 10
                total += pt_tup[1]

        print(sorted_gpt_tups)

        return total

 
    # position of points.        
    # sharp_pt -> yellow_number -> slash_pt -> gray_number

    def grade_search(self, sharp_pt, video_name, count):

        # cv2.imwrite(os.path.join('./capture/' , "origin_" + video_name + '_' + str(count) + '.png') , self.crop_image)
        # cv2.imwrite(os.path.join('./capture/' , "cannyed_" + video_name + '_' + str(count) + '.png') , self.crop_edges)

        (grade, slash_pt) = self.yellow_search(sharp_pt)

        if(grade == -1) :
            return (-1,-1)

        total = self.gray_search(slash_pt)

        return (grade, total)
