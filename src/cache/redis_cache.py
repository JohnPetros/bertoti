from redis import Redis


class RedisCache:
    def __init__(self):
        self._redis = Redis(
            host="internal-satyr-11463.upstash.io",
            port=6379,
            password="ASzHAAIjcDFiOWFlNzZmNmZkZTg0YzAyYjFhNDdhZTM1YTllZjAxNXAxMA",
            ssl=True,
        )

    def add_item(self, key: str, value: str):
        self._redis.rpush(key, value)

    def get_last_items(self, key: str):
        return self._redis.lrange(key, -100, -1)
