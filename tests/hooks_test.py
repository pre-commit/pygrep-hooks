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
