#!/usr/bin/env python

import sys
import os
import unittest

sys.path.append('../')

import dirpylint as mod



def suite():

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestLeveler))

    return suite

class TestLeveler(unittest.TestCase):

    def testOne(self):
        self.assertEqual(mod.Leveler(2,'/home/william/Projects','/home', 'False'), True)
        self.assertEqual(mod.Leveler(0,'/home/william/Projects','/home', 'False'), False)
        self.assertEqual(mod.Leveler(0,'/home','/home', 'False'), True)

    def testTwo(self):
        self.assertEqual(mod.Leveler(0,'/home','/home','False'), True)

    def testThree(self):
        self.assertEqual(mod.Leveler(0,'/home/william/Projects','/home','/home/william'), False)


if __name__ == '__main__':
   unittest.main(defaultTest="suite")
    
