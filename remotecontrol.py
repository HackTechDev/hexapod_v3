#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# File name   : client.py
# Description : client  
# Website	 : www.adeept.com
# E-mail	  : support@adeept.com
# Author	  : William
# Date		: 2018/08/22

from socket import *
import sys
import time
import threading as thread
import tkinter as tk
import math

tcpClicSock = ''
stat = 0
ip_stu=1
stop_stu = 1
x_range = 1

def replace_num(initial,new_num):   #Call this function to replace data in '.txt' file
	newline=""
	str_num=str(new_num)
	with open("ip.txt","r") as f:
		for line in f.readlines():
			if(line.find(initial) == 0):
				line = initial+"%s" %(str_num)
			newline += line
	with open("ip.txt","w") as f:
		f.writelines(newline)	#Call this function to replace data in '.txt' file


def num_import(initial):			#Call this function to import data from '.txt' file
	with open("ip.txt") as f:
		for line in f.readlines():
			if(line.find(initial) == 0):
				r=line
	begin=len(list(initial))
	snum=r[begin:]
	n=snum
	return n	


def call_forward(event):		 #When this function is called,client commands the car to move forward
	global stop_stu
	if stop_stu:
		tcpClicSock.send(('1').encode())
		stop_stu = 0


def call_back(event):
	global stop_stu
	if stop_stu:
		tcpClicSock.send(('2').encode())
		stop_stu = 0


def call_right(event):
	global stop_stu
	if stop_stu:
		print("3 r")
		tcpClicSock.send(('3').encode())
		stop_stu = 0


def call_left(event):
	global stop_stu
	if stop_stu:
		tcpClicSock.send(('4').encode())
		stop_stu = 0

def call_head_left(event):
	print("head left : 12")
	tcpClicSock.send(('12').encode())

def call_head_right(event):
	print("head right : 13")
	tcpClicSock.send(('13').encode())		

def call_steady(event):
	tcpClicSock.send(('5').encode())

def call_stop(event):
	global stop_stu
	print("9stop")
	tcpClicSock.send(('9').encode())
	stop_stu = 1


def call_attack(event):
	tcpClicSock.send(('10').encode())


def call_auto(event):
	tcpClicSock.send(('8').encode())


def call_ultra(event):
	tcpClicSock.send(('7').encode())


def connection_thread():
	global funcMode, Switch_3, Switch_2, Switch_1, SmoothMode
	while 1:
		car_info = (tcpClicSock.recv(BUFSIZ)).decode()
		print(car_info)
		if not car_info:
			continue

		elif 'V:' in car_info:
			#try:
			car_info = car_info[2:]
			print(car_info)
			vot=float(car_info)
			if vot > 6.8:
				l_ip.config(text='Battery:%.2f'%vot)
			else:
				l_ip.config(text='Battery State Low:%.2f'%vot)

			try:
				canvas_battery.delete(canvas_rec)
			except:
				pass

			if vot >= 7.3:
				canvas_rec=canvas_battery.create_rectangle(0,0,int((vot-6.7)/1.7*132),30,fill = '#558B2F',width=0)
			elif vot < 7.3:
				canvas_rec=canvas_battery.create_rectangle(0,0,int((vot-6.7)/1.7*132),30,fill = '#FF8F00',width=0)
			else:
				pass

		else:
			pass


