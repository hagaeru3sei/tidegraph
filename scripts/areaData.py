#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import tornado.escape
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

def main():
    conn = MySQLdb.connect(host='localhost',user='root',
                           passwd='',
                           db='tide2',
                           charset='utf8')
    cur = conn.cursor(MySQLdb.cursors.DictCursor)

    #cur.execute("SELECT * FROM area")
    #row = cur.fetchone()
    #while row:
    #    print row['areaname']
    #    row = cur.fetchone()

    def getStateData():
        cur.execute("SELECT * FROM state")
        row = cur.fetchone()
        r = {}
        while row:
            r[row['stateid']] = row['statename']
            row = cur.fetchone()

        return r

    def getAreaData(state=True):
        """getAreaData
        return dict
        """
        r = {}
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
        return r

    states = getStateData() 
    d = getAreaData(True)
    for i in sorted(d):
        print states[i]
        for k, area in d[i].iteritems():
            #print "\t%s\t%s" % (k, area['location'],)
            print "\t"+str(k), area

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
