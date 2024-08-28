import os
import subprocess
from subprocess import Popen
import sys
from winreg import *
from RegFunctions import *

#---Ignores OLE Exception error (win11)---#
import warnings
warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2
#-----------------------------------------#

from PyQt5.Qt import Qt
from PyQt5 import QtCore
from PyQt5.QtCore import QPoint, QTimer
from PyQt5.QtWidgets import QLabel, QToolButton,QToolBar,QLineEdit,QPushButton,QWidget,QApplication,QTableWidget,QTableWidgetItem, QAbstractItemView, QVBoxLayout,QHBoxLayout, QWidget,QHeaderView

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        self.setWindowTitle("Command Control")
        
        
        self.txt = QLineEdit(self)
        self.txt.setGeometry(5,5,300,40)
        font = self.txt.font()      # lineedit current font
        font.setPointSize(22)       # change it's size
        self.txt.setFont(font) 

        def cmdstart():
            cmd = subprocess.Popen('start ' + self.txt.text(), shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(cmd)
            self.txt.clear()

        self.txt.returnPressed.connect(cmdstart)

    def SettingsDisplay(self, checked):
        self.w = SettingsWindow()
        self.w.show


#----Key Commands---------------------#

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        if event.key() == Qt.Key_F4:
            MainWindow.SettingsDisplay(self,checked=None)

#----Borderless drag functionality----#

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

#-----------------------------------------#

class SettingsWindow(QWidget):

    def __init__(self):
        
        super().__init__()
        self.title = 'Tag Settings'
        self.left = 250
        self.top = 100
        self.width = 800
        self.height = 400

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createTable()

        def RemTag():
            self.Tag = self.tableWidget.item(self.tableWidget.currentRow(), 0)
            
            print(self.Tag.text())

            self.r = DelConf(self.Tag, self)
            self.r.show()

        self.toolBar = QToolBar()                           

        self.toolButton = QToolButton()                     
        self.toolButton.clicked.connect(RemTag)
        self.toolButton.setText("Delete Tag")              
        self.toolButton.setCheckable(False)                 
        self.toolButton.setAutoExclusive(True)              
        self.toolBar.addWidget(self.toolButton)             
        # Add buttons to toolbar

        # if self.toolButton.clicked:
        #     pass
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.toolBar)
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        def AmendTag():

            self.TagName = self.tableWidget.item(self.tableWidget.currentRow(), 0)
            self.TagPath = self.tableWidget.item(self.tableWidget.currentRow(), 1) 
        # ------------- Pass Current Instance to next Window ▼ otherwise you will have no control over updating it
            self.w = TagAmend(self.TagName.text(),self.TagPath.text(),self)
            self.w.show()
            
        #TableConnections  
        self.tableWidget.doubleClicked.connect(AmendTag)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  
        #Show window

        self.show()
        
     #Create table
    def createTable(self):
       
        self.tableWidget = QTableWidget()
        
        #Row count
        
        self.tableWidget.setRowCount(len(combine_key2path()))
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        #Column count
        self.tableWidget.setColumnCount(2)
        
        #Header Labels & Visibility  
        self.tableWidget.setHorizontalHeaderLabels(['Tag','Path'])
  
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(True)
        
        col1 = 0
        col2 = 1
               
        #iteration counter
        count = 0
        
        for key, value in combine_key2path().items():
           
           self.tableWidget.setItem(count,col1, QTableWidgetItem(key))
           self.tableWidget.setItem(count,col2, QTableWidgetItem(value))
           count = count +1
           print(count,col1,col2,key,value,)
           
        #Table will fit the screen horizontally
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

class DelConf(QWidget):

    def __init__(self, TagName, Settingtbl):
        super().__init__()
           
        # print (TagName.text())

        self.layout1 = QVBoxLayout()
        self.Settingtbl = Settingtbl
        self.setWindowTitle("Delete Confirmation")
        
        self.label = QLabel("Are you sure you wish to delete?")
        self.bt_Del =QPushButton("Delete")
        self.bt_Cancel =QPushButton("Cancel")
        
        # NOTE: Update functioning correctly however not refreshing in place
               
        def update():
            self.close()
            print(TagName.text())
            DelRunTag(TagName.text()[:-4])
            Settingtbl.close()
            SettingsWindow()
        
        def closefrm():
            self.close()
                
       
        self.bt_Del.clicked.connect(update)
        self.bt_Cancel.clicked.connect(closefrm)
        
        self.layout1.addWidget(self.label)
        self.layout1.addWidget(self.bt_Del)
        self.layout1.addWidget(self.bt_Cancel)

        self.setLayout(self.layout1)

