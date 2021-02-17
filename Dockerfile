FROM python:3.8-slim

RUN apt-get update && apt-get -y install \
    git openssh-server curl

ARG DEPLOY_KEY

ENV \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.1.4 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  PATH="$PATH:/root/.poetry/bin"

RUN mkdir ~/.ssh \
    && ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts \
    && echo $DEPLOY_KEY | base64 -d > ~/.ssh/id_rsa \
    && chmod 400 ~/.ssh/id_rsa \
    && echo "IdentityFile ~/.ssh/id_rsa" >> /etc/ssh/ssh_config

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python -

WORKDIR /tmp
COPY pyproject.toml poetry.lock /tmp/
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

ARG APP_HOME=/opt/backend
RUN apt-get update && \
    apt-get -y install \
        curl bash \
        ; \
    groupadd kbpp && \
    useradd -r -m -s /bin/bash -g kbpp kbpp && \
    mkdir -p $APP_HOME &&\
    chown -R kbpp:kbpp $APP_HOME/

WORKDIR $APP_HOME
COPY --chown=kbpp:kbpp . .
USER kbpp
ENTRYPOINT python run.py
