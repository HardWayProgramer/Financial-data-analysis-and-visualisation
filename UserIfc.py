import sys
import Collector
from PyQt4 import QtGui, QtCore
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as fcanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as ntbar
import matplotlib.dates as mdate
import time as ct
import numpy as np
import urllib2
from threading import Thread

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


  def __init__():
    pass

    
  def updatePlot():
    ax = self.figure.add_subplot(111)
    ax.plot(self.plotX,self.plotY)
    self.canvas.draw()

  def splitToPlot([]):
    pass





def main():
  app = QtGui.QApplication([])
  GUI = Window(app)
  sys.exit(app.exec_())

if __name__=='__main__':
  main()
