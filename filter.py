# -*- coding: utf-8 -*-
import cv2

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QCheckBox
import numpy as np
from outMsg import OutMsg
import sys
import random
import os

class Filter(QtWidgets.QWidget):
	def __init__(self, shower):
		super().__init__()
		self.initData(shower)
		# self.list_test_imgs = []#['001_after.jpg', '002_after.jpg', '2_after.jpg', '003_after.jpg', '3_after.jpg']
		# if False:
		# 	self.list_test_imgs = ['3_after.jpg']
		# else:
		# 	for i in range(0, 22):
		# 		self.list_test_imgs.append('ct'+str(i)+'.jpg')

		self.initUi()
		#self.list_test_imgs = ['ct3.jpg','ct3_lr.jpg']


	def initData(self, shower):
		self.test_index = 0
		self.cur_contour_index = 0  # 当前轮廓
		self.contours = []  # 所有轮廓
		self.wall_list = []  # 墙
		self.kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
		self.map_wall_depth = {}
		self.wall_index = 0
		self.approx = 1
		self.test_step = 0
		# self.log = open('log.txt', 'a')

		self.shower = shower
		self.data = shower.data
		if self.data.check():
			self.img_binary = self.data.img_binary.copy()
			self.img_binary_raw = self.data.img_binary.copy()
			self.img_binary_cur = self.data.img_binary.copy()

		self.filter_size = 20
		self.fufill_size = 9
		self._index = 3
		self.process_index = 0
		# 墙厚度
		self.rect_thresh_min = 5
		self.rect_thresh_max = 30
		self.wall_depth_min = 5
		self.wall_depth_max = 30
		self.is_rect_use_percent = False

	def initUi(self):
		#过滤
		self.label0 = QtWidgets.QLabel(self)
		self.label0.setGeometry(QtCore.QRect(10, 10, 85, 20))
		self.label0.setText('Filter Size:')

		self.sld_size = QtWidgets.QSlider(Qt.Horizontal, self)
		self.sld_size.setGeometry(QtCore.QRect(105, 10, 200, 20))
		self.sld_size.setMinimum(2)
		self.sld_size.setMaximum(50)
		self.sld_size.setValue(self.filter_size)
		self.sld_size.valueChanged.connect(self.filterSizeChange)

		self.text_size = QtWidgets.QLineEdit(self)
		self.text_size.setGeometry(QtCore.QRect(310, 10, 40, 20))
		self.text_size.setText(str(self.sld_size.value()))
		self.text_size.textChanged.connect(self.filterSizeChangeByText)

		self.btn0 = QtWidgets.QPushButton('过滤尺寸',self)
		self.btn0.setGeometry(QtCore.QRect(360, 10, 80, 20))
		self.btn0.clicked.connect(self.filterSize)

		#填充
		self.label1 = QtWidgets.QLabel(self)
		self.label1.setGeometry(QtCore.QRect(10, 40, 85, 20))
		self.label1.setText('Fufill Size:')

		self.sld_fufill_size = QtWidgets.QSlider(Qt.Horizontal, self)
		self.sld_fufill_size.setGeometry(QtCore.QRect(105, 40, 200, 20))
		self.sld_fufill_size.setMinimum(0)
		self.sld_fufill_size.setMaximum(20)
		self.sld_fufill_size.setValue(self.fufill_size)
		self.sld_fufill_size.valueChanged.connect(self.fufillSizeChange)

		self.text_fufill_size = QtWidgets.QLineEdit(self)
		self.text_fufill_size.setGeometry(QtCore.QRect(310, 40, 40, 20))
		self.text_fufill_size.setText(str(self.sld_fufill_size.value()))
		self.text_fufill_size.textChanged.connect(self.fufillSizeChangeByText)

		self.btn1 = QtWidgets.QPushButton('填充', self)
		self.btn1.setGeometry(QtCore.QRect(360, 40, 80, 20))
		self.btn1.clicked.connect(self.fufillImg)

		self.btn2 = QtWidgets.QPushButton('还原', self)
		self.btn2.setGeometry(QtCore.QRect(10, 70, 60, 30))
		self.btn2.clicked.connect(self.recoverAllFilter)

		#矩形化
		self.label2 = QtWidgets.QLabel(self)
		self.label2.setGeometry(QtCore.QRect(500, 10, 95, 20))
		self.label2.setText('Rect Thresh Min:')

		self.sld_rect_thresh_min = QtWidgets.QSlider(Qt.Horizontal, self)
		self.sld_rect_thresh_min.setGeometry(QtCore.QRect(610, 10, 200, 20))
		self.sld_rect_thresh_min.setMinimum(0)
		self.sld_rect_thresh_min.setMaximum(50)
		self.sld_rect_thresh_min.setValue(self.rect_thresh_min)
		self.sld_rect_thresh_min.valueChanged.connect(self.rectThreshMinChange)

		self.text_rect_thresh_min = QtWidgets.QLineEdit(self)
		self.text_rect_thresh_min.setGeometry(QtCore.QRect(810, 10, 40, 20))
		self.text_rect_thresh_min.setText(str(self.rect_thresh_min))
		self.text_rect_thresh_min.textChanged.connect(self.rectThreshMinChangeByText)

		self.label3 = QtWidgets.QLabel(self)
		self.label3.setGeometry(QtCore.QRect(500, 40, 95, 20))
		self.label3.setText('Rect Thresh Max:')

		self.sld_rect_thresh_max = QtWidgets.QSlider(Qt.Horizontal, self)
		self.sld_rect_thresh_max.setGeometry(QtCore.QRect(610, 40, 200, 20))
		self.sld_rect_thresh_max.setMinimum(10)
		self.sld_rect_thresh_max.setMaximum(100)
		self.sld_rect_thresh_max.setValue(self.rect_thresh_max)
		self.sld_rect_thresh_max.valueChanged.connect(self.rectThreshMaxChange)

		self.text_rect_thresh_max = QtWidgets.QLineEdit(self)
		self.text_rect_thresh_max.setGeometry(QtCore.QRect(810, 40, 40, 20))
		self.text_rect_thresh_max.setText(str(self.rect_thresh_max))
		self.text_rect_thresh_max.textChanged.connect(self.rectThreshMaxChangeByText)

		self.btn2 = QtWidgets.QPushButton('矩形化', self)
		self.btn2.setGeometry(QtCore.QRect(860, 40, 80, 25))
		self.btn2.clicked.connect(self.rectangulazie)

		self.label3 = QtWidgets.QLabel(self)
		self.label3.move(860, 12)
		self.label3.setText('使用百分比')
		self.btn_chk0 = QtWidgets.QRadioButton('', self)
		self.btn_chk0.move(920, 12)
		self.btn_chk0.setChecked(self.is_rect_use_percent)
		self.btn_chk0.clicked.connect(self.rectUsePercentChange)

		self.btn4 = QtWidgets.QPushButton('切割', self)
		self.btn4.setGeometry(QtCore.QRect(955, 10, 80, 25))
		self.btn4.clicked.connect(self.cutContour)

		self.btn5 = QtWidgets.QPushButton('填充', self)
		self.btn5.setGeometry(QtCore.QRect(955, 40, 80, 25))
		self.btn5.clicked.connect(self.getRectWalls)

		self.btn6 = QtWidgets.QPushButton('切割+填充', self)
		self.btn6.setGeometry(QtCore.QRect(1040, 10, 100, 25))
		self.btn6.clicked.connect(self.cutAndFufillContour)

		self.btn7 = QtWidgets.QPushButton('保存轮廓', self)
		self.btn7.setGeometry(QtCore.QRect(1040, 40, 100, 25))
		self.btn7.clicked.connect(self.saveContour)

		self.btn3 = QtWidgets.QPushButton('导入测试', self)
		self.btn3.setGeometry(QtCore.QRect(285, 70, 70, 30))
		self.btn3.clicked.connect(self.importTestImg)
		self.text_img_name = QtWidgets.QLineEdit(self)
		self.text_img_name.setGeometry(QtCore.QRect(360, 72, 80, 25))
		self.label4 = QtWidgets.QLabel(self)
		self.label4.move(85, 78)
		self.label4.setText('测试范围：')
		self.sld_img_min = QtWidgets.QSlider(Qt.Vertical, self)
		self.sld_img_min.setGeometry(QtCore.QRect(150, 70, 20, 30))
		#self.sld_img_min.setOrientation(QtCore.Qt.Vertical)
		self.sld_img_min.setMinimum(1)
		self.sld_img_min.setMaximum(25)
		self.sld_img_min.setValue(17)
		self.sld_img_min.valueChanged.connect(self.imgMinChange)
		self.text_img_min = QtWidgets.QLineEdit(self)
		self.text_img_min.setGeometry(QtCore.QRect(172, 75, 40, 20))
		self.text_img_min.setText(str(self.sld_img_min.value()))
		self.text_img_min.textChanged.connect(self.imgMinChangeByText)
		self.sld_img_max = QtWidgets.QSlider(Qt.Vertical, self)
		self.sld_img_max.setGeometry(QtCore.QRect(215, 70, 20, 30))
		#self.sld_img_max.setOrientation(QtCore.Qt.Vertical)
		self.sld_img_max.setMinimum(1)
		self.sld_img_max.setMaximum(25)
		self.sld_img_max.setValue(17)
		self.sld_img_max.valueChanged.connect(self.imgMaxChange)
		self.text_img_max = QtWidgets.QLineEdit(self)
		self.text_img_max.setGeometry(QtCore.QRect(237, 75, 40, 20))
		self.text_img_max.setText(str(self.sld_img_max.value()))
		self.text_img_max.textChanged.connect(self.imgMaxChangeByText)

		#近似
		self.label4 = QtWidgets.QLabel(self)
		self.label4.move(445, 78)
		self.label4.setText('近似：')
		self.sld_approx = QtWidgets.QSlider(Qt.Horizontal, self)
		self.sld_approx.setGeometry(QtCore.QRect(480, 75, 60, 20))
		self.sld_approx.setMinimum(1)
		self.sld_approx.setMaximum(30)
		self.sld_approx.setValue(1)
		self.sld_approx.valueChanged.connect(self.approxChange)
		self.text_approx = QtWidgets.QLineEdit(self)
		self.text_approx.setGeometry(QtCore.QRect(545, 75, 40, 20))
		self.text_approx.setText(str(self.sld_approx.value()))
		self.text_approx.textChanged.connect(self.approxChangeByText)

		#导入轮廓
		self.bt4 = QtWidgets.QPushButton(self)
		self.bt4.setGeometry(QtCore.QRect(590, 70, 70, 30))
		self.bt4.setText('导入轮廓')
		self.bt4.clicked.connect(self.loadContourImg)

	def addOuter(self, out_msg):
		self.out_msg = out_msg
		sys.stdout = self.out_msg
		#sys.stdout = self.log

	def filterSizeChange(self):
		self.filter_size = self.sld_size.value()
		self.text_size.setText(str(self.filter_size))
		self.filterSize()

	def filterSizeChangeByText(self):
		self.filter_size = int(self.text_size.text())
		self.sld_size.setValue(self.filter_size)
		self.filterSize()

	def fufillSizeChange(self):
		self.fufill_size = self.sld_fufill_size.value()
		self.text_fufill_size.setText(str(self.fufill_size))
		self.fufillImg()

	def fufillSizeChangeByText(self):
		self.fufill_size = int(self.text_fufill_size.text())
		self.sld_fufill_size.setValue(self.fufill_size)
		self.fufillImg()

	def rectThreshMinChange(self):
		self.rect_thresh_min = self.sld_rect_thresh_min.value()
		self.text_rect_thresh_min.setText(str(self.rect_thresh_min))
		if self.rect_thresh_max < self.rect_thresh_min:
			self.rect_thresh_max = self.rect_thresh_min
			self.sld_rect_thresh_max.setValue(self.rect_thresh_max)
			self.text_rect_thresh_max.setText(str(self.rect_thresh_max))
		#self.rectangulazie()

	def rectThreshMinChangeByText(self):
		self.rect_thresh_min = int(self.text_rect_thresh_min.text())
		self.sld_rect_thresh_min.setValue(self.rect_thresh_min)
		if self.rect_thresh_max < self.rect_thresh_min:
			self.rect_thresh_max = self.rect_thresh_min
			self.sld_rect_thresh_max.setValue(self.rect_thresh_max)
			self.text_rect_thresh_max.setText(str(self.rect_thresh_max))
		#self.rectangulazie()

	def rectThreshMaxChange(self):
		self.rect_thresh_max = self.sld_rect_thresh_max.value()
		self.text_rect_thresh_max.setText(str(self.rect_thresh_max))
		if self.rect_thresh_max < self.rect_thresh_min:
			self.rect_thresh_min = self.rect_thresh_max
			self.sld_rect_thresh_min.setValue(self.rect_thresh_min)
			self.text_rect_thresh_min.setText(str(self.rect_thresh_min))
		#self.rectangulazie()

	def rectThreshMaxChangeByText(self):
		self.rect_thresh_max = int(self.text_rect_thresh_max.text())
		self.sld_rect_thresh_max.setValue(self.rect_thresh_max)
		if self.rect_thresh_max < self.rect_thresh_min:
			self.rect_thresh_min = self.rect_thresh_max
			self.sld_rect_thresh_min.setValue(self.rect_thresh_min)
			self.text_rect_thresh_min.setText(str(self.rect_thresh_min))

	def rectUsePercentChange(self):
		if self.is_rect_use_percent:
			pass
		else:
			pass

		self.is_rect_use_percent = not self.is_rect_use_percent

	def filterSize(self):
		self.recover(0)
		self.process_index = 0
		img = self.data.img_binary
		contours,hieracy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		for i in range(len(contours)):
			x, y, w, h = cv2.boundingRect(contours[i])
			if w < self.filter_size and h < self.filter_size:
				for row in range(y, y + h):
					for col in range(x, x + w):
						img[row][col] = 255


		self.data.img_show = img.copy()
		self.data.img_binary = img.copy()
		self.img_binary_cur = img.copy()
		self.shower.showProcessedImg(True)

	def recover(self, process_index = 0):
		if self.data.cur_index == self._index:
			#还原
			print('还原')
			if process_index != self.process_index:
				#切换
				self.img_binary_raw = self.img_binary_cur.copy()
			self.data.img_binary = self.img_binary_raw.copy()
		else:
			print('回复')
			self.data.cur_index = self._index
			self.img_binary = self.data.img_binary.copy()
			self.img_binary_raw = self.data.img_binary.copy()
			self.img_binary_cur = self.data.img_binary.copy()

	def fufillImg(self):
		self.recover(1)
		self.process_index = 1
		print('fufillImg')
		img = self.data.img_binary
		kernel = cv2.getStructuringElement(cv2.MORPH_RECT,
										   (self.fufill_size * 2 + 1, self.fufill_size * 2 + 1),
										   (self.fufill_size, self.fufill_size))
		img = cv2.erode(img, kernel)
		img = cv2.dilate(img, kernel)
		self.data.img_show = img.copy()
		self.data.img_binary = img.copy()
		self.img_binary_cur = img.copy()
		self.img_binary_raw = img.copy()
		self.img_binary = img
		self.contours, hieracy = cv2.findContours(self.img_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		self.shower.showProcessedImg(True)

	def rectangulazie(self):
		self.recover(2)
		self.process_index = 2
		img = self.data.img_binary.copy()
		self.count = 0
		contours, hieracy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		'''
		for row in range(self.data.height):
			for col in range(219, self.data.width):
				self.data.img_binary[row][col] = 255
		#self.data.img_binary[219:][:] = 255
		self.shower.showProcessedImg(True)
		return'''
		self.data.img_show = self.data.img_rgb
		self.cur_contour_index = 0
		self.wall_list = []
		for i in range(len(contours)):
			self.cur_contour_index = i
			self.rectangulazieContour()

		#self.rectangulazieContour(contours[1])
		#print('轮廓1：',contours[1])

		#img = cv2.drawContours(img, contours, -1, (60, 35, 155), 1)
		#print(self.count)
		self.data.img_show = self.data.img_rgb.copy()
		img_show = self.data.img_show
		for wall in self.wall_list:
			min_x, min_y, max_x, max_y = wall
			color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
			if max_x - min_x > max_y - min_y:
				# 横向墙
				row = int((max_y + min_y) / 2)
				cv2.arrowedLine(img_show, (min_x, row), (max_x, row), color)
				cv2.putText(img_show, str(max_x - min_x), (int((max_x + min_x) / 2) - 5, min_y - 2), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 2)
				#cv2.arrowedLine(img, (min_x, row), (max_x, row), (200,0,0))
				cv2.putText(img, str(max_x - min_x), (int((max_x + min_x) / 2) - 5, min_y - 2), cv2.FONT_HERSHEY_SIMPLEX,
							0.8, color, 1)
			else:
				# 竖向墙
				col = int((max_x + min_x) / 2)
				cv2.arrowedLine(img_show, (col, min_y), (col, max_y), color)
				cv2.putText(img_show, str(max_y - min_y), (max_x + 2, int((max_y + min_y) / 2) - 5), cv2.FONT_HERSHEY_SIMPLEX,
							1.2, color, 2)
				#cv2.arrowedLine(img, (col, min_y), (col, max_y), (200,0,0))
				cv2.putText(img, str(max_y - min_y), (max_x + 2, int((max_y + min_y) / 2) - 5), cv2.FONT_HERSHEY_SIMPLEX,
							0.8, color, 1)
			img[min_y : max_y + 1, min_x : max_x + 1] = 0
			#cv2.rectangle(img, (min_x, min_y), (max_x, max_y), color, 2)

		self.data.img_binary = img.copy()
		self.shower.showProcessedImg(True)

	def rectangulazieContour(self):
		self.cutContour()
		self.getRectWalls()

	# img = self.data.img_binary
	# ct = cv2.boundingRect(contour)
	# #print(ct)
	# x, y, w, h = ct
	# if (w + 5 > self.data.width and h + 5 > self.data.height or
	# 		(max([w, h]) < 20)):
	# 	return
	#
	# self.count += 1
	# start = self.getStartPoint(ct, self.data.img_binary)
	# #print(contour)
	# print(start)
	# cv2.circle(self.data.img_show, start, 5, (0,0,255), -1)
	# cv2.putText(self.data.img_show, str(self.cur_contour_index), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)


	#边缘点近似
	def approxEdgePoints(self):
		self.recover(3)
		self.process_index = 3
		if 0 == len(self.contours):
			self.contours, hieracy = cv2.findContours(self.data.img_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		contours = self.contours.copy()
		#contours[self.cur_contour_index] = []
		# self.data.img_binary = self.img_binary_raw.copy()

		# if 0 == self.cur_contour_index:
		# 	self.cur_contour_index = (self.cur_contour_index + 1) % len(contours)
			#return

		img = self.data.img_binary
		for i in range(1, len(contours)):
			contours[i] = cv2.approxPolyDP(contours[i], 2, True)
			cv2.fillPoly(img, [contours[i]], (0, 0, 0))

		self.shower.showProcessedImg(True)

	def cutContour(self):
		#切割当前轮廓
		# if 3 != self.process_index:
		# 	self.img_binary_raw = self.img_binary_cur.copy()
		self.recover(4)
		self.process_index = 4

		if 0 == len(self.contours):
			self.contours, hieracy = cv2.findContours(self.data.img_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		contours = self.contours.copy()
		#contours[self.cur_contour_index] = []
		self.data.img_binary = self.img_binary_raw.copy()

		if 0 == self.cur_contour_index:
			self.cur_contour_index = (self.cur_contour_index + 1) % len(contours)
			#return

		img = self.data.img_binary
		for i in range(1, len(contours)):
			if i != self.cur_contour_index:
				contours[i] = cv2.approxPolyDP(contours[i], 1, True)
				cv2.fillPoly(img, [contours[i]], (255,0,0))

		ct = cv2.boundingRect(contours[self.cur_contour_index])
		x, y, w, h = ct
		print('第 ', self.cur_contour_index, ' 个轮廓:', ct, '共 ', len(contours), ' 个轮廓')
		#print('contour:',contours[self.cur_contour_index],'\n')
		#cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
		#cv2.putText(img, str(self.cur_contour_index), (x + int(w/2), y + int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0),2)
		self.getWallsDepthInOneContour(contours[self.cur_contour_index])

		self.shower.showProcessedImg(True)
		self.data.img_show = self.data.img_binary
		# self.data.img_name = 'ct' + str(17 + self.cur_contour_index)+'.jpg'
		# cv2.imwrite(self.data.img_name, img)
		self.img_binary_cur = img.copy()
		self.cur_contour_index = (self.cur_contour_index + 1) % len(contours)

	#检测墙厚度
	def getWallsDepth(self):
		for contour in self.contours:
			self.getWallsDepthInOneContour(contour)

	def getWallsDepthInOneContour(self, contour):
		ct = cv2.boundingRect(contour)
		x, y, w, h = ct
		depths = []
		img = self.data.img_binary
		for row in range(y, y + h, 5):
			start = x + w
			for col in range(x, x + w):
				if img[row][col] == 0:
					if start > col:
						start = col
				elif start < col:
					#扫描结束
					depth = col - start + 1
					if depth >= self.rect_thresh_min and depth <= self.rect_thresh_max:
						#print('添加竖墙厚度:',depth,'row:', row)
						depths.append(depth)
					break
		for col in range(x, x + w, 5):
			start = y + h
			for row in range(y, y + h):
				if img[row][col] == 0:
					if start > row:
						start = row
				elif start < row:
					# 扫描结束
					depth = row - start + 1
					if depth >= self.rect_thresh_min and depth <= self.rect_thresh_max:
						#print('添加横墙厚度:', depth, 'col:', col)
						depths.append(depth)
					break
		depths.sort()

		self.wall_depth_min = self.rect_thresh_min
		self.wall_depth_max = self.rect_thresh_max
		if len(depths) > 0:
			self.wall_depth_min = depths[0]
			self.wall_depth_max = depths[len(depths) - 1]
			if self.wall_depth_max - self.wall_depth_min > 10:
				# 厚度差过大
				for index in range(1, len(depths)):
					differ = depths[index] - depths[index - 1]
					if differ > 5:
						#差异过大，排除
						if index > len(depths) / 4 * 3:
							self.wall_depth_max = depths[index - 1]
							break

		#print('墙厚：', depths, '\n')
		print('墙范围：{0}--{1}\n'.format(self.wall_depth_min, self.wall_depth_max))

	def getRectWalls(self):
		self.test_step = 0
		contour_index = (self.cur_contour_index + len(self.contours) - 1) % len(self.contours)
		img = self.img_binary_cur.copy()
		img = self.data.img_binary
		ct = cv2.boundingRect(self.contours[contour_index])
		x, y, w, h = ct
		start = self.getStartPoint(ct, img)
		print('包围：', x, y, w, h)
		print('起始点:', start)
		dir, max = self.getDirection(start, img)
		cur_row = start[1]
		cur_col = start[0]
		rect_list = self.wall_list#[]
		self.rectWall(ct, (cur_col, cur_row, dir, max), img, rect_list)
		self.data.img_show = self.data.img_binary.copy()
		print('包围矩形：', rect_list)
		index = 0
		for rect in rect_list:
			# if 1 != dir and 2 != dir:
			# 	break
			min_x, min_y, max_x, max_y = rect
			color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
			cv2.rectangle(self.data.img_show, (min_x, min_y), (max_x, max_y), color, 2)
			#cv2.putText(self.data.img_show, str(index), (min_x, min_y),	cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 2)
			self.data.img_binary[min_y: max_y + 1, min_x: max_x + 1] = 0
			#cv2.rectangle(self.data.img_binary, (min_x, min_y), (max_x, max_y), (150, 50, 70), 1)
			index += 1
		self.shower.showProcessedImg()

		'''if 2 == dir or max < self.rect_thresh_min:
			#方向待定
			print('方向待定:', max)
			if max > self.rect_thresh_max:
				#夹角
				pass
		elif 1 == dir:
			#竖向墙
			max_width = 0
			width = 0
			min_x = x + w
			max_x = x
			min_y = y + h
			max_y = y
			for row in range(cur_row, y+h):
				if img[row][cur_col] > 0:
					width = 0
					get_left = True
					get_right = True
					for i in range(1, self.rect_thresh_max):
						#print(row, cur_col, i, img[row][cur_col - i], img[row][cur_col + i])
						if get_left and cur_col - i >= 0 and img[row][cur_col - i] == 0:
							if cur_col - i < min_x:
								# print('min_x赋值1：', cur_col - i)
								min_x = cur_col - i
							width += 1
						else:
							if get_left:
								print('左边到头了', row, cur_col - i, img[row][cur_col - i])
							get_left = False
						if get_right and cur_col+i < x+w and img[row][cur_col + i] == 0:
							if cur_col + i > max_x:
								#print('max_x赋值1：', cur_col + i)
								max_x = cur_col + i
							width += 1
						else:
							if get_right:
								print('右边到头了', row, cur_col + i, img[row][cur_col + i])
							get_right = False
					if width == 0:
						#到头了
						end_y = row
						print('到头了：', max_y)
						break
					elif width > self.rect_thresh_max:
						#转角
						pass
					else:
						pass
				else:
					get_left = True
					get_right = True
					for i in range(0, self.rect_thresh_max):
						if get_left and cur_col - i >= 0 and img[row][cur_col - i] == 0:
							if cur_col - i < min_x:
								# print('min_x赋值2：', cur_col - i)
								min_x = cur_col - i
							else:
								pass
								#print('min_x没有赋值2：', cur_col - i)
						else:
							get_left = False
						if get_right and cur_col+i < x+w and img[row][cur_col + i] == 0:
							if cur_col + i > max_x:
								# print('max_x赋值2：', cur_col + i)
								max_x = cur_col + i
						else:
							get_right = False
					if row < min_y:
						start_y = row
					if row > max_y:
						max_y = row
			print('包围：', x, y, w, h)
			print('竖向墙：', min_x, max_x, min_y, max_y)

			self.data.img_show = self.data.img_binary.copy()
			cv2.rectangle(self.data.img_binary, (min_x, min_y), (max_x, max_y), (150, 50, 70), 1)

			self.shower.showProcessedImg(True)
		else:
			#横向墙

			print('横向墙:', max)
			pass
		'''

	def cutAndFufillContour(self):
		print('开始切割')
		self.cutContour()
		print('填充墙的外包围矩形')
		self.getRectWalls()

	def saveContour(self):
		img_name = 'ct-'+str(self.cur_contour_index)+'.jpg'
		print('保存轮廓：', img_name)
		cv2.imwrite(img_name, self.data.img_show)

	def rectWall(self, contour, point, img, rect_list):
		if 0 == self.test_step:
			# for root, dir, file_list in os.walk('./'):
			# 	print(root, dir, file_list)
			file_list = os.listdir('./')
			for file in file_list:
				pos = file.find('test-')
				if 0 == pos:
					pos = file.rfind('.jpg')
					if pos == len(file) - 4:
						os.remove(file)
		#cv2.imwrite('test-{0}.jpg'.format(self.test_step), img)
		self.test_step += 1
		cur_col, cur_row, dir, max = point
		x, y, w, h = contour
		min_x = x + w
		max_x = x
		min_y = y + h
		max_y = y
		#rect_list = []
		wall = []
		if 2 == dir or max < self.wall_depth_min:
			#方向待定
			print('方向待定:', max)
			if max > self.wall_depth_max:
				#夹角
				new_dir = 0
				wall = self.getOneWall(contour, (cur_col, cur_row, new_dir, max), img)
				min_x, min_y, max_x, max_y = wall[0]
				rect_list.append(wall[0])

				print('墙：', wall)
				img_roi = np.zeros((abs(max_y - min_y), abs(max_x - min_x)), dtype=np.uint8)
				img[min_y:max_y + 1, min_x:max_x + 1] = 255

		elif 1 == dir:
			#竖向墙
			wall = self.getOneWall(contour, point, img)
			min_x, min_y, max_x, max_y = wall[0]
			rect_list.append(wall[0])
			img_roi = np.zeros((abs(max_y - min_y), abs(max_x - min_x)), dtype=np.uint8)
			img[min_y:max_y + 1, min_x:max_x + 1] = 255
		else:
			#横向墙
			wall = self.getOneWall(contour, point, img)
			min_x, min_y, max_x, max_y = wall[0]
			rect_list.append(wall[0])

			img_roi = np.zeros((abs(max_y - min_y), abs(max_x - min_x)), dtype=np.uint8)
			img[min_y:max_y+1, min_x:max_x+1] = 255
		wall_dir = lambda dir : '竖墙' if 1 == dir else '横墙' if 0 == dir else "其他墙"
		print('墙({0}-{1})：{2}'.format(self.test_step, wall_dir(dir), wall))
		if len(wall) > 1 and len(wall[1]) > 0:
			other_walls = wall[1]
			for other_wall in other_walls:
				#print('other_wall:',other_wall)
				width = 0
				height = 0
				start_point = []
				if 1 == dir:
					#竖向墙
					width = max_x - min_x + 1
					height = other_wall[3] - other_wall[2] + 1
					img_roi = np.zeros((abs(height), abs(width)), dtype=np.uint8)
					img[other_wall[2]:other_wall[3] + 1, min_x:max_x + 1] = img_roi
				else:
					#横向墙
					width = other_wall[3] - other_wall[2] + 1
					height = max_y - min_y + 1
					img_roi = np.zeros((abs(height), abs(width)), dtype=np.uint8)
					img[min_y:max_y + 1, other_wall[2]:other_wall[3] + 1] = img_roi

			for other_wall in other_walls:
				print('other_wall:',other_wall)
				# width = 0
				# height = 0
				start_point = []
				if 1 == dir:
					#竖向墙
					# width = max_x - min_x + 1
					# height = other_wall[3] - other_wall[2] + 1
					# img_roi = np.zeros((abs(height), abs(width)), dtype=np.uint8)
					# img[other_wall[2]:other_wall[3] + 1, min_x:max_x + 1] = img_roi
					start_point = [min_x, other_wall[2], 0, other_wall[1] - other_wall[0]]
				else:
					#横向墙
					# width = other_wall[3] - other_wall[2] + 1
					# height = max_y - min_y + 1
					# img_roi = np.zeros((abs(height), abs(width)), dtype=np.uint8)
					# img[min_y:max_y + 1, other_wall[2]:other_wall[3] + 1] = img_roi
					start_point = [other_wall[2], min_y, 1, other_wall[1] - other_wall[0]]
				print('img_roi:',(height, width))

				# cv2.putText(self.data.img_show, str(self.cur_contour_index), (start_point[0], start_point[1]), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
				# 			(0, 255, 0), 2)

				new_dir, max = self.getDirection((start_point[0],start_point[1]), img)
				# start_point += [dir, max]
				print('new start:', start_point,'test_dir:',new_dir)
				#cv2.rectangle(self.data.img_binary, (other_wall[2], min_y), (other_wall[3], max_y), (0, 0, 0), 1)

				self.rectWall(contour, start_point, img, rect_list)
				# wall = self.getOneWall(contour, start_point, img)
				# rect_list.append(wall[0])

	def getOneWall(self, contour, point, img):
		cur_col, cur_row, dir, max = point
		print('起始点：',point)
		x, y, w, h = contour #外包围框
		min_x = cur_col	#左边界
		max_x = cur_col #右边界
		min_y = cur_row	#上边界
		max_y = cur_row	#下边界
		wall = []		#墙，第一个参数为起始-结束的矩形，第二个参数为下一个起始点及方向(如果存在的话)
		next_start = []	#下一个起始点及方向(如果存在的话)
		start_index = 0	#0:未开始，1：已开始，2：结束
		end_index = 0
		line_edges = [] # 每行/列边界，元素结构：左，右，行数
		other_walls = []

		if 2 == dir or max < self.wall_depth_min:
			#方向待定
			print('方向待定:', max)
			if max > self.wall_depth_max:
				#夹角
				pass
		elif 1 == dir:
			#竖向墙
			width = 0
			#print('竖向墙起始：', cur_row,'-->', y + h)
			cur_line_min = cur_col #竖墙已探测的左右边界
			cur_line_max = cur_col
			signs = [-1, 1]  # 偏离方向
			# for row in range(cur_row, y+h):
			get_top = False		#顶部到头
			get_bottom = False	#底部到头
			is_start = False	#开始
			for sign in signs:
				for offset in range(0, h):
					offset = offset * sign
					row = cur_row + offset
					if row >= y + h:
						get_bottom = True
					if row <= y:
						get_top = True

					if get_bottom and get_top:
						break
					if offset < 0 and get_top:
						continue
					if offset > 0 and get_bottom:
						continue

					line_min = cur_col
					line_max = cur_col
					if img[row][cur_col] > 0 and is_start:
						#扫描到非墙体
						width = 0
						get_left = 0	#0:未找到第一个，1：已开始统计
						get_right = 0
						print('非墙体：',[row, cur_col])
						for i in range(1, w):#self.rect_thresh_max + 10):
							#print(row, cur_col, i, img[row][cur_col - i], img[row][cur_col + i])
							if 2 == get_left and 2 == get_right:
								if line_min == line_max:
									if offset > 0:
										#print('非墙体向下到头了：',[row, cur_col, i])
										get_bottom = True
									else:
										#print('非墙体向上到头了：', [row, cur_col, i])
										get_top = True
								break
							if cur_line_max > cur_line_min:
								#如果扫描到之前找到的最大边界，还没有发现墙体，不再扫描
								if (cur_col - i < x) or (cur_col - i <= cur_line_min and img[row][cur_col - i] > 0 and 0 == get_left):
									# if 3 == self.test_step:
									# 	print('停止扫描左侧:',[cur_col - i, row], '当前边界:',[line_min, line_max])
									get_left = 2
								if (cur_col + i >= x + w) or (cur_col + i >= cur_line_max and img[row][cur_col + i] > 0 and 0 == get_right):
									# if 3 == self.test_step:
									# 	print('停止扫描右侧:', [cur_col + i,row], '当前边界:',[line_min, line_max])
									get_right = 2

							if 2 != get_left:
								if cur_col - i < x:
									#左边到头
									get_left = 2
								elif img[row][cur_col - i] == 0:
									if cur_col - i < line_min:
										# print('min_x赋值1：', cur_col - i)
										line_min = cur_col - i
									width += 1
									if 0 == get_left:
										get_left = 1
								elif 1 == get_left and img[row][cur_col - i] > 0:
									#print('左边到头了1', row, cur_col - i, img[row][cur_col - i])
									get_left = 2

							if 2 != get_right:
								if cur_col+i >= x+w:
									get_right = 2
								elif img[row][cur_col + i] == 0:
									if cur_col + i > line_max:
										#print('max_x赋值1：', cur_col + i)
										line_max = cur_col + i
									width += 1
									if 0 == get_right:
										get_right = 1
								elif 1 == get_right and img[row][cur_col + i] > 0:
									#print('右边到头了1', row, cur_col + i, i, img[row][cur_col + i])
									get_right = 2

						if width > 0 and max_y < row:
							#print('更新高度：', row, 'width:', width, get_left, get_right, line_min, line_max)
							max_y = row

						if width == 0 and not (2 == get_right or 2 == get_left):
							#到头了
							max_y = row
							print('到头了：', max_y)
							break
						elif width > self.wall_depth_max:
							#转角
							line_edges.append([line_min, line_max, row])
							print('竖墙转角')
						elif line_max > line_min:
							line_edges.append([line_min, line_max, row])
					else:
						is_start = True
						get_left = 0
						get_right = 0
						for i in range(0, w):#self.rect_thresh_max + 10):
							if 2 == get_right and 2 == get_left:
								break
							if 2 != get_left:
								if cur_col - i < x:
									#左边到头
									get_left = 2
								elif img[row][cur_col - i] == 0:
									if cur_col - i < line_min:
										# print('min_x赋值2：', cur_col - i,'。行:',row)
										line_min = cur_col - i
									if 0 == get_left:
										get_left = 1
								elif 1 == get_left and img[row][cur_col - i] > 0:
									# print('左边到头了', row, cur_col - i, img[row][cur_col - i])
									get_left = 2

							if 2 != get_right:
								if cur_col+i >= x+w:
									get_right = 2
								elif cur_col+i < x+w and img[row][cur_col + i] == 0:
									if cur_col + i > line_max:
										#print('max_x赋值2：', cur_col + i)
										line_max = cur_col + i
									if 0 == get_right:
										get_right = 1
								elif 1 == get_right and img[row][cur_col + i] > 0:
									# print('右边到头了', row, cur_col + i, img[row][cur_col + i])
									get_right = 2
						# print('添加边界：',[line_min, line_max, row])
						if line_max > line_min:
							line_edges.append([line_min, line_max, row])

						if row < min_y:
							min_y = row
						if row > max_y:
							if 3 == self.test_step and True:
								print('更新下边界：{0}-->{1}'.format(max_y, row))
							max_y = row

					if line_max > line_min and line_max - line_min < self.wall_depth_max:
						if line_min < cur_line_min:
							print('更新左边界：row:',row,cur_line_min,'-->',line_min)
							cur_line_min = line_min
						if line_max > cur_line_max:
							print('更新右边界：row:', row, cur_line_max, '-->', line_max)
							cur_line_max = line_max

			# print('竖墙line_edges[左 右 行]:', line_edges)

			#遍历，获取边界
			other_wall_min = cur_row - 1
			other_wall_max = cur_row - 1
			is_other_wall = False
			other_wall = []
			line_edges.sort(key=lambda x: x[2])
			#min_y = line_edges[0][2]
			#max_y = line_edges[len(line_edges) - 1][2]
			for line_edge in line_edges:
				line_min, line_max, row = line_edge
				if line_max - line_min >= self.wall_depth_max:
					#干扰墙
					if not is_other_wall:
						print('发现新干扰墙：',line_edge)
						other_wall = [line_min, line_max]
						other_wall_min = row
						is_other_wall = True
					else:
						other_wall_max = row
				else:
					if is_other_wall:
						other_wall += [other_wall_min, other_wall_max]
						print('添加外墙:', [other_wall_min, other_wall_max],line_edge)
						other_walls.append(other_wall)
						other_wall = []
					is_other_wall = False
					if other_wall_min == other_wall_max or \
							(other_wall_min != other_wall_max and
										 row - other_wall_min > self.wall_depth_max):
						#排除其他墙干扰
						if line_min < min_x:
							print('更新边界:', (min_x, max_x), '-->', (line_min, line_max),'其他墙：',(other_wall_min, other_wall_max, row))
							min_x = line_min
						if line_max > max_x:
							print('更新边界:', (min_x, max_x), '-->', (line_min, line_max),'其他墙：',(other_wall_min, other_wall_max, row))
							max_x = line_max
			if len(other_wall) > 0:
				other_wall += [other_wall_min, other_wall_max]
				#print('到头了,添加外墙:', other_wall)
				other_walls.append(other_wall)

			print('包围：', x, y, w, h)
			print('竖向墙：列：', min_x, '->', max_x, '行：', min_y, '->', max_y)
		else:
			#横向墙
			height = 0
			min_x = x + w
			max_x = x
			min_y = y + h
			max_y = y
			signs = [-1, 1] #偏离方向
			#for col in range(cur_col, x + w):

			for sign in signs:
				for offset in range(0, w):
					offset = offset * sign
					col = cur_col + offset
					if col >= x + w or col < x:
						continue
					#print('当前列:',col)
					line_min = y + h
					line_max = y
					if img[cur_row][col] > 0:
						width = 0
						get_top = 0  # 0:未找到第一个，1：已开始统计
						get_bottom = 0
						for i in range(1, self.wall_depth_max + 30):
							# print(row, cur_col, i, img[row][cur_col - i], img[row][cur_col + i])
							if 2 == get_top and 2 == get_bottom:
								break
							if 2 != get_top:
								if cur_row - i >= y and img[cur_row - i][col] == 0:
									if cur_row - i < line_min:
										# print('min_x赋值1：', cur_col - i)
										line_min = cur_row - i
									height += 1
									if 0 == get_top:
										get_top = 1
								elif 1 == get_top and img[cur_row - i][col] > 0:
									#print('上边到头了1', cur_row - i, col, img[cur_row - i][col])
									get_top = 2

							if 2 != get_bottom:
								if cur_row + i < y + h and img[cur_row + i][col] == 0:
									if cur_row + i > line_max:
										# print('max_y赋值1：', cur_col + i)
										line_max = cur_row + i
									height += 1
									if 0 == get_bottom:
										get_bottom = 1
								elif 1 == get_bottom and img[cur_row + i][col] > 0:
									#print('下边到头了1', cur_row + i, col, i, img[cur_row + i][col])
									get_bottom = 2

						if height == 0:
							# 到头了
							max_x = col
							#print('向右到头了：', max_x)
							break
						elif height > self.wall_depth_max:
							# 转角
							if line_max > line_min:
								line_edges.append([line_min, line_max, col])
							pass
						else:
							if line_max > line_min:
								line_edges.append([line_min, line_max, col])
					else:
						get_top = 0
						get_bottom = 0
						for i in range(0, self.wall_depth_max + 10):
							if 2 != get_top:
								if cur_row - i >= 0 and img[cur_row - i][col] == 0:
									if cur_row - i < line_min:
										# print('min_y赋值2：', cur_row - i)
										line_min = cur_row - i
									if 0 == get_top:
										get_top = 1
								elif 1 == get_top and img[cur_row - i][col] > 0:
									#print('上边到头了', cur_row - i, col, img[cur_row - i][col])
									get_top = 2

							if 2 != get_bottom:
								if cur_row + i < y + h and img[cur_row + i][col] == 0:
									if cur_row + i > line_max:
										# print('max_y赋值2：', cur_col + i)
										line_max = cur_row + i
									if 0 == get_bottom:
										get_bottom = 1
								elif 1 == get_bottom and img[cur_row + i][col] > 0:
									#print('下边到头了2', cur_row + i, col, i, img[cur_row + i][col])
									get_bottom = 2
						if line_max > line_min:
							line_edges.append([line_min, line_max, col])
						if col < min_x:
							min_x = col
						if col > max_x:
							max_x = col
						if line_max - line_min > 0 and line_max - line_min < self.wall_depth_max:
							cur_row = int((line_min + line_max)/2)

			# 遍历，获取边界
			other_wall_min = cur_col - 1
			other_wall_max = cur_col - 1
			is_other_wall = False
			other_wall = []
			line_edges.sort(key = lambda x:x[2])
			#print('横墙line_edges[上 下 列]:', line_edges)
			for line_edge in line_edges:
				line_min, line_max, col = line_edge
				#print('line_edge:',line_edge)
				if line_max - line_min >= self.wall_depth_max:
					# 干扰墙
					#print('此处为干扰墙。',line_edge, is_other_wall)
					if not is_other_wall:
						other_wall = [line_min, line_max]
						other_wall_min = col
						is_other_wall = True
					else:
						other_wall_max = col
				else:
					if is_other_wall:
						other_wall += [other_wall_min, other_wall_max]
						other_walls.append(other_wall)
						other_wall = []
					is_other_wall = False
					if other_wall_min == other_wall_max or \
							(other_wall_min != other_wall_max and
										 col - other_wall_min > self.wall_depth_max):
						# 排除其他墙干扰
						if line_min < min_y:
							print('更新边界:', (min_y, max_y), '-->', (line_min, line_max), '其他墙：',
								  (other_wall_min, other_wall_max, col))
							min_y = line_min
						if line_max > max_y:
							print('更新边界:', (min_y, max_y), '-->', (line_min, line_max), '其他墙：',
								  (other_wall_min, other_wall_max, col))
							max_y = line_max

			if len(other_wall) > 0:
				other_wall += [other_wall_min, other_wall_max]
				other_walls.append(other_wall)

			print('包围：', x, y, w, h)
			print('横向墙：列：', min_x, '->', max_x, '行：', min_y, '->', max_y)
		wall.append([min_x, min_y, max_x, max_y])
		wall.append(other_walls)

		return wall

	def getDirection(self, point, img):
		#获取当前点所在墙的方向
		thresh_min = self.wall_depth_min
		thresn_max = self.wall_depth_max
		x, y = point
		max_height = 0
		max_width = 0

		get_top = True
		get_bottom = True
		#print('获取墙方向')
		for row in range(thresn_max):
			if not (get_top or get_bottom):
				break
			if get_bottom and img[y + row][x] == 0:
				max_height += 1
			else:
				get_bottom = False
			if get_top and img[y - row][x] == 0:
				max_height += 1
			else:
				get_top = False

		get_left = True
		get_right = True
		for col in range(thresn_max):
			#print('当前：', x, y, col, img[y][x-col], img[y][x+col])
			if not (get_left or get_right):
				break
			if get_right and img[y][x+col] == 0:
				max_width += 1
				#print('右边加一')
			else:
				get_right = False
				#print('右边到头了',max_width)
			if get_left and img[y][x-col] == 0:
				max_width += 1
				#print('左边加一')
			else:
				get_left = False
				#print('左边到头了',max_width)


		print('最大宽度:',max_width,'最大高度:',max_height)
		if max_width > max_height:
			return 0, max_width
		elif max_width < max_height:
			return 1, max_height
		else:
			return 2, max_height

	def getStartPoint(self, list_contour, img):
		x, y, w, h = list_contour
		#print(list_contour)
		start = (x, y)
		#print('上:', y)
		for col in range(x, x + w):
			#print(self.data.img_binary[y][col])
			if img[y][col] == 0:
				return ((col, y))
		#print('左:', x)
		for row in range(y, y + h):
			#print(self.data.img_binary[row][x])
			if img[row][x] == 0:
				return ((x, row))
		#print('右:', x+w-1)
		for row in range(y, y + h):
			#print(self.data.img_binary[row][x])
			if img[row][x + w - 1] == 0:
				return ((x + w - 1, row))
		#print('下:',y+h-1)
		for col in range(x, x + w):
			#print(self.data.img_binary[y+h-1][col])
			if img[y+h-1][col] == 0:
				return ((col, y+h-1))

		return self.getStartPoint([x + 1, y + 1, w - 2, h - 2], img)

	def recoverAllFilter(self):
		self.img_binary_raw = self.img_binary.copy()
		self.img_binary_cur = self.img_binary.copy()
		self.data.img_binary = self.img_binary
		self.data.img_show = self.img_binary
		self.shower.showProcessedImg(True)

	def imgMinChange(self):
		index = self.sld_img_min.value()
		self.text_img_min.setText(str(self.sld_img_min.value()))
		if index > self.test_index:
			self.test_index = index

	def imgMinChangeByText(self):
		text = self.text_img_min.text()
		try:
			img_min = int(text)
			if img_min < self.sld_img_min.minimum():
				self.sld_img_min.setMinimum(img_min)
			elif img_min > self.sld_img_min.maximum():
				self.sld_img_min.setMaximum(img_min)
			self.sld_img_min.setValue(img_min)
			#self.imgMinChange()
		except:
			print('设置img_min:{0}失败!'.format(text))
			self.text_img_min.setText(str(self.sld_img_min.value()))


	def imgMaxChange(self):
		self.text_img_max.setText(str(self.sld_img_max.value()))
		index = self.sld_img_max.value()
		if index < self.test_index:
			self.test_index = index

	def imgMaxChangeByText(self):
		text = self.text_img_max.text()
		try:
			img_max = int(text)
			if img_max < self.sld_img_max.minimum():
				self.sld_img_max.setMinimum(img_max)
			elif img_max > self.sld_img_max.maximum():
				self.sld_img_max.setMaximum(img_max)
			self.sld_img_max.setValue(img_max)
			#self.imgMaxChange()
		except:
			print('设置img_max:{0}失败!'.format(text))
			self.text_img_max.setText(str(self.sld_img_max.value()))

	def approxChange(self):
		self.approx = self.sld_approx.value()
		self.text_approx.setText(str(self.approx))
		self.approxEdgePoints()

	def approxChangeByText(self):
		text = self.text_approx.text()
		try:
			approx = int(text)
			self.sld_approx.setValue(approx)
			self.approxEdgePoints()
		except:
			print('近视值:{0}失败!'.format(text))
			self.text_approx.setText(str(self.approx))

	def loadContourImg(self):
		img_name, chose = QtWidgets.QFileDialog.getOpenFileName(self, "选择图像", './',
																"JPG (*.jpg);;ALL(*);;PNG (*.png);;BMP(*.bmp)")

		if self.readImg(img_name):
			print('读取成功!')
		else:
			print('读取失败!')

	def importTestImg(self):
		img_min_index = self.sld_img_min.value()
		img_max_index = self.sld_img_max.value()
		test_index = self.test_index
		if img_min_index > img_max_index:
			img_min_index = img_max_index
			img_max_index = self.sld_img_min.value()
		elif img_max_index == img_min_index:
			test_index = img_min_index
		img_name = 'ct' + str(test_index) + '.jpg'

		if self.readImg(img_name):
			self.test_index = test_index
			print(img_min_index, '->', img_max_index)
			self.test_index = (self.test_index - img_min_index + 1) % (
			img_max_index - img_min_index + 1) + img_min_index
		# self.data.read(img_name)#self.list_test_imgs[self.test_index])
		# if not self.data.check():
		# 	print('越界!找不到该图片！')
		#
		# self.test_index = test_index
		#
		# self.data.img_binary = self.data.img_show
		# if 3 == len(self.data.img_binary.shape):
		# 	print('3通道')
		# 	thresh, self.data.img_binary = cv2.threshold(self.data.img_gray, 10, 255, cv2.THRESH_BINARY)
		# self.img_binary = self.data.img_binary.copy()
		# self.img_binary_raw = self.img_binary.copy()
		# self.img_binary_cur = self.img_binary.copy()
		# self.contours, hieracy = cv2.findContours(self.img_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		# self.shower.showProcessedImg(True)
		# self.text_img_name.setText(img_name)#self.list_test_imgs[self.test_index])
		#
		#
		# print(img_min_index,'->',img_max_index)
		# self.test_index = (self.test_index - img_min_index + 1) % (img_max_index - img_min_index + 1) + img_min_index

	def readImg(self, img_name):
		self.data.read(img_name)  # self.list_test_imgs[self.test_index])
		if not self.data.check():
			print('越界!找不到图片{0}！'.format(img_name))
			return False

		self.data.img_binary = self.data.img_show
		if 3 == len(self.data.img_binary.shape):
			print('3通道')
			thresh, self.data.img_binary = cv2.threshold(self.data.img_gray, 10, 255, cv2.THRESH_BINARY)
		self.img_binary = self.data.img_binary.copy()
		self.img_binary_raw = self.img_binary.copy()
		self.img_binary_cur = self.img_binary.copy()
		self.contours, hieracy = cv2.findContours(self.img_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		self.shower.showProcessedImg(True)
		self.text_img_name.setText(img_name)
		return True

if __name__ == '__main__':
	'''
	img = cv2.imread('ct14.jpg',1)
	cv2.imshow('ct3',img)
	img1 = cv2.flip(img,1,dst=None) #水平镜像
	cv2.imshow('lr',img1)
	cv2.imwrite('ct3_lr.jpg',img1)
	img2 = cv2.flip(img,0,dst=None) #垂直镜像
	cv2.imshow('tb',img2)
	cv2.imwrite('ct3_tb.jpg',img1)
	img3 = cv2.flip(img,-1,dst=None) #对角镜像
	cv2.imshow('ct',img3)
	'''
	# img = np.zeros((5, 8), dtype=np.uint8)
	# img[1:4, 1:7] = 255
	# contours, hieracy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	# for i in range(len(contours)):
	# 	x, y, w, h = cv2.boundingRect(contours[i])
	# 	print(x, y, w, h)
	# cv2.imshow('img', img)
	#
	# for col in range(1, 3):
	# 	print(col)
	# cv2.waitKey(0)

	list1 = [[1,3], [4,2]]
	list1.sort(key = lambda x:x[1])
	print(list1)

	arr = np.array([[1,2,3],[4,5,6]])
	print(arr)
	# print(arr[np.newaxis,:])
	# print(arr[:2,np.newaxis])
	# print(arr.reshape(3,2))
	# print(arr.reshape(6,1))
	arr = np.arange(36.0)
	print(arr)
	arr = arr.reshape(6, 6)
	print(arr)
	print(np.split(arr,2))#拆分为2个
	print(np.split(arr,3,axis=1))#以列为单位，拆分为3个


