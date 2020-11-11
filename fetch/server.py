#!/usr/bin/env python3
from flask import Flask, request, Response, abort
import sys
import logging
import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
sys.path.append("..")
from plugins.json2time import *
from fetch.fetch_client import client
import urllib.parse

engine=create_engine('mysql+mysqlconnector://root:iamwf@localhost:3306/server',pool_size=100)
Session_server = sessionmaker(bind=engine)
Base = declarative_base()

app = Flask(__name__)

def get_next_id():
        session = Session_server()
        id_now=session.query(client.id).all()
        session.close()
        if  id_now==[]:
            id_next=0
        else:
            id_next=id_now[len(id_now)-1][0]+1
        return  id_next

def write_local_db(p):
    session = Session_server()
    id =get_next_id()
    client1 = client(id=id,ssid=p['ssid'],mac=p['mac'],Spmac=p['Spmac'],Obstime=p['Obstime'],Type=p['Type'],Subtype=p['Subtype'],Rssi=p['Rssi'],Verdor=p['Verdor'])
    session.add(client1)
    session.commit()
    session.close()

@app.route('/', methods=['POST'])
def catch_data():
    if request.method=="POST":
        if  request.headers['Content-Type'] == 'application/json':
            print(request.data)
            data=request.data.decode()
            data=json.loads(data)
            print(data)
            print(type(data),'\n')
                
            for name, value in data.items():
                for name1,value1 in data[name].items():
                    if type(data[name][name1])==float:
                        data[name][name1]=epoch_to_date(data[name][name1])
                
            write_local_db(data['client'])
            print(data)
            print(type(data),'\n')


            f= open(r"/home/zzl/Desktop/re.txt", 'a+')
            f.write(str(data))
            f.close()
            return 'data upload successly'

    else:
        return ('post?')

def run_webserver(ip="0.0.0.0",port=5001):
    app.run(host=ip, port=port,debug=True)


if __name__ == "__main__":
    run_webserver()

'''#print('\n',urllib.parse.parse_qsl(request.data))
#data=urllib.parse.parse_qsl(request.data)
print(data[0][1].decode())
print(type(data[0][1].decode()),'\n1')'''
'''except:
return 'error'''