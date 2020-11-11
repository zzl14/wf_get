#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# zzl 2020

'''
###################################

question :
				id cann't control
				connection too many
				time json change 
				sever encode error
				id get some error??
###################################
'''
import os
import json
from plugins.json2time import *
import urllib.request
import urllib.parse
from fetch.fetch_client import *
from fetch.server import *
import argparse



class Wf_get():
	def __init__(self,monitor,flush_data_time,Spmac,server):
		self.all_data=[]
		self.packet_queue = []
		self.server=server
		self.monitor=monitor
		self.flush_data_time=flush_data_time

		self.Spmac=Spmac
		self.m=__import__('fetch.fetch_client', fromlist=['fetch']).fetch()
		self.go()

	def go(self):
		last_update = 0
		if self.server!=None:
			self.read_txt()
		while True:
			#time1=int(os.times()[4])
			self.get_data()
			if self.packet_queue!=[]:
				self.write_local_db()
			now = int(os.times()[4])
			if self.server!=None and abs(now - last_update) > 5 and self.all_data!=[]:
				print(self.all_data)
				last_update = now
				if self.web_upload()!=True:
					print('upload error')
					self.write_txt()
						
	def read_txt(self):
		with open("%s/data.txt" % path,"r+") as f:
			for i in f:
				print(i)
				if i!="":
					self.all_data.append(json.loads(i.strip())) 
			f.seek(0)	
			f.truncate()
			#print(self.all_data)

 	




	def write_txt(self):
		with open("%s/data.txt" % path,"a+") as f:
			for line in self.all_data:
				line=json.dumps(line)
				#print("\n\ni\n\n")
				f.write(line+'\n')
				self.all_data=[]

	def packeteer(self, p):
		if self.m.proc_packet(p)!=None:
			self.packet_queue.append(self.m.proc_packet(p))

	def get_data(self):

		sniff(iface=self.monitor, prn=self.packeteer,count=100)
	
	'''def get_local_data(self):
					print('###################################################################')
					session = Session_client()
					for p in session.query(client).filter(client.id>self.max_id).order_by(client.id):
						self.all_data.append({"ssid":p.ssid,"mac":p.mac,"Spmac":self.Spmac,"Obstime":p.Obstime,
							"Type":p.Type,"Subtype":p.Subtype,"Rssi":p.Rssi,"Verdor":p.Verdor})
					session.close()
					for i in self.all_data:
						print(i)
					print('\n\n')
					print('###################################################################')'''

	def delete_local_data(self):
		session = Session_client()
		session.query(client).filter(client.id>=0).delete()
		session.commit()
		session.close()


	def web_upload(self):
		x='zzl'
		headers = {'content-type': 'application/json','Authorization':'Basic %s' %x}
		data=''
		for p in self.all_data:
			print(p)
			data={"client":{"ssid":p['ssid'],"mac":p['mac'],"Spmac":self.Spmac,"Obstime":p['Obstime'],"Type":p['Type'],"Subtype":p['Subtype'],"Rssi":p['Rssi'],"Verdor":p['Verdor']}}
			data=json.dumps(data).encode('utf-8')
			try:
				req = urllib.request.Request(url=self.server, headers=headers, data=data)
				response = urllib.request.urlopen(req)
				print(response.read().decode(" utf-8"))
			except:
				return False
		self.all_data=[]
		return True

	def write_local_db(self):
		session = Session_client()
		for p in self.packet_queue:
			if self.flush_data_time!=0:
				if self.m.flush_data(self.flush_data_time,p['mac'],p['Obstime'])==True:
					print("the monitor "+self.monitor+" get:")
					print(p,'\n')
					id =self.m.get_next_id()
					client1 = client(id=id,ssid=p['ssid'],mac=p['mac'],Spmac=self.Spmac,Obstime=p['Obstime'],Type=p['Type'],Subtype=p['Subtype'],Rssi=p['Rssi'],Verdor=p['Verdor'])
					session.add(client1)
					session.commit()
					p['Obstime']=data2json(p['Obstime'])
					self.all_data.append(p)

		session.close()
		self.packet_queue=[]

def main():
	print ("""welcome to 
__        ___       __________      ______   ___________________
\ \      / _ \     / /_______/     / _____/ /______/  /________/        
 \ \    / / \ \   / /_____        / / __   //______      / /
  \ \__/ /   \ \_/ /_____/       /_/__\ \ //______      / /
   \____/     \___/      _______/_______///______/     /_/
""")
	if os.geteuid() != 0:
		print("Running without root privilages!")
		exit(0)

	# menu create by argparse
	usage="""Usage: [--g get information]"""
	parser = argparse.ArgumentParser(epilog='''run with 
		`-m <monitor> -p  <probemac> -t <time> -s <server>` to get and upload information or 
		run with ` -webserver 0.0.0.0:5001` to run web server ''')
	#parser.add_argument('g', action='store_true',help='get information default(true)')
	parser.add_argument('-m','--monitor',help='type the monitor name you have',default=None)
	parser.add_argument('-s','--server',help='type the url of your server to upload',default=None)
	parser.add_argument('-webserver',help='run your web server<ip:port>',default=None)
	parser.add_argument('-t','--flush_data_time',default=3,help='get same mac_packet until <time> seconds later')
	parser.add_argument('-p','--probemac',default='00:87:11:01:48:10',help='type <probemac> to  location')
	arg=parser.parse_args()
	Path=os.path.dirname(os.path.realpath(__file__))
	os.chdir(Path)
	print(Path)
	exit(0)
	if arg.webserver!=None:
		p=arg.webserver.split(':')
		print(p[0],p[1])
		run_webserver(p[0],p[1])
	#print arg.get,
	if arg.monitor and arg.webserver==None:
		Wf_get(arg.monitor,arg.flush_data_time,arg.probemac,arg.server)
if __name__=="__main__":
	main()
