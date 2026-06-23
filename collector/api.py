import asyncio
import logging
from abc import ABC, abstractmethod

import httpx

from .models import Post, User

log = logging.getLogger(__name__)


class ApiError(Exception):
    pass


class HttpClient(ABC):
    @abstractmethod
    async def get(self, path: str):
        ...


class HttpxClient(HttpClient):
    def __init__(self, base_url, retries=3, timeout=10.0):
        self.base_url = base_url
        self.retries = retries
        self._client = httpx.AsyncClient(base_url=base_url, timeout=timeout)

    async def get(self, path):
        for attempt in range(self.retries):
            try:
                resp = await self._client.get(path)
                resp.raise_for_status()
                return resp.json()
            except httpx.HTTPStatusError as e:
                code = e.response.status_code
                # 4xx — наша вина, повторять нечего
                if code < 500:
                    raise ApiError(f"{path} -> {code}") from e
                log.warning("%s вернул %s, пробуем ещё раз", path, code)
            except httpx.HTTPError as e:
                log.warning("сетевая ошибка на %s: %s", path, e)
                if attempt == self.retries - 1:
                    raise ApiError(f"не достучались до {path}: {e}") from e

            await asyncio.sleep(0.5 * (attempt + 1))

        raise ApiError(f"{path}: исчерпаны попытки")

    async def close(self):
        await self._client.aclose()


class Source(ABC):
# Один источник = один ресурс из API

    path: str

    def __init__(self, client: HttpClient):
        self.client = client

    @abstractmethod
    def parse(self, item):
        ...

    async def load(self):
        data = await self.client.get(self.path)
        return [self.parse(x) for x in data]


class Users(Source):
    path = "/users"

    def parse(self, item):
        return User.from_json(item)


class Posts(Source):
    path = "/posts"

    def parse(self, item):
        return Post.from_json(item)
