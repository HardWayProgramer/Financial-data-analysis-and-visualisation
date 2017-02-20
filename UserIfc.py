import sys
from PyQt4 import QtGui, QtCore
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as fcanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as ntbar
import matplotlib.dates as mdate
import matplotlib.cbook as cbk
import numpy as np

class Window(QtGui.QWidget):
  harvestFlag = False
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
    ax = self.figure.add_subplot(111)
    ax.hold(False)
    ax.plot(self.x,self.y)

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
    self.srcombo.addItem("Wig20")
    self.srcombo.addItem("CAC 40")
    self.srcombo.addItem("DAX")
    self.srcombo.addItem("NIKKEI 225")
    self.srcombo.addItem("FTSE 100")
############################################init stock selection button###################################   
    self.srcbtn = QtGui.QPushButton("Get Data",self)
    self.grid.addWidget(self.srcbtn,1,9)
#######################################init company selection combo#######################################
    self.cmpcombo = QtGui.QComboBox()
    self.grid.addWidget(self.cmpcombo,2,9)
    self.cmpcombo.addItem("empty")
########################################init company selection button#####################################
    self.shocom = QtGui.QPushButton("Confirm",self)
    self.grid.addWidget(self.shocom,3,9)
    self.shocom.clicked.connect(self.updatePlot)
####################################################checkbox init#########################################
    self.harvbox = QtGui.QCheckBox('automatically harvest data',self)
    self.harvbox.stateChanged.connect(self.turnAutoHarvest)
    self.grid.addWidget(self.harvbox,9,9)
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
