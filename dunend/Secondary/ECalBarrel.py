#!/usr/bin/env python
'''
Subbuilder of SecondaryBuilder
'''

import gegede.builder
from gegede import Quantity as Q

class ECalBarrelBuilder(gegede.builder.Builder):
    '''
    Assemble all the subsystems into one bounding box.
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
                  ECalBarrelDim = None, ECalMat = 'Air', 
                  ModulePos = None,  
                  **kwds):

        self.ECalMat    = ECalMat 
        self.ECalDim    = ECalBarrelDim 
        self.ModulePos  = ModulePos 

        self.ModuleBldr   = self.get_builder('Module')

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        # generate ECal lv 

        ECalBarrelBox = geom.shapes.Box(self.name, self.ECalDim[0], self.ECalDim[1], self.ECalDim[2])
       
        ECalBarrel_lv = geom.structure.Volume('vol'+self.name, material=self.ECalMat , shape=ECalBarrelBox )
        
        self.add_volume(ECalBarrel_lv)

        # Get Module lv

        secModule_lv  = self.ModuleBldr.get_volume('volModule')
 

        # Position of the Module

        ECalModule_Pos = geom.structure.Position('ECalModule_pos'+self.name, self.ModulePos[0], self.ModulePos[1], self.ModulePos[2])
							        
        # Make Module box
       
        pModule_lv = geom.structure.Placement('place_ECalModule'+self.name, volume = secModule_lv, pos = ECalModule_Pos)

        ECalBarrel_lv.placements.append(pModule_lv.name ) 


    	return
