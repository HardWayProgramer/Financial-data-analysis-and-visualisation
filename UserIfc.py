import sys
from PyQt4 import QtGui, QtCore
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as fcanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as ntbar
import matplotlib.dates as mdate
import time as ct
import matplotlib.cbook as cbk
import numpy as np
import urllib2
from threading import Thread

class Window(QtGui.QWidget):
  DJI = ['PFE','V','UTX','KO','TRV','MSFT','INTC','MRK','MMM','AXP','GE','AAPL','CVX','PG','JPM','GS','DD','CSCO','IBM','DIS','CAT','XOM','JNJ','WMT','NKE','MCD','HD','BA','VZ','UNH']
  FTSE100 = ['EXPN.L','AHT.L','SKY.L','CPG.L','PFG.L','WPG.L','PPB.L','VOD.L','SDR.L','BATS.L','PSN.L','SSE.L','GKN.L']
  NIKKEI225 = []
  selectedS = None
  selectedC = None
  currency = None
  def updateSS(self):
    self.selectedS = self.srcombo.currentText()
    self.selectStock()    

  def updateSC(self):
    self.selectedC = self.cmpcombo.currentText()
    self.getData()

  def selectStock(self):
    self.cmpcombo.clear()
    if self.selectedS == 'DJI':
      for i in self.DJI:
        self.cmpcombo.addItem(i)
    elif self.selectedS == 'FTSE100':
      for i in self.FTSE100:
        self.cmpcombo.addItem(i)
    elif self.selectedS == 'NIKKEI255':
      for i in self.NIKKEI255:
        self.cmpcombo.addItem(i)

  def scrapTheWebsite(self):
    stockUrl = str( 'http://chartapi.finance.yahoo.com/instrument/1.0/'+self.selectedC+'/chartdata;type=quote;range=10y/csv')
    try:
      src = urllib2.urlopen(stockUrl).read()
    except:
      #self.grid.addWidget()
      print 'cos nie pyklo'
    print src
    print 'debug scrap wbs'
  
  def getData(self):
    nth = Thread(target = self.scrapTheWebsite, args = ())
    nth.start()

  def updatePlot(self):  
    ax = self.figure.add_subplot(111)
    ax.hold(False)
    ax.ylabel('value'+self.currency)
    ax.plot()
    self.canvas.draw()
  def __init__(self,appref):
    super(Window,self).__init__()
    self.scrRes = appref.desktop().screenGeometry()
    self.setGeometry(1,25,self.scrRes.width(),(self.scrRes.height()-53))
    self.setWindowTitle("Notowania gieldowe")
    self.grid = QtGui.QGridLayout()
    self.setLayout(self.grid)
#########################################################################################################
    
#################################################plot init###############################################
    self.figure = plt.figure() # inner part of plot passed to canvas
    self.canvas = fcanvas(self.figure) # initializing canvas with figure
    self.toolbar = ntbar(self.canvas,self) #passing a canvas and parent to navigation toolbar
    self.grid.addWidget(self.toolbar,9,0)
    self.grid.addWidget(self.canvas,0,0,9,9)
    self.x = [1]
    self.y = [1]

###########################################init stock selection combo####################################   
    self.srcombo = QtGui.QComboBox()
    self.grid.addWidget(self.srcombo,0,9)
    self.srcombo.addItem("stock select")
    self.srcombo.addItem("DJI")
    self.srcombo.addItem("NIKKEI225")
    self.srcombo.addItem("FTSE100")
    
############################################init stock selection button###################################   
    self.srcbtn = QtGui.QPushButton("Get Data",self)
    self.grid.addWidget(self.srcbtn,1,9)
    self.srcbtn.clicked.connect(self.updateSS)
#######################################init company selection combo#######################################
    self.cmpcombo = QtGui.QComboBox()
    self.grid.addWidget(self.cmpcombo,2,9)
    self.cmpcombo.addItem("company select")
########################################init company selection button#####################################
    self.shocom = QtGui.QPushButton("Confirm",self)
    self.grid.addWidget(self.shocom,3,9)
    self.shocom.clicked.connect(self.updateSC)
##########################################################################################################
    self.show()

############################## time.strftime("%Y. %m. %d (%H:%M)")  time format


def main():
  app = QtGui.QApplication(sys.argv)
  GUI = Window(app)
  sys.exit(app.exec_())








main()
