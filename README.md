# SibDev Test Task

# Installation and Running
## Using docker
```bash
cat env_sample > .env  # change variables values if you need
docker-compose up -d
```

## Without docker for development
```zsh
python -m venv .venv
. .venv/bin/activate
cat env_sample > .env  # change variables values if you need

poetry install
pre-commit install
sibdev migrate
sibdev runserver
```
