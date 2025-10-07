from globalnoc import wsc
import getpass
from pprint import pprint


#create WSC connection
client = wsc.WSC()
client.username = input("Enter username: ")
client.password = getpass.getpass('Enter password: ')
client.url = "https://db.net.internet2.edu/cds2/node.cgi"
client.realm = "https://idp.net.internet2.edu/idp/profile/SAML2/SOAP/ECP"



data = client.get_node_roles(network_id = 14)

role_codes = [item["role_code"] for item in data.get("results", [])]

for code in role_codes:
    print(code)

