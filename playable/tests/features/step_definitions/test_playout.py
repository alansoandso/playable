import pytest
from pytest_bdd import scenario, given, then, parsers

from playable import tool


# Generate the following test stubs with:
# cd playable/tests/features/step_definitions
# pytest-bdd generate ../playout.feature
@scenario('../playout.feature', 'List available crids')
def test_list_available_crids():
    """List available crids."""


@scenario('../playout.feature', 'Play by crid')
def test_play_by_crid():
    """Play by crid."""


@scenario('../playout.feature', 'Play by title')
def test_play_by_title():
    """Play by title."""


@scenario('../playout.feature', 'Play by title on integration environment')
def test_play_by_title_on_int():
    """Play by title on integration environment"""


@scenario('../playout.feature', 'Play unknown title - fails')
def test_play_unknown_title__fails():
    """Play unknown title - fails."""


# Test steps go here...
@pytest.fixture
def cli():
    """Fixture to override and provide an exit status to test against"""
    return dict(status=-1)


@given(parsers.parse('I playout "{asset}"'), target_fixture='cli')
def playout(asset, capsys):
    status = tool.command_line_runner(f'playable {asset}'.split())
    return dict(status=status)


@given('I list all available QA crids', target_fixture='cli')
def list_all_crids(capsys):
    status = tool.command_line_runner(f'playable --list_crids'.split())
    return dict(status=status)


@then('exit status is OK')
def outcome(cli):
    assert cli.get('status') != 1


@then(parsers.parse('exit status is "{expected:d}"'))
def exit_status_expected(cli, expected):
    assert cli.get('status') == expected


@then(parsers.parse('output contains "{expected_out}"'))
def output_expected(expected_out, capsys, cli):
    out, err = capsys.readouterr()
    assert expected_out in out
    assert cli.get('status') != 1
