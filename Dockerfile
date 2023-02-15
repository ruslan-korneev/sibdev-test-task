# `python-base` sets up all our shared environment variables
FROM python:3.11-slim as python-base

    # python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.2.1 \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"


# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


# `builder-base` stage is used to build deps + create our virtual environment
FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential \
        openssh-client \
        libffi-dev \
        git \
        libpcre3 libpcre3-dev

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python -

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
COPY src ./src/
COPY README.md ./
# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev


# `development` image is used during development / testing
FROM python-base as development
WORKDIR $PYSETUP_PATH

# copy in our built poetry + venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# quicker install as runtime deps are already installed
RUN poetry install --no-root

COPY . .

# creating open api schema
FROM python-base as rapidoc

# copy in our built poetry + venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

ENV DJANGO_SETTINGS_MODULE=src.sibdev.spectacular_settings

RUN ["sibdev", "spectacular", "--file", "schema.yml"]

FROM mrin9/rapidoc as rapidoc-run

COPY --from=rapidoc schema.yml /usr/share/nginx/html/schema.yml
ENV PAGE_TITLE="SibDev RapiDoc"
ENV SPEC_URL="schema.yml"

# `production` image used for runtime
FROM python-base as production

WORKDIR /app
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY entrypoint.sh .

# Create user so we don't run docker as root
RUN groupadd -r django && useradd -r -u 999 -g django django

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "src.sibdev.wsgi:application", \
    "-w", "4", \
    "-b", "0.0.0.0:8000", \
    "--error-logfile", "-", \
    "--enable-stdio-inheritance", \
    "--log-level", "debug"]
