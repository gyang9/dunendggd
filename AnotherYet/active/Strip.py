#!/usr/bin/env python
'''
Subbuilder of PlaneBuilder
'''

import gegede.builder
from gegede import Quantity as Q

class StripBuilder(gegede.builder.Builder):
    '''
    Assemble all the subsystems into one bounding box.
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
                  StripDet = [Q('10cm'), Q('10cm'), Q('4m')], StripMat = 'Steel',
                  nStrip = 120 , lowEnd = Q('-2m'), StripDis = Q('5cm'), StripWidth = Q('1cm'), StripLeng = Q('4m'), # [Q('4m'), Q('6m')],
                  **kwds):
        print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        self.StripMat   = StripMat 
        self.StripDet   = StripDet 
        self.nStrip     = nStrip 
        self.lowEnd    = lowEnd
        self.StripDis   = StripDis
        self.StripWidth = StripWidth
        self.StripLeng  = StripLeng

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        print '****************************************'
        # vol is a bounding box ~ not corresponding to physical volume.
        #  assume Barrel biggest in x and y

        self.nStripa     = self.nStrip
        self.lowEnda    = self.lowEnd
        self.StripDisa   = self.StripDis
							        
        # Make detector box
        secStripShape = geom.shapes.Tubs('ShapeVol', '0cm', self.StripWidth, self.StripLeng)

        secStrip_lv = geom.structure.Volume('volStrip', material=self.StripMat, shape=secStripShape )

        self.add_volume(secStrip_lv)
        print '----------------------------------------'
     
