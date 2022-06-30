from asyncio import CancelledError, Task, sleep, TimeoutError, create_task
from datetime import datetime
from json import loads
from typing import Callable, Dict, List
from async_timeout import timeout
from redis.asyncio import Redis
from fastapi import FastAPI
from starlette.requests import Request

from ..settings import Settings


class RedisContext:
    settings: Settings
    redis: Redis
    subscriptions: List[Task] = []

    def __init__(self, settings: Settings):
        self.settings = settings

    def start(self):
        self.redis = Redis(host=self.settings.REDIS_HOSTNAME)

    async def stop(self):
        for task in self.subscriptions:
            task.cancel()
            try:
                await task
            except Exception as ex:
                print(ex)  # handle these better...
        await self.redis.close()

    async def _create_subscription(self, channel: str, cancelled: Callable = None):
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(channel)
        while True:
            try:
                if cancelled and await cancelled():
                    break
                async with timeout(1):
                    message = await pubsub.get_message(ignore_subscribe_messages=True)
                    if message:
                        yield self._process_message(message)
                        await sleep(0.01)
            except TimeoutError:
                pass

    def _process_message(self, message: Dict[str, any]):
        try:
            return {
                "timestamp": datetime.utcnow(),
                "channel": message.get("channel").decode("utf8"),
                "data": loads(message.get("data").decode("utf8")),
            }
        except Exception as ex:
            print(ex)

    def subscribe(
        self,
        channel: str,
        handler: Callable[[dict], None] = None,
        cancelled: Callable = None,
    ):
        subscription = self._create_subscription(channel, cancelled)

        async def loop():
            async for message in subscription:
                if handler:
                    await handler(message)
                pass

        self.subscriptions.append(create_task(loop()))
        return subscription


def start_redis_context(app: FastAPI, settings: Settings):
    redis = RedisContext(settings)
    redis.start()
    app.state.redis = redis
    return redis


async def stop_redis_context(app: FastAPI):
    redis: RedisContext = app.state.redis
    await redis.stop()


def get_redis_context(request: Request):
    redis: RedisContext = request.app.state.redis
    return redis
