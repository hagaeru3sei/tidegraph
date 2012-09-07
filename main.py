# -*- coding: utf-8 -*-
## ----------------------------------------------------------------
## tornado web server
## 
## use reverse proxy (nginx or apache or etc..)
## don't use stand alone.
## 
## auther nobuaki mochizuki <hagaeru3sei@yahoo.co.jp>
## create 2012-05-17
## ----------------------------------------------------------------
import tornado.ioloop
import tornado.web
import tornado.escape
import base64
import pymongo
import pytz
import datetime
import sys
import os
import re
import yaml
import logging
import urllib2
import MySQLdb
import numpy
#from xml.sax.saxutils import *
from pylab import *
import  matplotlib.pyplot as plt
from xml.etree.ElementTree import ElementTree
## import mylibs
sys.path.append('/opt/tornado')
from app.models import Error
from app.models import Caching


## defined values
HOME    = "/opt/tornado"
LOG_DIR = HOME+"/logs"
DB      = {"name" : "localhost", 
           "port" : 27017, 
           "db"   : "tide"}
DATABASE = {"host"    : "localhost",
            "port"    : 3306,
            "user"    : "root", 
            "passwd"  : "",
            "name"    : "tide2",
            "charset" : "utf8"}

UTC = pytz.timezone('UTC')
JST = pytz.timezone('Asia/Tokyo')

TIDEAPI    = "http://www1.kaiho.mlit.go.jp/KANKYO/TIDE/real_time_tide/images/tide_real/%sToday.txt"
WEATHERAPI = "http://rss.rssad.jp/rss/tenki/forecast/pref_%s.xml"
INTERVAL_COUNT=3600*24/300

## variable values
Port = 8888
Pid = -1


class DBConnection(object):
    """
    """
    _conn  = None
    cursor = None
    
    def __init__(self):
        """
        """
        self._conn = pymongo.Connection(DB['name'], DB['port'])

    def getDB(self, name):
        """
        """
        if self._conn == None:
            self._conn = pymongo.Connection(DB['name'], DB['port'])
        return self._conn[name]


class DBCursor(object):
    """
    """
    def __init__(self, cursorType=0):
        pass
    def fetchOne(self):
        pass 
    def fetchAll(self):
        pass


