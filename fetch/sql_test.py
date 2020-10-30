from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
class Client(Base):
	__tablename__ = 'Client'
	id = Column(Integer, primary_key=True)
	mac = Column(String)
	ssid = Column(String)
	vender = Column(String)

def proc_packet(p)


def  add(p):
	engine=create_engine('mysql+mysqlconnector://root:iamwf@localhost:3306/test')
	Session = sessionmaker(bind=engine)
	session = Session()
	id_now=session.query(Client.id).all()
	if 	id_now==[]:
		id_next=0
	else:
		id_next=id_now[len(id_now)-1][0]+1
	client1 = Client(id=id_next,mac=p[0],vender=p[1],ssid=p[2])
	session.add(client1)
	session.commit()
	session.close()
def main():
	sniff(iface=monitor, prn=get_data,count=10000)
	
if __name__=="__main__":
	main()

'''
sql order

use test
show tables;
desc Client;
delete from Client where id>=0;
select * from Client;

create table client(id INTEGER Primary key, 
mac VARCHAR(64) NOT NULL, 
Spmac varchar(64) not null, 
Obstime DATETIME NOT NULL,
 Type varchar(64) not null, 
 Subtype varchar(64) not null, 
 Rssi varchar(64) not null, 
 Verdor varchar(64) not null);

'''
'''
Wifi_sp 探针表
Wifi_sp
序号	列名	类型	是否为空	说明
2	Spmac	VARCHAR(64)	NOT NULL,	mac
3	Location	VARCHAR(128)		
4	spLng	VARCHAR(64)		
5	SpLat	VARCHAR(64)		

wifi_client_list：
wifi_client_list
	Id	INTEGER	NOT NULL,	
	mac	VARCHAR(64)	NOT NULL,	
	Spmac	INTEGER	NOT NULL,	mac
	Obstime	DATETIME	NOT NULL,	
	wifiPacktype	VARCHAR(64)	NOT NULL,	
	Wifisubtype	VARCHAR(64)	NOT NULL,
	Mrssi	VARCHAR(64)	NOT NULL,
	mVendor	VARCHAR(64)	
'''