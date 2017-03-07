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
                  SecondaryDim = [Q('20m'), Q('20m'), Q('40m')], SecondaryMat = 'Air', 
                  ECalPos = None,  HCalPos = None, ECalBarrelPos = None, ECalBarrelPos2 = None, ECalBarrelPos3 = None, ECalBarrelPos4 = None, 
                  MagnetPos = None, MagnetPos2 = None,                  
                  **kwds):

        self.SecondaryMat      = SecondaryMat
        self.SecondaryDim      = SecondaryDim 
        self.ECalPos    = ECalPos
        self.ECalBarrelPos    = ECalBarrelPos
        self.ECalBarrelPos2    = ECalBarrelPos2
        self.ECalBarrelPos3    = ECalBarrelPos3
        self.ECalBarrelPos4    = ECalBarrelPos4
        self.HCalPos    = HCalPos
        self.MagnetPos    = MagnetPos
        self.MagnetPos2    = MagnetPos2

        self.ECalBldr   = self.get_builder('ECal')
        self.ECalBarrelBldr   = self.get_builder('ECalBarrel')
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

        # Get ECal Barrel lv

        ECalBarrel_lv  = self.ECalBarrelBldr.get_volume('volECalBarrel')
 

        # Position of the ECal Barrel

        ECalBarrel_Pos = geom.structure.Position('ECalBarrel_pos', self.ECalBarrelPos[0], self.ECalBarrelPos[1], self.ECalBarrelPos[2])
							        
        # Make ECal Barrel box
       
        pECalBarrel_lv = geom.structure.Placement('place_ECalECalBarrel', volume = ECalBarrel_lv, pos = ECalBarrel_Pos)

        Secondary_lv.placements.append(pECalBarrel_lv.name )


        ECalBarrel_Pos2 = geom.structure.Position('ECalBarrel_pos2', self.ECalBarrelPos2[0], self.ECalBarrelPos2[1], self.ECalBarrelPos2[2])
        pECalBarrel_lv2 = geom.structure.Placement('place_ECalECalBarrel2', volume = ECalBarrel_lv, pos = ECalBarrel_Pos2, rot = "r90aboutZ")
        Secondary_lv.placements.append(pECalBarrel_lv2.name )

        ECalBarrel_Pos3 = geom.structure.Position('ECalBarrel_pos3', self.ECalBarrelPos3[0], self.ECalBarrelPos3[1], self.ECalBarrelPos3[2])
        pECalBarrel_lv3 = geom.structure.Placement('place_ECalECalBarrel3', volume = ECalBarrel_lv, pos = ECalBarrel_Pos3 )
        Secondary_lv.placements.append(pECalBarrel_lv3.name )

        ECalBarrel_Pos4 = geom.structure.Position('ECalBarrel_pos4', self.ECalBarrelPos4[0], self.ECalBarrelPos4[1], self.ECalBarrelPos4[2])
        pECalBarrel_lv4 = geom.structure.Placement('place_ECalECalBarrel4', volume = ECalBarrel_lv, pos = ECalBarrel_Pos4, rot = "r90aboutZ")
        Secondary_lv.placements.append(pECalBarrel_lv4.name )

        print '########################################'

        # Get HCal lv

        HCal_lv  = self.HCalBldr.get_volume('volHCal')
 

        # Position of the HCal

        HCal_Pos = geom.structure.Position('HCal_pos', self.HCalPos[0], self.HCalPos[1], self.HCalPos[2])
							        
        # Make DownStream ECal box
       
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



        Magnet_Pos2 = geom.structure.Position('Magnet_pos2', self.MagnetPos2[0], self.MagnetPos2[1], self.MagnetPos2[2])  
        pMagnet_lv2 = geom.structure.Placement('place_Magnet2', volume = Magnet_lv, pos = Magnet_Pos2)
        Secondary_lv.placements.append(pMagnet_lv2.name )


    	return
