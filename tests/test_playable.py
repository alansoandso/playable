from unittest.mock import call, patch, mock_open

import pytest

from tool import playable


@patch('builtins.open', mock_open(read_data='{"default":{"first": "crid1","second":"crid2"}}'))
@patch('argparse.ArgumentParser')
def test_parser_print_usage(mock_parser):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        playable.parse_args(['playable'])
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    mock_parser.assert_has_calls([call().print_usage()])


def test_parser_a_title():
    args = playable.parse_args('playable title'.split())
    assert args.asset == ['title']


def test_parser_long_title():
    args = playable.parse_args('playable some title'.split())
    assert args.asset == ['some', 'title']


@patch('tool.playable.assets')
def test_clr_list_users(mock_list_crids):
    playable.command_line_runner('playable --list_crids'.split())
    assert mock_list_crids.list_titles.called_once()


@patch('tool.playable.assets.get_crid')
@patch('tool.playable.play')
def test_clr_play_title(mock_play, mock_get_crid):
    playable.command_line_runner('playable movies only'.split())
    mock_get_crid.assert_called_once()
    mock_play.assert_called_once()


@patch('tool.playable.play')
def test_clr_play_title_2_crid(mock_play):
    playable.command_line_runner('playable The Firm'.split())
    mock_play.assert_called_with('3e1589785251a510VgnVCM1000000b43150a____')


@patch('tool.playable.play')
def test_clr_play_crid(mock_play):
    playable.command_line_runner('playable crid is not in list'.split())
    mock_play.assert_called_with('crid')
