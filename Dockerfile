FROM python:3.13-slim AS python-base

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc as files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    APP_PATH="/src"

# prepend venv to path
ENV PATH="$VENV_PATH/bin:$PATH"


FROM python-base AS builder-base

# install uv - https://docs.astral.sh/uv/guides/integration/docker/
COPY --from=ghcr.io/astral-sh/uv:0.12.8 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT="$VENV_PATH"

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY pyproject.toml uv.lock ./

# install runtime deps into $VENV_PATH from the lock file
RUN uv sync --frozen --no-dev


FROM python-base AS production

# vars
ARG APP_ENV=production
ENV APP_ENV=$APP_ENV

# copy generated files (python libs)
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# copy app files
WORKDIR $APP_PATH
COPY tools/check_health.py ./
COPY app ./app

# good luck! :)
CMD python -m app
