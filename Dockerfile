FROM python:3.11-slim AS python-base

ARG POETRY_VERSION=1.5.1
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc as files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=$POETRY_VERSION \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    LOCALES_PATH="/opt/locales" \
    APP_PATH="/src"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM python-base AS builder-base
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        # for installing poetry
        curl \
        # for building python deps
        build-essential \
    && apt-get clean

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python -

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev


FROM python-base AS production

# vars
ARG APP_ENV=production
ENV APP_ENV=$APP_ENV

# copy generated files (python libs, .mo locales, migrations)
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# copy app files
WORKDIR $APP_PATH
COPY tools/check_health.py ./
COPY app ./app

# good luck! :)
CMD python -m app
