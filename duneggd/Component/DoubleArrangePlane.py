#!/usr/bin/env python
import gegede.builder
from gegede import Quantity as Q

class DoubleArrangePlaneBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, Material=None,
                    NElements1=None, InsideGap1=None,
                    TranspV1=None, Rotation1=None,
                    NElements2=None, InsideGap2=None,
                    TranspV2=None, **kwds ):
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.NElements1, self.InsideGap1 = ( NElements1, InsideGap1 )
        self.NElements2, self.InsideGap2 = ( NElements2, InsideGap2 )
        self.TranspV1, self.Rotation1 = ( TranspV1, Rotation1 )
        self.TranspV2 = TranspV2

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        main_shape = geom.shapes.Box( self.name, dx=self.halfDimension['dx'],
                                        dy=self.halfDimension['dy'], dz=self.halfDimension['dz'] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.Material, shape=main_shape )
        self.add_volume( main_lv )

        # definition local rotation
        rotation1 = geom.structure.Rotation( self.name+'_rot1', str(self.Rotation1[0]),
                                            str(self.Rotation1[1]),  str(self.Rotation1[2]) )

        # get sub-builders and its logic volume
        el_sb = self.get_builder()
        el_lv = el_sb.get_volume()

        # get the sub-builder dimension, using its shape
        el_shape = geom.store.shapes.get(el_lv.shape)
        el_dim = [el_shape.dx, el_shape.dy, el_shape.dz]

        # calculate half dimension of element plus the gap projected to the transportation vector
        sb_dim_v1 = [t*(d+0.5*self.InsideGap1) for t,d in zip(self.TranspV1,el_dim)]
        sb_dim_v2 = [t*(d+0.5*self.InsideGap2) for t,d in zip(self.TranspV2,el_dim)]

        # lower edge, the ule dimension projected on transportation vector
        low_end_v1  = [-t*d+ed for t,d,ed in zip(self.TranspV1,self.Dimension,sb_dim_v1)]
        low_end_v2  = [-t*d+ed for t,d,ed in zip(self.TranspV2,self.Dimension,sb_dim_v2)]

        for elem2 in range(self.NElements2):
            for elem1 in range(self.NElements1):
                # calculate the distance for n elements = i*2*halfdinemsion
                temp_v = [elem1*2*d1+elem2*2*d2 for d1,d2 in zip(sb_dim_v1,sb_dim_v2)]
                # define the position for the element based on edge
                temp_v = [te+l1+l2 for te,l1,l2 in zip(temp_v,low_end_v1,low_end_v2)]
                # defining position, placement, and finally insert into the ule.
                el_pos = geom.structure.Position(self.name+"_el"+str(elem1)+'_'+str(elem2)+'_pos',
                                                    temp_v[0], temp_v[1], temp_v[2])
                el_pla = geom.structure.Placement(self.name+"_el"+str(elem1)+'_'+str(elem2)+'_pla',
                                                    volume=el_lv, pos=el_pos, rot =rotation1)
                main_lv.placements.append(el_pla.name)
