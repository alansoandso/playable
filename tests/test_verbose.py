from unittest.mock import patch, mock_open
from tool.verbose import Verbose
import logging
LOGGER = logging.getLogger(__name__)


def test_status():
    Verbose().unset()
    assert Verbose().level() == 0
    Verbose().set()
    assert Verbose().level() == 1


def test_borg():
    """There is only one Borg..."""
    Verbose().set()
    borg = Verbose()
    assert Verbose().level()
    assert borg.level()

    borg.unset()
    assert not borg.level()


def test_output(capsys):
    """Output to stdout"""
    Verbose().set()
    Verbose().output('show when true')
    out, err = capsys.readouterr()
    assert 'show when true' in out


def test_output_supressed(capsys):
    """Output to stdout suppressed """
    Verbose().unset()
    Verbose().output('This will always be hidden')
    out, err = capsys.readouterr()
    assert '' == out


def test_verbosity_level_defaults(capsys):
    Verbose().set()
    Verbose().output('You can not hide this', verbosity=0)
    out, err = capsys.readouterr()
    assert 'You can not hide this' in out


def test_verbosity_level_under(capsys):
    Verbose().set(0)
    Verbose().output('Hide unless level is set to 1 or more', verbosity=1)
    out, err = capsys.readouterr()
    assert '' == out


def test_verbosity_level_reached(capsys):
    Verbose().set(2)
    Verbose().output('level is set to 2', verbosity=1)
    out, err = capsys.readouterr()
    assert 'level is set to 2' in out

    Verbose().set(3)
    Verbose().output('level is set to 3', verbosity=1)
    out, err = capsys.readouterr()
    assert 'level is set to 3' in out

