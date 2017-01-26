from unittest import TestCase
from unittest.mock import MagicMock

from redis import Redis

from winzig.utils import RedisCache


class RedisCacheTestCase(TestCase):
    def setUp(self):
        redis = Redis('redis.local')
        redis.flushdb()

    def get_conn_config(self, cache, key):
        return cache.redis.connection_pool.connection_kwargs.get(key)

    def test_initializing_cache(self):
        cache = RedisCache()
        self.assertEquals(cache.kwargs, {})

        cache = RedisCache(host='redis.local', port=5432)
        self.assertEquals(cache.kwargs, {'host': 'redis.local', 'port': 5432})

    def test_configure_updates_config(self):
        cache = RedisCache()
        cache.configure(host='redis.local')

        self.assertEquals(cache.kwargs, {'host': 'redis.local'})

    def test_redis_property_changeable_config(self):
        cache = RedisCache()
        self.assertEquals(self.get_conn_config(cache, 'host'), 'localhost')

        cache.configure(host='redis.local')
        self.assertEquals(self.get_conn_config(cache, 'host'), 'redis.local')

    def test_set(self):
        cache = RedisCache()
        cache._redis = MagicMock()
        cache._redis.set = MagicMock()
        cache.set('key', 'value', 300)
        cache._redis.set.assert_called_once_with('key', 'value', 300)

    def test_get(self):
        cache = RedisCache()
        cache._redis = MagicMock()
        cache._redis.get = MagicMock()
        cache._redis.get.return_value = b'ok'
        result = cache.get('key')
        cache._redis.get.assert_called_once_with('key')
        self.assertEquals('ok', result)

    def test_set_get_with_real_redis(self):
        cache = RedisCache(host='redis.local')
        self.assertIsNone(cache.get('key'))
        cache.set('key', 'testvalue')
        self.assertEquals('testvalue', cache.get('key'))
