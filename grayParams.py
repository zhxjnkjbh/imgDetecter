#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QPushButton
import cv2
import numpy as np

class GrayParams(QWidget):
	def __init__(self, shower):
		super().__init__()
		self.names = ['红','绿','蓝','原始','灰']
		self.initUi()
		self.initData(shower)
		self._index = 0
		self.img_index = 0
		self.is_color = False
		self.is_rgb = False

	def initUi(self):
		self.qbt0 = QPushButton('切换图像,当前为原始', self)
		self.qbt0.resize(150, 25)
		self.qbt0.move(10, 10)
		self.qbt0.clicked.connect(self.changeSplitePhoto)

		self.qbt1 = QPushButton('当前为原始图像', self)
		self.qbt1.resize(120, 25)
		self.qbt1.move(200, 10)
		self.qbt1.clicked.connect(self.changeGray)

		self.btn2 = QPushButton('切换', self)
		self.cur_index = 0
		self.btn2.resize(100, 25)
		self.btn2.move(360, 10)
		self.btn2.clicked.connect(lambda : self.changeImg(self.cur_index))

	def initData(self, shower):
		self.shower = shower
		self.data = self.shower.data
		self.img_show = self.data.img_show

	def recover(self, process_index = 0):
		if self.data.cur_index == self._index:
			#还原
			print('还原')
			self.data.img_show = self.img_show.copy()
		else:
			print('切换')
			self.data.cur_index = self._index
			self.img_show = self.data.img_show.copy()

	def changeSplitePhoto(self):
		self.is_rgb = True
		self.img_index = (self.img_index + 1) % 3
		self.qbt0.setText('切换图像，当前为：' + self.names[self.img_index])

	def changeGray(self):
		self.is_color = not self.is_color
		self.is_rgb = False
		if self.is_color:
			self.qbt1.setText('切换为灰度图像')
		else:
			self.qbt1.setText('切换为原始图像')

	def changeImg(self, cur_index = 1):
		self.recover(0)
		self._index = 0
		img = self.data.img_show
		img_r, img_g, img_b = cv2.split(img)
		# print(img)
		if 0 == cur_index:
			img_b = np.where(img_b < img_g, img_b, img_g)
			img_b = np.where(img_b < img_r, img_b, img_r)
			img_g = img_b.copy()
			img_r = img_b.copy()
			self.data.img_show = cv2.merge([img_b, img_g, img_r])
		elif 1 == cur_index:
			img_b = np.where(img_b > img_g, img_b, img_g)
			img_b = np.where(img_b > img_r, img_b, img_r)
			img_g = img_b.copy()
			img_r = img_b.copy()
			self.data.img_show = cv2.merge([img_b, img_g, img_r])
		else:
			img_b = ((img_b + img_r + img_g) / 3).astype(int)
			img_g = img_b.copy()
			img_r = img_b.copy()
			self.data.img_show = cv2.merge([img_b, img_g, img_r])

		# print((cur_index,self.cur_index))
		self.cur_index = (self.cur_index + 1) % 2
		self.shower.showProcessedImg()


if __name__ == '__main__':

	a1 = np.array([1,5,3,4])
	a2 = np.array([3,4,5,6])
	a3 = np.array([6,7,8,9])
	print(np.maximum(a1,a2))
	a4 = ((a1+a2+a3)/3).astype(int)



	l1 = [1,2,3,4]
	l2 = l1
	l1[0]=2
	print(l2)
	img = cv2.imread('11.jpg')
	print('shape:', img.shape)
	cv2.imwrite('cp1.jpg',img)
	cv2.imwrite('cp2.bmp',img)
	cv2.imwrite('cp3.png', img)

	#img = cv2.resize(img,(4, 3))
	#print('raw:',img)
	b,g,r = cv2.split(img)
	print(len(img.shape),len(b.shape))


	#print(b)
	b = np.where(b > g, b, g)
	b = np.where(b > r, b, r)
	g = b.copy()
	r = b.copy()
	cv2.circle(img, (100, 200), 2, (0, 0, 255), -1)
	cv2.imshow('raw', img)
	img_new = cv2.merge((b,g,r))

	kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
	img = cv2.filter2D(img, -1, kernel)
	#print('new:',img)
	cv2.imshow('new', img)
	cv2.waitKey(0)

	a = np.random.randint(-5, 5, (4, 3))
	print(a)
	a = a.reshape(2, 6)
	print(a)
	print(a.T)#转置
	print(np.square(a))

	a,b,c,d = l1
	print(l1)
	print(a,b,c,d)

	l5 = np.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
	print(l5[0][1])
	print(l5.shape)
	print(l5)
	l5[:][1:] = 0
	print(l5)
