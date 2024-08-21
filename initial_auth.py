import requests
import json

with open('ford_config.json', 'r') as json_file:
    config_data = json.load(json_file)

# check that both the access_token and refresh_token are blank or not present in the config data
if 'access_token' in config_data and 'refresh_token' in config_data:
    if config_data['access_token'] != '' and config_data['refresh_token'] != '':
        print("Access and refresh tokens already exist in the config file.")
        exit()

# URL for the OAuth2 token endpoint
token_url = "https://dah2vb2cprod.b2clogin.com/914d88b1-3523-4bf6-9be4-1b96b4f6f919/oauth2/v2.0/token?p=B2C_1A_signup_signin_common"

# Client credentials
client_id = config_data['client_id']
client_secret = config_data['client_secret']

# Authorization code (received when you click the link in Ford's Word document)
authorization_code = config_data['authorization_code']

# Redirect URI (the same one you used in the authorization request)
redirect_uri = "https://localhost:3000"

# Data for the token request
data = {
    'grant_type': 'authorization_code',
    'code': authorization_code,
    'redirect_uri': redirect_uri,
    'client_id': client_id,
    'client_secret': client_secret
}

# Send POST request to obtain the token
response = requests.post(token_url, data=data)

# Check if the request was successful
if response.status_code == 200:
    token_info = response.json()  # Get the token info as JSON
    access_token = token_info['access_token']  # Extract the access token
    refresh_token = token_info['refresh_token']  # Extract the refresh token

    # Save the new access and refresh tokens to the ford_config.json file
    config_data['access_token'] = access_token
    config_data['refresh_token'] = refresh_token
    with open('ford_config.json', 'w') as json_file:
        json.dump(config_data, json_file)


else:
    print(f"Failed to get token. Status Code: {response.status_code}")
    print("Error response:", response.text)

