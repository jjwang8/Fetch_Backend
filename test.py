import requests
import json

URL = 'http://127.0.0.1:5000' #Change if you change the port or etc in app.py

def add(payer, points, timestamp): 
    response = requests.post(f'{URL}/add', json={
        "payer": payer,
        "points": points,
        "timestamp": timestamp
    })
    if response.status_code == 200:
        print(f"Added {points} points for {payer} worked.")
    else:
        print(f"Failed to add points for {payer}: {response.text}")

def spend(points):
    response = requests.post(f'{URL}/spend', json={
        "points": points
    })
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Failed to spend points: {response.text}")

def get_balance():
    response = requests.get(f'{URL}/balance')
    if response.status_code == 200:
        print(f"Current balance:\n{json.dumps(response.json(), indent=4)}")
    else:
        print(f"Failed to get balance: {response.text}")

#Run the cases
print("Starting sample test!!!!")

add("DANNON", 300, "2022-10-31T10:00:00Z")
add("UNILEVER", 200, "2022-10-31T11:00:00Z")
add("DANNON", -200, "2022-10-31T15:00:00Z")
add("MILLER COORS", 10000, "2022-11-01T14:00:00Z")
add("DANNON", 1000, "2022-11-02T14:00:00Z")

# Spend points
spend(5000)

# Get balance
get_balance()