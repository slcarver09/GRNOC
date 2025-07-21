from globalnoc import wsc
import getpass
import csv


#create WSC connection
client = wsc.WSC()
client.username = input("Enter username: ")
client.password = getpass.getpass('Enter password: ')
client.url = "https://db.net.internet2.edu/cds2/circuit.cgi"
client.realm = "https://idp.net.internet2.edu/idp/profile/SAML2/SOAP/ECP"


cidCLR = {}

#open csv create dictionary keys,values
with open('cid-clr.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cidRecord = row.get('Circuit ID')
        clrRecord = row.get('CLR')
        if cidRecord and clrRecord:
            cidCLR[cidRecord] = clrRecord

#iterate through dictionary and update CLR values
#currently need to update NETWORK_ID EVERYTIME
for cid, clr in cidCLR.items():
    #print(f"CID:{cid} -> CLR:{clr}")
    data = client.update_circuits(network_id = 50, circuit_id = cid, circuit_layout_record = clr)
    print(f"Added as CID: {cid} CLR: {clr}")
