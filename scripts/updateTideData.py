#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
import MySQLdb
import urllib2
import datetime
import pytz
import re

DBNAME='tide'

def main():
    tz = pytz.timezone('Asia/Tokyo')
    try:
        db = pymongo.Connection('localhost', 27017)[DBNAME]
        
        rdb_conn = MySQLdb.connect(host='localhost',
                    user='root',
                    passwd='',
                    port=3306,
                    db='tide2',
                    charset='utf8')

        ## get master area data
        r = []
        cur = rdb_conn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM area")
        row = cur.fetchone()
        while row:
            r.append(row['location'])
            row = cur.fetchone()

        for location in r:
            fh = urllib2.urlopen(
                    "http://www1.kaiho.mlit.go.jp/KANKYO/TIDE/real_time_tide/images/tide_real/%sYesterday.txt" % (location,))
            items = fh.read().split("\n")

            for i,item in enumerate(items):
                if i > 10 and item:
                    c = re.split("[ ]*", item)
                    c = map((lambda x: int(x)), c)
                    d = datetime.datetime(c[0], c[1], c[2], c[3], c[4], tzinfo=tz)

                    if c[5] == 9999: 
                        c[5] = None

                    if len(c) == 7:
                        hpa = c[6]
                    else:
                        hpa = 0

                    ## update mongodb
                    if hpa == 0:
                        doc = {"datetime": d, "location": location, "tidalheight": c[5]}
                    else:
                        doc = {"datetime": d, "location": location, "tidalheight": c[5], "hectopascal": hpa}
                    #print doc
                    db.tide.insert(doc)
              
    except Exception, e:
        print e

if __name__ == "__main__":
    main()
