# Web Service Template

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

- pydantic settings
- uvloop
- ujson
- backoff

---

## How to launch

### Pure python

```bash
python -m app
```

### Docker / Docker-compose

````yaml
docker-compose up -d
````
