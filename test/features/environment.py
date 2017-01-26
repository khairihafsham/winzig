from redis import Redis


def before_feature(context, feature):
    redis = Redis(host='redis.local')
    redis.flushdb()
