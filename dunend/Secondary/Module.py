#!/usr/bin/env python
'''
Subbuilder of ECalandHCalBuilder
'''

import gegede.builder
from gegede import Quantity as Q

class ModuleBuilder(gegede.builder.Builder):
    '''
    Assemble all the subsystems into one bounding box.
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
                  ModuleDim = [Q('10m'), Q('10m'), Q('10m')], ModuleMat = 'Air', 
                  PlanePos = [Q('0m'),Q('0m'),Q('0m')],  
                  **kwds):

        self.ModuleMat    = ModuleMat 
        self.ModuleDim    = ModuleDim
        self.PlanePos     = PlanePos 

        self.PlaneBldr   = self.get_builder('Plane')

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        # generate Module lv 

        ModuleBox = geom.shapes.Box(self.name, self.ModuleDim[0], self.ModuleDim[1], self.ModuleDim[2])
       
        secModule_lv = geom.structure.Volume('vol'+self.name, material=self.ModuleMat , shape=ModuleBox )

        self.add_volume(secModule_lv) 

        # Get Plane lv

        secPlane_lv  = self.PlaneBldr.get_volume('volPlane')
 

        # Position of the Plane

        secPlane_Pos = geom.structure.Position('Plane_pos', self.PlanePos[0], self.PlanePos[1], self.PlanePos[2])
							        
        # Make Plane box
       
        pPlane_lv = geom.structure.Placement('place_Plane', volume = secPlane_lv, pos = secPlane_Pos)

        secModule_lv.placements.append(pPlane_lv.name )


    	return
