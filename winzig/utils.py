from redis import Redis


class RedisCache(object):
    """
    A cache class to assist with deferred connection configuration of Redis.
    Loosely inspired by SQLAlchemy
    """

    def __init__(self, **kwargs):
        """
        All the kwargs are passed to the redis.Redis class. See redis.Redis for
        reference
        """
        self.kwargs = kwargs
        self._redis = None
        self.config_updated = False

    def configure(self, **kwargs):
        """
        All the kwargs are passed to the redis.Redis class. See redis.Redis for
        reference
        """
        self.kwargs.update(kwargs)
        self.config_updated = True

    @property
    def redis(self):
        if self._redis is None or self.config_updated:
            self._redis = Redis(**self.kwargs)

        return self._redis

    def set(self, key, value, expiry=None):
        """
        :key: string of cache key
        :value: string value to cache
        :expiry: integer expiry in seconds
        """
        self.redis.set(key, value, expiry)

    def get(self, key):
        """
        :key: get the cache by key
        :returns: string for cache value
        """
        result = self.redis.get(key)

        if result is not None:
            result = result.decode('utf8')

        return result
