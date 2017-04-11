#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class WagasciBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, Material=None, NElements=None,  InsideGap=None,
                    TranspV=None, Rotation=None, **kwds ):
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.NElements, self.InsideGap = ( NElements, InsideGap )
        self.TranspV, self.Rotation = ( TranspV, Rotation )

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")
        self.add_volume( main_lv )

        # definition local rotation
        rotation = geom.structure.Rotation( self.name+'_rot', str(self.Rotation[0]),
                                                str(self.Rotation[1]),  str(self.Rotation[2]) )

        sb_dim = [Q('0cm'),Q('0cm'),Q('0cm')]
        gap_step = Q('0cm')
        for i,sb in enumerate(self.get_builders()):
            sb_lv = sb.get_volume()
            sb_shape = geom.store.shapes.get(sb_lv.shape)
            sb_dim = [sb_dim[0]+sb_shape.dx,sb_dim[1]+sb_shape.dy,sb_dim[2]+sb_shape.dz]
            gap_step = gap_step+self.InsideGap[i]

        # calculate the joint step size
        sb_dim_step = [t*d for t,d in zip(self.TranspV,sb_dim)]

        sb_dim = [Q('0cm'),Q('0cm'),Q('0cm')]
        gap = Q('0cm')
        for i,sb in enumerate(self.get_builders()):
            sb_lv = sb.get_volume()
            sb_shape = geom.store.shapes.get(sb_lv.shape)
            sb_dim = [sb_dim[0]+sb_shape.dx,sb_dim[1]+sb_shape.dy,sb_dim[2]+sb_shape.dz]
            gap = gap+self.InsideGap[i]
            # lower edge, the compute dimension projected on transportation vector
            low_edge = [-t*(d-sbd-gap) for t,d,sbd in zip(self.TranspV,main_hDim,sb_dim)]
            for elem in range(self.NElements):
                # calculate the distance for n elements = i*2*halfdimension+gap
                temp_v = [elem*(2*d+gap)*t for d,t in zip(sb_dim_step,self.TranspV)]
                # define the position for the element based on edge
                temp_v = [te+le for te,le in zip(temp_v,low_edge)]
                # defining position, placement, and finally insert into the compule.
                sb_pos = geom.structure.Position(self.name+sb_lv.name+str(elem)+'_pos',
                                                        temp_v[0], temp_v[1], temp_v[2])
                sb_pla = geom.structure.Placement(self.name+sb_lv.name+str(elem)+'_pla',
                                                        volume=sb_lv, pos=sb_pos, rot =rotation)
                main_lv.placements.append(sb_pla.name)