class TideGraph(tornado.web.RequestHandler):
    """
    """
    _db  = None
    _rdb = None

    target_date = ""
    areaname    = ""

    def initialize(self):
        """initialize
        override
        """
        ## connect mongodb
        if self._db == None:
            self._db = DBConnection().getDB('tide')

        ## connect rdbms
        if self._rdb == None:
            self._rdb = MySQLdb.connect(host=DATABASE['host'],
                            user=DATABASE['user'],
                            passwd=DATABASE['passwd'],
                            port=DATABASE['port'],
                            db=DATABASE['name'],
                            charset=DATABASE['charset'])
 

    def getViewData(self):
        """getViewData"""
        views = {}
        views['title']          = 'tide graph'
        views['areaname']       = self.areaname
        views['location']       = self.areaname
        views['target_date']    = ''
        views['prev_date']      = ''
        views['next_date']      = ''
        views['rows']           = []
        views['prev_rows']      = []
        views['next_rows']      = []
        views['wind_speed']     = ''
        views['wind_direction'] = ''
        views['weather']        = ''
        views['header_title']   = 'tide graph'
        views['areas']          = self.getAreaData()
        views['states']         = self.getStateData()

        return views


    def valid(self):
        """ """
        ## area
        if 'area' in self.request.arguments:
            self.areaname = self.get_argument('area')
        if self.areaname == "-" or self.areaname == "":
            views = self.getViewData()
            self.render(HOME+"/app/views/tidegraph.html", items=views)
            return
        
        if self.areaname not in self.areaData:
            logging.error("GET request area name not found.")
            raise tornado.web.HTTPError(400)


        ## date format %Y%m%d
        if 'date' in self.request.arguments:
            self.target_date = self.get_argument('date')
        if self.target_date != "" and re.compile('^20[0-9]{2}[0-9]{2}[0-9]{2}$').match(self.target_date):
            logging.error("GET request target date not found.")
            #raise tornado.web.HTTPError(400)

        self.today = datetime.datetime.now().replace(tzinfo=UTC).astimezone(JST).strftime("%Y%m%d")
        if self.target_date == "":
            self.target_date = self.today


    def get(self):
        """get
        """
        data  = []
        views = {}

        ## get master area data
        self.areaData = self.getAreaData(state=False)

        ## validation
        self.valid()
        #self.write("today = %s" % self.today)
        #self.write("target_date = %s<br>" % self.target_date)

        ## create view data
        views = self.getViewData()
        td = datetime.datetime.strptime(self.target_date, '%Y%m%d')
        pd = td - datetime.timedelta(days=1)
        nd = td + datetime.timedelta(days=1)
        views['target_date'] = self.target_date
        views['prev_date'] = pd.strftime('%Y%m%d')
        views['next_date'] = nd.strftime('%Y%m%d')
        #self.write("prev_date = %s<br>" % views['prev_date'])
        #self.write("next_date = %s<br>" % views['next_date'])

        ## get wind data
        wind = self.getWindData(self.areaname)
        if wind:
            views['wind_speed']     = str(wind[0]['wind_speed'])
            views['wind_direction'] = wind[0]['wind_direction']

        ## get weather data
        weathers = self.getWeatherData(self.areaname)
        if weathers:
            for weather in weathers:
                views['weather'] += "  "+ weather['title']

        ## get todays tide data
        views['rows']      = self.getTideData(self.target_date)
        views['prev_rows'] = self.getTideData(self.target_date, 'prev')
        views['next_rows'] = self.getTideData(self.target_date, 'next')

        ## use predicted tidal data
        self.render(HOME+"/app/views/tidegraph.html", items=views)


    def getStateData(self):
        """
        """
        cur = self._rdb.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM state")
        row = cur.fetchone()
        r = {}
        while row:
            r[row['stateid']] = row['statename']
            row = cur.fetchone()

        cur.close()
        return r


    def getAreaData(self, state=True):
        """getAreaData
        return dict
        """
        r = {}
        cur = self._rdb.cursor(MySQLdb.cursors.DictCursor)
        query = """SELECT 
                    a.areaid, 
                    a.areaname, 
                    a.location, 
                    s.stateid, 
                    s.statename
                   FROM 
                    area a 
                    left join area_has_state ahs on (a.areaid=ahs.areaid) 
                    left join state s on (ahs.stateid=s.stateid) 
                   ORDER BY s.stateid, areaid"""
        cur.execute(query)
        row = cur.fetchone()
        while row:
            row['areaname'] = tornado.escape.to_unicode(row['areaname'])
            if state == True:
                if row['stateid'] not in r: 
                    r[row['stateid']] = {}
                r[row['stateid']][row['location']] = row
                
            else:
                r[row['location']] = row
            
            row = cur.fetchone()
        cur.close()
        return r


    def getTideData(self, target_date, type=''):
        """
        return list data
        """
        data = []

        if int(target_date) == int(self.today) and type == '':

            fh = urllib2.urlopen(TIDEAPI % (self.areaname,))
            items = fh.read().split("\n")
            for i,item in enumerate(items):
                if i > 10 and item:
                    c = re.split("[ ]*", item)
                    c = map((lambda x: int(x)), c)
                    d = datetime.datetime(c[0], c[1], c[2], c[3], c[4], tzinfo=JST)
                    if c[5] == 9999: 
                        c[5] = None
                    if d.strftime('%M') == "00":
                        hh = d.strftime('%H')
                        data.append({"datetime":hh, "tidalheight": c[5]})

        else:

            td = datetime.datetime.strptime(target_date, '%Y%m%d')
            if type == 'prev':
                pd = td - datetime.timedelta(days=1)
                td = pd
            elif type == 'next':
                nd = td + datetime.timedelta(days=1)
                td = nd

            offset = datetime.datetime.strptime(
                        td.strftime('%Y-%m-%d 00:00:00'), 
                        '%Y-%m-%d %H:%M:%S').replace(tzinfo=JST).astimezone(UTC)
            limit  = datetime.datetime.strptime(
                        td.strftime('%Y-%m-%d 23:59:59'), 
                        '%Y-%m-%d %H:%M:%S').replace(tzinfo=JST).astimezone(UTC)

            ## predicted tide data
            if int(target_date) > int(self.today) or (type == 'next' and int(nd.strftime('%Y%m%d')) >= int(self.today)):
                rows = self._db.pre_tide.find({"datetime":{"$gte":offset, "$lte":limit}, "location": self.areaname})
            ## real tide data
            else:
                rows = self._db.tide.find({"datetime":{"$gte":offset, "$lte":limit}, "location": self.areaname})
            rows.sort("datetime", pymongo.ASCENDING)

            for i, row in enumerate(rows):
                dt = row['datetime'].replace(tzinfo=UTC).astimezone(JST).strftime('%H')
                if row['datetime'].replace(tzinfo=UTC).astimezone(JST).strftime('%M') == "00":
                    data.append({"datetime":dt, "tidalheight": row['tidalheight']})

        return data

    ## ----------------------------------------------------------------
    ## getWindData
    ## 
    ## @param location str
    ## @return data: list
    ## ----------------------------------------------------------------
    def getWindData(self, location):
        """
        """
        data = []
        rows = self._db.wind.find({"location":location})
        rows.sort("datetime", pymongo.DESCENDING)
        for row in rows:
            dt = row['datetime'].replace(tzinfo=UTC).astimezone(JST)
            data.append({"datetime":dt, "wind_speed":row['wind_speed'], "wind_direction": row['wind_direction']})
            break
        return data

    ## ----------------------------------------------------------------
    ## getWeatherData
    ## 
    ## @param location str
    ## @return data: list
    ## ----------------------------------------------------------------
    def getWeatherData(self, location):
        """
        """
        ## if cached 
        yymmddhh = datetime.datetime.now().replace(tzinfo=UTC).astimezone(JST).strftime('%Y%m%d%H')
        key = str(yymmddhh + "_" + location)
        mc = Caching.MemcacheStore()
        data = mc.get(key)
        if data:
            return data

        data = []
        patt = re.compile(u"^.* \[ ([0-9]+).* \] ([0-9.]+).*$")
        cur = self._rdb.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("""SELECT sht.prefid AS prefid FROM area a 
                        JOIN area_has_state ahs ON (a.areaid=ahs.areaid) 
                        JOIN state s ON (s.stateid=ahs.stateid) 
                        JOIN state_has_tenkijpPref sht ON (s.stateid=sht.stateid) 
                        WHERE a.location=%s""", (location,))
        row = cur.fetchone()

        cur.close()

        ## temperature
        fh    = urllib2.urlopen(WEATHERAPI % row['prefid'])
        rss   = ElementTree(file=fh)
        items = rss.findall('.//item')
        for item in items:
            title = item.find('title').text
            data.append({'title':title})

        mc.set(key, data)
        return data


def worker_process():
    """worker_process
    """
    global Port
    
    if len(sys.argv) == 2:
        Port = int(sys.argv[1])

    ##  
    application = tornado.web.Application([
        (r"/tidegraph", TideGraph),
    ])
    
    application.listen(Port)
    tornado.ioloop.IOLoop.instance().start()
  

def main(*args, **kw):
    """main
    """
    global Pid

    logging.basicConfig(level    = logging.DEBUG,
                        format   = '%(asctime)s [%(levelname)s]\t%(message)s',
                        filename = 'logs/debug.log',
                        filemode = 'a')
    
    try:
        Pid = os.fork()

        if Pid == -1:
            raise "fail to fork"
        
        ## child
        if Pid == 0:
            worker_process()
        else: 
            sys.exit(0)
        
    except Exception, e:
        if Pid == 0:
            logging.error('exit main thread - %s' % e)
            sys.exit(-1)


if __name__ == "__main__":
    main()

