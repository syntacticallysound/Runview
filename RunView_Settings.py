from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QAbstractItemView, QVBoxLayout, QWidget,QHeaderView
from RegFunctions import *
from PyQt5 import QtCore
from RunView_Settings import *

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
           
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        def CurRowDataAmend(): 
            currow = self.tableWidget.item(self.tableWidget.currentRow(), 0)
            currow1 = self.tableWidget.item(self.tableWidget.currentRow(), 1)
            self.w = RegCrud(currow.text(),currow1.text())
            self.w.show()
            # print (currow.text(),">",currow1.text())

        
        #TableConnections           
        self.tableWidget.doubleClicked.connect(CurRowDataAmend)
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