#!/usr/bin/python
#! -*- coding: utf-8 -*-
from threading import Thread
import sqlite3
import urllib2

class Digger():
  stockList = ['DJI','FTSE100']
  currList = []
  DJI = ['PFE','V','UTX','KO','TRV','MSFT','INTC','MRK','MMM','AXP','GE','AAPL','CVX','PG','JPM','GS','DD','CSCO','IBM','DIS','CAT','XOM','JNJ','WMT','NKE','MCD','HD','BA','VZ','UNH']
  FTSE100 = ['EXPN.L','AHT.L','SKY.L','CPG.L','PFG.L','WPG.L','PPB.L','VOD.L','SDR.L','BATS.L','PSN.L','SSE.L','GKN.L','RB.L','BA.L','TUI.L','PRU.L','RDSA.L','RR.L','CCL.L','MDC.L','STJ.L','TSCO.L','CCH.L','EZJ.L','CNA.L','SHP.L','ANTO.L','DLG.L']
  def __init__(self):
    self.connection = None
    try:
      self.connection = sqlite3.connect('companiesxcurrencies.db')
      self.cur = self.connection.cursor()
      print 'connected'
      self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
      if( self.cur.fetchone() == None ):
        print 'empty db'
        self.initCurrList()
        #self.createCompanyTable(lambda x,y:x+y,self.DJI,self.FTSE100)
        #self.createCurrencyTable()

    except sqlite3.Error,e:
      print 'error :{}'.format(e.args[0])
      
  def initCurrList(self):
    src = urllib2.urlopen('http://www.nbp.pl/kursy/Archiwum/archiwum_tab_a_2012.csv').read()
    lines = src.split('\n')
    items = []
    for line in lines:
      items.append(line.split(';'))
    print len(items[0])
    self.currList = items[0][1:38]

  def createCompanyTable(self,com):
    try:
      for i in com:
        self.cur.execute('''CREATE TABLE ? (ID TEXT PRIMARY KEY  NOT NULL,CLOSEP REAL,MAXP REAL,MINP REAL,OPENP REAL,VOL REAL);''',(i))	
    except sqlite3.Error,e:
      print 'error:{}'.format(e.args[0])

  def createCurrencyTable(self):
    try:
      for i in self.currList:
        self.cur.execute('''CREATE TABLE ? (ID TEXT PRIMARY KEY  NOT NULL,VALUE REAL)''',(i))
    except sqlite3.Error,e:
      print 'error:{}'.format(e.args[0])

  def fromDatabase(self,tName):
    print 'f'
  def toDatabase(self,tName):
    print 't'
  def scrapYahoo(self,urlPart):
    print 'y'

  def scrapNBP(self):
    print 'n'

def debug():
    x = Digger()

    
if __name__=='__main__':
  debug()
