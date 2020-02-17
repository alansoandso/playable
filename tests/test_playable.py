import sys
from unittest.mock import patch
from tool import playable


@patch('sys.argv', ['playable'])
def test_cli_usage(capsys):
    """Test if command_line_runner shows help when called without parameters."""
    # def test_cli_usage(monkeypatch, capsys):
    # monkeypatch.setattr(sys, "argv", ["playable"])
    playable.command_line_runner()
    out, err = capsys.readouterr()
    assert 'usage: playable [-h]' in out


def test_parser_a_title():
    args = playable.get_parser().parse_args('title'.split())
    assert args.asset == ['title']


def test_parser_long_title():
    args = playable.get_parser().parse_args('some title'.split())
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
    mock_play.assert_called_with('3e1589785251a510VgnVCM1000000b43150a____', env='quality')


@patch('tool.playable.play')
def test_clr_play_crid(mock_play):
    playable.command_line_runner('playable crid is not in list'.split())
    mock_play.assert_called_with('crid', env='quality')


@patch('tool.playable.play')
def test_clr_play_in_integration_title_2_crid(mock_play):
    playable.command_line_runner('playable --env integration The Firm'.split())
    mock_play.assert_called_with('3e1589785251a510VgnVCM1000000b43150a____', env='integration')


