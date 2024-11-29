import requests

token = 'token'
url = 'https://api.vk.com/method/users.get'
params = {
    'access_token': token,
    'v': '5.131'
}
response = requests.get(url, params=params)
data = response.json()

if 'error' in data:
    print(f"Error: {data['error']['error_msg']}")
else:
    print("Token is valid, user info:", data)
