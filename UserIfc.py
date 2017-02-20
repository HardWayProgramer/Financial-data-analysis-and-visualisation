import sys
from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
import datetime as dt

class Window(QtGui.QWidget):
  scrRes = None
  harvestFlag = False
  harvbox = None
  srcbtn = None
  shocom = None
  plo = None
  grid = None
  def turnAutoHarvest(self,checked):
    if checked:
        self.harvestFlag = True
	print self.harvestFlag
    else:
        self.harvestFlag = False
        print self.harvestFlag
  def updatePlot(self):
    self.x=[3,2,3,4,5,6,7,8,9]
    self.y=[1,3,5,7,9,2,5,3,1]
    self.plo.plot(self.x,self.y)
  def __init__(self,appref):
    super(Window,self).__init__()
    self.scrRes = appref.desktop().screenGeometry()
    self.setGeometry(1,25,self.scrRes.width(),(self.scrRes.height()-53))
    self.setWindowTitle("Notowania gieldowe")
    self.grid = QtGui.QGridLayout()
    self.setLayout(self.grid)
#########################################################################################################
    
##########################################################################################################
    self.plo = pg.PlotWidget()
    self.grid.addWidget(self.plo)
    self.x = [1]
    self.y = [1]
    self.plo.plotItem.plot(self.x,self.y)
    self.grid.addWidget(self.plo,0,0)
###########################################init stock selection combo####################################   
    self.srcombo = QtGui.QComboBox()
    self.grid.addWidget(self.srcombo,1,9)
    self.srcombo.addItem("Wig20")
    self.srcombo.addItem("CAC 40")
    self.srcombo.addItem("DAX")
    self.srcombo.addItem("NIKKEI 225")
    self.srcombo.addItem("FTSE 100")
############################################init stock selection button###################################   
    self.srcbtn = QtGui.QPushButton("Get Data",self)
    self.grid.addWidget(self.srcbtn,2,9)
#######################################init company selection combo#######################################
    self.cmpcombo = QtGui.QComboBox()
    self.grid.addWidget(self.cmpcombo,3,9)
    self.cmpcombo.addItem("empty")
########################################init company selection button#####################################
    self.shocom = QtGui.QPushButton("Confirm",self)
    self.grid.addWidget(self.shocom,4,9)
    self.shocom.clicked.connect(self.updatePlot)
####################################################checkbox init#########################################
    self.harvbox = QtGui.QCheckBox('automatically harvest data',self)
    self.harvbox.stateChanged.connect(self.turnAutoHarvest)
    self.grid.addWidget(self.harvbox,7,9)
##########################################################################################################
    self.show()
    if self.harvestFlag == True:
	self.autoCollector = Collector(harvestFlag) 
############################## time.strftime("%Y. %m. %d (%H:%M)")  time format
class Collector():
  def __init__(self,flag):
    axn=1

def main():
  app = QtGui.QApplication(sys.argv)
  GUI = Window(app)
  sys.exit(app.exec_())








main()
