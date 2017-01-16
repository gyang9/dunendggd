#!/usr/bin/env python
'''
Subbuilder of SecondaryBuilder
'''

import gegede.builder
from gegede import Quantity as Q

class HCalBuilder(gegede.builder.Builder):
    '''
    Assemble all the subsystems into one bounding box.
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
                  HCalDim = None, HCalMat = 'Air', 
                  ModulePos = [Q('100m'),Q('100m'),Q('0m')],  
                  **kwds):

        self.HCalMat    = HCalMat 
        self.HCalDim    = HCalDim
        self.ModulePos  = ModulePos 

        self.ModuleBldr   = self.get_builder('Module')

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        # generate HCal lv 

        HCalBox = geom.shapes.Box(self.name, self.HCalDim[0], self.HCalDim[1], self.HCalDim[2])
       
        HCal_lv = geom.structure.Volume('vol'+self.name, material=self.HCalMat , shape=HCalBox )

        self.add_volume(HCal_lv)

        # Get Module lv

        Module_lv  = self.ModuleBldr.get_volume('volModule')
 

        # Position of the Module

        HCalModule_Pos = geom.structure.Position('HCalModule_pos', self.ModulePos[0], self.ModulePos[1], self.ModulePos[2])
							        
        # Make Module box
       
        pModule_lv = geom.structure.Placement('place_HCalModule', volume = Module_lv, pos = HCalModule_Pos)

        HCal_lv.placements.append(pModule_lv.name )


    	return
