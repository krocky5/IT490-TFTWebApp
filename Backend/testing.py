from api import *

# file for testing when not connected to the other containers
body = (str)(input('name: '))
response = riotAPI.main(body)

print(response)





