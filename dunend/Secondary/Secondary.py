#!/usr/bin/env python
'''
Subbuilder of DetEncBuilder
'''

import gegede.builder
from gegede import Quantity as Q

class SecondaryBuilder(gegede.builder.Builder):
    '''
    Assemble all the subsystems into one bounding box.
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
                  SecondaryDim = [Q('10m'), Q('10m'), Q('10m')], SecondaryMat = 'Air', 
                  ECalPos = None,  HCalPos = None,
                  MagnetPos = None,                  
                  **kwds):

        self.SecondaryMat      = SecondaryMat
        self.SecondaryDim      = SecondaryDim 
        self.ECalPos    = ECalPos
        self.HCalPos    = HCalPos
        self.MagnetPos    = MagnetPos

        self.ECalBldr   = self.get_builder('ECal')
        self.HCalBldr   = self.get_builder('HCal')
        self.MagnetBldr   = self.get_builder('Magnet')

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        # generate Secondary lv 

        SecondaryBox = geom.shapes.Box(self.name, self.SecondaryDim[0], self.SecondaryDim[1], self.SecondaryDim[2])
       
        Secondary_lv = geom.structure.Volume('vol'+self.name, material=self.SecondaryMat, shape=SecondaryBox )

        self.add_volume(Secondary_lv)

        # Get ECal lv

        ECal_lv  = self.ECalBldr.get_volume('volECal')
 

        # Position of the ECal

        ECal_Pos = geom.structure.Position('ECal_pos', self.ECalPos[0], self.ECalPos[1], self.ECalPos[2])
							        
        # Make ECal box
       
        pECal_lv = geom.structure.Placement('place_ECal', volume = ECal_lv, pos = ECal_Pos)

        Secondary_lv.placements.append(pECal_lv.name )

        print '########################################'

        # Get HCal lv

        HCal_lv  = self.HCalBldr.get_volume('volHCal')
 

        # Position of the HCal

        HCal_Pos = geom.structure.Position('HCal_pos', self.HCalPos[0], self.HCalPos[1], self.HCalPos[2])
							        
        # Make ECal box
       
        pHCal_lv = geom.structure.Placement('place_HCal', volume = HCal_lv, pos = HCal_Pos)

        Secondary_lv.placements.append(pHCal_lv.name )

        print '########################################'

        # Get Magnet lv

        Magnet_lv  = self.MagnetBldr.get_volume('volMagnet')
 

        # Position of the Magnet

        Magnet_Pos = geom.structure.Position('Magnet_pos', self.MagnetPos[0], self.MagnetPos[1], self.MagnetPos[2])
							        
        # Make Magnet box
       
        pMagnet_lv = geom.structure.Placement('place_Magnet', volume = Magnet_lv, pos = Magnet_Pos)

        Secondary_lv.placements.append(pMagnet_lv.name )


    	return
