import re

import pytest
from pre_commit.clientlib import load_manifest
from pre_commit.constants import MANIFEST_FILE

HOOKS = {h['id']: re.compile(h['entry']) for h in load_manifest(MANIFEST_FILE)}


@pytest.mark.parametrize(
    's',
    (
        'x = 1 # type: ignore_me',
        'x = 1  # type: int',
        'x = 1  # type int',
        'x = 1  # type: int  # noqa',
    ),
)
def test_python_use_type_annotations_positive(s):
    assert HOOKS['python-use-type-annotations'].search(s)


@pytest.mark.parametrize(
    's',
    (
        'x = 1',
        'x = 1  # type:ignore',
        'x = 1  # type: ignore',
        'x = 1  # type:  ignore',
        'x = 1  # type: ignore # noqa',
        'x = 1  # type: ignore  # noqa',
    ),
)
def test_python_use_type_annotations_negative(s):
    assert not HOOKS['python-use-type-annotations'].search(s)


@pytest.mark.parametrize(
    's',
    (
        '# noqa',
        '# noqa:F401',
        '# noqa:F401,W203',
    ),
)
def test_python_check_blanket_noqa_positive(s):
    assert HOOKS['python-check-blanket-noqa'].search(s)


@pytest.mark.parametrize(
    's',
    (
        'x = 1',
        '# noqa: F401',
        '# noqa: F401, W203',
    ),
)
def test_python_check_blanket_noqa_negative(s):
    assert not HOOKS['python-check-blanket-noqa'].search(s)


@pytest.mark.parametrize(
    's',
    (
        'assert my_mock.not_called()',
        'assert my_mock.called_once_with()',
        'my_mock.assert_not_called',
        'my_mock.assert_called',
        'my_mock.assert_called_once_with',
        'my_mock.assert_called_once_with# noqa',
    ),
)
def test_python_check_mock_methods_positive(s):
    assert HOOKS['python-check-mock-methods'].search(s)


@pytest.mark.parametrize(
    's',
    (
        'assert my_mock.call_count == 1',
        'assert my_mock.called',
        'my_mock.assert_not_called()',
        'my_mock.assert_called()',
        'my_mock.assert_called_once_with()',
    ),
)
def test_python_check_mock_methods_negative(s):
    assert not HOOKS['python-check-mock-methods'].search(s)


def test_python_noeval_positive():
    assert HOOKS['python-no-eval'].search('eval("3 + 4")')


def test_python_noeval_negative():
    assert not HOOKS['python-no-eval'].search('literal_eval("{1: 2}")')


@pytest.mark.parametrize(
    "s",
    (
        'log.warn("help")',
        'logger.warn("well warn dresses found")',
        'logging.warn("to be or not to be")',
    ),
)
def test_python_no_log_warn_positive(s):
    assert HOOKS["python-no-log-warn"].search(s)


@pytest.mark.parametrize(
    "s",
    (
        "warnings.warn()",
        'log.warning("this is ok")',
        'warnings.warn("bee be bad")',
        'print("if warn is just somewhere random")',
        'warn("test from warnings import warn")',
        "xx1234warning0394warn",
        "from warnings import warn",
        "this does not have a trigger word",
    ),
)
def test_python_no_log_warn_negative(s):
    assert not HOOKS["python-no-log-warn"].search(s)
