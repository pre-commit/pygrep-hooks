[![Build Status](https://travis-ci.org/pre-commit/pygrep-hooks.svg?branch=master)](https://travis-ci.org/pre-commit/pygrep-hooks)

pygrep-hooks
============

A collection of fast, cheap, regex based pre-commit hooks.


### Adding to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/pre-commit/pygrep-hooks
    rev: v1.2.0  # Use the ref you want to point at
    hooks:
    -   id: python-use-type-annotations
    # ...
```

### Naming conventions

Where possible, these hooks will be prefixed with the file types they target.
For example, a hook which targets python will be called `python-...`.

### Provided hooks

[generated]: # (generated)
- **`python-check-blanket-noqa`**: Enforce that `noqa` annotations always occur with specific codes
- **`python-check-mock-methods`**: Prevent a common mistake of `assert mck.not_called()` or `assert mck.called_once_with(...)`
- **`python-noeval`**: A quick check for `eval()` built-in function
- **`python-no-log-warn`**: A quick check for the deprecated `.warn()` method of python loggers
- **`python-use-type-annotations`**: Enforce that python3.6+ type annotations are used instead of type comments
- **`rst-backticks`**: Detect common mistake of using single backticks when writing rst
