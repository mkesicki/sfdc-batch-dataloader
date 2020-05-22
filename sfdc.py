#!/usr/bin/python3 -u

import requests
import pprint

headers = {}
instance = ""

def login(args):


    url =  "https://" + args.login_url.replace("https://", "")
    print("Login to salesforce: " + url)

    params = {
        "client_id": args.client_id,
        "client_secret": args.client_secret,
        "username": args.username,
        "password": args.password,
        "grant_type": "password"
    }

    r = requests.post(url + "/services/oauth2/token", data=params)

    pprint.pprint(params)
    pprint.pprint(r.json())

    access_token = r.json().get("access_token")
    instance_url = r.json().get("instance_url")

    global headers

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token
    }

    print("Salesforce instance: " + instance_url)

    global instance
    instance = instance_url

    return instance_url