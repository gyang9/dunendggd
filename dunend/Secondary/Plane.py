#!/usr/bin/env python
'''
Subbuilder of ModuleBuilder
'''

import gegede.builder
from gegede import Quantity as Q

class PlaneBuilder(gegede.builder.Builder):
    '''
    Assemble all the subsystems into one bounding box.
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
                  PlaneDim = [Q('10m'), Q('10m'), Q('10m')], PlaneMat = 'Air', 
                  StripPos = [Q('0m'),Q('0m'),Q('0m')],  
                  **kwds):

        self.PlaneMat    = PlaneMat 
        self.PlaneDim    = PlaneDim
        self.StripPos    = StripPos 

        self.StripBldr   = self.get_builder('Strip')

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        # generate Plane lv 

        PlaneBox = geom.shapes.Box(self.name, self.PlaneDim[0], self.PlaneDim[1], self.PlaneDim[2])
       
        Plane_lv = geom.structure.Volume('vol'+self.name, material=self.PlaneMat, shape=PlaneBox )

        self.add_volume(Plane_lv)

        # Get Strip lv

        Strip_lv  = self.StripBldr.get_volume('volStrip')
 

        # Position of the Strip

        Strip_Pos = geom.structure.Position('Strip_pos', self.StripPos[0], self.StripPos[1], self.StripPos[2])
							        
        # Make Strip box
       
        pStrip_lv = geom.structure.Placement('place_Strip', volume = Strip_lv, pos = Strip_Pos)

        Plane_lv.placements.append(pStrip_lv.name )


    	return