def socket_connect():	 #Call this function to connect with the server
	global ADDR,tcpClicSock,BUFSIZ,ip_stu,ipaddr
	ip_adr=E1.get()	   #Get the IP address from Entry

	if ip_adr == '':	  #If no input IP address in Entry,import a default IP
		ip_adr=num_import('IP:')
		l_ip_4.config(text='Connecting')
		l_ip_4.config(bg='#FF8F00')
		l_ip_5.config(text='Default:%s'%ip_adr)
		pass
	
	SERVER_IP = ip_adr
	SERVER_PORT = 333   #Define port serial 
	BUFSIZ = 1024		 #Define buffer size
	ADDR = (SERVER_IP, SERVER_PORT)
	tcpClicSock = socket(AF_INET, SOCK_STREAM) #Set connection value for socket

	for i in range (1,6): #Try 5 times if disconnected
		#try:
		if ip_stu == 1:
			print("Connecting to server @ %s:%d..." %(SERVER_IP, SERVER_PORT))
			print("Connecting")
			tcpClicSock.connect(ADDR)		#Connection with the server
		
			print("Connected")
		
			l_ip_5.config(text='IP:%s'%ip_adr)
			l_ip_4.config(text='Connected')
			l_ip_4.config(bg='#558B2F')

			replace_num('IP:',ip_adr)
			E1.config(state='disabled')	  #Disable the Entry
			Btn14.config(state='disabled')   #Disable the Entry
			
			ip_stu=0						 #'0' means connected

			connection_threading=thread.Thread(target=connection_thread)		 #Define a thread for FPV and OpenCV
			connection_threading.setDaemon(True)							 #'True' means it is a front thread,it would close when the mainloop() closes
			connection_threading.start()									 #Thread starts

			break
		else:
			print("Cannot connecting to server,try it latter!")
			l_ip_4.config(text='Try %d/5 time(s)'%i)
			l_ip_4.config(bg='#EF6C00')
			print('Try %d/5 time(s)'%i)
			ip_stu=1
			time.sleep(1)
			continue

	if ip_stu == 1:
		l_ip_4.config(text='Disconnected')
		l_ip_4.config(bg='#F44336')


def connect(event):	   #Call this function to connect with the server
	if ip_stu == 1:
		sc=thread.Thread(target=socket_connect) #Define a thread for connection
		sc.setDaemon(True)					  #'True' means it is a front thread,it would close when the mainloop() closes
		sc.start()							  #Thread starts


def connect_click():	   #Call this function to connect with the server
	if ip_stu == 1:
		sc=thread.Thread(target=socket_connect) #Define a thread for connection
		sc.setDaemon(True)					  #'True' means it is a front thread,it would close when the mainloop() closes
		sc.start()							  #Thread starts


def set_R(event):
	time.sleep(0.03)
	tcpClicSock.send(('wsR %s'%var_R.get()).encode())


def set_G(event):
	time.sleep(0.03)
	tcpClicSock.send(('wsG %s'%var_G.get()).encode())


def set_B(event):
	time.sleep(0.03)
	tcpClicSock.send(('wsB %s'%var_B.get()).encode())


