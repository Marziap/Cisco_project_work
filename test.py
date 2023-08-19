import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

umbrella_token = os.getenv("UMBRELLA_TOKEN")


def ListAllActivity(ip, time_to, time_from, limit, verdict):
    url = "https://api.umbrella.com/reports/v2/activity?from={}&to={}&limit={}&ip={}&verdict={}".format(time_from, time_to, limit, ip, verdict)
    headers = {
        'Authorization':'Bearer {}'.format(umbrella_token)
    }
    
    res = requests.get(url, headers = headers)
    #print(json.dumps(res.json(), indent = 4))
    
    try:
        response_data = res.json()
    except json.JSONDecodeError as e:
        print("Error decoding JSON response:", e)
        print("Response content:", res.content)
        response_data = None  # O qualsiasi altra azione appropriata che desideri intraprendere

    list = []

    for el in response_data["data"] :
        dominio = str(el["domain"])
        verdetto = str(el["verdict"])

        dict = {'verdetto' : verdetto, 'dominio' : dominio}
        if dict not in list :
            list.append(dict)

    return list
