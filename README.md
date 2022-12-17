# Local development notes
### pre-commit
The most straightforward way to install pre-commit is to create and activate a Python virtualenv per the `python/requirements.txt` file.
To start using `pre-commit`, run `pre-commit install` in the repo root.

### Python
In this repo, I made the slightly unconventional choice to put python-specific config files in the python/ directory rather than the repo root.
The goal is to keep the repo root clean because this repo will include many languages.
In order to run Python formatters/linters/checkers, you should first navigate to the `python/` directory, ensuring config files will be respected.

In general, older code in this repo may not be runnable (e.g. it may not be Python 3 compatible).
This is expected, and I'm mostly not changing that old code; it'll serve as a record to how I used to write Python code :)
