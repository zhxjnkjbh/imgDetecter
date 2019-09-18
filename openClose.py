#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import cv2
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton

from photoShower import PhotoShower
from photoData import PhotoData

class OpenClose(QWidget):
	def __init__(self, shower):
		super().__init__()
		self.initData(shower)
		self.index = 0
		self.type_list = ['腐蚀', '膨胀', '开', '闭', '先开后闭', '先闭后开']
		self.kernel_list = [cv2.MORPH_CROSS, cv2.MORPH_RECT, cv2.MORPH_ELLIPSE]
		self.type = 3  # 0-5:腐蚀，膨胀，开，闭，先开后闭，先闭后开
		self._index = 1
		self.kernel_type = 1
		self.kernel_size = 2
		self.kernel = cv2.getStructuringElement(self.kernel_list[self.kernel_type],
												(self.kernel_size * 2 + 1, self.kernel_size * 2 + 1),
												(self.kernel_size, self.kernel_size))
		self.initUi()

	def initData(self, shower):
		self.shower = shower
		self.data = self.shower.data  # PhotoData
		self.img_show = self.data.img_show


	def initUi(self):
		self.label0 = QtWidgets.QLabel(self)
		self.label0.setGeometry(QtCore.QRect(10, 8, 40, 20))
		self.label0.setText('类型:')
		self.btn_chk0 = QtWidgets.QRadioButton('腐蚀', self)
		self.btn_chk0.move(60, 10)
		self.btn_chk1 = QtWidgets.QRadioButton('膨胀', self)
		self.btn_chk1.move(120, 10)
		self.btn_chk2 = QtWidgets.QRadioButton('开', self)
		self.btn_chk2.move(180, 10)
		self.btn_chk3 = QtWidgets.QRadioButton('闭', self)
		self.btn_chk3.move(240, 10)
		self.btn_chk3.setChecked(True)
		self.btn_chk4 = QtWidgets.QRadioButton('先开后闭', self)
		self.btn_chk4.move(300, 10)
		self.btn_chk5 = QtWidgets.QRadioButton('先闭后开', self)
		self.btn_chk5.move(380, 10)
		self.btn_grp0 = QtWidgets.QButtonGroup(self)
		self.btn_grp0.addButton(self.btn_chk0, 0)
		self.btn_grp0.addButton(self.btn_chk1, 1)
		self.btn_grp0.addButton(self.btn_chk2, 2)
		self.btn_grp0.addButton(self.btn_chk3, 3)
		self.btn_grp0.addButton(self.btn_chk4, 4)
		self.btn_grp0.addButton(self.btn_chk5, 5)
		self.btn_grp0.buttonClicked.connect(self.typeChange)

		self.label0 = QtWidgets.QLabel(self)
		self.label0.setGeometry(QtCore.QRect(10, 40, 65, 20))
		self.label0.setText('卷积核尺寸:')

		self.sld_ksize = QtWidgets.QSlider(Qt.Horizontal, self)
		self.sld_ksize.setGeometry(QtCore.QRect(85, 40, 200, 20))
		self.sld_ksize.setMinimum(0)
		self.sld_ksize.setMaximum(20)
		self.sld_ksize.setValue(2)
		self.sld_ksize.valueChanged.connect(self.ksizeChange)

		self.text_ksize = QtWidgets.QLineEdit(self)
		self.text_ksize.setGeometry(QtCore.QRect(290, 40, 40, 20))
		self.text_ksize.setText(str(self.sld_ksize.value()))
		self.text_ksize.textChanged.connect(self.kSizeChangeByText)

		self.label1 = QtWidgets.QLabel(self)
		self.label1.setGeometry(QtCore.QRect(10, 70, 65, 20))
		self.label1.setText('卷积核类型:')

		self.btn_chk6 = QtWidgets.QRadioButton('Cross', self)
		self.btn_chk6.move(90, 70)
		self.btn_chk7 = QtWidgets.QRadioButton('Rect', self)
		self.btn_chk7.move(150, 70)
		self.btn_chk7.setChecked(True)
		self.btn_chk8 = QtWidgets.QRadioButton('Elipse', self)
		self.btn_chk8.move(210, 70)
		self.btn_grp1 = QtWidgets.QButtonGroup(self)
		self.btn_grp1.addButton(self.btn_chk6, 0)
		self.btn_grp1.addButton(self.btn_chk7, 1)
		self.btn_grp1.addButton(self.btn_chk8, 2)
		self.btn_grp1.buttonClicked.connect(self.kTypeChange)

		self.btn2 = QPushButton('运行', self)
		self.btn2.resize(100, 30)
		self.btn2.move(480, 30)
		self.btn2.clicked.connect(self.processImg)

		pass
		'''
		self.qbt0 = QPushButton('切换图像,当前为原始', self)
		self.qbt0.resize(150, 25)
		self.qbt0.move(10, 10)
		self.qbt0.clicked.connect(self.changeSplitePhoto)

		self.qbt1 = QPushButton('当前为原始图像', self)
		self.qbt1.resize(120, 25)
		self.qbt1.move(200, 10)
		self.qbt1.clicked.connect(self.changeGray)
		'''
	def typeChange(self):
		self.type = self.btn_grp0.checkedId()
		#self.text.setText(self.type_list[self.type])
		self.processImg()

	def ksizeChange(self):
		self.kernel_size = int(self.sld_ksize.value())
		self.text_ksize.setText(str(self.kernel_size))
		self.resetKernel()
		self.processImg()

	def kSizeChangeByText(self):
		self.kernel_size = int(self.text_ksize.text())
		self.sld_ksize.setValue(self.kernel_size)
		self.resetKernel()
		self.processImg()

	def resetKernel(self):
		self.kernel = cv2.getStructuringElement(self.kernel_list[self.kernel_type],
												(self.kernel_size * 2 + 1, self.kernel_size * 2 + 1),
												(self.kernel_size, self.kernel_size))
	def kTypeChange(self):
		self.kernel_type = self.btn_grp1.checkedId()
		self.resetKernel()
		self.processImg()

	def processImg(self):
		#self.data.img_show = self.img_show
		self.recover()
		if 0 == self.type:
			self.erode()
		elif 1 == self.type:
			self.dilate()
		elif 2 == self.type:
			self.open()
		elif 3 == self.type:
			self.close()
		elif 4 == self.type:
			self.closeAfterOpen()
		else:
			self.openAfterClose()
		print('show')
		if 2 == len(self.data.img_show.shape):
			self.data.img_binary = self.data.img_show.copy()
		self.shower.showProcessedImg()

	def recover(self):
		print('recover')
		if self.data.cur_index == self._index:
			#还原
			print('还原')
			self.data.img_show = self.img_show.copy()
		else:
			print('切换')
			self.data.cur_index = self._index
			self.img_show = self.data.img_show.copy()

	def erode(self):
		print('erode')
		self.data.img_show = cv2.erode(self.data.img_show, self.kernel)


	def dilate(self):
		print('dilate')
		self.data.img_show = cv2.dilate(self.data.img_show, self.kernel)
		pass

	def open(self):
		print('open')
		self.erode()
		self.dilate()

	def close(self):
		print('close')
		self.dilate()
		self.erode()

	def closeAfterOpen(self):
		self.open()
		self.close()

	def openAfterClose(self):
		self.close()
		self.open()
