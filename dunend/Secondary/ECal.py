#!/usr/bin/env python
'''
Subbuilder of SecondaryBuilder
'''

import gegede.builder
from gegede import Quantity as Q

class ECalBuilder(gegede.builder.Builder):
    '''
    Assemble all the subsystems into one bounding box.
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
                  ECalDim = None, ECalMat = 'Air', 
                  ModulePos = [Q('100m'),Q('0m'),Q('0m')],  
                  **kwds):

        self.ECalMat    = ECalMat 
        self.ECalDim    = ECalDim
        self.ModulePos  = ModulePos 

        self.ModuleBldr   = self.get_builder('Module')

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        # generate ECal lv 

        ECalBox = geom.shapes.Box(self.name, self.ECalDim[0], self.ECalDim[1], self.ECalDim[2])
       
        ECal_lv = geom.structure.Volume('vol'+self.name, material=self.ECalMat , shape=ECalBox )

        self.add_volume(ECal_lv)

        # Get Module lv

        Module_lv  = self.ModuleBldr.get_volume('volModule')
 

        # Position of the Module

        ECalModule_Pos = geom.structure.Position('ECalModule_pos', self.ModulePos[0], self.ModulePos[1], self.ModulePos[2])
							        
        # Make Module box
       
        pModule_lv = geom.structure.Placement('place_ECalModule', volume = Module_lv, pos = ECalModule_Pos)

        ECal_lv.placements.append(pModule_lv.name )


    	return
