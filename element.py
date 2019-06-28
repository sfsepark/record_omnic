'''
pubg.tnya.kr
    PUBG grade live tracking system

    LAST CHANGE : 2017-10-20
    developer : sfsepark@gmail.com

'''
'''
    USAGE :
    clear information using clear()
    -> register infomation of each match result
    -> organize informations
    -> get total and 
'''

import operator
from singleton import SingletonType

class ElementManager :

    __metaclass__ = SingletonType

    def __init__(self) :
        self.yellow_info = []
        self.gray_info = []
        self.template_width = {}

    def clear(self) :
        self.yellow_info = []
        self.gray_info = []

    # ex) [(2, {1: 2}), (30, {5: 3, 6 :1})]
    def add_info(self, element_type, num, matched_res) :
        if element_type == 0:
            infos = self.yellow_info
        else :
            infos = self.gray_info

        for new_pt in matched_res :
            Checked = True
            index = 0
            for (point,num_dic)  in infos:
                index = index + 1
                if point-5 <= new_pt[0] and new_pt[0] <= point+5 :
                    if num in num_dic :
                        num_dic[num] = num_dic[num] + 1
                    else :
                        num_dic[num] = 1
                    Checked = False
                    break
                elif new_pt[0] < point :
                    infos.insert(index-1, (new_pt[0], {num : 1}))
                    Checked = False
                    break
        
            if Checked == True :
                infos.insert(index,(new_pt[0], {num : 1}))

    def get_number_from_element(self, info) :
        sorted_num_dic = sorted(info[1].items() , 
                key =operator.itemgetter(1), 
                reverse=True)
        return sorted_num_dic[0][0]

    def get_gray_start_pt(self) : 

        last_element_info = self.yellow_info[len(self.yellow_info) -1]
        number = self.get_number_from_element(last_element_info)

        return last_element_info[0] + self.template_width['yellow_' + str(number)] + 4 + 20

    def get_number(self, element_type) :

        if(element_type == 0) :
            infos = self.yellow_info
            pre_key = 'yellow_'
        else :
            infos = self.gray_info
            pre_key = 'gray_mask_'

        number = 0

        cnt = 0
        length = len(infos)

        while cnt < length :
            number *= 10

            cur_pt = infos[cnt][0]
            cur_num = self.get_number_from_element(infos[cnt])
            next_pt = cur_pt + self.template_width[pre_key + str(cur_num)]

            while True :
                cnt += 1
            
                if cnt >= length :
                    break

                if not infos[cnt][0] < next_pt - 5 :
                    break

            number += cur_num

        return number
                
