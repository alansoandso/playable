import requests
import json
from pretty_json import format_json
from tool.verbose import Verbose


class AsJson(dict):
    """
    Traverse through the JSON
    """

    def get(self, path, default=""):
        keys = path.split(".")
        val = None

        for key in keys:
            if val:
                if isinstance(val, list):
                    val = [v.get(key, default) if v else None for v in val]
                else:
                    val = val.get(key, default)
            else:
                val = dict.get(self, key, default)

            if not val:
                break

        return val


def pprint(output):
    print(pformat(output))


def pformat(output):
    return format_json(output, 'solarized')


def highlight(string):
    """ Highlight error strings with white on blue """
    return "\033[01;44m" + string + "\033[01;0m"


def session(user):
    url = "http://services.quality.nowtv.bskyb.com/sessions"
    payload = json.dumps({'username': user.get('email', user.get('username')), 'password': user['password']})
    headers = {'x-nowtv-deviceid': "2d54f40c51dd8df4109e1c6009998d17bef1261a NowTV_Player;1;roku;Win32", 'accept': "application/json", 'content-type': "application/json",
               'x-nowtv-clientid': "QATEST Password 1.0", 'cache-control': "no-cache"}

    # print('Request: {}'.format(url))
    response = requests.post(url, data=payload, headers=headers, timeout=5)

    if response.status_code == 201:
        return 'NowTV-Auth {}'.format(response.headers['X-NowTV-Token'])
    else:
        print('{}: Failed to get UMV token'.format(response.status_code))
        return


def in_atom(crid):
    url = 'http://e2e.dev.aws.atom.sky.com/adapter-atlas/v1/query/content_id/' + crid

    headers = {'x-skyott-proposition': "NOWTV", 'x-skyott-territory': "GB", 'x-skyott-device': "MOBILE", 'x-skyott-platform': "IOS", 'cache-control': "no-cache"}

    response = requests.get(url, headers=headers, timeout=5)
    Verbose().output(f'Atom lookup request: {url}\nReturned: {response.status_code}')
    Verbose().output(f'{pformat(response.json())}', verbosity=1)
    if response.status_code == 200:
        return True

    return False
