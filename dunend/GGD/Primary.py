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
    def configure(self, ggdDimension=None, ggdMaterial=None, ggdInsideGap=None,
                        ggdTranspV=None, ggdRotation=None, **kwds):
        self.ggdDimension, self.ggdMaterial = ( ggdDimension, ggdMaterial )
        self.ggdInsideGap = ggdInsideGap
        self.ggdTranspV, self.ggdRotation = ( ggdTranspV, ggdRotation )

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        main_shape = geom.shapes.Box( self.name, dx=self.ggdDimension[0], 
                                        dy=self.ggdDimension[1], dz=self.ggdDimension[2] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.ggdMaterial, shape=main_shape )
        self.add_volume( main_lv )
        
        postemp = [Q('0m'),Q('0m'),Q('0m')]
        for i,sb in enumerate(self.get_builders()):
            sb_lv = sb.get_volume()
            sb_shape = geom.store.shapes.get(sb_lv.shape)
            sb_dim = [sb_shape.dx,sb_shape.dy,sb_shape.dz]
            postemp = [pt+(self.ggdInsideGap[i]+d)*t for pt,d,t in zip(postemp, sb_dim, self.ggdTranspV)]
            sb_pos = geom.structure.Position( sb_lv.name+'_pos', postemp[0], postemp[1], postemp[2])
            sb_pla = geom.structure.Placement(sb_lv.name+'_pla', volume=sb_lv, pos=sb_pos)
            main_lv.placements.append(sb_pla.name )

