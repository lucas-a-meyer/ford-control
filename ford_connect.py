import requests
import json
import datetime as dt
import pytz


def create_headers(config_data):
    access_token = get_access_token(config_data)
    application_id = config_data['application_id']

    return {
        'Authorization': f'Bearer {access_token}',
        'Application-Id': f'{application_id}',
        'Accept': 'application/json'
    }

def get_access_token(config_data):
    client_id = config_data['client_id']
    client_secret = config_data['client_secret']
    refresh_token = config_data['refresh_token']
    token_expires = config_data['token_expires']
    application_id = config_data['application_id']

    refresh_token_url = f"https://dah2vb2cprod.b2clogin.com/{application_id}/oauth2/v2.0/token?p=B2C_1A_signup_signin_common"

    # Parse token_expires to a datetime object
    token_expires_dt = dt.datetime.fromisoformat(token_expires)
    now_utc = dt.datetime.now(pytz.utc)

    # check if the token is expired
    if token_expires_dt < now_utc:

        # Need to refresh the token
        print("Refreshing token...")

        # Data for the token request
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': client_id,
            'client_secret': client_secret
        }

        # Send POST request to obtain the token
        response = requests.post(refresh_token_url, data=data)

        # Check if the request was successful
        if response.status_code == 200:
            token_info = response.json()  # Get the token info as JSON
            access_token = token_info['access_token']  # Extract the access token
            refresh_token = token_info['refresh_token']  # Extract the refresh token
            token_expires = token_info['expires_on']

            # Convert the token_expires to a datetime object
            token_expires_dt = dt.datetime.fromtimestamp(int(token_expires))

            # The token_expires_dt is in Detroit time, convert to UTC
            token_expires_dt = token_expires_dt.astimezone(pytz.timezone('UTC'))

            token_expires = token_expires_dt.isoformat()

            # Save the new refresh token to the ford_config.json file
            config_data['refresh_token'] = refresh_token
            config_data['access_token'] = access_token
            config_data['token_expires'] = token_expires
            with open('ford_config.json', 'w') as json_file:
                json.dump(config_data, json_file)

        else:
            print(f"Failed to get token. Status Code: {response.status_code}")
            print("Error response:", response.text)

    else:
        access_token = config_data['access_token']

    return access_token    

def get_vehicle_info(config_data):

    vehicle_id = config_data['vehicle_id']

    get_info_url = f"https://api.mps.ford.com/api/fordconnect/v3/vehicles/{vehicle_id}"
    print("get_info_url:", get_info_url)  

    headers = create_headers(config_data)
    print("headers:", headers)

    response = requests.get(get_info_url, headers=headers)

    if response.status_code == 200:
        vehicles_data = response.json()
        print("Vehicle Data:", vehicles_data)
    else:
        print(f"Failed to retrieve data. Status Code: {response.status_code}")
        print("Error response:", response.text)


def list_vehicles(config_data):
    list_vehicles_url = "https://api.mps.ford.com/api/fordconnect/v2/vehicles"
    print("list_vehicles_url:", list_vehicles_url)
    
    headers = create_headers(config_data)
    print("headers:", headers)

    response = requests.get(list_vehicles_url, headers=headers)
    print("response:", response)   

    if response.status_code == 200:
        vehicles_data = response.json()
        print("Vehicles Data:", vehicles_data)
    else:
        print(f"Failed to retrieve data. Status Code: {response.status_code}")
        # print everything you can about the response
        print("Error response:", response.text)

def get_service_health(config_data):
    list_vehicles_url = "https://api.mps.ford.com/api/fordconnect/v1/health"
    print("list_vehicles_url:", list_vehicles_url)
    
    headers = create_headers(config_data)
    print("headers:", headers)

    response = requests.get(list_vehicles_url, headers=headers)
    print("response:", response)   

    if response.status_code == 200:
        vehicles_data = response.json()
        print("Vehicles Data:", vehicles_data)
    else:
        print(f"Failed to retrieve data. Status Code: {response.status_code}")
        # print everything you can about the response
        print("Error response:", response.text)


def lock_vehicle(config_data):
    vehicle_id = config_data['vehicle_id']
    lock_url = f"https://api.mps.ford.com/api/fordconnect/v1/vehicles/{vehicle_id}/lock"

    print("lock_url:", lock_url)  
    headers = create_headers(config_data)

    print("headers:", headers)

    response = requests.post(lock_url, headers=headers)
    if response.status_code == 200:
        print("Vehicle locked successfully.")
    else:
        print(f"Failed to lock vehicle. Status Code: {response.status_code}")
        print("Error response:", response.text)


def main():
    with open('ford_config.json', 'r') as json_file:
        config_data = json.load(json_file)

    # get_service_health(config_data)
    # list_vehicles(config_data)
    get_vehicle_info(config_data)
    # lock_vehicle(config_data)

if __name__=="__main__":
    main()
