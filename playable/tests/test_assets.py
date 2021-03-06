from unittest.mock import patch, mock_open
from playable.assets import Assets
import logging
LOGGER = logging.getLogger(__name__)


@patch('builtins.open', mock_open(read_data='{"default":{"The Firm": "crid1", "Joker": "crid2"}}'))
def test_load_crids():
    LOGGER.info('Log some info to stdout')
    assert Assets.load_crids() == {"The Firm": "crid1", "Joker": "crid2"}
    # noinspection PyUnresolvedReferences
    open.assert_called_once()


@patch('builtins.open', mock_open(read_data='{"default":{"The Firm": "crid1", "Joker": "crid2"}}'))
def test_get_crid_defaults():
    quality = Assets()
    assert quality.get_crid('unknown') == ''


@patch('builtins.open', mock_open(read_data='{"default":{"The Firm": "crid1", "Joker": "crid2"}}'))
def test_get_crid():
    quality = Assets()
    assert quality.get_crid('The Firm')
