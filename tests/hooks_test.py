import re

import pytest
from pre_commit.clientlib import load_manifest
from pre_commit.constants import MANIFEST_FILE

HOOKS = {h['id']: re.compile(h['entry']) for h in load_manifest(MANIFEST_FILE)}


@pytest.mark.parametrize(
    's',
    (
        'x = 1 # type: ignoreme',
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
        'x = 1  # type: ignore[type-mismatch]',
        'x = 1  # type: ignore=E123',
    ),
)
def test_python_use_type_annotations_negative(s):
    assert not HOOKS['python-use-type-annotations'].search(s)


@pytest.mark.parametrize(
    's',
    (
        '# noqa',
        '# NOQA',
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
        'MyMock.assert_called_once_with',
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
        '"""like :meth:`Mock.assert_called_once_with`"""',
        '"""like :meth:`MagicMock.assert_called_once_with`"""',
    ),
)
def test_python_check_mock_methods_negative(s):
    assert not HOOKS['python-check-mock-methods'].search(s)


def test_python_noeval_positive():
    assert HOOKS['python-no-eval'].search('eval("3 + 4")')


def test_python_noeval_negative():
    assert not HOOKS['python-no-eval'].search('literal_eval("{1: 2}")')


@pytest.mark.parametrize(
    's',
    (
        'log.warn("this is deprecated")',
    ),
)
def test_python_no_log_warn_positive(s):
    assert HOOKS['python-no-log-warn'].search(s)


@pytest.mark.parametrize(
    's',
    (
        "warnings.warn('this is ok')",
        'log.warning("this is ok")',
        'from warnings import warn',
        'warn("by itself is also ok")',
    ),
)
def test_python_no_log_warn_negative(s):
    assert not HOOKS['python-no-log-warn'].search(s)


@pytest.mark.parametrize(
    's',
    (
        '`[code]`',
        'i like `_kitty`',
        'i like `_`',
        '`a`',
        '`cd`',
    ),
)
def test_python_rst_backticks_positive(s):
    assert HOOKS['rst-backticks'].search(s)


@pytest.mark.parametrize(
    's',
    (
        ' ``[code]``',
        'i like _`kitty`',
        'i like `kitty`_',
        '``b``',
        '``ef``',
    ),
)
def test_python_rst_backticks_negative(s):
    assert not HOOKS['rst-backticks'].search(s)


@pytest.mark.parametrize(
    's',
    (
        '``PyMem_Realloc()`` indirectly call``PyObject_Malloc()`` and',
        'This PEP proposes that ``bytes`` and ``bytearray``gain an optimised',
        'Reading this we first see the``break``, which obviously applies to',
        'for using``long_description`` and a corresponding',
        '``inline`` normal``inline',
        '``inline``normal ``inline',
        '``inline``normal',
        '``inline``normal``inline',
        'normal ``inline``normal',
        'normal``inline`` normal',
        'normal``inline``',
        'normal``inline``normal',
    ),
)
def test_python_rst_inline_touching_normal_positive(s):
    assert HOOKS['rst-inline-touching-normal'].search(s)


@pytest.mark.parametrize(
    's',
    (
        '``PyMem_Realloc()`` indirectly call ``PyObject_Malloc()`` and',
        'This PEP proposes that ``bytes`` and ``bytearray`` gain an optimised',
        'Reading this we first see the ``break``, which obviously applies to',
        'for using ``long_description`` and a corresponding',
        '``inline`` normal ``inline',
        '``inline`` normal',
        'normal ``inline`` normal',
        'normal ``inline``',
    ),
)
def test_python_rst_inline_touching_normal_negative(s):
    assert not HOOKS['rst-inline-touching-normal'].search(s)


@pytest.mark.parametrize(
    's',
    (
        str(b'\x80abc', errors='replace'),
    ),
)
def test_text_unicode_replacement_char_positive(s):
    assert HOOKS['text-unicode-replacement-char'].search(s)


@pytest.mark.parametrize(
    's',
    (
        'foo',
    ),
)
def test_text_unicode_replacement_char_negative(s):
    assert not HOOKS['text-unicode-replacement-char'].search(s)


@pytest.mark.parametrize(
    's',
    (
        'tap(() => {debugger}),',
        'foo(); debugger;',
    ),
)
def test_ts_no_debugger_positive(s):
    assert HOOKS['ts-no-debugger'].search(s)


@pytest.mark.parametrize(
    's',
    (
        'debug("function is ok")',
    ),
)
def test_ts_no_debugger_negative(s):
    assert not HOOKS['ts-no-debugger'].search(s)


@pytest.mark.parametrize(
    's',
    (
        'fdescribe("focus block", () => ({}))',
        'xdescribe("ignore block", () => ({}))',
        'xdescribe ("ignore block with space", () => ({}))',
        'fit("focus case", () => ({}))',
        'xit("ignore case", () => ({}))',
        'xit ("ignore case with space", () => ({}))',
    ),
)
def test_ts_no_focus_ignore_positive(s):
    assert HOOKS['ts-no-focus-ignore'].search(s)


@pytest.mark.parametrize(
    's',
    (
        'describe("block", () => {',
        'it("case", () => {',
    ),
)
def test_ts_no_focus_ignore_negative(s):
    assert not HOOKS['ts-no-focus-ignore'].search(s)
