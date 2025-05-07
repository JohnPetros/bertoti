from redis import Redis


class RedisCache:
    def __init__(self):
        self._redis = Redis(
            host="infinite-starfish-31994.upstash.io",
            port=6379,
            password="AXz6AAIjcDFkYWQ5N2Q0Mjg2NGI0ZjdiYTVjZTNjOWVkZmRmMDZhYXAxMA",
            ssl=True,
        )

    def add_item(self, key: str, value: str):
        self._redis.rpush(key, value)

    def get_last_items(self, key: str):
        return self._redis.lrange(key, -100, -1)
