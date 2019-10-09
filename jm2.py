# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'jm2.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import sys
import os
import fix_qt_import_error
from PyQt5.QtWidgets import QApplication

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QPushButton
from PyQt5.QtGui import QPixmap
import photoShower
from photoShower import PhotoShower
from grayParams import GrayParams
from openClose import OpenClose
from thresh import Thresh
from filter import Filter
from beautify import Beautify
from saver import Saver
from outMsg import OutMsg
import cv2

class Ui_Form(QWidget):
    def setupUi(self):
        self.setObjectName("Form")
        self.resize(1600, 1000)
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(20, 20, 1151, 131))
        self.tabWidget.setObjectName("tabWidget")

        self.img = '003.jpg'
        self.path = './'
        self.photo_shower = PhotoShower()
        # self.photo_shower.data.read(self.img)
        # self.photo_shower.show(0)
        # self.photo_shower.resize(1024, 768)

        self.tab_splite = GrayParams(self.photo_shower)#QtWidgets.QWidget()
        self.tab_splite.setObjectName("tab_splite")
        self.tab_splite.qbt0.clicked.connect(self.changeColorImg)
        self.tab_splite.qbt1.clicked.connect(self.changeColorImg)
        self.tabWidget.addTab(self.tab_splite, "拆分")


        self.tab_open_close = OpenClose(self.photo_shower)#QtWidgets.QWidget()
        self.tab_open_close.setObjectName("tab_open_close")
        #self.tab_open_close.sld_ksize.valueChanged.connect(self.photo_shower.showProcessedImg)
        self.tabWidget.addTab(self.tab_open_close, "开闭")

        self.tab_thresh = Thresh(self.photo_shower)
        self.tab_thresh.setObjectName('tab_thresh')
        self.tabWidget.addTab(self.tab_thresh, "Threshold")

        self.tab_filter = Filter(self.photo_shower)
        self.tab_filter.setObjectName('filter')
        self.tabWidget.addTab(self.tab_filter, '过滤')
        self.photo_shower.cur_index = 3
        #self.tabWidget.setCurrentIndex(3)

        self.tab_beautify = Beautify(self.photo_shower)
        self.tab_beautify.setObjectName('beautify')
        self.tabWidget.addTab(self.tab_beautify, '美化')
        #self.tabWidget.setCurrentIndex(4)

        self.tab_saver = Saver(self.photo_shower)
        self.tab_saver.setObjectName('saver')
        self.tabWidget.addTab(self.tab_saver, '保存')
        self.tabWidget.setCurrentIndex(4)

        self.horizontalLayoutWidget = QtWidgets.QWidget(self)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 160, 1151, 811))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 5, 0, 10)#左，顶，右，底边距

        self.horizontalLayout.addWidget(self.photo_shower)
        self.horizontalLayout.setObjectName("horizontalLayout")

        #self.vlayout
        self.img_index = 0#0-3:gray,rgb
        self.is_gray = False

        self.vlayout_widget = QtWidgets.QWidget(self)
        self.vlayout_widget.setGeometry(QtCore.QRect(1100, 0, 351, 900))
        self.vlayout_widget.setObjectName("verticalLayoutWidget")
        # self.vlayout.addStretch(0)

        self.groupBox = QtWidgets.QGroupBox(self.vlayout_widget)
        self.groupBox.resize(420, 720)
        self.groupBox.setTitle("123")
        self.groupBox.setObjectName("groupBox")

        self.qbt0 = QtWidgets.QPushButton(self.groupBox)
        self.qbt0.setGeometry(QtCore.QRect(10, 20, 150, 30))
        self.qbt0.setText('一键处理')
        #self.qbt0 = QPushButton('原始图像-->灰度图像')
        self.qbt0.clicked.connect(self.processImg)
        #self.qbt0.move(0, 0)

        self.qbt1 = QtWidgets.QPushButton(self.groupBox)
        self.qbt1.setGeometry(QtCore.QRect(10, 60, 150, 30))
        self.qbt1.setText('批量处理')
        self.qbt1.clicked.connect(self.processImgsTogether)

        self.qbt2 = QtWidgets.QPushButton(self.groupBox)
        self.qbt2.setGeometry(QtCore.QRect(190, 20, 150, 30))
        self.qbt2.setText('转换图像')
        self.is_process = True
        self.qbt2.clicked.connect(self.restore)

        self.qbt3 = QtWidgets.QPushButton(self.groupBox)
        self.qbt3.setGeometry(QtCore.QRect(190, 60, 150, 30))
        self.qbt3.setText('保存')
        self.qbt3.clicked.connect(self.saveImg)


        #切换图像
        self.label0 = QtWidgets.QLabel(self.groupBox)
        self.label0.setGeometry(QtCore.QRect(10, 100, 60, 20))
        self.label0.setText('当前图像:')

        self.text_img = QtWidgets.QLineEdit(self.groupBox)
        self.text_img.setGeometry(QtCore.QRect(70, 100, 210, 20))
        self.text_img.setText(self.img)

        self.qbt4 = QtWidgets.QPushButton(self.groupBox)
        self.qbt4.setGeometry(QtCore.QRect(290, 99, 50, 22))
        self.qbt4.setText('...')
        self.qbt4.clicked.connect(self.changeImg)



        self.slider = QtWidgets.QSlider(Qt.Horizontal, self.groupBox)
        self.slider.setGeometry(QtCore.QRect(40, 140, 200, 20))
        self.slider.setMinimum(0)
        self.slider.setMaximum(200)
        self.slider.setValue(100)
        self.slider.valueChanged.connect(self.sliderChange)


        self.label1 = QtWidgets.QLabel(self.groupBox)
        self.label1.setGeometry(QtCore.QRect(10, 140, 40, 20))
        self.label1.setText('比例:')

        self.text = QtWidgets.QLineEdit(self.groupBox)
        self.text.setGeometry(QtCore.QRect(270, 140, 40, 20))
        self.text.setText(str(self.slider.value()))
        self.text.textChanged.connect(self.kChange)

        #输出
        self.edit_msg = QtWidgets.QTextEdit(self.groupBox)
        self.edit_msg.resize(330, 420)
        self.edit_msg.move(10, 170)
        self.msg = OutMsg(self.edit_msg)
        self.qbt5 = QPushButton('清理', self.groupBox)
        self.qbt5.setGeometry(QtCore.QRect(280, 595, 60, 20))
        self.qbt5.clicked.connect(self.msg.clear)
        self.tab_filter.addOuter(self.msg)

        self.vlayout = QtWidgets.QVBoxLayout(self.vlayout_widget)#groupBox)
        self.vlayout.setContentsMargins(0, 200, 0, 10)  # 左，顶，右，底边距

        #self.vlayout.addWidget(self.qbt0)
        #self.vlayout.addWidget(self.qbt1)
        self.groupBox.setFixedWidth(350)
        self.groupBox.setFixedHeight(620)
        self.vlayout.addWidget(self.groupBox)

        #self.vlayout.addWidget(self.groupBox)
        self.vlayout.addStretch()

        self.horizontalLayout.addLayout(self.vlayout)

        #self.retranslateUi(Form)
        #QtCore.QMetaObject.connectSlotsByName(Form)
        self.show()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Tab 2"))

    def changeColorImg(self):
        index = 0
        if not self.tab_splite.is_rgb:
            if not self.tab_splite.is_color:
                index = 4
        else:
            index = self.tab_splite.img_index + 1
        self.photo_shower.show(index)

    def changeRawGray(self):
        self.is_gray = not self.is_gray
        if self.is_gray:
            self.photo_shower.show(4)
            self.qbt0.setText('灰度图像-->彩色图像')
        else:
            self.photo_shower.show(0)
            self.qbt0.setText('彩色图像-->灰度图像')

    def processImgsTogether(self):
        if not os.path.exists('image.txt'):
            print("找不到待处理图片文件！")
        f = open('image.txt','r')
        for line in f.readlines():
            img_name = line.replace('\n','')
            if self.photo_shower.data.read(img_name):
                self.tab_open_close.initData(self.photo_shower)
                self.tab_thresh.initData(self.photo_shower)
                self.tab_filter.initData(self.photo_shower)
                self.processImg()
                pos = img_name.rfind('.')
                img_color_name = img_name[:pos] + '_color.jpg'
                img_black_name = img_name[:pos] + '_black.jpg'
                print(img_color_name,'\n', img_black_name)
                width = self.photo_shower.data.raw_width
                height = self.photo_shower.data.raw_height
                img_color = cv2.resize(self.photo_shower.data.img_show, (width, height))
                img_color = cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB)
                cv2.imwrite(img_color_name, img_color)
                img_black = cv2.resize(self.photo_shower.data.img_binary, (width, height))
                cv2.imwrite(img_black_name, img_black)
                print('读取成功!')
            else:
                print('读取失败!')

        #self.processImg()
        # color_list = ['灰', '红', '绿', '蓝']
        # self.img_index = (self.img_index + 1) % 4
        # if 0 == self.img_index:
        #     self.photo_shower.show(4)
        # else:
        #     self.photo_shower.show(self.img_index)
        # self.qbt1.setText('图像切换:' + color_list[self.img_index] + '-->' + color_list[(self.img_index + 1) % 4])

    def restore(self):
        if self.is_process:
            self.qbt2.setText('原始图像')
            self.photo_shower.show(5)
        else:
            self.qbt2.setText('处理后图像')
            self.photo_shower.showProcessedImg()
        self.is_process = not self.is_process

    def sliderChange(self):
        self.text.setText(str(self.slider.value()))

    def kChange(self):
        self.slider.setValue(int(self.text.text()))
        pass

    def changeImg(self):
        self.img, chose = QtWidgets.QFileDialog.getOpenFileName(self,
                                                    "选择图像", self.path,
                                                    "ALL(*);;JPG (*.jpg);;PNG (*.png);;BMP(*.bmp)")
        #self.path = ''
        #print(self.img)
        if self.photo_shower.data.read(self.img):
            self.photo_shower.show(0)
            self.text_img.setText(self.img)
            self.tab_splite.initData(self.photo_shower)
            self.tab_open_close.initData(self.photo_shower)
            self.tab_thresh.initData(self.photo_shower)
            self.tab_filter.initData(self.photo_shower)
            pos = self.img.rfind('/')
            if pos > 0:
                self.path = self.img[:pos]
            else:
                pos = self.img.rfind('\\')
                if pos > 0:
                    self.path = self.img[:pos]
            print('读取成功!')
        else:
            print('读取失败!')

    def saveImg(self):
        data = self.photo_shower.data
        img_name = data.img_name
        pos = img_name.rfind('.')
        if pos > 0:
            img_type = img_name[pos:len(img_name)]
            img_type = '.jpg'
            img_name = img_name[:pos] + '_after' + img_type
            #img_name = img_name[:pos] + img_type
            print(data.raw_width, data.raw_height)
            img = cv2.resize(data.img_show, (data.raw_width, data.raw_height))
            cv2.imwrite(img_name, img)

    def processImg(self):
        self.tab_splite.changeImg(1)#(self.tab_splite.cur_index)
        self.tab_open_close.processImg()
        self.tab_thresh.processImgByThresh()
        self.tab_filter.filterSize()
        self.tab_filter.fufillImg()
        self.tab_filter.rectangulazie()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Ui_Form()
    ui.setupUi()
    #MainWindow.show()
    sys.exit(app.exec_())