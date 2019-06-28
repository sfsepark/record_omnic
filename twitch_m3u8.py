import requests

def load(URL , client_id = '' , headers={}):
    if client_id != '' :
        headers = {'http-headers', clinet_id} 

    response = requests.get(URL, headers=headers)
    if response.status_code != 200 :
        return None

class twitch_ts_object():
    def __init__(inf, is_live = False) :
        self.start_secs = -1
        self.inf = inf
        self.is_live = is_live

class twitch_m3u8_object():
    def __init__() :
        self.version = -1
        self.target_duration = -1
        self.media_sequence = -1
        self.twitch_elapsed_secs = -1
        self.twitch_total_secs = -1
        self.ts_objects = []

    def add_ts_object(ts_obj) :
        if ts_obj_inf > 0 :
            ts_obj.start_secs =  self.twitch_elapsed_sec + ts_obj.inf
        self.ts_objects.append(ts_obj)