class TagAmend(QWidget):

    def __init__(self, TagName, TagPath, SettingTbl):
        super().__init__()

        self.layout1 = QVBoxLayout()
        self.layout2 = QHBoxLayout()
        self.setWindowTitle("Amend Run Tag Properties")
        self.setGeometry(200,200,320,100)
        
        
        self.Tag_label = QLabel("Run Tag")
        self.Tag_Value = QLineEdit (TagName[:-4])
        self.TagValueStore = self.Tag_Value.text()+".exe"   #stores value on load
        
        self.TagPath_label = QLabel("Run Path")
        self.Tag_Path = QLineEdit (str(TagPath)) 
        self.TagPathStore =self.Tag_Path.text()             #store value on load

        self.bt_update =QPushButton("Update")
        self.bt_cancel =QPushButton("Cancel")
        
        # NOTE: Update functioning correctly however not refreshing in place
        col1 = 0
        col2 = 1
               
        #iteration counter
        count = 0   

        def update():
            self.hide()
            SettingTbl.close()
            AmendRunTag(self.TagValueStore,self.Tag_Value.text(),self.Tag_Path.text())
            c2k = combine_key2path()
            SettingsWindow()
                
        def closefrm():
            self.close()
           
        #    MainWindow.SettingsDisplay(self,checked=None)

        #    print(self.TagValueStore,self.Tag_Value.text(),self.Tag_Path.text())

        self.bt_update.clicked.connect(update)
        self.bt_cancel.clicked.connect(closefrm)
        
        # self.Tag_Value.text(),self.Tag_Path.text())
        
        #AddTo Layout
        self.layout1.addWidget(self.Tag_label)
        self.layout1.addWidget(self.Tag_Value)
        self.layout1.addWidget(self.TagPath_label)
        self.layout1.addWidget(self.Tag_Path)
        self.layout1.addWidget(self.bt_update)
        self.layout1.addWidget(self.bt_cancel)

        self.setLayout(self.layout1)

class TagAdd(QWidget):

    def __init__(self, TagName, TagPath, SettingTbl):
        super().__init__()

        self.layout1 = QVBoxLayout()
        self.layout2 = QHBoxLayout()
        self.setWindowTitle("Amend Run Tag Properties")
        
        self.Tag_label = QLabel("Run Tag")
        self.Tag_Value = QLineEdit (Tagname)
        self.TagValueStore = self.Tag_Value.text()+".exe"   #stores value on load
        
        self.TagPath_label = QLabel("Run Path")
        self.Tag_Path = QLineEdit (str(TagPath)) 
        self.TagPathStore =self.Tag_Path.text()             #store value on load

        self.bt_update =QPushButton("Update")
        self.bt_cancel =QPushButton("Cancel")
        
        # NOTE: Update functioning correctly however not refreshing in place
        col1 = 0
        col2 = 1
               
        #iteration counter
        count = 0   

        def update():
            self.hide()
            SettingTbl.close()
            AddRunTag(self.TagValueStore,self.Tag_Value.text(),self.Tag_Path.text())
            c2k = combine_key2path()
            SettingsWindow()
                
        def closefrm():
            self.close()


           
           
        #    MainWindow.SettingsDisplay(self,checked=None)


        
        #    print(self.TagValueStore,self.Tag_Value.text(),self.Tag_Path.text())
        
        self.bt_update.clicked.connect(update)
        self.bt_cancel.clicked.connect(closefrm)
        # self.Tag_Value.text(),self.Tag_Path.text())
        


        #AddTo Layout
        self.layout1.addWidget(self.Tag_label)
        self.layout1.addWidget(self.Tag_Value)
        self.layout1.addWidget(self.TagPath_label)
        self.layout1.addWidget(self.Tag_Path)
        self.layout1.addWidget(self.bt_update)
        self.layout1.addWidget(self.bt_cancel)

        self.setLayout(self.layout1)

app = QApplication(sys.argv)

w = MainWindow()
w.show()

app.exec()