import cv2

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QCheckBox
import numpy as np

class Beautify(QtWidgets.QWidget):
	def __init__(self, shower):
		super().__init__()
		self.initData(shower)
		self.initUi()

	def initData(self, shower):
		self.shower = shower
		self.data = shower.data

	def initUi(self):
		self.btn0 = QtWidgets.QPushButton('锐化', self)
		self.btn0.setGeometry(QtCore.QRect(10, 10, 80, 30))
		self.btn0.clicked.connect(self.sharpenImg)

	def sharpenImg(self):
		kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
		img = self.data.img_rgb
		self.data.img_show = cv2.filter2D(img, -1, kernel)
		self.shower.showProcessedImg()