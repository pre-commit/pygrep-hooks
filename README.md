[![Build Status](https://travis-ci.org/pre-commit/pygrep-hooks.svg?branch=master)](https://travis-ci.org/pre-commit/pygrep-hooks)

pygrep-hooks
============

A collection of fast, cheap, regex based pre-commit hooks.


### Adding to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/pre-commit/pygrep-hooks
    rev: v0.0.0  # Use the ref you want to point at
    hooks:
    -   id: python-use-type-annotations
    # ...
```

### Naming conventions

Where possible, these hooks will be prefixed with the file types they target.
For example, a hook which targest python will be called `python-...`.

### Provided hooks

[generated]: # (generated)
- `python-check-mock-methods`: Prevent a common mistake of `assert mck.not_called()` or `assert mck.called_once_with(...)`
- `python-no-log-warn`: A quick check for the deprecated `.warn()` method of python loggers
- `python-use-type-annotations`: Enforce that python3.6+ type annotations are used instead of type comments
