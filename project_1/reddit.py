import sys
import time
import numpy as np
from pandas import Series, DataFrame
import pandas as pd
import json 
from datetime import datetime
import pickle
from pymongo import MongoClient 
import requests 


def reader():
    file1 = open("stop.txt","r+") 
    file1 = file1.readlines()
    if file1[0] == 'stop':
        sys.exit()
        
def writer():
    dateTimeObj = datetime.now()
    ct = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    with open('status.txt', 'w') as filetowrite:
        filetowrite.write('running' + " "+ct)

def autho(first):
    base_url = 'https://www.reddit.com/'
    data = {'grant_type': 'password', 'username': 'pro7on', 'password': ''}
    auth = requests.auth.HTTPBasicAuth('g00GDJpLRnFHBQ', 'kDKxU0g7Up1_0r_Au8Msdg0BbbA')
    r = requests.post(base_url + 'api/v1/access_token',
                      data=data,
                      headers={'user-agent': 'DataScience'},
              auth=auth)
    d = r.json()


    token = 'bearer ' + d['access_token']

    base_url = 'https://oauth.reddit.com'

    headers = {'Authorization': token, 'User-Agent': 'APP-NAME by REDDIT-USERNAME'}
    response = requests.get(base_url + '/api/v1/me', headers=headers)

    #if response.status_code == 200:
    #print(response.json()['name'], response.json()['comment_karma'])
    #print(r.status_code)
    
    headers = {'Authorization': token, 'User-Agent': 'APP-NAME by REDDIT-USERNAME'}
    response = requests.get('https://oauth.reddit.com' + '/r/%s/?sort=new&t=all&limit=100' % first, headers=headers)
    #print(response.status_code)
    return response

def autho2():
    base_url = 'https://www.reddit.com/'
    data = {'grant_type': 'password', 'username': 'pro7on', 'password': 'rajivs24'}
    auth = requests.auth.HTTPBasicAuth('g00GDJpLRnFHBQ', 'kDKxU0g7Up1_0r_Au8Msdg0BbbA')
    r = requests.post(base_url + 'api/v1/access_token',
                      data=data,
                      headers={'user-agent': 'DataScience'},
              auth=auth)
    d = r.json()


    token = 'bearer ' + d['access_token']
    return token
    
    
def getter(first,last,token):
    headers = {'Authorization': token, 'User-Agent': 'APP-NAME by REDDIT-USERNAME'}
    response = requests.get('https://oauth.reddit.com' + '/r/%s/?sort=new&t=all&limit=100&before=%s' % (first , last), headers=headers)
    #print(response.status_code)
    return response

    
    
def data_saviour(response):
    data_all = []
    text_data = response.json()
    data = text_data['data']['children']
    data_all+=data
    return data_all
    
        
def time_stamp(data_all):
    dateTimeObj = datetime.now()
    ct = dateTimeObj.strftime("%d-%b-%Y, %H:%M:%S")
    for i in range(len(data_all)):
        data_all[i]['time'] = ct
    return data_all

def ins_mongo(file_data):
    myclient = MongoClient("mongodb://localhost:27017/")  
    try: 
        print("Connected successfully!!!") 
    except:   
        print("Could not connect to MongoDB") 

    # database  
    db = myclient["DataSci"] 

    # Created or Switched to collection  
    Collection = db["data2"] 

    if file_data:
        # Inserting the loaded data in the Collection 
        # if JSON contains data more than one entry 
        # insert_many is used else inser_one is used 
        if isinstance(file_data, list): 
            Collection.insert_many(file_data)   
        else: 
            Collection.insert_one(file_data) 



def main():
    data_all = []
    last = []
    with open("test.txt", "rb") as fp:   # Unpickling
        b = pickle.load(fp)
    len(b)
    writer()
    for i in range(len(b)):
        response = autho(b[i])
        if response.status_code != 200:
                continue
        data_all = data_saviour(response)
        data_all = time_stamp(data_all)
        ins_mongo(data_all)
        time.sleep(2)
        last.append(data_all[1]['data']['name'])
    print(last)
    while True:
        token = autho2()
        for i in range(len(b)):
            response = getter(b[i],last[i],token)
            if response.status_code != 200:
                time.sleep(3)
                continue
            data_all = data_saviour(response)
            data_all = time_stamp(data_all)
            ins_mongo(data_all)
            if len(data_all)>=2:
                last[i] = data_all[1]['data']['name']
            time.sleep(2)
        time.sleep(3)
        reader()

main()
