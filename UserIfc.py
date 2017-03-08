#!/usr/bin/python
#! -*- coding: utf-8 -*-
import sys
from Digging import Digger
from PyQt4 import QtGui, QtCore
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as fcanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as ntbar
import matplotlib.dates as mdate
import time as ct
import numpy as np
import urllib2


class Window(QtGui.QTabWidget):
  plotX = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
  plotY = [1,1,2,1,2,3,4,5,3,4,3,2,3,4,5,6]
  plotRGB = []
  currency = None
  dateX = []
  openX = []
  maxX = []
  minX = []
  closeX = []
  volX = []

  def dspNetError(self):
    errinfo = QtGui.QMessageBox()
    errinfo.setIcon(QtGui.QMessageBox.Information)
    errinfo.setText('Failed to obtain data')
    errinfo.setDetailedText('One or more of the following might have occured:\n-You have no network connection\n-Source servers are down\n-Your firewall or provider is blocking the connection with finance.yahoo.com\n-The site might be redirected / blocked in:\n   /etc/hosts (linux)\n  ..\Windows\System32\drivers\etc\hosts')
    errinfo.setGeometry((self.scrRes.width()/2 -150),(self.scrRes.height()/2 -100),300, 200)
    errinfo.setStandardButtons(QtGui.QMessageBox.Ok)
    errinfo.exec_()
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
  @QtCore.pyqtSlot(str)
  def on_companyCombo_currentIndexChanged(self,index):
    if self.companyCombo.itemText(0) == 'Select Company':
      self.companyCombo.removeItem(0)
    Digger.scrapYahoo(str(index))

  def __init__(self,appref):
    super(Window,self).__init__()
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
    print self.scrRes.height()
    self.createPlot()
    self.pinToLayouts()
    self.tabs.show()

  def pinToLayouts(self):
    self.layout1.addWidget(self.canvas,0,0,10,10)
    self.layout1.addWidget(self.toolbar,11,0,1,10)
    self.layout1.addWidget(self.indexCombo,0,10,1,2)
    
    self.layout2.addWidget(self.canvas2,0,0,10,10)
    self.layout2.addWidget(self.toolbar2,11,0,1,10)


  def updatePlot(self,pType,tabId):
    if tabId == 1:
      self.wykres1.cla()
      self.wykres2.cla()
      self.wykres1.plot(self.plotX,self.plotY,'.k')
      self.wykres2.plot(self.plotY,self.plotX,'{}'.format(pType))
      self.canvas.draw()
    else:
      self.wykres21.cla()
      self.wykres22.cla()
      self.wykres11.plot(self.plotX,self.plotY,'.k')
      self.wykres22.plot(self.plotY,self.plotX,'{}'.format(pType))
      self.canvas.draw()
  
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


#  def splitToPlot([]):


def main():
  app = QtGui.QApplication(sys.argv)
  GUI = Window(app)
  sys.exit(app.exec_())

if __name__=='__main__':
  main()
