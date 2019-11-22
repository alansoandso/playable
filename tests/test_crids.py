from unittest.mock import patch, mock_open
from tool.assets import Assets


@patch('builtins.open',
       mock_open(read_data='{"default":{"first": "crid1","second":"crid2"}}'))

def test_load_crids():
    assert Assets.load_users() == {"moviesonly": {"profileId": "15706100", "username": "nowtvAutomation"}}
    # noinspection PyUnresolvedReferences
    open.assert_called_once()


def test_profileid_from_user():
    quality = Assets()
    assert quality.get_profileid('moviesonly') == '15706100'


def test_get_profileid_defaults():
    quality = Assets()
    assert quality.get_profileid('1234') == '1234'
