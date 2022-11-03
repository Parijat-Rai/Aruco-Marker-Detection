# importing the requests library
import requests

# defining the api-endpoint
cart_api = "http://10.12.27.219:3000/cart"

# data to be sent to api
data = { "userTag" : 1 }

# sending post request and saving response as response object
r = requests.post(url = cart_api, json= data)

data = r.json()
print(data)

# # extracting response text
# pastebin_url = r.text
# print("The pastebin URL is:%s"%pastebin_url)
