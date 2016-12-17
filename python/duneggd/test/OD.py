#!/usr/bin/env python
'''
Subbuilder of DetEncBuilder
'''

import gegede.builder
from gegede import Quantity as Q

class ODBuilder(gegede.builder.Builder):
    '''
    Assemble all the subsystems into one bounding box.
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
                  ODDim = [Q('10m'), Q('10m'), Q('10m')], ODMat = 'Air', 
                  ECalPos = [Q('0m'),Q('0m'),Q('0m')],  HCalPos = [Q('15m'),Q('0m'),Q('0m')],
                  **kwds):

        self.ODMat      = ODMat
        self.ODDim      = ODDim 
        self.ECalPos    = ECalPos
        self.HCalPos    = HCalPos

        self.ECalBldr   = self.get_builder('ECal')
        self.HCalBldr   = self.get_builder('HCal')

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        # generate OD lv 

        IOBox = geom.shapes.Box(self.name, self.ODDim[0], self.ODDim[1], self.ODDim[2])
       
        OD_lv = geom.structure.Volume('vol'+self.name, material=self.ODMat, shape=ODBox )

        self.add_volume(OD_lv)

        # Get ECal lv

        ECal_lv  = self.LArDBldr.get_volume('volECal')
 

        # Position of the ECal

        ECal_Pos = geom.structure.Position('LArD_pos', self.ECalPos[0], self.ECalPos[1], self.ECalPos[2])
							        
        # Make ECal box
       
        pECal_lv = geom.structure.Placement('place_LAr', volume = ECal_lv, pos = ECal_Pos)

        OD_lv.placements.append(pLArBox_lv.name )

        print '########################################'

        # Get HCal lv

        HCal_lv  = self.HCalBldr.get_volume('volHCal')
 

        # Position of the HCal

        HCal_Pos = geom.structure.Position('HCal_pos', self.HCalPos[0], self.HCalPos[1], self.HCalPos[2])
							        
        # Make ECal box
       
        pHCal_lv = geom.structure.Placement('place_HCal', volume = HCal_lv, pos = HCal_Pos)

        OD_lv.placements.append(pHCal_lv.name )

    	return
