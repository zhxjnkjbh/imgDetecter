# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
							 QLabel, QApplication)

from PyQt5 import QtGui

from PyQt5.QtGui import QPixmap

from photoData import PhotoData

class PhotoShower(QLabel):
	def __init__(self):
		super().__init__()
		self.data = PhotoData()
		self.initUI()

	def initUI(self):
		#hbox = QHBoxLayout(self)
		self.pixmap = QPixmap()
		#self.lbl = QLabel(self)
		#self.show(QPixmap('3.jpg'))
		'''
		hbox.addWidget(lbl)
		self.setLayout(hbox)

		self.move(300, 200)
		self.setWindowTitle('Red Rock')
		self.show()'''

		'''
		print(self.data.width, '*', self.data.height)
		self.QtImg = QtGui.QImage(self.data.img_raw, self.data.width, self.data.height,self.data.width * 3,
								  QtGui.QImage.Format_RGB888)

		self.QtImg = QtGui.QImage(self.data.img_g, self.data.width, self.data.height,  QtGui.QImage.Format_Grayscale8)
		print('test:', self.QtImg.width(),'*', self.QtImg.height())
		'''
		#self.show(0)


	def show(self, index):
		img_show = self.data.show(index)
		#self.show(QtGui.QPixmap.fromImage(img_show))
		self.pixmap = QtGui.QPixmap.fromImage(img_show)
		self.setPixmap(self.pixmap)

	def showProcessedImg(self, is_binary = False):
		#print('photoShower::showProcessedImg')
		img_show = self.data.showProcessedImg(is_binary)
		#print('photoShower::fromImage')
		#print(img_show)
		self.pixmap = QtGui.QPixmap.fromImage(img_show)
		#print('photoShower::show')
		self.setPixmap(self.pixmap)
