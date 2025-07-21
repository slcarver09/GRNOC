from globalnoc import wsc
import getpass
import csv


#create WSC connection need to update URL/REALM
client = wsc.WSC()
client.username = input("Enter username: ")
client.password = getpass.getpass('Enter password: ')
client.url = ""
client.realm = ""


circuitNames = []


#open csv
with open('circuits.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row.get('circuit_name')
        if name:
            circuitNames.append(name)

#iterate through list print CID:
#currently need to update NETWORK_ID EVERYTIME
for circuitName in circuitNames:

    data = client.get_circuits(network_id = 50, name = circuitName)

    results = data.get("results", [])

    for circuit in results:
        if results:
            cid = results[0]
            circuit_id =  cid.get("circuit_id")
            print(f"Circuit Name: {circuitName} - Circuit ID: {circuit_id}")
        else:
            print("No circuits found.")

