import asyncio
import logging
import sys
from http import HTTPStatus

from app.core.base_client import BaseClient
from app.core.settings import WebAppSettings


class HealthCheck(BaseClient):
    """Represents health checker.

    How to use with docker-compose:
    ```yaml
    services:
      app:
        ...
        healthcheck:
          test: python3 check_health.py || exit 1
          interval: 10s
          timeout: 5s
          retries: 5
    ```
    """

    def __init__(self) -> None:
        settings = WebAppSettings()
        super().__init__(f"http://{settings.HOST}:{settings.PORT}")
        self.log = logging.getLogger(self.__class__.__name__)

    async def check_health(self) -> bool:
        """Check service health.

        True - service healthy.
        False - service unhealthy.
        """
        status, result = await self._make_request(
            method="GET",
            url="/health/liveness",
        )

        if status == HTTPStatus.OK:
            self.log.info("Liveness probe successful.")
            return True

        msg = f"Liveness is not successful. {status=}, {result=}"
        self.log.warning(msg)
        return False


async def main() -> int:
    """Run health check app (entrypoint)."""
    checker = HealthCheck()
    try:
        return await checker.check_health()
    finally:
        await checker.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ok = asyncio.run(main())
    exit_code = int(not ok)
    sys.exit(exit_code)
