import cv2

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QCheckBox
import numpy as np

class Filter(QtWidgets.QWidget):
	def __init__(self, shower):
		super().__init__()
		self.initData(shower)
		self.filter_size = 15
		self.fufill_size = 9
		self._index = 3
		self.process_index = 0
		self.rect_thresh_min = 5
		self.rect_thresh_max = 30
		self.is_rect_use_percent = False
		# self.list_test_imgs = ['ct10.jpg']#['001_after.jpg', '002_after.jpg', '2_after.jpg', '003_after.jpg', '3_after.jpg']
		self.list_test_imgs = []
		if False:
			self.list_test_imgs = ['3_after.jpg']
		else:
			for i in range(13):
				self.list_test_imgs.append('ct'+str(i)+'.jpg')
		self.test_index = 0
		self.cur_contour_index = 0 #当前轮廓
		self.contours = []
		self.kernel = np.array([[0, -1, 0],[-1, 5, -1], [0, -1, 0]])
		self.initUi()

	def initData(self, shower):
		self.shower = shower
		self.data = shower.data
		if self.data.check():
			self.img_binary = self.data.img_binary.copy()
			self.img_binary_raw = self.data.img_binary.copy()
			self.img_binary_cur = self.data.img_binary.copy()

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
		self.btn2.setGeometry(QtCore.QRect(20, 70, 90, 30))
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
		self.btn2.setGeometry(QtCore.QRect(860, 40, 80, 20))
		self.btn2.clicked.connect(self.rectangulazie)

		self.label3 = QtWidgets.QLabel(self)
		self.label3.move(860, 12)
		self.label3.setText('使用百分比')
		self.btn_chk0 = QtWidgets.QRadioButton('', self)
		self.btn_chk0.move(920, 12)
		self.btn_chk0.setChecked(self.is_rect_use_percent)
		self.btn_chk0.clicked.connect(self.rectUsePercentChange)

		self.btn4 = QtWidgets.QPushButton('切割', self)
		self.btn4.setGeometry(QtCore.QRect(955, 10, 80, 20))
		self.btn4.clicked.connect(self.cutContour)

		self.btn5 = QtWidgets.QPushButton('填充', self)
		self.btn5.setGeometry(QtCore.QRect(955, 40, 80, 20))
		self.btn5.clicked.connect(self.fufillContour)

		self.btn3 = QtWidgets.QPushButton('导入测试', self)
		self.btn3.setGeometry(QtCore.QRect(150, 70, 90, 30))
		self.btn3.clicked.connect(self.importTestImg)

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
		self.img_binary = img
		self.shower.showProcessedImg(True)

	def rectangulazie(self):
		self.recover(2)
		self.process_index = 2
		img = self.data.img_binary
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
		for i in range(len(contours)):
			self.cur_contour_index = i
			self.rectangulazieContour(contours[i])
		#self.rectangulazieContour(contours[1])
		print('轮廓1：',contours[1])
		ct = cv2.boundingRect(contours[0])
		#print(ct)

		#img = cv2.drawContours(img, contours, -1, (60, 35, 155), 1)
		print(self.count)
		self.shower.showProcessedImg()
		pass

	def cutContour(self):
		#切割当前轮廓
		if 3 != self.process_index:
			self.img_binary_raw = self.img_binary_cur.copy()
		self.process_index = 3

		if 0 == len(self.contours):
			self.contours, hieracy = cv2.findContours(self.img_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		contours = self.contours.copy()
		#contours[self.cur_contour_index] = []
		self.data.img_binary = self.img_binary_raw.copy()

		if 0 == self.cur_contour_index:
			self.cur_contour_index = (self.cur_contour_index + 1) % len(contours)
			return

		img = self.data.img_binary
		for i in range(1, len(contours)):
			if i != self.cur_contour_index:
				cv2.fillPoly(img, [contours[i]], (255,0,0))

		ct = cv2.boundingRect(contours[self.cur_contour_index])
		x, y, w, h = ct
		#cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
		#cv2.putText(img, str(self.cur_contour_index), (x + int(w/2), y + int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0),2)

		self.shower.showProcessedImg(True)
		self.data.img_show = self.data.img_binary
		self.data.img_name = 'ct' + str(self.cur_contour_index)+'.jpg'
		self.img_binary_cur = img.copy()
		self.cur_contour_index = (self.cur_contour_index + 1) % len(contours)

	def fufillContour(self):
		contour_index = (self.cur_contour_index + len(self.contours) - 1) % len(self.contours)
		img = self.img_binary_cur.copy()
		ct = cv2.boundingRect(self.contours[contour_index])
		x, y, w, h = ct
		start = self.getStartPoint(ct, img)
		print('包围：', x, y, w, h)
		print('起始点:', start)
		dir, max = self.getDirection(start, img)
		cur_row = start[1]
		cur_col = start[0]

		rect_list = self.rectWall(ct, (cur_row, cur_col, dir, max), img)
		self.data.img_show = self.data.img_binary.copy()
		print('包围矩形：', rect_list)
		for rect in rect_list:
			# if 1 != dir and 2 != dir:
			# 	break
			min_x, min_y, max_x, max_y = rect
			cv2.rectangle(self.data.img_binary, (min_x, min_y), (max_x, max_y), (150, 50, 70), 3)

		self.shower.showProcessedImg(True)

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

	def rectWall(self, contour, point, img):
		cur_row, cur_col, dir, max = point
		x, y, w, h = contour
		min_x = x + w
		max_x = x
		min_y = y + h
		max_y = y
		rect_list = []

		if 2 == dir or max < self.rect_thresh_min:
			#方向待定
			print('方向待定:', max)
			if max > self.rect_thresh_max:
				#夹角
				pass
		elif 1 == dir:
			#竖向墙
			width = 0
			min_x = x + w
			max_x = x
			min_y = y + h
			max_y = y
			for row in range(cur_row, y+h):
				if img[row][cur_col] > 0:
					width = 0
					get_left = 0#0:未找到第一个，1：已开始统计
					get_right = 0
					for i in range(1, self.rect_thresh_max):
						#print(row, cur_col, i, img[row][cur_col - i], img[row][cur_col + i])
						if 2 != get_left:
							if cur_col - i >= 0 and img[row][cur_col - i] == 0:
								if cur_col - i < min_x:
									# print('min_x赋值1：', cur_col - i)
									min_x = cur_col - i
								width += 1
								if 0 == get_left:
									get_left = 1
							elif 1 == get_left and img[row][cur_col - i] > 0:
								print('左边到头了1', row, cur_col - i, img[row][cur_col - i])
								get_left = 2

						if 2 != get_right:
							if cur_col+i < x+w and img[row][cur_col + i] == 0:
								if cur_col + i > max_x:
									#print('max_x赋值1：', cur_col + i)
									max_x = cur_col + i
								width += 1
								if 0 == get_right:
									get_right = 1
							elif 1 == get_right and img[row][cur_col + i] > 0:
								print('右边到头了1', row, cur_col + i, i, img[row][cur_col + i])
								get_right = 2

					if width == 0:
						#到头了
						max_y = row
						print('到头了：', max_y)
						break
					elif width > self.rect_thresh_max:
						#转角
						pass
					else:
						pass
				else:
					get_left = 0
					get_right = 0
					for i in range(0, self.rect_thresh_max):
						if 2 != get_left:
							if cur_col - i >= 0 and img[row][cur_col - i] == 0:
								if cur_col - i < min_x:
									# print('min_x赋值2：', cur_col - i)
									min_x = cur_col - i
								if 0 == get_left:
									get_left = 1
							elif 1 == get_left and img[row][cur_col - i] > 0:
								print('左边到头了', row, cur_col - i, img[row][cur_col - i])
								get_left = 2

						if 2 != get_right:
							if cur_col+i < x+w and img[row][cur_col + i] == 0:
								if cur_col + i > max_x:
									#print('max_x赋值2：', cur_col + i)
									max_x = cur_col + i
								if 0 == get_right:
									get_right = 1
							elif 1 == get_right and img[row][cur_col + i] > 0:
								print('右边到头了', row, cur_col + i, img[row][cur_col + i])
								get_right = 2


						'''if get_right and cur_col+i < x+w and img[row][cur_col + i] == 0:
							if cur_col + i > max_x:
								# print('max_x赋值2：', cur_col + i)
								max_x = cur_col + i
						else:
							get_right = False'''

					if row < min_y:
						min_y = row
					if row > max_y:
						max_y = row
			print('包围：', x, y, w, h)
			print('竖向墙：', min_x, max_x, min_y, max_y)

			#self.data.img_show = self.data.img_binary.copy()
			#cv2.rectangle(self.data.img_binary, (min_x, min_y), (max_x, max_y), (150, 50, 70), 1)

			self.shower.showProcessedImg(True)
		else:
			#横向墙
			height = 0
			min_x = x + w
			max_x = x
			min_y = y + h
			max_y = y
			for col in range(cur_col, x + w):
				if img[cur_row][col] > 0:
					width = 0
					get_top = 0  # 0:未找到第一个，1：已开始统计
					get_bottom = 0
					for i in range(1, self.rect_thresh_max):
						# print(row, cur_col, i, img[row][cur_col - i], img[row][cur_col + i])
						if 2 != get_top:
							if cur_row - i >= 0 and img[cur_row - i][col] == 0:
								if cur_row - i < min_y:
									# print('min_x赋值1：', cur_col - i)
									min_y = cur_row - i
								height += 1
								if 0 == get_top:
									get_top = 1
							elif 1 == get_top and img[cur_row - i][col] > 0:
								print('上边到头了1', cur_row - i, col, img[cur_row - i][col])
								get_top = 2

						if 2 != get_bottom:
							if cur_row + i < y + h and img[cur_row + i][col] == 0:
								if cur_row + i > max_y:
									# print('max_y赋值1：', cur_col + i)
									max_y = cur_row + i
								height += 1
								if 0 == get_bottom:
									get_bottom = 1
							elif 1 == get_bottom and img[cur_row + i][col] > 0:
								print('下边到头了1', cur_row + i, col, i, img[cur_row + i][col])
								get_bottom = 2

					if height == 0:
						# 到头了
						max_x = col
						print('向右到头了：', max_x)
						break
					elif height > self.rect_thresh_max:
						# 转角
						pass
					else:
						pass
				else:
					get_top = 0
					get_bottom = 0
					for i in range(0, self.rect_thresh_max):
						if 2 != get_top:
							if cur_row - i >= 0 and img[cur_row - i][col] == 0:
								if cur_row - i < min_y:
									# print('min_y赋值2：', cur_row - i)
									min_y = cur_row - i
								if 0 == get_top:
									get_top = 1
							elif 1 == get_top and img[cur_row - i][col] > 0:
								print('上边到头了', cur_row - i, col, img[cur_row - i][col])
								get_top = 2

						if 2 != get_bottom:
							if cur_row + i < y + h and img[cur_row + i][col] == 0:
								if cur_row + i > max_y:
									# print('max_y赋值2：', cur_col + i)
									max_y = cur_row + i
								if 0 == get_bottom:
									get_bottom = 1
							elif 1 == get_bottom and img[cur_row + i][col] > 0:
								print('下边到头了2', cur_row + i, col, i, img[cur_row + i][col])
								get_bottom = 2


					if col < min_x:
						min_x = col
					if col > max_x:
						max_x = col
			print('包围：', x, y, w, h)
			print('横向墙：', min_x, max_x, min_y, max_y)

		rect_list.append([min_x, min_y, max_x, max_y])
		return rect_list

	def getOneWall(self, contour, point, img):
		cur_row, cur_col, dir, max = point
		x, y, w, h = contour
		min_x = x + w
		max_x = x
		min_y = y + h
		max_y = y
		wall = []

		return wall

	def getDirection(self, point, img):
		#获取当前点所在墙的方向
		thresh_min = self.rect_thresh_min
		thresn_max = self.rect_thresh_max
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

	def rectangulazieContour(self, contour):
		img = self.data.img_binary
		ct = cv2.boundingRect(contour)
		#print(ct)
		x, y, w, h = ct
		if (w + 5 > self.data.width and h + 5 > self.data.height or
				(max([w, h]) < 20)):
			return

		self.count += 1
		start = self.getStartPoint(ct, self.data.img_binary)
		#print(contour)
		print(start)
		cv2.circle(self.data.img_show, start, 5, (0,0,255), -1)
		cv2.putText(self.data.img_show, str(self.cur_contour_index), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

	def getStartPoint(self, list_contour, img):
		x, y, w, h = list_contour
		#print(list_contour)
		start = (x, y)
		print('上')
		for col in range(x, x + w):
			#print(self.data.img_binary[y][col])
			if img[y][col] == 0:
				return ((col, y))
		print('左')
		for row in range(y, y + h):
			#print(self.data.img_binary[row][x])
			if img[row][x] == 0:
				return ((x, row))
		print('右')
		for row in range(y, y + h):
			#print(self.data.img_binary[row][x])
			if img[row][x + w - 1] == 0:
				return ((x + w - 1, row))
		print('下')
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

	def importTestImg(self):
		self.test_index = (self.test_index + 1) % (len(self.list_test_imgs))
		self.data.read(self.list_test_imgs[self.test_index])
		self.data.img_binary = self.data.img_show
		if 3 == len(self.data.img_binary.shape):
			print('3通道')
			thresh, self.data.img_binary = cv2.threshold(self.data.img_gray, 10, 255, cv2.THRESH_BINARY)
		self.img_binary = self.data.img_binary.copy()
		self.img_binary_raw = self.img_binary.copy()
		self.img_binary_cur = self.img_binary.copy()
		self.contours, hieracy = cv2.findContours(self.img_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		self.shower.showProcessedImg(True)
		pass


