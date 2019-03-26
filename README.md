[![Build Status](https://dev.azure.com/asottile/asottile/_apis/build/status/pre-commit.pygrep-hooks?branchName=master)](https://dev.azure.com/asottile/asottile/_build/latest?definitionId=9&branchName=master)

pygrep-hooks
============

A collection of fast, cheap, regex based pre-commit hooks.


### Adding to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/pre-commit/pygrep-hooks
    rev: v1.3.0  # Use the ref you want to point at
    hooks:
    -   id: python-use-type-annotations
    # ...
```

### Naming conventions

Where possible, these hooks will be prefixed with the file types they target.
For example, a hook which targest python will be called `python-...`.

### Provided hooks

[generated]: # (generated)
- **`python-check-blanket-noqa`**: Enforce that `noqa` annotations always occur with specific codes
- **`python-check-mock-methods`**: Prevent common mistakes of `assert mck.not_called()`, `assert mck.called_once_with(...)` and `mck.assert_called`.
- **`python-no-log-warn`**: A quick check for the deprecated `.warn()` method of python loggers
- **`python-private-access-enforcement`**: Allow referencing self._whatever but not something._whatever; disable with `# private`
- **`python-use-type-annotations`**: Enforce that python3.6+ type annotations are used instead of type comments
- **`rst-backticks`**: Detect common mistake of using single backticks when writing rst
