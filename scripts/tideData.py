#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pymongo
import datetime
import pytz
import sys
import re
import MySQLdb

UTC=pytz.timezone('UTC')
JST=pytz.timezone('Asia/Tokyo')

def main():

    conn = MySQLdb.connect(host='localhost',user='root',
                           passwd='',
                           db='tide2',
                           charset='utf8')
    cur = conn.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("SELECT * FROM area")
    areas = []
    row = cur.fetchone()
    while row:
        areas.append(row['location'])
        row = cur.fetchone()

    cur.close()
    conn.close()


    # date
    if len(sys.argv) >= 2:
        target_date = sys.argv[1]
    
    df = re.compile('^20[0-9]{2}[0-9]{2}[0-9]{2}$')
    if not df.match(target_date):
        raise Exception("not date format")

    td = datetime.datetime.strptime(target_date, '%Y%m%d')
    offset = datetime.datetime.strptime(
                td.strftime('%Y-%m-%d 00:00:00'), 
                '%Y-%m-%d %H:%M:%S').replace(tzinfo=JST).astimezone(UTC)
    limit  = datetime.datetime.strptime(
                td.strftime('%Y-%m-%d 23:59:59'), 
                '%Y-%m-%d %H:%M:%S').replace(tzinfo=JST).astimezone(UTC)

    #print offset, limit

    # location
    location = 'shimizuminato'
    if len(sys.argv) == 3:
        location = sys.argv[2]

    if location not in areas:
        raise Exception("area is no match")

    try:
        db = pymongo.Connection('localhost', 27017)['tide']
        rows = db.tide.find({
                    'datetime' : {'$gte' : offset, '$lte' : limit}, 
                    'location' : location})
        for row in rows:
            print "%s\t%s\t%s" % (
                location, 
                row['datetime'].replace(tzinfo=UTC).astimezone(JST).strftime('%Y-%m-%d %H:%M:00'), 
                str(row['tidalheight']),
                )

    except Exception, e:
        print e

if __name__ == "__main__":
    main()
