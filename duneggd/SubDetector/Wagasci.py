#!/usr/bin/env python
## Subbuilder of WagasciBuilder
#

import gegede.builder
from gegede import Quantity as Q

## WagasciBuilder
#
# builder for mod SubDet
class WagasciBuilder(gegede.builder.Builder):

    ## The configure
    def configure( self, modDimension=None, modMaterial=None, modNElements=None,  modInsideGap=None,
                    modTranspV=None, modRotation=None, **kwds ):
        self.modDimension, self.modMaterial = ( modDimension, modMaterial )
        self.modNElements, self.modInsideGap = ( modNElements, modInsideGap )
        self.modTranspV, self.modRotation = ( modTranspV, modRotation )
        pass

    ## The construct
    def construct( self, geom ):
        main_shape = geom.shapes.Box( self.name+"_shape", dx = self.modDimension[0],
                                        dy = self.modDimension[1], dz = self.modDimension[2] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.modMaterial, shape=main_shape )
        self.add_volume( main_lv )

        # definition local rotation
        rotation = geom.structure.Rotation( self.name+'_rot', str(self.modRotation[0]),
                                                str(self.modRotation[1]),  str(self.modRotation[2]) )

        sb_dim = [Q('0cm'),Q('0cm'),Q('0cm')]
        gap_step = Q('0cm')
        for i,sb in enumerate(self.get_builders()):
            sb_lv = sb.get_volume()
            sb_shape = geom.store.shapes.get(sb_lv.shape)
            sb_dim = [sb_dim[0]+sb_shape.dx,sb_dim[1]+sb_shape.dy,sb_dim[2]+sb_shape.dz]
            gap_step = gap_step+self.modInsideGap[i]

        # calculate the joint step size
        sb_dim_step = [t*d for t,d in zip(self.modTranspV,sb_dim)]

        sb_dim = [Q('0cm'),Q('0cm'),Q('0cm')]
        gap = Q('0cm')
        for i,sb in enumerate(self.get_builders()):
            sb_lv = sb.get_volume()
            sb_shape = geom.store.shapes.get(sb_lv.shape)
            sb_dim = [sb_dim[0]+sb_shape.dx,sb_dim[1]+sb_shape.dy,sb_dim[2]+sb_shape.dz]
            gap = gap+self.modInsideGap[i]
            # lower edge, the compute dimension projected on transportation vector
            low_edge = [-t*(d-sbd-gap) for t,d,sbd in zip(self.modTranspV,self.modDimension,sb_dim)]
            for elem in range(self.modNElements):
                # calculate the distance for n elements = i*2*halfdimension+gap
                temp_v = [elem*(2*d+gap)*t for d,t in zip(sb_dim_step,self.modTranspV)]
                # define the position for the element based on edge
                temp_v = [te+le for te,le in zip(temp_v,low_edge)]
                # defining position, placement, and finally insert into the compule.
                sb_pos = geom.structure.Position(self.name+sb_lv.name+str(elem)+'_pos',
                                                        temp_v[0], temp_v[1], temp_v[2])
                sb_pla = geom.structure.Placement(self.name+sb_lv.name+str(elem)+'_pla',
                                                        volume=sb_lv, pos=sb_pos, rot =rotation)
                main_lv.placements.append(sb_pla.name)
