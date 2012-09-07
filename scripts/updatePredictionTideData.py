#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib2
import datetime
import pytz
import pymongo
import MySQLdb

UTC = pytz.timezone('UTC')
JST = pytz.timezone('Asia/Tokyo')
YEAR=datetime.datetime.now().replace(tzinfo=UTC).astimezone(JST).strftime("%Y")
API="http://www.data.kishou.go.jp/db/tide/suisan/txt/%s/%s.txt"

def main():

    ## KVS 
    conn = pymongo.Connection('localhost', 27017)
    db = conn.tide

    ## RDBMS
    rdbconn = MySQLdb.connect(
                host='localhost',
                user='root',
                passwd='',
                db='tide2',
                port=3306,
                charset='utf8')
    cur = rdbconn.cursor(MySQLdb.cursors.DictCursor)

    query = """SELECT a.location, l.codename FROM area a 
               LEFT JOIN location_code l ON (a.location=l.location)"""
    cur.execute(query)
    row = cur.fetchone()
    while row:
        location = row['location']
        codename = row['codename']

        fh = urllib2.urlopen(API % (YEAR, codename,))
        lines = fh.read().split("\n")
        for line in lines:
            if not line: continue
            mmdd, tide = line[74:78], line[0:73]
            # month
            if len(mmdd[0:2].replace(" ", "")) == 1: 
                mm = "0"+str(int(mmdd[0:2]))
            else:
                mm = mmdd[0:2]
            # date
            if len(mmdd[2:4].replace(" ", "")) == 1: 
                dd = "0"+str(int(mmdd[2:4]))
            else:
                dd = mmdd[2:4]
                
            dt = datetime.datetime.strptime("%s-%s-%s" % (YEAR, mm, dd,), '%Y-%m-%d')
            #print dt

            s = ""
            tides = []
            for i in tide:
                s += i
                if len(s) == 3:
                    tides.append(s.replace(" ", ""))
                    s = ""

            for i, tidalheight in enumerate(tides):
                if len(str(i)) == 1:
                    hh = "0"+str(i)
                else:
                    hh = str(i)
                d = datetime.datetime.strptime(
                        dt.strftime("%Y-%m-%d") +" "+hh+":00:00", "%Y-%m-%d %H:%M:%S"
                        ).replace(tzinfo=JST)
                #print d, tidalheight
                doc = {"datetime": d,
                       "location": location,
                       "tidalheight": int(tidalheight)}
                
                db.pre_tide.insert(doc)

        row = cur.fetchone()

    conn.close()
    cur.close()
    rdbconn.close()

if __name__ == "__main__":
    main()
