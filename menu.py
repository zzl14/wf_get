#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# zzl 2020

'''
###################################

question :
				id cann't control
				connection too many

###################################
'''
import os
from collections import deque
from fetch.fetch_client import *
import argparse


def packeteer(self, p):
        """In the interest of thread safety, we now do this sequentially."""
        # Give the packet to each module
        #for m in self.modules:
        #    m.proc_packet(p)
        self.packet_queue.append(p)

class Wf_get():
	def __init__(self,monitor,flush_data_time,Spmac="Empty"):
		self.all_data={}
		self.packet_queue = []

		self.monitor=monitor
		self.flush_data_time=flush_data_time
		self.Spmac=Spmac
		#self.db=create_engine('mysql+mysqlconnector://root:iamwf@localhost:3306/test')
		self.go()

	def go(self):
		while True:
			self.get_data()
			self.write_local_db()

	def packeteer(self, p):
		if proc_packet(p)!=None:
			self.packet_queue.append(proc_packet(p))

	def get_data(self):
		sniff(iface=self.monitor, prn=self.packeteer,count=100)
	


	def write_local_db(self):
		session = Session_client()
		length=len(self.packet_queue)
		for p in self.packet_queue:
			if flush_data(self.flush_data_time,p[1],p[2])==False:
				continue
			print("the monitor "+self.monitor+" get:")
			print(p,'\n')
			id =get_next_id()
			client1 = client(id=id,ssid=p[0],mac=p[1],Spmac=self.Spmac,Obstime=p[2],Type=p[3],Subtype=p[4],Rssi=p[5],Verdor=p[6])
			session.add(client1)
			session.commit()
		session.close()
		packet_queue=[]

def main():
	print ("""welcome to 
__        ___       __________      ______   ___________________
\ \      / _ \     / /_______/     / _____/ /______/  /________/        
 \ \    / / \ \   / /_____        / / __   //______      / /
  \ \__/ /   \ \_/ /_____/       /_/__\ \ //______      / /
   \____/     \___/      _______/_______///______/     /_/
""")
	if os.geteuid() != 0:
		print("Running without root privilages. Some things may not work.")

	# menu create by argparse
	usage="""Usage: [--g get information]"""
	parser = argparse.ArgumentParser(epilog="run with `-m <monitor> -p  <probemac> ` to get information")
	parser.add_argument('g', action='store_true',help='get information default(true)')
	parser.add_argument('-m','--monitor',help='type the monitor name you have')
	parser.add_argument('-t','--time',default='0',help='get same mac_packet until <time> seconds later')
	parser.add_argument('-p','--probemac',default='00:87:11:01:48:10',help='type <probemac> to  location')
	arg=parser.parse_args()
	Path=os.path.dirname(os.path.realpath(__file__))
	os.chdir(Path)
	#print arg.get,
	if arg.monitor:
		Wf_get(arg.monitor,arg.time,arg.probemac)
if __name__=="__main__":
	main()
