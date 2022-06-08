from flask import Flask, request
import requests
from requests.auth import HTTPBasicAuth
import json

app = Flask(__name__)

# mpesa details

consumer_key = 'izXt7aaWvhXg35sYgUuBMNqQlcx2GxbA'
consumer_secret = 'XNHlyPvTA5a3xgsD'
base_url='http://192.168.43.132:801/'

@app.route("/")
def home():
    return "Hello"
# access token

@app.route("/access_token")
def ac_token():
    data=ac_token()
    return data 

# simulate
@app.route("/simulate")
def simulate():
    mpesa_endpoint="https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
    access_token=ac_token()
    headers = { "Authorization": "Bearer %s" % access_token }
    request_body={
        "ShortCode": "600383",
        "CommandID": "CustomerPayBillOnline",
        "BillRefNumber": "TestPay1",
        "Msisdn": "254724628580",
        "Amount": "10"
    }

    simulate_response=requests.post(mpesa_endpoint, json=request_body, headers=headers)
    return simulate_response.json()

@app.route("/register_urls")
def register():
    mpesa_endpoint="https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = { "Authorization":"Bearer %s" % ac_token() }

    req_body = {
            "ShortCode": "600383",
            "ResponseType": "Completed",
            "ConfirmationURL": base_url + "/c2b/confirm",
            "ValidationURL": base_url + "/c2b/validation"        
    }

    # response_data=requests.post(
    #     mpesa_endpoint,
    #     json={
    #         "ShortCode": "200200",
    #         "ResponseType": "Transaction Completed",
    #         "ConfirmationURL": base_url + "/c2b/confirm",
    #         "ValidationURL": base_url + "/c2b/validation"
    #     },
        
    response_data = requests.post(
        mpesa_endpoint,
        headers = headers,
        json=req_body
    )

    return response_data.json()

@app.route('/c2b/confirm', methods=['POST'])
def confirm():
    data=request.get_json()

    # write to file
    with open('confirm.json', 'a') as file:
        file.write(json.dumps(data))
        return {
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        }

@app.route('/c2b/validation', methods=['POST'])
def validate():
    data=request.get_json()

    # write to file
    with open('confirm.json', 'a') as file:
        file.write(json.dumps(data))
        return {
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        }


def ac_token():
    mpesa_auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    data = (requests.get(mpesa_auth_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))).json()
    return data['access_token']


if __name__=="__main__":
    app.run(port=7000, debug=True)

