import requests

# Define the server URL
server_url = "http://127.0.0.1:5000"

# Define the data you want to send to the server (modify this based on your needs)
input_data = {
    "can_Chow" : False,
    "can_Pong" : False,
    "can_Kong" : False,
    "throw" : [],
    "hand_tiles" : [1, 2, 0, 0, 1, 0, 0, 1, 2, 1, 1, 2, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
}

# Send a POST request to the /predict endpoint
response = requests.post(f"{server_url}/discard_tile/", json=input_data)

# Check the response
if response.status_code == 200:
    result = response.json()
    if result["success"]:
        
        print(result['action']+":{0}".format(result['tile_index']))
    else:
        error_message = result["error"]
        print("Error:", error_message)
else:
    print("Server returned status code:", response.status_code)
