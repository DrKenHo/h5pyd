##############################################################################
# Copyright by The HDF Group.                                                #
# All rights reserved.                                                       #
#                                                                            #
# This file is part of H5Serv (HDF5 REST Server) Service, Libraries and      #
# Utilities.  The full HDF5 REST Server copyright notice, including          #
# terms governing use, modification, and redistribution, is contained in     #
# the file COPYING, which can be found at the root of the source code        #
# distribution tree.  If you do not have access to this file, you may        #
# request a copy from help@hdfgroup.org.                                     #
##############################################################################

import config

if config.get("use_h5py"):
    import h5py
else:
    import h5pyd as h5py
    
from common import ut, TestCase

        
class TestFile(TestCase):
    
    def test_version(self):
        version = h5py.version.version
        # should be of form "n.n.n"
        n = version.find(".")
        self.assertTrue(n>=1)
        m = version[(n+1):].find('.')
        self.assertTrue(n>=1)
         
        
    def test_create(self):
        filename = self.getFileName("new_file")
        print("filename:", filename)
         
        f = h5py.File(filename, 'w')
        self.assertEqual(f.filename, filename)
        self.assertEqual(f.name, "/")
        self.assertTrue(f.id.id is not None)
        self.assertEqual(len(f.keys()), 0)
        self.assertEqual(f.mode, 'r+')
        self.assertTrue('/' in f)      
        r = f['/']
        self.assertTrue(isinstance(r, h5py.Group))
        self.assertEqual(len(f.attrs.keys()), 0)
        f.close()
        self.assertEqual(f.id.id, 0)
        
        
        # re-open as read-write
        f = h5py.File(filename, 'r+')
        self.assertTrue(f.id.id is not None)
        self.assertEqual(f.mode, 'r+')
        self.assertEqual(len(f.keys()), 0)
        f.create_group("subgrp")
        self.assertEqual(len(f.keys()), 1)
        f.close()
        self.assertEqual(f.id.id, 0)
        
        # re-open as read-only
        f = h5py.File(filename, 'r')
        self.assertEqual(f.filename, filename)
        self.assertEqual(f.name, "/")
        self.assertTrue(f.id.id is not None)
        self.assertEqual(len(f.keys()), 1)
        self.assertEqual(f.mode, 'r')
        self.assertTrue('/' in f)      
        r = f['/']
        self.assertTrue(isinstance(r, h5py.Group))
        self.assertEqual(len(f.attrs.keys()), 0)
        
        try:
            f.create_group("another_subgrp")
            self.assertTrue(False)  # expect exception
        except ValueError:
            pass
        self.assertEqual(len(f.keys()), 1)
        
        f.close()
        self.assertEqual(f.id.id, 0)
        
        # open in truncate mode
        f = h5py.File(filename, 'w')
        self.assertEqual(f.filename, filename)
        self.assertEqual(f.name, "/")
        self.assertTrue(f.id.id is not None)
        self.assertEqual(len(f.keys()), 0)
        self.assertEqual(f.mode, 'r+')
        self.assertTrue('/' in f)      
        r = f['/']
        self.assertTrue(isinstance(r, h5py.Group))
        self.assertEqual(len(f.attrs.keys()), 0)
        
        f.close()
        self.assertEqual(f.id.id, 0)
           
        # verify open of non-existent file throws exception
        try:
            filename = self.getFileName("no_file_here")
            print("filename:", filename)
            f = h5py.File(filename, 'r')
            self.assertTrue(False) #expect exception
        except IOError:
            pass
        

         
        
if __name__ == '__main__':
    ut.main()


     
    
