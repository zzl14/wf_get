#from scapy.all import sniff, Dot11Elt, Dot11ProbeReq, rdpcap, PcapReader
from scapy.all import *
import time
import datetime
#from  .sql_test import *
from sqlalchemy import Sequence
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
 
engine=create_engine('mysql+mysqlconnector://root:iamwf@localhost:3306/test',pool_size=100)
Session_client = sessionmaker(bind=engine)
Base = declarative_base()
class client(Base):
	__tablename__ = 'client'
	id = Column(Integer, primary_key=True)
	ssid = Column(String)
	mac = Column(String)
	Spmac = Column(String)
	Obstime = Column(String)
	Type=Column(String)
	Subtype=Column(String)
	Rssi=Column(String)
	Verdor=Column(String)
	#ssid = Column(String)	


def flush_data(time,mac,now):
	session = Session_client()
	last_time=session.query(client.Obstime).filter(client.mac==mac)
	session.close()
	#print(mac,now,last_time[-1:],'\n'*3)
	if last_time[-1:]==[]:
		return True
	#print(now.timestamp()-last_time[-1:][0][0].timestamp(),int(time))
	if now.timestamp()-last_time[-1:][0][0].timestamp()>=int(time):
		return True
	else:
		return False
	

	

def get_next_id():
	session = Session_client()
	id_now=session.query(client.id).all()
	session.close()
	if 	id_now==[]:
		id_next=0
	else:
		id_next=id_now[len(id_now)-1][0]+1
	return  id_next

def proc_packet(p):
	if not p.haslayer(Dot11ProbeReq):
		return 
	if p[Dot11Elt].info !=None:
		try:
			ssid = p[Dot11Elt].info.decode('utf-8')
		except:
			ssid="none"
	mac = p.addr2
	Obstime = datetime.datetime.fromtimestamp(int(p.time))
	Type=p.type
	Subtype=p.subtype
	Rssi=p.dBm_AntSignal
	Verdor=mac[0:8]
	return [ssid,mac,Obstime,Type,Subtype,Rssi,Verdor]
'''
def get_data(p):
	if not p.haslayer(Dot11ProbeReq):
		return
	timeStamp = datetime.datetime.fromtimestamp(int(p.time))
	mac = p.addr2
	vendor =mac[0:8]
	ssid="none"
	if p[Dot11Elt].info != '':
		ssid = p[Dot11Elt].info.decode('utf-8')
	#print(p.show())
	print (timeStamp,'get data:')
	print ('mac:',mac)
	print ('type',p.type)
	print ('subtype',p.subtype)
	print ('dBm_signal',p.dBm_AntSignal)
	print ('vendor:',vendor)
	print ('ssid:',ssid,'\n')
	#print("time",time)
	add([mac,vendor,ssid]) 
#a=sniff(iface="wlx008711014810",count=10000)
'''