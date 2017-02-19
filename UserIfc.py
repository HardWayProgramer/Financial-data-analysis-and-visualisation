import sys
from PyQt4 import QtGui, QtCore
import pyqtgraph as pg

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

  def __init__(self,appref):
    super(Window,self).__init__()
    self.scrRes = appref.desktop().screenGeometry()
    self.setGeometry(1,25,self.scrRes.width(),(self.scrRes.height()-53))
    self.setWindowTitle("Notowania gieldowe")
    self.grid = QtGui.QGridLayout()
    self.setLayout(self.grid)
    #harvest
#########################################################################################################
    
##########################################################################################################
    self.plo = pg.PlotWidget()
    self.grid.addWidget(self.plo)
    x= set([1,2,3,4,5,6,7,8,9,5])
    y= set([1,3,4,5,6,7,8,9,10])
    self.plo.plotItem.plot()
##########################################################################################################   
    #srcombo = QtGui,QC
    

    self.srcbtn = QtGui.QPushButton("Get Data",self)
    self.grid.addWidget(self.srcbtn,2,9)

    self.shocom = QtGui.QPushButton("Confirm",self)
    self.grid.addWidget(self.shocom,4,9)

    self.harvbox = QtGui.QCheckBox('automatically harvest data',self)
    self.harvbox.stateChanged.connect(self.turnAutoHarvest)
    self.grid.addWidget(self.harvbox,1,9)
##########################################################################################################
    self.show()
##############################3
def main():
  app = QtGui.QApplication(sys.argv)
  GUI = Window(app)
  sys.exit(app.exec_())








main()
