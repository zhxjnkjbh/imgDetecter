# -*- coding: utf-8 -*-
import cv2
import numpy as np
from PyQt5 import QtGui

class PhotoData:
	def __init__(self):
		self.img_raw = None
		self.img_rgb = None
		self.img_gray = None
		self.img_r = None
		self.img_g = None
		self.img_b = None
		self.img_show = None
		self.img_binary = None
		self.qimg_show = QtGui.QImage(1024, 768, QtGui.QImage.Format_RGB888)
		self.width = 0
		self.height = 0
		self.img_list = ['001.png', '003.jpg']
		#self.read('3.jpg')
		self.img_name = ''#self.img_list[0]
		self.cur_index  = 0 #当前处理,0:grayParam,1:openClose,2:thresh,3:filter
		self.raw_width = 0
		self.raw_height = 0
		print('after read:', self.width, '*', self.height)

	def read(self, img_name):
		print(img_name)
		self.img_raw = cv2.imread(img_name.encode('gbk').decode(), 1)
		if self.check():
			self.img_name = img_name
			self.raw_width = self.img_raw.shape[1]
			self.raw_height = self.img_raw.shape[0]
			self.img_raw = cv2.resize(self.img_raw, (1024, 768))
			self.img_raw = cv2.cvtColor(self.img_raw, cv2.COLOR_BGR2RGB)
			self.img_rgb = self.img_raw.copy()
			self.img_show = self.img_rgb.copy()
			self.toGray()
			self.img_b = self.img_raw[:, :, 0]
			self.img_g = self.img_raw[:, :, 1]
			self.img_r = self.img_raw[:, :, 2]
			self.img_r, self.img_g, self.img_b = cv2.split(self.img_raw)  # 拆分
			self.width = self.img_raw.shape[1]
			self.height = self.img_raw.shape[0]
			self.img_binary = np.zeros((self.height, self.width), dtype=np.uint8)

			#print(type(self.img_raw))
			#print(self.img_raw.shape[0], '*', self.width)
			return True
		else:
			print('check fail!')
			return False
		print('raw:', self.width, '*', self.height)

	def check(self):
		return (not (self.img_raw is None))

	def toGray(self):
		self.img_gray = cv2.cvtColor(self.img_rgb, cv2.COLOR_BGR2GRAY)

	def show(self, index):
		#print('show:', self.qimg_show.width(), '*', self.height)
		img_show = self.img_rgb
		if 0 == index:
			# color
			img_show = self.img_rgb
			#self.qimg_show = QtGui.QImage(self.img_rgb, self.width, self.height, self.width * 3, QtGui.QImage.Format_RGB888)
		elif 5 == index:
			#raw
			img_show = self.img_raw
			#self.qimg_show = QtGui.QImage(self.img_raw, self.width, self.height, self.width * 3, QtGui.QImage.Format_RGB888)
		else:
			'''
			if 0 <= index and 4 > index:
			img_data = None
			if 0 == index:
				# raw
				self.img_show = self.img_raw
				print('raw:')
				#self.img_show = QtGui.QImage(self.img_raw, self.width, self.height, self.width * 3, QtGui.QImage.Format_RGB888)
				print('img_raw:', self.qimg_show.width(), '*', self.qimg_show.height())
			'''
			if 1 == index:
				# r
				img_show = self.img_r
				print('r')
			elif 2 == index:
				# g
				img_show = self.img_g
				print('g')
			elif 3 == index:
				# b
				img_show = self.img_b
				print('b')
			else:
				# gray
				img_show = self.img_gray

			#self.qimg_show = QtGui.QImage(self.img_show, self.width, self.height, QtGui.QImage.Format_Grayscale8)
			#print('raw0:', self.img_show.width(), '*', self.img_show.height())
			#self.qimg_show = QtGui.QImage(self.img_show, self.width, self.height, self.width * 3, QtGui.QImage.Format_RGB888)

			#print('raw1:', self.qimg_show.width(), '*', self.qimg_show.height())

		if 3 == len(img_show.shape):
			self.qimg_show = QtGui.QImage(img_show, self.width, self.height, self.width * 3, QtGui.QImage.Format_RGB888)
		else:
			self.qimg_show = QtGui.QImage(img_show, self.width, self.height, QtGui.QImage.Format_Grayscale8)
		#print('raw2:', self.qimg_show.width(), '*', self.qimg_show.height())
		print('img_show:', self.width, '*', self.qimg_show.height())
		return self.qimg_show

#data = PhotoData()
#print(type(data.img_raw))

	def showProcessedImg(self, is_binary = False):
		img = self.img_show
		print('photoData::showProcessedImg:', self.width, '*', self.height)

		if is_binary:
			img = self.img_binary
			'''
			self.qimg_show = QtGui.QImage(img, self.width, self.height, QtGui.QImage.Format_Grayscale8)
		else:
			self.qimg_show = QtGui.QImage(img, self.width, self.height, width,
									  QtGui.QImage.Format_RGB888)
		'''
		if 3 == len(img.shape):
			self.qimg_show = QtGui.QImage(img, self.width, self.height, self.width * 3, QtGui.QImage.Format_RGB888)
		else:
			self.qimg_show = QtGui.QImage(img, self.width, self.height, QtGui.QImage.Format_Grayscale8)
		return self.qimg_show