import re
import requests
from livestreamer import Livestreamer

headers = {'Client-ID' : '03uamzu42b8grbcd174vfm02ta6vv4'}
Client_ID_header = 'Client-ID=03uamzu42b8grbcd174vfm02ta6vv4'

livestreamer = Livestreamer()
livestreamer.set_option('http-headers',Client_ID_header)

plugin = livestreamer.resolve_url('http://twitch.tv/runner0608')
streams = plugin.get_streams()
p = re.compile("<HLSStream\('(.)'\)>")

def getM3U8fromHLS(HLS) :
    response = requests.get(HLS.url,headers=headers)
    print(response.text)
    return response.text
    

print('WORST')
print(streams['worst'].url + '\n')
getM3U8fromHLS(streams['worst'])

print('BEST')
print(streams['best'].url + '\n')
getM3U8fromHLS(streams['best'])
