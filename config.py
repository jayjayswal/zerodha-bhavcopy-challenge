import redis

REDIS_HOST="127.0.0.1"
REDIS_PORT=6379
BHAV_COPY_URL="https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx"

def get_redis_connection():
    """
    build connection to redis
    returns:
        dict:
            success response : {"status":1,"data":"--success message--"}
            fail response : {"status":0,"data":"--error message--"}

    """
    res = {"status": 0, "data": ""}
    try:
        r = redis.StrictRedis(host='localhost',charset="utf-8",decode_responses=True, port=6379, db=0)
        res["status"]=1
        res["data"]=r
    except Exception as e:
        res["data"]="Redis connection error, Kindly contact administrator"
    return res

