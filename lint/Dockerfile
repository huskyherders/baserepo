FROM ubuntu:20.04

# Labels and info
LABEL name="Linter" \
      version="0.0" \
      description="Container to run lint_wrapper and all linters as git pre-commit hook" \
      maintainer="huskyherders" \
      help="Build image and run linter commands." \
      architecture="x86_64"

# Setup Env
ENV TERM=xterm
WORKDIR /work

# Libraries installed:
# Git for determining files that were modified.
# wget for downloading libraries
# python 3.7 for running lint_wrapper
# python3-pip for installing requirements.txt
# clang-format=9 for linting c
RUN apt-get -y update && apt-get install -y --no-install-recommends \
    git \
    wget \
    python3.7 \
    python3-pip \
    clang-format-9

# Download hadolint for Dockerfile
RUN wget -O /bin/hadolint \
    https://github.com/hadolint/hadolint/releases/download/v1.18.0/hadolint-Linux-x86_64 \
    && chmod +x /bin/hadolint

# Copy files from lintdir - set ARG here so that can restart from here on change
ARG LINTDIR=.
COPY $LINTDIR /work
RUN pip3 install -r /work/requirements.txt

# Setup non-root access to docker
ARG USER_ID
ARG GROUP_ID
RUN groupadd -r user -g $GROUP_ID && useradd --no-log-init -r -g $GROUP_ID -u $USER_ID user
USER user
