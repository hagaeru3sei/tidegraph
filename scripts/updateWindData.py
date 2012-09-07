#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import datetime
import pytz
import pymongo
import MySQLdb
import urllib2
from xml.etree.ElementTree import ElementTree, register_namespace, _namespace_map, tostring

WINDAPI="http://tenki.jp/component/static_api/rss/amedas/wind_pref_%s.xml"
PLACES=[]
UTC=pytz.timezone('UTC')
JST=pytz.timezone('Asia/Tokyo')

def main():

    patt = re.compile(u"^.* \[ ([0-9]+)*.* \] ([東西南北]+).*([0-9]+)m/s$")
    d = datetime.datetime.now().replace(tzinfo=UTC).astimezone(JST)
    locations= {}

    try:
        db = pymongo.Connection('localhost', 27017)['tide']

        conn = MySQLdb.connect(host='localhost',user='root',
                               passwd='',
                               db='tide2',
                               port=3306,
                               charset='utf8')
        cur = conn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM location_code WHERE codenamejp IS NOT NULL")
        row = cur.fetchone()
        while row:
            PLACES.append(row['codenamejp'])
            locations[row['codenamejp']] = row['location']
            row = cur.fetchone()

        cur.execute("SELECT * FROM state s LEFT JOIN state_has_tenkijpPref sh ON (s.stateid=sh.stateid) WHERE sh.prefid>0")
        areas = []
        row = cur.fetchone()
        while row:
            areas.append(row['prefid'])
            row = cur.fetchone()

        cur.close()
        conn.close()

        #register_namespace('tenkiJP', 'http://tenki.jp/ns/rss/2.0')

        for prefid in areas:
            fh    = urllib2.urlopen(WINDAPI % prefid)
            rss   = ElementTree(file=fh)
            items = rss.findall('.//item')
            for item in items:
                title = item.find('title').text
                place = item.find('{http://tenki.jp/ns/rss/2.0}amedas').attrib['name']

                if place in PLACES:
                    m = patt.match(title)
                    hour, wind_direction, wind_speed = int(m.group(1)), m.group(2), int(m.group(3))
                    yy = int(d.strftime('%Y'))
                    mm = int(d.strftime('%m'))
                    dd = int(d.strftime('%d'))
                    hh = int(d.strftime('%H'))
                    dt = datetime.datetime(yy, mm, dd, hh).replace(tzinfo=JST)
                    doc = {'location':locations[place], 'wind_speed':wind_speed,'wind_direction':wind_direction, 'datetime':dt}
                    #print doc
                    db.wind.insert(doc)

    except Exception, e:
        print e

if __name__ == "__main__":
    main()
