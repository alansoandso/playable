import requests
from pprint import pprint
from tool.usernames import Usernames
from tool.utils import session, in_atom


def play(crid):
    users = Usernames
    scratchy = users.get('scratch_tester')
    umv = session(scratchy)
    # print(umv)

    if in_atom(crid):
        playout(umv, crid)


def playout(umv, crid):
    url = 'http://playout.quality.nowtv.bskyb.com/vod/' + crid
    headers = {'authorization': umv, 'X-NowTV-DeviceID': 'playps3 NowTV_Player;1;PS3;Win32', 'X-NowTV-ClientID': 'ps3 client crosstv:1.5.1', }

    print('Request: {}'.format(url))
    response = requests.get(url, headers=headers, timeout=5)

    if response.status_code == 200:
        pprint(response.json())
        return True

    print('{}: Failed to playout'.format(response.status_code))
    pprint(response.json())
    return False


