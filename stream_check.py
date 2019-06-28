import threading
import requests
import json
import time
from print_log import print_log

class Stream_check :

    def __init__(self, user_name) :
        self.user_name = user_name
        self.headers = {"Accept" : 'application/vnd.twitchtv.v5+json' , "Client-ID" : '03uamzu42b8grbcd174vfm02ta6vv4'}
    
    def get_user_id(self) :
        url = 'https://api.twitch.tv/kraken/users?login=' + self.user_name

        r = requests.get(url,  headers = self.headers)
        status_code = r.status_code
        if status_code != 200 :
            return -2
        
        data = r.json()
        if data['_total'] == 0 :
            return -1
        
        self.user_id = data['users'][0]['_id']
        return self.user_id
   
    def check_playing_pubg(self) :
        url = 'https://api.twitch.tv/kraken/streams/' + self.user_id
        
        try :
            response = requests.get(url , headers=self.headers)
            status_code = response.status_code
            if status_code != 200 :
                print_log('request ERROR')
                return False

            data = response.json()

            if data['stream'] == None :
                return False
            else :
                if data['stream']['game'] == "PLAYERUNKNOWN'S BATTLEGROUNDS" :
                    return True
                else :
                    return False
        except :
            print_log('Except')
            return False
