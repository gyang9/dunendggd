#!/usr/bin/env python
'''
Subbuilder of DetEncBuilder
'''

import gegede.builder
from gegede import Quantity as Q

class WireBuilder(gegede.builder.Builder):
    '''
    Assemble all the subsystems into one bounding box.
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
                  wireDet = [Q('10cm'), Q('10cm'), Q('4m')], WireMat = 'Steel',
                  nWire = 120 , lowEnd = Q('-2m'), wireDis = Q('5cm'), wireWidth = Q('1cm'), wireLeng = Q('4m'), # [Q('4m'), Q('6m')],
                  **kwds):
        print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        self.WireMat   = WireMat 
        self.wireDet   = wireDet 
        self.nWire     = nWire 
        self.lowEnd    = lowEnd
        self.wireDis   = wireDis
        self.wireWidth = wireWidth
        self.wireLeng  = wireLeng

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        print '****************************************'
        # vol is a bounding box ~ not corresponding to physical volume.
        #  assume Barrel biggest in x and y

        self.nWirea     = self.nWire
        self.lowEnda    = self.lowEnd
        self.wireDisa   = self.wireDis
							        
        # Make detector box
        WireShape = geom.shapes.Tubs('ShapeVol', '0cm', self.wireWidth, self.wireLeng)

        wire_lv = geom.structure.Volume('volWire', material=self.WireMat, shape=WireShape )

        self.add_volume(wire_lv)
        print '----------------------------------------'
     
