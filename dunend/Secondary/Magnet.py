#!/usr/bin/env python
'''
Subbuilder of SecondaryBuilder
'''

import gegede.builder
from gegede import Quantity as Q

class MagnetBuilder(gegede.builder.Builder):
    '''
    Assemble all the subsystems into one bounding box.
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
                  MagnetDim = None, MagnetMat = 'Steel',
                  **kwds):
        print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        self.MagnetMat = MagnetMat 
        self.MagnetDet = MagnetDim 

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        print '****************************************'
        # vol is a bounding box ~ not corresponding to physical volume.
        #  assume Barrel biggest in x and y

							        
        # Make detector box
        MagnetShape = geom.shapes.Box('ShapeMagnet', self.MagnetDet[0], self.MagnetDet[1], self.MagnetDet[2])

        Magnet_lv = geom.structure.Volume('volMagnet', material=self.MagnetMat , shape=MagnetShape )

        self.add_volume(Magnet_lv)
        print '----------------------------------------' 
     
