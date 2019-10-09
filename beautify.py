import cv2

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QCheckBox, QSlider, QLabel
import numpy as np

class Beautify(QtWidgets.QWidget):
	def __init__(self, shower):
		super().__init__()
		self.initData(shower)
		self.initUi()

	def initData(self, shower):
		self.shower = shower
		self.data = shower.data
		self.bil_size = 5

	def initUi(self):
		self.btn0 = QtWidgets.QPushButton('锐化', self)
		self.btn0.setGeometry(QtCore.QRect(10, 10, 80, 25))
		self.btn0.clicked.connect(self.sharpenImg)

		self.lab0 = QLabel(self)
		self.lab0.move(10, 45)
		self.lab0.setText("滤波半径:")

		self.btn_filter_minus = QPushButton('-', self)
		self.btn_filter_minus.setGeometry(QtCore.QRect(70, 40, 20, 20))
		self.btn_filter_minus.clicked.connect(self.bilateralFilterMinus)

		self.sld_bil_filter = QSlider(Qt.Horizontal, self)
		self.sld_bil_filter.setGeometry(QtCore.QRect(92, 40, 100, 20))
		self.sld_bil_filter.setMinimum(0)
		self.sld_bil_filter.setMaximum(50)
		self.sld_bil_filter.setValue(self.bil_size)
		self.sld_bil_filter.valueChanged.connect(self.bilateralFilterSizeChange)

		self.btn_filter_plus = QPushButton('+', self)
		self.btn_filter_plus.setGeometry(QtCore.QRect(194, 40, 20, 20))
		self.btn_filter_plus.clicked.connect(self.bilateralFilterPlus)

		self.text_bil_filter = QtWidgets.QLineEdit(self)
		self.text_bil_filter.setGeometry(QtCore.QRect(220, 40, 40, 20))
		self.text_bil_filter.setText(str(self.sld_bil_filter.value()))
		self.text_bil_filter.textChanged.connect(self.bilateralFilterSizeChangeByText)

		self.btn_filter = QPushButton('滤波', self)
		self.btn_filter.setGeometry(QtCore.QRect(265, 38, 80, 25))
		self.btn_filter.clicked.connect(self.bilateralFilter)

	def sharpenImg(self):
		kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
		img = self.data.img_rgb
		self.data.img_show = cv2.filter2D(img, -1, kernel)
		self.shower.showProcessedImg()

	def bilateralFilterMinus(self):
		size = self.bil_size - 1
		if size < self.sld_bil_filter.minimum():
			size += 1
		else:
			self.sld_bil_filter.setValue(size)
			self.text_bil_filter.setText(str(self.bil_size))
			#self.bilateralFilter()


	def bilateralFilterSizeChange(self):
		self.bil_size = self.sld_bil_filter.value()
		self.text_bil_filter.setText(str(self.bil_size))
		#self.bilateralFilter()

	def bilateralFilterPlus(self):
		size = self.bil_size + 1
		if size > self.sld_bil_filter.maximum():
			size -= 1
		else:
			self.sld_bil_filter.setValue(size)
			self.text_bil_filter.setText(str(self.bil_size))
			#self.bilateralFilter()


	def bilateralFilterSizeChangeByText(self):
		try:
			text = int(self.text_bil_filter.text())
			self.sld_bil_filter.setValue(text)
			#self.bilateralFilter()
		except:
			print('输入错误！')

	def bilateralFilter(self):
		img = self.data.img_rgb
		self.data.img_show = cv2.bilateralFilter(img, self.bil_size, 50, 15)
		self.shower.showProcessedImg()

		pass

if __name__ == "__main__":
	kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
	img = cv2.imread('2019.jpg')
	b,g,r = cv2.split(img)
	img = cv2.filter2D(img, -1, kernel)
	cv2.imwrite('0-merge.jpg', img)
	b = cv2.filter2D(b, -1, kernel)
	g = cv2.filter2D(g, -1, kernel)
	r = cv2.filter2D(r, -1, kernel)
	img = cv2.merge([b, g, r])
	cv2.imwrite('0-splite.jpg', img)

