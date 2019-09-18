import cv2

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QCheckBox
import numpy as np

class Thresh(QtWidgets.QWidget):
	def __init__(self, shower):
		super().__init__()
		self.initData(shower)
		self.thresh_min = 80
		self.thresh_max = 255
		self.thresh_type = 0	#0:只使用最小值，1：只使用最大值，2：同时使用
		self.chose_type_min = 1 #0:取上, 1:取下
		self.chose_type_max = 0 #0:取上, 1:取下
		self.is_splite = False #是否拆分使用阈值
		self.is_use_rgb_differ = False #是否使用rgb差异
		self._index = 2
		self.initUi()

	def initData(self, shower):
		self.shower = shower
		self.data = shower.data
		self.img_show = self.data.img_show

	def initUi(self):
		#min threshold
		self.label0 = QtWidgets.QLabel(self)
		self.label0.setGeometry(QtCore.QRect(10, 10, 85, 20))
		self.label0.setText('Min Threahold:')

		self.sld_min = QtWidgets.QSlider(Qt.Horizontal, self)
		self.sld_min.setGeometry(QtCore.QRect(105, 10, 200, 20))
		self.sld_min.setMinimum(0)
		self.sld_min.setMaximum(255)
		self.sld_min.setValue(self.thresh_min)
		self.sld_min.valueChanged.connect(self.minChange)

		self.text_min = QtWidgets.QLineEdit(self)
		self.text_min.setGeometry(QtCore.QRect(310, 10, 40, 20))
		self.text_min.setText(str(self.sld_min.value()))
		self.text_min.textChanged.connect(self.minChangeByText)

		#max threshold
		self.label1 = QtWidgets.QLabel(self)
		self.label1.setGeometry(QtCore.QRect(10, 40, 85, 20))
		self.label1.setText('Min Threahold:')

		self.sld_max = QtWidgets.QSlider(Qt.Horizontal, self)
		self.sld_max.setGeometry(QtCore.QRect(105, 40, 200, 20))
		self.sld_max.setMinimum(0)
		self.sld_max.setMaximum(255)
		self.sld_max.setValue(self.thresh_max)
		self.sld_max.valueChanged.connect(self.maxChange)

		self.text_max = QtWidgets.QLineEdit(self)
		self.text_max.setGeometry(QtCore.QRect(310,40, 40, 20))
		self.text_max.setText(str(self.sld_max.value()))
		self.text_max.textChanged.connect(self.maxChangeByText)

		#使用阈值类型
		#self.chk_min = QCheckBox('')
		self.label1 = QtWidgets.QLabel(self)
		self.label1.setGeometry(QtCore.QRect(10, 70, 65, 20))
		self.label1.setText('阈值类型:')

		self.btn_chk0 = QtWidgets.QRadioButton('使用小阈值', self)
		self.btn_chk0.move(90, 70)
		self.btn_chk0.setChecked(True)
		self.btn_chk1 = QtWidgets.QRadioButton('使用大阈值', self)
		self.btn_chk1.move(180, 70)
		self.btn_chk2 = QtWidgets.QRadioButton('同时使用', self)
		self.btn_chk2.move(270, 70)
		self.btn_grp0 = QtWidgets.QButtonGroup(self)
		self.btn_grp0.addButton(self.btn_chk0, 0)
		self.btn_grp0.addButton(self.btn_chk1, 1)
		self.btn_grp0.addButton(self.btn_chk2, 2)
		self.btn_grp0.buttonClicked.connect(self.threshTypeChange)

		#使用方式
		#min
		self.btn_chk3 = QtWidgets.QRadioButton('取上', self)
		self.btn_chk3.move(360, 12)
		self.btn_chk3.setChecked(True)
		self.btn_chk4 = QtWidgets.QRadioButton('取下', self)
		self.btn_chk4.move(410, 12)
		self.btn_grp1 = QtWidgets.QButtonGroup(self)
		self.btn_grp1.addButton(self.btn_chk3, 0)
		self.btn_grp1.addButton(self.btn_chk4, 1)
		self.btn_grp1.buttonClicked.connect(self.threshMinChoseTypeChange)
		#max
		self.btn_chk5 = QtWidgets.QRadioButton('取上', self)
		self.btn_chk5.move(360, 42)
		self.btn_chk6 = QtWidgets.QRadioButton('取下', self)
		self.btn_chk6.move(410, 42)
		self.btn_chk5.setChecked(False)
		self.btn_grp2 = QtWidgets.QButtonGroup(self)
		self.btn_grp2.addButton(self.btn_chk5, 0)
		self.btn_grp2.addButton(self.btn_chk6, 1)
		self.btn_chk5.setVisible(False)
		self.btn_chk6.setVisible(False)
		self.btn_grp2.buttonClicked.connect(self.threshMaxChoseTypeChange)

		#拆分使用
		self.label2 = QtWidgets.QLabel(self)
		self.label2.move(480, 12)
		self.label2.setText('拆分使用阈值:')
		self.btn_chk7 = QtWidgets.QRadioButton('', self)
		self.btn_chk7.move(570, 12)
		'''self.btn_grp3 = QtWidgets.QButtonGroup(self)
		self.btn_grp3.addButton(self.btn_chk7, 0)
		self.btn_grp3.buttonClicked.connect(self.spliteUseChange)'''
		self.btn_chk7.clicked.connect(self.spliteUseChange)

		#使用rgb差异
		self.label3 = QtWidgets.QLabel(self)
		self.label3.move(480, 42)
		self.label3.setText('参考rgb差异:')
		self.btn_chk8 = QtWidgets.QCheckBox('', self)
		self.btn_chk8.move(570, 42)
		self.btn_chk8.clicked.connect(self.rgbDifferUseChange)

		self.btn0 = QtWidgets.QPushButton('运行', self)
		self.btn0.move(620,10)
		self.btn0.clicked.connect(self.processImgByThresh)

	def minChange(self):
		self.thresh_min = self.sld_min.value()
		self.text_min.setText(str(self.thresh_min))
		#self.processImgByThresh()

	def minChangeByText(self):
		self.sld_min.setValue(int(self.text_min.text()))
		self.thresh_min = self.sld_min.value()

	def maxChange(self):
		self.thresh_max = self.sld_max.value()
		self.text_max.setText(str(self.thresh_max))

	def maxChangeByText(self):
		self.sld_max.setValue(int(self.text_max.text()))
		self.thresh_max = self.sld_max.value()

	def threshTypeChange(self):
		self.thresh_type = self.btn_grp0.checkedId()
		print(self.thresh_type)
		if 0 == self.thresh_type:
			self.btn_chk3.setVisible(True)
			self.btn_chk4.setVisible(True)
			self.btn_chk5.setVisible(False)
			self.btn_chk6.setVisible(False)
		elif 1 == self.thresh_type:
			self.btn_chk3.setVisible(False)
			self.btn_chk4.setVisible(False)
			self.btn_chk5.setVisible(True)
			self.btn_chk6.setVisible(True)
		else:
			self.btn_chk3.setVisible(True)
			self.btn_chk4.setVisible(True)
			self.btn_chk5.setVisible(True)
			self.btn_chk6.setVisible(True)

	def threshMinChoseTypeChange(self):
		self.chose_type_min = self.btn_grp1.checkedId()

	def threshMaxChoseTypeChange(self):
		self.chose_type_max = self.btn_grp1.checkedId()

	def spliteUseChange(self):
		print('spliteUseChange:',self.is_splite)
		self.is_splite = not self.is_splite
		self.btn_chk7.setChecked(self.is_splite)

	def rgbDifferUseChange(self):
		self.is_use_rgb_differ = not self.is_use_rgb_differ
		self.btn_chk8.setChecked(self.is_use_rgb_differ)

	def processImgByThresh(self):
		self.recover()
		img = self.data.img_show.copy()
		img_binary = self.data.img_binary.copy()
		'''img_r = self.data.img_r.copy()
		img_g = self.data.img_g.copy()
		img_b = self.data.img_b.copy()'''
		img_b, img_g, img_r = cv2.split(img)
		avg = cv2.mean(img)
		thresh_min = min(avg[:2])

		get_max = lambda x : self.thresh_max if x > self.thresh_min else x
		get_min = lambda x: self.thresh_max if x > self.thresh_min else x


		'''
		print('平均像素值：', avg, thresh_min)
		if 0 == self.thresh_type or 2 == self.thresh_type:
			# 使用最小值
			if 0 == self.chose_type_min:
				#取上
				pass
		
		print(self.thresh_type)
		for row in range (5):
			for col in range (5):
				print(img[row][col],img_r[row][col],img_g[row][col],img_b[row][col])

		thresh, img_r = cv2.threshold(img_r, self.thresh_min, 255, cv2.THRESH_BINARY)# | cv2.THRESH_TRUNC)
		thresh, img_g = cv2.threshold(img_g, self.thresh_min, 255, cv2.THRESH_BINARY)# | cv2.THRESH_TRUNC)
		thresh, img_b = cv2.threshold(img_b, self.thresh_min, 255, cv2.THRESH_BINARY)# | cv2.THRESH_TRUNC)
		#self.data.img_show = cv2.merge([img_r, img_g, img_b])
		#self.shower.showProcessedImg(True)
		print(self.data.height, self.data.width)
		print('type:', type(img_binary))'''
		'''img_b, img_g, img_r = cv2.split(img)
		img_gray = cv2.cvtColor(self.data.img_show, cv2.COLOR_BGR2GRAY)
		#img_binary = cv2.equalizeHist(img_gray)
		img_b = cv2.equalizeHist(img_b)
		img_g = cv2.equalizeHist(img_g)
		img_r = cv2.equalizeHist(img_r)
		img_binary = cv2.merge((img_b, img_g, img_r))
		self.data.img_show = img_binary
		self.shower.showProcessedImg()
		return
		'''
		if self.is_splite:
			for row in range (self.data.height):
				for col in range (self.data.width):
					value = img[row][col]
					min_value = min(value)
					max_value = max(value)
					if 0 == self.thresh_type or 2 == self.thresh_type:
						# 使用最小值
						if min_value > self.thresh_min or (self.is_use_rgb_differ and min_value + 50 < max_value):
							img_binary[row][col] = self.thresh_max

						'''
						if 0 == self.chose_type_min:
							for i in range(3):
								if value[i] > self.thresh_min:
									img_binary[row][col] = self.thresh_max
									pass
						else:
							for i in range(3):
								if img[row][col][i] > self.thresh_min:
									img[row][col][i] = self.thresh_min
						'''

					elif 1 == self.thresh_type or 2 == self.thresh_type:
						if 0 == self.chose_type_min or 2 == self.chose_type:
							pass
		else:
			print('不拆分')
			img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			thresh, img_binary = cv2.threshold(img_gray, self.thresh_min, 255, cv2.THRESH_BINARY)
			img_differ = self.getDiffer(self.data.img_rgb)
			size = len(img_differ)
			img_differ = np.array(img_differ)
			print('size:',img_differ.shape)
			print(img_differ)
			if self.is_use_rgb_differ:
				for i in range(self.data.height):
					for j in range(self.data.width):
						#if img_differ[i][j] > 50:
						if 0 == img_binary[i][j] and img_differ[i][j] > 50:#rgb最大差异
							img_binary[i][j] = 255


		self.data.img_binary = img_binary
		self.data.img_show = img_binary.copy()
		self.shower.showProcessedImg(True)

	def recover(self):
		if self.data.cur_index == self._index:
			#还原
			self.data.img_show = self.img_show.copy()
		else:
			self.data.cur_index = self._index
			self.img_show = self.data.img_show.copy()

	def getDiffer(self, img):
		img_b, img_g, img_r = cv2.split(img)
		list_differ0 = list(np.array(img_b) - np.array(img_g))
		list_differ0 = list(map(abs, list_differ0))
		list_differ1 = list(np.array(img_b) - np.array(img_r))
		list_differ1 = list(map(abs, list_differ1))
		list_differ2 = list(np.array(img_g) - np.array(img_r))
		list_differ2 = list(map(abs, list_differ1))
		list_differ = list(np.array(list_differ0) + np.array(list_differ1) + np.array(list_differ2))
		list_differ = list((np.array(list_differ)/3).astype(int))
		return list_differ

if __name__ == '__main__':
	l1 = [1,2,3]
	l2 = [3,4,1]
	l3 = list(np.array(l1)-np.array(l2))
	print(l3)
	print(list(abs(np.array(l3))))
	l4 = map(abs, l3)
	l4 = list(l4)
	print(l4)
	l4 = list(np.array(l4)/3)
	print(l4)
	print(list(np.array(l4).astype(int)))
	L = [[1,1,1],[2,2,2],[3,3,3],[4,4,4]]
	L = np.array(L)
	print(L.shape)

	arr1 = np.array(l1)
	arr2 = np.array(l2)
	print(arr1,arr2)
	arr3 = np.where(arr1 < arr2, arr2, arr1)

	print(arr3)