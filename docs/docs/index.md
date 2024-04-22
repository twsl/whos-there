# whos-there: The spiritual successor to knockknock for PyTorch Lightning, get notified when your training ends

Welcome to whos-there's documentation!

<!--- BADGES: START --->
[![Build](https://github.com/twsl/whos-there/actions/workflows/build.yaml/badge.svg)](https://github.com/twsl/whos-there/actions/workflows/build.yaml)
[![Documentation](https://github.com/twsl/whos-there/actions/workflows/docs.yaml/badge.svg)](https://github.com/twsl/whos-there/actions/workflows/docs.yaml)
![GitHub Release](https://img.shields.io/github/v/release/twsl/whos-there?include_prereleases)
[![PyPI - Package Version](https://img.shields.io/pypi/v/whos-there?logo=pypi&style=flat&color=orange)](https://pypi.org/project/whos-there/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/whos-there?logo=pypi&style=flat&color=blue)](https://pypi.org/project/whos-there/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/twsl/whos-there/pulls?utf8=✓&q=is:pr%20author:app/dependabot)
[![Conda - Platform](https://img.shields.io/conda/pn/conda-forge/whos-there?logo=anaconda&style=flat)](https://anaconda.org/conda-forge/whos-there)
[![Conda (channel only)](https://img.shields.io/conda/vn/conda-forge/whos-there?logo=anaconda&style=flat&color=orange)](https://anaconda.org/conda-forge/whos-there)
[![Docs with MkDocs](https://img.shields.io/badge/MkDocs-docs?style=flat&logo=materialformkdocs&logoColor=white&color=%23526CFE)](https://squidfunk.github.io/mkdocs-material/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![linting: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](.pre-commit-config.yaml)
[![Checked with pyright](https://microsoft.github.io/pyright/img/pyright_badge.svg)](https://microsoft.github.io/pyright/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![vulnerability: safety](https://img.shields.io/badge/vulnerability-safety-yellow.svg)](https://github.com/pyupio/safety)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/twsl/whos-there/releases)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
<!--- BADGES: END --->

The spiritual successor to [knockknock](https://github.com/huggingface/knockknock) for [PyTorch Lightning](https://github.com/PyTorchLightning/pytorch-lightning), to get a notification when your training is complete or when it crashes during the process with a single callback.


## Features

- Supports E-Mail, Discord, Slack, Teams, Telegram

## Installation

With `pip`:
```bash
python -m pip install whos-there
```

With [`poetry`](https://python-poetry.org/):
```bash
poetry add whos-there
```

With `conda`:

```bash
conda install conda-forge::whos-there
```
Check [here](https://github.com/conda-forge/whos-there-feedstock) for more information.


## Usage

```python
from whos_there.callback import NotificationCallback
from whos_there.senders.debug import DebugSender
```

See a more complete example in the [notebooks](notebooks) folder.

## API

Check the [API reference](api/whos_there/) for more details.
