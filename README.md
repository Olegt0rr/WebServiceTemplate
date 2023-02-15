Web Service Template
===

[![Python](https://img.shields.io/badge/python-^3.11-blue)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Code linter: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
---

Simple aiohttp-based webservice template.
Extendable.
Scalable.

---

## Consists of

### 1. CORE

Webserver and client are based on [aiohttp](https://github.com/aio-libs/aiohttp).

### 2. REDIS

Service for cache and states based on [redis.asyncio](https://github.com/redis/redis-py)

### 3. TELEGRAM

Telegram API client based on [aiogram v3](https://github.com/aiogram/aiogram/tree/dev-3.x)

- ready for polling/webhook update listening mode

### 4. OTHER SERVICES

You easily can add any other service :)

### Utils

- **pydantic settings** – ready to read .env / docker secrets
- **uvloop** – speed up asyncio event loop
- **ujson** – speed up json (de)serialization
- **backoff** – retry on network and other failures

---

## How to launch

### 1. CREATE / COPY CONFING

Example of .env config located in /examples folder. \
Copy it to the root of the project or copy into your app manager (e.g. portainer) \
Don't forget to edit it :)

### 2. LAUNCH THE APP WITH:

### Pure python

```bash
python -m app
```

### Docker / Docker-compose

````yaml
docker-compose up -d
````
