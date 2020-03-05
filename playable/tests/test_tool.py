import sys
from unittest.mock import patch
from playable import tool


@patch('sys.argv', ['playable'])
def test_cli_usage(capsys):
    """Test if command_line_runner shows help when called without parameters."""
    # def test_cli_usage(monkeypatch, capsys):
    # monkeypatch.setattr(sys, "argv", ["playable"])
    tool.command_line_runner()
    out, err = capsys.readouterr()
    assert 'usage: playable [-h]' in out


def test_parser_a_title():
    args = tool.get_parser().parse_args('title'.split())
    assert args.asset == ['title']


def test_parser_long_title():
    args = tool.get_parser().parse_args('some title'.split())
    assert args.asset == ['some', 'title']


@patch('playable.tool.assets')
def test_clr_list_users(mock_list_crids):
    tool.command_line_runner('playable --list_crids'.split())
    assert mock_list_crids.list_titles.called_once()


@patch('playable.tool.assets.get_crid')
@patch('playable.tool.play')
def test_clr_play_title(mock_play, mock_get_crid):
    tool.command_line_runner('playable movies only'.split())
    mock_get_crid.assert_called_once()
    mock_play.assert_called_once()


@patch('playable.tool.play')
def test_clr_play_title_2_crid(mock_play):
    tool.command_line_runner('playable The Firm'.split())
    mock_play.assert_called_with('458431384f556510VgnVCM1000000b43150a____', env='quality')


@patch('playable.tool.play')
def test_clr_play_crid(mock_play):
    tool.command_line_runner('playable crid is not in list'.split())
    mock_play.assert_called_with('crid', env='quality')


@patch('playable.tool.play')
def test_clr_play_in_integration_title_2_crid(mock_play):
    tool.command_line_runner('playable --env integration The Firm'.split())
    mock_play.assert_called_with('458431384f556510VgnVCM1000000b43150a____', env='integration')


