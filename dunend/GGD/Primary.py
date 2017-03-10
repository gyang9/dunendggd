#!/usr/bin/env python
'''
Subbuilder of Primary
'''

import gegede.builder
from gegede import Quantity as Q

class PrimaryBuilder(gegede.builder.Builder):
    '''
    Assemble all the subsystems into one bounding box.
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, ggdDimension=None, ggdMaterial=None, **kwds):
        self.ggdDimension = ggdDimension
        self.ggdMaterial  = ggdMaterial

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        main_shape = geom.shapes.Box( self.name, dx=self.ggdDimension[0], dy=self.ggdDimension[1], dz=self.ggdDimension[2] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.ggdMaterial, shape=main_shape )
        self.add_volume( main_lv )
        
        for sb in self.get_builders():
            sb_lv = sb.get_volume()
            sb_pos = [Q('0m'),Q('0m'),Q('0m')]
            sb_pla = geom.structure.Placement(sb_lv.name+'_pla', volume=sb_lv, pos=sb_pos)
            main_lv.placements.append(sb_pla.name )


