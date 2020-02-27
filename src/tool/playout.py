import requests
from tool.verbose import Verbose
from tool.usernames import Usernames
from tool.utils import session, in_atom, AsJson, highlight, pformat


def get_umv():
    users = Usernames
    scratchy = users.get('scratch_tester')
    umv = session(scratchy)
    Verbose().output('Using user: scratch_tester', verbosity=1)
    return umv


def play(crid, env='quality'):
    if in_atom(crid):
        return playout(get_umv(), crid, env)


def playout(umv, crid, env='quality'):
    url = f'http://playout.{env}.nowtv.bskyb.com/vod/{crid}'
    headers = {'authorization': umv, 'X-NowTV-DeviceID': 'playps3 NowTV_Player;1;PS3;Win32', 'X-NowTV-ClientID': 'ps3 client crosstv:1.5.1', }

    Verbose().output(f'Request: {url}')
    response = requests.get(url, headers=headers, timeout=5)
    Verbose().output(f'Returned: {response.status_code}')

    if response.status_code == 200:
        Verbose().output(f'{pformat(response.json())}', verbosity=1)
        return True
    Verbose().output(f'{pformat(response.json())}')
    return False


def catalogue_movies(certificate='', env='quality'):
    url = f'http://client.{env}.nowtv.bskyb.com/catalogue/programs?limit=20&offset='
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
                title = AsJson(content).get("title", "n/a")
                # matching cert or no cert filter
                if certificate and content.get('certificate', 'x') == certificate or not certificate:
                    if in_atom(crid) and playout(umv, crid, env):
                        print(f"{content.get('certificate', ''):<3} {title:<50} {crid:<15} {content.get('uri', 'n/a'):<120} Ends: {end_date(content)}")
        else:
            print('No data')
            return


def end_date(details):
    end = AsJson(details).get("episode.availabilities.list.end")

    if not end:
        end = AsJson(details).get("program.availabilities.list.end")

    if not end:
        end = AsJson(details).get("availabilities.list.end")[0]

    if not end:
        end = AsJson(details).get("show.episodes.count")

    if not end:
        end = AsJson(details).get("message", "N/A")

    return end


def catalogue_collections(env='quality'):
    url = f'http://client.{env}.nowtv.bskyb.com/catalogue/collections?kidsAware=true'
    if env == 'production':
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
        uri = AsJson(collection).get("programs.uri", "")
        if not uri:
            uri = AsJson(collection).get("episodes.uri", "")
        if not uri:
            uri = AsJson(collection).get("shows.uri", "")
        if uri:
            response = requests.request("GET", uri, headers=headers)
            if response.status_code == 200:
                total += 1
                print(uri)
            else:
                print(highlight(uri))

    print(f'\nFound: {total} out of {len(collections)}')
