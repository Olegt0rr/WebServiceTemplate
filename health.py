import asyncio
import logging
import sys
from http import HTTPStatus

from app.core.base_client import BaseClient
from app.core.settings import WebAppSettings


class HealthCheck(BaseClient):
    def __init__(self) -> None:
        settings = WebAppSettings()
        super().__init__(f"http://{settings.HOST}:{settings.PORT}")
        self.log = logging.getLogger(self.__class__.__name__)

    async def check_liveness(self) -> int:
        """Check service liveness. Return exit code."""
        status, result = await self._make_request(
            method="GET",
            url="/health/liveness",
        )

        if status == HTTPStatus.OK:
            self.log.info("Liveness probe successful.")
            return 0

        msg = f"Liveness is not successful. {status=}, {result=}"
        self.log.warning(msg)
        return 1


async def main() -> None:
    """App entrypoint."""
    checker = HealthCheck()
    try:
        exit_code = await checker.check_liveness()
    finally:
        await checker.close()

    sys.exit(exit_code)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
