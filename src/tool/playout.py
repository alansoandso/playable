import requests
from pprint import pformat
from tool.verbose import Verbose
from tool.usernames import Usernames
from tool.utils import session, in_atom, AsJson, highlight


def get_umv():
    users = Usernames
    scratchy = users.get('scratch_tester')
    umv = session(scratchy)
    # print(umv)
    return umv


def play(crid):
    if in_atom(crid):
        return playout(get_umv(), crid)


def playout(umv, crid):
    url = 'http://playout.quality.nowtv.bskyb.com/vod/' + crid
    headers = {'authorization': umv, 'X-NowTV-DeviceID': 'playps3 NowTV_Player;1;PS3;Win32', 'X-NowTV-ClientID': 'ps3 client crosstv:1.5.1', }

    Verbose().output('Request: {}'.format(url))
    response = requests.get(url, headers=headers, timeout=5)

    if response.status_code == 200:
        Verbose().output(pformat(response.json()))
        return True
    Verbose().output(f'{response.status_code}: {response.json()}')
    return False


def catalogue_movies():
    url = 'http://client.quality.nowtv.bskyb.com/catalogue/programs?limit=20&offset='
    umv = get_umv()

    headers = {'cache-control': 'no-cache'}

    for offset in range(0, 1000, 20):
        url_offset = '{}{}'.format(url, offset)
        Verbose().output(url_offset, end=' ')

        response = requests.request('GET', url_offset, headers=headers)

        if response.status_code == 200:
            Verbose().output('Got a catalogue of {} bytes'.format(len(response.text)))
            catalogue = response.json()

            for content in catalogue['list']:
                crid = content.get('id', 'n/a')
                title = AsJson(content).getString("title", "n/a")
                if in_atom(crid) and playout(umv, crid):
                    print(f"{content.get('certificate', ''):<3} {title:<50} {crid:<15} {content.get('uri', 'n/a'):<120} Ends: {enddate(content)}")
        else:
            print('No data')
            return


def enddate(details):
    end_date = AsJson(details).getString("episode.availabilities.list.end")

    if not end_date:
        end_date = AsJson(details).getString("program.availabilities.list.end")

    if not end_date:
        end_date = AsJson(details).getString("availabilities.list.end")[0]

    if not end_date:
        end_date = AsJson(details).getString("show.episodes.count")

    if not end_date:
        end_date = AsJson(details).getString("message", "N/A")

    return end_date


def catalogue_collections(env='qa'):
    if env == 'qa':
        url = "http://client.quality.nowtv.bskyb.com/catalogue/collections?kidsAware=true"

    elif env == 'integration':
        url = "http://client.integration.nowtv.bskyb.com/catalogue/collections?kidsAware=true"

    elif env == 'production':
        url = "http://client.nowtv.com/catalogue/collections?kidsAware=true"

    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        print("Got a catalogue of {} bytes".format(len(response.text)))
        catalogue = response.json()
        # pprint(catalogue)
        # return
    else:
        print("No data")
        return

    # Extract the collection urls from the collections
    collections = catalogue.get("list", [])
    total = 0

    for collection in collections:
        uri = AsJson(collection).getString("programs.uri", "")
        if not uri:
            uri = AsJson(collection).getString("episodes.uri", "")
        if not uri:
            uri = AsJson(collection).getString("shows.uri", "")
        if uri:
            response = requests.request("GET", uri, headers=headers)
            if response.status_code == 200:
                total += 1
                print(uri)
            else:
                print(highlight(uri))

    print(f'\nFound: {total} out of {len(collections)}')
