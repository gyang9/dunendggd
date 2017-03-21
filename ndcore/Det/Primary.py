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

        # definition local rotation
        rotation = geom.structure.Rotation( self.name+'_rot', str(self.ggdRotation[0]),
                                                str(self.ggdRotation[1]),  str(self.ggdRotation[2]) )

        # lower edge, using builder and sub-builder dimension projected on transportation vector
        low_edge = [-t*d for t,d in zip(self.ggdTranspV,self.ggdDimension)]

        for i,sb in enumerate(self.get_builders()):
            sb_lv = sb.get_volume()
            sb_shape = geom.store.shapes.get(sb_lv.shape)
            sb_dim = [sb_shape.dx,sb_shape.dy,sb_shape.dz]
            # lower edge, using builder and sub-builder dimension projected on transportation vector
            low_edge = [le+t*(sbd+self.ggdInsideGap[i]) for le,t,sbd in zip(low_edge, self.ggdTranspV,sb_dim)]
            # defining position, placement, and finally insert into main logic volume.
            sb_pos = geom.structure.Position(self.name+sb_lv.name+'_pos',
                                                low_edge[0], low_edge[1], low_edge[2])
            sb_pla = geom.structure.Placement(self.name+sb_lv.name+'_pla',
                                                volume=sb_lv, pos=sb_pos, rot =rotation)
            main_lv.placements.append(sb_pla.name)
            low_edge = [le+t*sbd for le,t,sbd in zip(low_edge, self.ggdTranspV,sb_dim)]
