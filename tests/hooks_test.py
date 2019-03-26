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


@pytest.mark.parametrize(
    's',
    (
        'foo._bar',
        'foo._bar()',
        'foo._bar ==',
        'foo._bar=',
        'fooself._bar',
        # At beginning of string, presumably not in a method with normal 'self'
        'self._bar',
        # Non-comment instance of 'private' disabler comment
        'foo._bar == private',
    ),
)
def test_python_private_access_enforcement_positive(s):
    assert HOOKS['python-private-access-enforcement'].search(s)


@pytest.mark.parametrize(
    's',
    (
        'foo.bar',
        ' self._bar',
        '(self._bar',
        '_bar()',
        '_bar == ',
        'super(Cls, cls).__init__(',
        'super(Cls, self)._set',
        'type(self).__name__',
        # Allow disabling per-line
        'foo._bar #private',
        'foo._bar       #   private',
    ),
)
def test_python_private_access_enforcement_negative(s):
    assert not HOOKS['python-private-access-enforcement'].search(s)
