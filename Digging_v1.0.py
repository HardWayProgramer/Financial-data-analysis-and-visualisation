#!/usr/bin/python

import sqlite3
import urllib2
import re

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
      self.initCurrList()
      if( self.cur.fetchone() == None ):
        print 'empty db'
        self.createCompanyTable(self.DJI+self.FTSE100)
        self.createCurrencyTable()
      self.scrapYahoo()
      self.scrapNBP()

    except sqlite3.Error,e:
      print 'error :{}'.format(e.args[0])
      
  def initCurrList(self):
    src = urllib2.urlopen('http://www.nbp.pl/kursy/Archiwum/archiwum_tab_a_2012.csv').read().decode('utf-8',errors='ignore')
    lines = src.split('\n')
    items = []
    convertedItems=[]
    for line in lines:
      items.append(line.split(';'))
    convertedItems =items[0][1:38]
    for i in convertedItems:
      i = re.sub(' .*','',i)
      self.currList.append(i)


  def createCompanyTable(self,com):
    try:
      for i in com:
        self.cur.execute('CREATE TABLE "{}" (ID INTEGER PRIMARY KEY  NOT NULL,CLOSEP REAL,MAXP REAL,MINP REAL,OPENP REAL,VOL REAL);'.format(i))
    except sqlite3.Error,e:
      print 'error:{}'.format(e.args[0])

  def createCurrencyTable(self):
    try:
      for i in self.currList:
        self.cur.execute('CREATE TABLE "{}" (ID INTEGER PRIMARY KEY  NOT NULL,VALUE REAL)'.format(i))
    except sqlite3.Error,e:
      print 'error:{}'.format(e.args[0])

  def fromDatabase(self,tName):
    self.cur.execute('SELECT * FROM "{}"'.format(tName))
    return self.cur.fetchall()

  def toDatabase(self,tName,data,dType): # data should be alredy .split('\n')
    if(dType == 'curr'):            #requires specifying type of the data ( 'comp' or 'curr'[actually 'curr' or whatever])
      timestamp = data[0]
      del data[0]
      for item in data:
          self.cur.execute('INSERT OR IGNORE INTO "{}" (ID,VALUE) VALUES(?,?)'.format(self.currList[data.index(item)]),(timestamp,item))
    else:
      for line in data:
        self.cur.execute('INSERT OR IGNORE INTO "{}" (ID,CLOSEP,MAXP,MINP,OPENP,VOL) VALUES(?,?,?,?,?,?)'.format(tName),(data[0], data[1], data[2], data[3], data[4], data[5]))
    self.connection.commit()  

  def scrapYahoo(self):
    links = self.DJI+self.FTSE100
    for link in links:
      src = urllib2.urlopen('http://chartapi.finance.yahoo.com/instrument/1.0/'+link+'/chartdata;type=quote;range=10y/csv').read().decode('utf-8')
      split_src = src.split('\n')
      for line in split_src:
        split_line = line.split(',')
        if len(split_line) == 6:
          if 'values' not in line and 'labels' not in line:
           self.toDatabase(link,split_line,'comp')

  def scrapNBP(self):
    i = 2016
    src = urllib2.urlopen('http://www.nbp.pl/kursy/Archiwum/archiwum_tab_a_'+str(i)+'.csv').read().decode('utf-8',errors='ignore')
    lines = src.split('\n') 
    for i in range(4):
      del lines[-1]
    del lines[0:2]
    for i in lines:
      spline = i.split(';')
      del spline[38:]
      self.toDatabase(None,spline,'curr')

def debug():
    x = Digger()
    #print x.fromDatabase("V")

    
if __name__=='__main__':
  debug()
