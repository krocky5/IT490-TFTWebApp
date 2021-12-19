import time
from api import *

start_time = time.time()

# file for testing when not connected to the other containers
body = (str)(input('name: '))
response = RiotAPI.main(body)

print(time.time() - start_time)
print(response)

