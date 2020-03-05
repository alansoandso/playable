import json


class Assets(object):
    crids = None

    def __init__(self):
        # Only load in the file once
        if not Assets.crids:
            Assets.crids = self.load_crids()

    @staticmethod
    def load_crids():
        crids_path = '/Users/alan/workspace/popcorn-qa-cucumber-jvm/src/test/resources/environment/crid.json'
        try:
            # Load all QA crids
            with open(crids_path) as json_data:
                return json.load(json_data).get('default')
        except json.decoder.JSONDecodeError as error:
            print(f'Error on loading JSON from: {crids_path}')
            raise error

    @staticmethod
    def list_titles():
        for title in Assets.crids.keys():
            print(title)
        print(f'\nFound {len(Assets.crids)} available assets')

    @staticmethod
    def get_crid(title):
        return Assets.crids.get(title, '')
