import sys
from PyQt4 import QtGui, QtCore

class Window(QtGui.QMainWindow):
  def __init__(self,appref):
    super(Window,self).__init__()
    scrRes = appref.desktop().screenGeometry()
    self.setGeometry(1,25,scrRes.width(),(scrRes.height()-53))
    self.setWindowTitle("Notowania gieldowe")
    self.initComponents()
  def initComponents(self):
    btn = QtGui.QPushButton("Exit",self)
    QtCore.QObject.connect(btn,QtCore.SIGNAL('clicked()'),QtCore.QCoreApplication.instance().quit)
    btn.resize(100,50)
    btn.move(1,1)
    self.show()

def main():
  app = QtGui.QApplication(sys.argv)
  GUI = Window(app)
  sys.exit(app.exec_())








main()
