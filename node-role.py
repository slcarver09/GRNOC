from globalnoc import wsc
import getpass
from pprint import pprint


#create WSC connection
client = wsc.WSC()
client.username = input("Enter username: ")
client.password = getpass.getpass('Enter password: ')
client.url = <redacted>
client.realm = <readacted>



data = client.get_node_roles(network_id = 14)

role_codes = [item["role_code"] for item in data.get("results", [])]

for code in role_codes:
    print(code)

