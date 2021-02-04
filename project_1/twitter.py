import requests
import os
import json
import ndjson
import datetime
import time

def connect_to_endpoint(url, headers):
   # params = {'q': 'covid-19'}
    # f = open("ds.json", "w")
    response = requests.request("GET", url, headers=headers, stream=True)
    print(response.status_code)
    count = 0
    #response = response.json(cls=ndjson.Decoder)
    with open("data.ndjson", "w", encoding="utf-8") as f, open("time.txt", "w") as f1:
        for response_line in response.iter_lines():
            if response_line:
                count = count + 1
                json_response = ndjson.loads(response_line)
               # print(ndjson.dumps(json_response, indent=4, ensure_ascii=False,sort_keys=True))
               # print('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
               # f.write('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + " " + str(count) + " ")
                ndjson.dump(json_response,f,ensure_ascii=False)
                f.write("\n")
                f1.write("{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()) + ";" + str(count) + "\n")
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
text = "covid19"
timeout = time.time() + 60 * 45
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAHzJIwEAAAAAjgBmBpuH3GffY86P2ABJrVUCm1c%3Dt4sv67ik545ON6Ea5eWS7gHGIg1RrmEr4fq4s71fNGHy6lSjTw'
url = 'https://api.twitter.com/2/tweets/sample/stream?tweet.fields=attachments,author_id,context_annotations,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,source,text,withheld&expansions=referenced_tweets.id'
headers = {"Authorization": "Bearer {}".format(BEARER_TOKEN),
           "Content-type": "application/x-ndjson"}

while True:
        connect_to_endpoint(url, headers)
        timeout += 1
