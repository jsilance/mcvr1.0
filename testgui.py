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

import threading, time
import numpy

import os
from glob import glob
from subprocess import check_output, CalledProcessError
from functools import partial


# Variable Setup

window = tkinter.Tk()
start_bt = []
stop_bt = []
select_bt = []
refresh = []
label_title = []
# vcap = cv2.VideoCapture('rtsp://admin:adsconcert169@192.168.0.65:554/Streaming/Channels/1/') # Use rtsp camera in network
vcap = cv2.VideoCapture(0) # Use local webcam
i = 0
color = '#404040'




def stream():
	global window
	global vcap
	
	FRAME_TIME = 1 / 60
	while(True):
    	# Capture frame-by-frame
		ret, frame = vcap.read()
		# frame = vcap.read()

		# Our operations on the frame come here
		dim = (240, 160)
		gray = cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

		# gray = cv2.cvtColor(gray, cv2.COLOR_BGR2BGRA)
		gray = cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)


		photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(gray))
		canvas = tkinter.Canvas(window, width = 240, height = 160)
		render(photo, canvas)
		# canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
		canvas.grid(row=0, column=1)
		time.sleep(FRAME_TIME)

def render(photo, canvas):
	canvas.delete(ALL)
	canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)

#---------------------------Windows Version-----------------------
# def get_mount_device():
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
def get_usb_devices():
    sdb_devices = map(os.path.realpath, glob('/sys/block/sd*'))
    usb_devices = (dev for dev in sdb_devices
        if 'usb' in dev.split('/')[5])
    return dict((os.path.basename(dev), dev) for dev in usb_devices)

def get_mount_device(devices=None):
    devices = devices or get_usb_devices() # if devices are None: get_usb_devices
    output = check_output(['mount']).splitlines()
    is_usb = lambda path: any(dev in path for dev in devices)
    usb_info = (line for line in output if is_usb(line.split()[0]))
    return [(info.split()[0], info.split()[2]) for info in usb_info]
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
	usb = get_mount_device()
	if usb:
		for device in usb:
			select_bt.append(Button(frame, text=device, width=30, height=2, font=("arial", 10), bg='#00a0ff', fg='#ffffff', command=partial(stop_record, device)))
			select_bt[i].place(rely=((i + 1) / 5), relx=.0)
			i += 1
	else:
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

def stop_record(path_usb):
	global i
	global select_bt
	global stop_bt

	kill_button(4)

	print(path_usb)

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
# stream()

th2 = threading.Thread(target=stream)
# th1 = threading.Thread(target=start_record)

th2.daemon = 1
# th1.start()
th2.start()


# start_record()

window.mainloop()