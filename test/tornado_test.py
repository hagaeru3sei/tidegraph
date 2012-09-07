# -*- coding:utf-8 -*-
import unittest
import pprint
import main

pp = pprint.PrettyPrinter(indent=4)

class TestTornado(unittest.TestCase):
    """TestTornado
    """
    
    def setUp(self):
        """
        """
        pass

    def test_defaultPort(self):
        """test_example
        """
        try:
            if main.Port != 8888:
                raise Exception('Port is not 8888') 
        except Exception, e:
            self.fail("example test exception. %s" % e)

    def test_appHome(self):
        """test_appHome
        """
        try:
            if main.HOME != '/opt/tornado':
                raise Exception('HOME is not /opt/tornado')
        except Exception, e:
            self.fail("%s" % e)

    def test_mongoConnSettings(self):
        """test_mongoConnSettings
        """
        try:
            if main.DB['name'] != 'localhost':
                raise Exception('hostname is not localhost')
            if main.DB['db'] != 'tide':
                raise Exception('db is not test')
            if main.DB['port'] != 27017:
                raise Exception('port is not 27017')
        except Exception, e:
            self.fail("%s" % e)

    def tearDown(self):
        """
        """
        pass

def suite():
    """
    """
    suite = unittest.TestSuite()
    tests = [TestTornado]
    
    suite.addTests(map(unittest.makeSuite, tests))

    return suite
