import requests

# api-endpoint
URL = "https://api.agify.io"

# location given here
name = "suresh"

# defining a params dict for the parameters to be sent to the API
PARAMS = {'name':name}

# sending get request and saving the response as response object
r = requests.get(url = URL, params = PARAMS)

# extracting data in json format
data = r.json()
url= r.url
print(url)

print(data)
