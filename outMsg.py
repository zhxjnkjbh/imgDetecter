# -*- coding: utf-8 -*-
import cv2

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTextEdit, QPushButton

class OutMsg():
	def __init__(self, text):
		#super().__init__(parent)
		self.msg = 'logs：'
		self.initData(text)


	def initData(self, text):
		self.text = text
		self.text.setText(self.msg)


	def update(self, msg):
		self.msg += msg
		self.text.setText(self.msg)

	def write(self, msg):
		self.msg += msg
		#self.text.setText(self.msg)
		#self.text.append(msg)#所有的间隔都会导致换行
		self.text.insertPlainText(msg)
		self.text.verticalScrollBar().setValue(self.text.verticalScrollBar().maximum())
		#self.moveCursor(QTextCursor.End)

	def clear(self):
		self.msg = ''
		self.text.setText('')

	def flush(self):
		pass

