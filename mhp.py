import requests
import json


app_key = '6lq72XbBxaQ5ccoz'
golf_event_type_id = 3

# log-in
def login():

    payload = 'username=martahp&password=Mitsloan01'
    headers = {'X-Application': '6lq72XbBxaQ5ccoz', 'Content-Type': 'application/x-www-form-urlencoded'}

    resp = requests.post('https://identitysso.betfair.com/api/certlogin', data=payload, cert=('C:\Users\Jason\mhp_certs\client-2048.crt', 'C:\Users\Jason\mhp_certs\client-2048.key'), headers=headers)
 
    if resp.status_code == 200:
        resp_json = resp.json()
        print resp_json['loginStatus']
        print resp_json['sessionToken']
        session_token = resp_json['sessionToken']
        return session_token
        
    else:
        print "Request failed."
        return 0
        

session_token = 'm1Zl51U1H/PYSWOIE3pQcDFocEjYv+IMv5tdPq9Z2sk='

 
url="https://api.betfair.com/exchange/betting/json-rpc/v1"
header = { 'X-Application' : app_key, 'X-Authentication' : session_token ,'content-type' : 'application/json' }
 
jsonrpc_req='{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEvents", "params": {"filter":{"eventTypeIds":["3"]}}, "id": 1}'
 
response = requests.post(url, data=jsonrpc_req, headers=header)
 
print json.dumps(json.loads(response.text), indent=3)

        

 
        
    