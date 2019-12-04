from unittest.mock import patch, mock_open
from tool.assets import Assets


@patch('builtins.open',
       mock_open(read_data='{"default":{"first": "crid1","second":"crid2"}}'))
def test_load_crids():
    assert Assets.load_crids() == {"first": "crid1", "second": "crid2"}
    # noinspection PyUnresolvedReferences
    open.assert_called_once()


@patch('builtins.open',
       mock_open(read_data='{"default":{"first": "crid1", "second": "crid2"}}'))
def test_get_crid_defaults():
    quality = Assets()
    assert quality.get_crid('unknown') == ''


def test_get_crid():
    quality = Assets()
    assert quality.get_crid('The Firm')
