from flask import Flask, request, jsonify
from collections import defaultdict
from datetime import datetime
import heapq

app = Flask(__name__)

#transactions and balance for the payer
history = [] #transaction history priority_queue to efficiently grab latest payment
balances = defaultdict(int) #balance of the payers, defaultdict because if payer's points are used up we will want to show name and points
total = 0 #total balance

#indexes into the tuple for history
TIMESTAMP = 0
POINTS = 1
PAYER = 2

def parse(s): #Parses the time stamp from json
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")

@app.route('/add', methods=['POST'])
def add_points():
    #The add route
    input = request.json
    #Grabs the info from the json input
    payer, points, timestamp = input['payer'], input['points'], parse(input['timestamp'])

    #process request
    heapq.heappush(history, [timestamp, points, payer])
    balances[payer] += points
    global total
    total += points

    return '', 200

@app.route('/spend', methods=['POST'])
def spend_points():
    global total
    #the spend route
    input = request.json
    #grabs info from json
    req_points = input['points']

    #Error case when not enough points
    if req_points > total:
        return "User doesn't have enough points.", 400
    
    #Main loop to retrieve the oldest payment first
    result = {} #result stored in dict first to track net changes
    ReAdd = [] #Re-adds payments after all payments are checked, case where only part of an beginning payment is used, prevent infinite loop
    while req_points > 0:
        #Grab the oldest payment
        if len(history) == 0: #If all payments have been checked but there are past ones still positive, then use them.
            for i in ReAdd:
                heapq.heappush(history, i)
            ReAdd.clear()

        item = heapq.heappop(history)
        payer, points = item[PAYER], item[POINTS]

        if points < 0: #add the negative balance to the current 
            req_points -= points
            balances[payer] -= points
            total -= points
            result[payer] = result.get(payer, 0) - points
            continue
        elif points == 0: #ignore 0 payments
            continue

        points = min(points, balances[payer]) #to prevent a payer's balance from going to negative 

        if req_points >= points: #Entire payment is spent
            #update the still needed points and balances
            req_points -= points
            balances[payer] -= points
            total -= points
            result[payer] = result.get(payer, 0) - points #update the response
            if item[POINTS] > points: #The case where line 65 happened, ie negative future payment and preventing from going negative
                item[POINTS] -= points
                ReAdd.append(item) #re-add the edited payment
        else:
            item[POINTS] -= req_points #inplace update of the oldest payment
            balances[payer] -= req_points
            total -= req_points
            result[payer] = result.get(payer, 0) - req_points
            req_points = 0 #just to end loop and for last json row
            ReAdd.append(item)
    
    for i in ReAdd: #Re-adds any payments if needed
        heapq.heappush(history, i)

    list_json = [{k: v} for k, v in result.items() if v != 0]
    return jsonify(list_json), 200

@app.route('/balance', methods=['GET'])
def get_balance():
    #grabs the current balances
    return jsonify(balances), 200

#Starting the app
if __name__ == '__main__':
    app.run(port=5000, debug=True)