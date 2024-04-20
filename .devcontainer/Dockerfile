# See here for image contents: https://github.com/devcontainers/images/blob/main/src/python/.devcontainer/Dockerfile

# [Choice] Python version (use -bookworm or -bullseye variants on local arm64/Apple Silicon): 3, 3.12, 3.11, 3.10, 3.9, 3.8, 3-bookworm, 3.12-bookworm, 3.11-bookworm, 3.10-bookworm, 3.9-bookworm, 3.8-bookworm, 3-bullseye, 3.12-bullseye, 3.11-bullseye, 3.10-bullseye, 3.9-bullseye, 3.8-bullseye, 3-buster, 3.12-buster, 3.11-buster, 3.10-buster, 3.9-buster, 3.8-buster
ARG VARIANT=3-bookworm
FROM mcr.microsoft.com/devcontainers/python:1-${VARIANT}

# [Optional] Uncomment this section to install additional OS packages.
# https://exerror.com/importerror-libgl-so-1-cannot-open-shared-object-file-no-such-file-or-directory/
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends libgl1-mesa-glx

# Temporary: Upgrade python packages due to https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-40897
# They are installed by the base image (python) which does not have the patch.
RUN python3 -m pip install --upgrade setuptools

# Install poetry
RUN pip install --upgrade pip

ENV PATH "/etc/poetry/bin:$PATH"
RUN curl -sSL  https://install.python-poetry.org | POETRY_HOME=/etc/poetry python - \
    && poetry completions bash >> ~/.bash_completion \
    && poetry config virtualenvs.create false \
    && poetry self add "poetry-dynamic-versioning[plugin]"
