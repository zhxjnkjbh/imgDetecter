#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QLabel,QLineEdit
from PyQt5 import QtCore
import cv2
import numpy as np

class Saver(QWidget):
	def __init__(self, shower):
		super().__init__()
		self.type_list = ['jpg', 'bmp', 'png']
		self.type = self.type_list[0]
		self.width = 1920
		self.height = 1080
		self.initUi()
		self.initData(shower)


	def initUi(self):
		self.label0 = QLabel('保存格式:', self)
		self.label0.resize(60,25)
		self.label0.move(10, 10)

		self.comb_type = QComboBox(self)
		self.comb_type.move(80, 10)
		self.comb_type.resize(50, 20)
		self.comb_type.addItems(self.type_list)
		self.comb_type.currentIndexChanged.connect(self.typeChange)

		self.label1 = QLabel('尺寸:', self)
		self.label1.resize(60, 25)
		self.label1.move(10, 40)

		self.text_width = QLineEdit(self)
		self.text_width.setGeometry(QtCore.QRect(50, 42, 40, 20))
		self.text_width.setText(str(self.width))
		self.text_width.textChanged.connect(self.widthChange)

		self.label2 = QLabel('*', self)
		self.label2.resize(20, 25)
		self.label2.move(95, 40)

		self.text_height = QLineEdit(self)
		self.text_height.setGeometry(QtCore.QRect(110, 42, 40, 20))
		self.text_height.setText(str(self.height))
		self.text_height.textChanged.connect(self.heightChange)


		self.qbt0 = QPushButton('切换图像,当前为原始', self)
		self.qbt0.resize(150, 25)
		self.qbt0.move(220, 10)
		self.qbt0.clicked.connect(self.saveImg)


	def initData(self, shower):
		self.shower = shower
		self.data = shower.data

	def typeChange(self):
		print(self.comb_type.currentIndex())
		self.type = self.type_list[self.comb_type.currentIndex()]

	def widthChange(self):
		try:
			self.width = int(self.text_width.text())
		except:
			print('请输入正整数！')

	def heightChange(self):
		try:
			self.height = int(self.height_width.text())
		except:
			print('请输入正整数！')

	def saveImg(self):
		pass

