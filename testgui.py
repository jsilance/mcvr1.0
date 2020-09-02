import tkinter
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
import cv2
import PIL.Image, PIL.ImageTk

# import win32file
# import win32api
import re
import subprocess

import threading
import numpy


# Variable Setup

window = tkinter.Tk()
start_bt = []
stop_bt = []
select_bt = []
refresh = []
label_title = []
# vcap = cv2.VideoCapture('rtsp://admin:adsconcert169@192.168.0.65:554/Streaming/Channels/1/')
vcap = cv2.VideoCapture(0)
i = 0
color = '#404040'




def stream():
	global window
	global vcap
	
	while(True):
    	# Capture frame-by-frame
		ret, frame = vcap.read()

		# Our operations on the frame come here
		dim = (240, 160)
		gray = cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

		# gray = cv2.cvtColor(gray, cv2.COLOR_BGR2BGRA)
		gray = cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)


		photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(gray))
		canvas = tkinter.Canvas(window, width = 240, height = 160)
		canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
		canvas.grid(row=0, column=1)


#---------------------------Windows Version-----------------------
# def get_usb_device():
# 	try:
# 		usb_list = []
# 		device = win32api.GetLogicalDriveStrings().split('\x00')[:-1]

# 		for usb in device:
# 			Utype = win32file.GetDriveType(usb)
# 			if Utype == win32file.DRIVE_REMOVABLE:
# 				usb_list.append(usb)
# 		return usb_list

# 	except Exception as error:
# 		print('error', error)
#-----------------------------------------------------------------

#----------------------LINUX VERSION------------------------------
def get_usb_device():
	device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
	df = subprocess.check_output("lsusb")
	devices = []
	for i in df.split('\n'):
	    if i:
	        info = device_re.match(i)
	        if info:
	            dinfo = info.groupdict()
	            dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
	            devices.append(dinfo)
	return devices
#-----------------------------------------------------------------




def usb_select():
	global label_title
	global select_bt
	global window
	global frame
	global i
	global refresh

	kill_button(4)

	try:
		for bt in refresh:
			bt.destroy()
	except Exception as error:
		print('No refresh button found')

	i = 0
	label_title.append(Label(frame, text="Select Disk", font=("arial", 25), bg=color, fg='#FFFFFF'))
	label_title[0].place(rely=.0, relx=.1)
	usb = get_usb_device()
	# if usb:
		# for device in usb:
			# select_bt.append(Button(frame, text=device, width=30, height=2, font=("arial", 10), bg='#00a0ff', fg='#ffffff', command=stop_record))
			# select_bt[i].place(rely=((i + 1) / 5), relx=.0)
			# i += 1
	# else:
	refresh.append(Button(frame, text='REFRESH LIST', width=30, height=2, font=("arial", 10), bg='#00a0ff', fg='#ffffff', command=usb_select))
	refresh[0].place(rely=((i + 1) / 5), relx=.0)
	return

def start_record():
	global start_bt
	global stop_bt
	global frame
	global window
	global vcap

	kill_button(4)

	# vcap.release()
	start_bt.append(Button(window, text="Record", width=10, height=3, font=("arial", 30), bg='#00a0ff', fg='#ffffff', command=usb_select))
	for btn in start_bt:
		# btn.pack()
		btn.place(rely=.24, relx=.0)
	return

def stop_record():
	global i
	global select_bt
	global stop_bt
	# label_title.destroy()

	kill_button(4)
	# for btn in select_bt:
	# 	btn.destroy()
	# 	select_bt.remove(btn)

	stop_bt.append(Button(frame, text="Stop Record", width=10, height=3, font=("arial", 30), bg='#F00000', fg='#FFFFFF', command=start_record))
	stop_bt[0].place(rely=.24, relx=.0)
	return

def window_init():
	global frame
	global frame_vid
	global window

	try:
		frame.destroy()
		# frame_vid.destroy()
	except Exception as error:
		print('no frame')

	frame = Frame(window, width=240, height=320, bg=color)
	# frame_vid = Frame(window, width=240, height=320, bg=color)
	frame.grid(row=0, column=0)
	# frame_vid.grid(row=0, column=1)
	window.geometry('480x320')
	window.minsize(480, 320)
	window.config(background=color)
	return

def kill_button(nb):
	global select_bt
	global start_bt
	global stop_bt
	global refresh

	try:
		if nb == 0 or nb == 4:
			for btn in start_bt:
				btn.destroy()
				start_bt.remove(btn)
		if nb == 1 or nb == 4:
			for btn in stop_bt:
				btn.destroy()
				stop_bt.remove(btn)
		if nb == 2 or nb == 4:
			for btn in select_bt:
				btn.destroy()
				select_bt.remove(btn)
		if nb == 3 or nb == 4:
			for btn in refresh:
				btn.destroy()
				refresh.remove(btn)
		for lbl in label_title:
			lbl.destroy()
			label_title.remove(lbl)
	except Exception as error:
		print('Killing error')
	return
	


window_init()

th2 = threading.Thread(target=stream)
th1 = threading.Thread(target=start_record)

th2.daemon = 1
th1.start()
th2.start()


# start_record()


window.mainloop()