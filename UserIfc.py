#!/usr/bin/python
#! -*- coding: utf-8 -*-
import sys
from Digging import Digger
from PyQt4 import QtGui, QtCore
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as fcanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as ntbar
import matplotlib.dates as mdates
import time as ct
import numpy as np
import urllib2
import datetime


class Window(QtGui.QTabWidget):
  currency = None
  dateX = []
  openX = []
  maxX = []
  minX = []
  closeX = []
  volX = []
  dateXt2 = []
  valXt2 = []
  trendDate = []

  def plotTrendX(self):
    pass
    

  def rmCrappyCoding(self,crap):
    for i in range(0, len(crap)):
      try:
        crap[i].encode('ascii')
      except:
        crap = crap[i].replace('')
    return crap
  
  def qdate2int(qd):
    return int(str(qd[0])+str(qd[1])+str(qd[2]))

  def addDate(self):
    if len(self.trendDate)==0:
      self.trendDate.append(qdate2int(self.dPicker1.selectedDate()))
      self.pickButton.setText('Pick 2nd date')
    elif len(self.trendDate)<2:
      self.trendDate.append(qdate2int(self.dPicker1.selectedDate()))
      
    print self.trendDate

  def updateTab1Variables(self,table):
    recData = self.kopacz.fromDatabase(table)
    self.dateX = []
    self.openX = []
    self.closeX = []
    self.minX = []
    self.maxX = []
    self.volX = []
    for line in recData:
      self.dateX.append(mdates.datestr2num(str(line[0])))
      self.openX.append(line[1])
      self.maxX.append(line[2])
      self.minX.append(line[3])
      self.closeX.append(line[4])
      self.volX.append(line[5])
    self.updatePlot()

  def updateTab2Variables(self,table,table2):
    tmp1 = []
    tmp2 = []
    if table != None:
      self.dateXt2 = []
      self.valXt2 = []
      recData = self.kopacz.fromDatabase(table)
      for line in recData:
        self.dateXt2.append(mdates.datestr2num(str(line[0])))
        self.valXt2.append(line[1])
    if table2 != None:
      self.dateXt22 = []
      self.valXt22  = []  
      recData2 = self.kopacz.fromDatabase(table2)
      for line in recData2:
        self.dateXt22.append(mdates.datestr2num(str(line[0])))
        self.valXt22.append(line[1])
    for i in range(0,len(self.valXt2)):
      self.valXt2[i] = self.rmCrappyCoding(self.valXt2[i])
      self.valXt22[i] = self.rmCrappyCoding(self.valXt22[i])
    print self.valXt2
    self.updatePlot()

  @QtCore.pyqtSlot(str)
  def on_indexCombo_currentIndexChanged(self,index):
    companyItems = self.stockItems[str(index)]
    self.companyCombo.clear()
    self.companyCombo.addItem('Select Company')
    self.companyCombo.addItems(companyItems)
    if self.indexCombo.itemText(0) == 'Select Index':
      self.indexCombo.removeItem(0)
      self.companyCombo.currentIndexChanged[str].connect(self.on_companyCombo_currentIndexChanged)
      self.layout1.addWidget(self.companyCombo,1,10,1,2)
      self.layout1.addWidget(self.maxChBox,2,10,1,2)
      self.layout1.addWidget(self.closeChBox,3,10,1,2)
      self.layout1.addWidget(self.openChBox,4,10,1,2)
      self.layout1.addWidget(self.minChBox,5,10,1,2)
      self.layout1.addWidget(self.dPicker1,6,10,4,1)
      self.layout1.addWidget(self.pickButton,11,10,1,1)
      self.pickButton.clicked.connect(self.addDate)

  @QtCore.pyqtSlot(str,)
  def on_companyCombo_currentIndexChanged(self,index):
    if self.companyCombo.itemText(0) == 'Select Company':
      self.companyCombo.removeItem(0)
    self.updateTab1Variables(self.companyCombo.currentText())

  @QtCore.pyqtSlot(str)
  def on_curr1combo_currentIndexChanged(self,index):
    self.updateTab2Variables(self.curr1combo.currentText(),None)

  @QtCore.pyqtSlot(str)
  def on_curr2combo_currentIndexChanged(self,index):
    self.updateTab2Variables(None,self.curr2combo.currentText())


  def __init__(self,appref):
    super(Window,self).__init__()
    self.kopacz = Digger()
    self.scrRes = appref.desktop().screenGeometry()
    self.setGeometry(1,25,self.scrRes.width(),self.scrRes.height()-53)
    self.setWindowTitle("Stock Prices")
    self.tabs = QtGui.QTabWidget()
    self.tab1,self.tab2 = QtGui.QWidget(), QtGui.QWidget()
    self.tabs.addTab(self.tab1,'companies')
    self.tabs.addTab(self.tab2,'currencies')
    self.layout1 = QtGui.QGridLayout()
    self.layout2 = QtGui.QGridLayout()
    self.tab1.setLayout(self.layout1)
    self.tab2.setLayout(self.layout2) 
    self.stockItems = {Digger.stockList[0]:Digger.DJI,Digger.stockList[1]:Digger.FTSE100} # edit this line as well as Digging.py in case of adding more companies / indexes
    self.indexCombo = QtGui.QComboBox(self)
    self.indexCombo.addItem('Select Index')
    self.indexCombo.addItems(self.stockItems.keys())
    self.indexCombo.currentIndexChanged[str].connect(self.on_indexCombo_currentIndexChanged)
    self.companyCombo = QtGui.QComboBox(self)
    self.curr1combo = QtGui.QComboBox(self)
    self.curr1combo.currentIndexChanged[str].connect(self.on_curr1combo_currentIndexChanged)
    self.curr1combo.addItems(self.kopacz.currList)
    self.curr2combo = QtGui.QComboBox(self)
    self.curr2combo.currentIndexChanged[str].connect(self.on_curr2combo_currentIndexChanged)
    self.curr2combo.addItems(self.kopacz.currList)
    self.openChBox = QtGui.QCheckBox('open price',self)
    self.closeChBox = QtGui.QCheckBox('close price',self)
    self.maxChBox = QtGui.QCheckBox('max price',self)
    self.minChBox = QtGui.QCheckBox('min price',self)
    self.dPicker1 = QtGui.QCalendarWidget()
    self.pickButton = QtGui.QPushButton('Pick date 1')
    self.createPlot()
    self.openChBox.stateChanged.connect(self.updatePlot)
    self.closeChBox.stateChanged.connect(self.updatePlot)
    self.maxChBox.stateChanged.connect(self.updatePlot)
    self.minChBox.stateChanged.connect(self.updatePlot) 
    self.pinToLayouts()
    self.tabs.show()

  def pinToLayouts(self):
    self.layout1.addWidget(self.canvas,0,0,10,10)
    self.layout1.addWidget(self.toolbar,11,0,1,10)
    self.layout1.addWidget(self.indexCombo,0,10,1,2)
    
    self.layout2.addWidget(self.canvas2,0,0,10,10)
    self.layout2.addWidget(self.toolbar2,11,0,1,10)
    self.layout2.addWidget(self.curr1combo,0,10,1,2)


  def updatePlot(self):
    if self.tabs.currentIndex() == 0:
      self.wykres1.cla()
      self.wykres2.cla()
      if self.maxChBox.isChecked():
        self.wykres1.plot_date(self.dateX,self.maxX,'ro')
      if self.openChBox.isChecked():
        self.wykres1.plot_date(self.dateX,self.openX,'ys')
      if self.closeChBox.isChecked():
        self.wykres1.plot_date(self.dateX,self.closeX,'.k')
      if self.minChBox.isChecked():
        self.wykres1.plot_date(self.dateX,self.minX,'b^')
      self.wykres2.plot_date(self.dateX,self.volX)
      self.canvas.draw()
    else:
      self.wykres11.cla()
      self.wykres22.cla()
      self.wykres11.plot_date(self.dateX,self.valXt2,'ro')
      self.wykres22.plot_date(self.dateXt22,self.valXt22,'b^')
      self.canvas2.draw()
  
  def createPlot(self):
    self.figure = plt.figure()
    self.figure2 = plt.figure()
    self.canvas = fcanvas(self.figure)
    self.canvas2 = fcanvas(self.figure2)
    self.toolbar = ntbar(self.canvas,self)
    self.toolbar2 = ntbar(self.canvas2,self)
    self.wykres1 = self.figure.add_subplot(2,1,1)
    self.wykres2 = self.figure.add_subplot(2,1,2)
    self.wykres11 = self.figure2.add_subplot(2,1,1)
    self.wykres22 = self.figure2.add_subplot(2,1,2)
    self.wykres1.hold(True)
    self.wykres11.hold(True)

def main():
  app = QtGui.QApplication(sys.argv)
  GUI = Window(app)
  sys.exit(app.exec_())

if __name__=='__main__':
  main()