def loop():					  #GUI
	global color_can,color_line,target_color,color_oval,tcpClicSock,root,E1,connect,l_ip,l_ip_4,l_ip_5,color_btn,color_text,Btn14,CPU_TEP_lab,CPU_USE_lab,RAM_lab,canvas_ultra,color_text,var_R,var_B,var_G,Btn_Steady,Btn_FindColor,Btn_WatchDog,Btn_Fun4,Btn_Fun5,Btn_Fun6,Btn_Switch_1,Btn_Switch_2,Btn_Switch_3,Btn_Smooth,canvas_battery   #The value of tcpClicSock changes in the function loop(),would also changes in global so the other functions could use it.
	while True:
		color_bg='#000000'		#Set background color
		color_text='#E1F5FE'	  #Set text color
		color_btn='#0277BD'	   #Set button color
		color_line='#01579B'	  #Set line color
		color_can='#212121'	   #Set canvas color
		color_oval='#2196F3'	  #Set oval color
		target_color='#FF6D00'

		root = tk.Tk()			#Define a window named root
		root.title('Hexapod Arduino Robot')	  #Main window title
		root.geometry('450x380')  #Main window size, middle of the English letter x.
		root.config(bg=color_bg)  #Set the background color of root window

		try:
			logo =tk.PhotoImage(file = 'logo.png')		 #Define the picture of logo,but only supports '.png' and '.gif'
			l_logo=tk.Label(root,image = logo,bg=color_bg) #Set a label to show the logo picture
			l_logo.place(x=30,y=13)						#Place the Label in a right position
		except:
			pass

		canvas_battery=tk.Canvas(root,bg=color_btn,height=23,width=132,highlightthickness=0)
		canvas_battery.place(x=30,y=145)

		l_ip=tk.Label(root,width=18,text='Status',fg=color_text,bg=color_btn)
		l_ip.place(x=30,y=110)						   #Define a Label and put it in position

		l_ip_4=tk.Label(root,width=18,text='Disconnected',fg=color_text,bg='#F44336')
		l_ip_4.place(x=218,y=110)						 #Define a Label and put it in position

		l_ip_5=tk.Label(root,width=18,text='Use default IP',fg=color_text,bg=color_btn)
		l_ip_5.place(x=218,y=145)						 #Define a Label and put it in position

		E1 = tk.Entry(root,show=None,width=16,bg="#37474F",fg='#eceff1')
		E1.place(x=148,y=40)							 #Define a Entry and put it in position

		l_ip_3=tk.Label(root,width=10,text='IP Address:',fg=color_text,bg='#000000')
		l_ip_3.place(x=143,y=15)						 #Define a Label and put it in position

		Btn_Steady = tk.Button(root, width=8, text='Steady',fg=color_text,bg=color_btn,relief='ridge')
		Btn_Steady.place(x=350,y=195)
		Btn_Steady.bind('<ButtonPress-1>', call_steady)
		root.bind('<KeyPress-f>', call_steady)

		Btn0 = tk.Button(root, width=8, text='Forward',fg=color_text,bg=color_btn,relief='ridge')
		Btn1 = tk.Button(root, width=8, text='Backward',fg=color_text,bg=color_btn,relief='ridge')
		Btn2 = tk.Button(root, width=8, text='Left',fg=color_text,bg=color_btn,relief='ridge')
		Btn3 = tk.Button(root, width=8, text='Right',fg=color_text,bg=color_btn,relief='ridge')


		Btn0.place(x=130,y=195)
		Btn1.place(x=130,y=230)
		Btn2.place(x=30,y=230)
		Btn3.place(x=230,y=230)
		
		
		
		Btn4 = tk.Button(root, width=8, text='H Left',fg=color_text,bg=color_btn,relief='ridge')
		Btn5 = tk.Button(root, width=8, text='H Right',fg=color_text,bg=color_btn,relief='ridge')

		Btn4.place(x=30,y=265)
		Btn5.place(x=230,y=265)
		
		

		Btn0.bind('<ButtonPress-1>', call_forward)
		Btn1.bind('<ButtonPress-1>', call_back)
		Btn2.bind('<ButtonPress-1>', call_left)
		Btn3.bind('<ButtonPress-1>', call_right)

		Btn0.bind('<ButtonRelease-1>', call_stop)
		Btn1.bind('<ButtonRelease-1>', call_stop)
		Btn2.bind('<ButtonRelease-1>', call_stop)
		Btn3.bind('<ButtonRelease-1>', call_stop)

		root.bind('<KeyPress-w>', call_forward) 
		root.bind('<KeyPress-a>', call_left)
		root.bind('<KeyPress-d>', call_right)
		root.bind('<KeyPress-s>', call_back)

		root.bind('<KeyPress-q>', call_auto)
		root.bind('<KeyPress-e>', call_attack)

		root.bind('<KeyRelease-w>', call_stop)
		root.bind('<KeyRelease-a>', call_stop)
		root.bind('<KeyRelease-d>', call_stop)
		root.bind('<KeyRelease-s>', call_stop)


		Btn4.bind('<ButtonPress-1>', call_head_left)
		Btn5.bind('<ButtonPress-1>', call_head_right)
		Btn4.bind('<ButtonRelease-1>', call_stop)
		Btn5.bind('<ButtonRelease-1>', call_stop)



		Btn14= tk.Button(root, width=8,height=2, text='Connect',fg=color_text,bg=color_btn,command=connect_click,relief='ridge')
		Btn14.place(x=283,y=15)						  #Define a Button and put it in position

		root.bind('<Return>', connect)

		var_R = tk.StringVar()
		var_R.set(0)

		global stat
		if stat==0:			  # Ensure the mainloop runs only once
			root.mainloop()  # Run the mainloop()
			stat=1		   # Change the value to '1' so the mainloop() would not run again.


if __name__ == '__main__':
	try:
		loop()				   # Load GUI
	except:
		tcpClicSock.close()		  # Close socket or it may not connect with the server again
		pass
