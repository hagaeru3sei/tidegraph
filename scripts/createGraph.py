#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import pylab

def main():
    try:
        x = range(24)
        y = [i*random.randint(2,4) for i in range(24)]
        b1 = pylab.bar(range(24),range(24))
        pylab.legend(b1[0], ('test'))
        pylab.plot(x, y)
        pylab.savefig("/usr/share/nginx/www/test.png")
        pylab.cla()
        
    except Exception, e:
        print e

if __name__ == "__main__":
    main()
