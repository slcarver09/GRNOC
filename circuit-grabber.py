from globalnoc import wsc
import getpass


#create WSC connection
client = wsc.WSC()
client.username = input("Enter username: ")
client.password = getpass.getpass('Enter password: ')
client.url = "https://db.net.internet2.edu/cds2/circuit.cgi"
client.realm = "https://idp.net.internet2.edu/idp/profile/SAML2/SOAP/ECP"


cidList = []


print("This will create and print the next N CID #s")
circuitNum = int(input("How many CID#s would you like generated? "))

while circuitNum > 0:
    data = client.add_circuit_name_id(network_id = 50)
    cidList.append(data)

    if data.get("error"):
        print(f"Error: {data.get('error_text')}")
        break

    results = data.get("results", [])

    for cid in results:
        cidID = cid.get("circuit_name_id")
        if cidID:
            print(cidID)
            cidList.append(cidID)


    circuitNum -= 1




