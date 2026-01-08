from redis import Redis
from rq import Queue

# creating a Redis connection by giving host_name and port number 
redis_connection = Redis(
  host="valkey",
  port="6379"
)

q = Queue(connection=redis_connection)  # give username and password