import time
import redis

r = redis.Redis(host='localhost', port=6379, db=0, charset='utf8', decode_responses=True)

r.set('mobile', '233')
r.expire('mobile', 1)
print(r.get('mobile'))

time.sleep(1)
print(r.get('mobile'))
