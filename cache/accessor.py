import redis


def get_redis_connection() -> redis.Redis:
    return redis.Redis(
        host='cache', 
        port=6379, 
        db=0
        )


