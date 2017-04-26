#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class SimpleSubDetectorBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, Material=None, NElements=None,  InsideGap=None,
                    TranspV=None, Rotation=None, Sensitive=None, **kwds ):
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.NElements, self.InsideGap = ( NElements, InsideGap )
        self.TranspV, self.Rotation = ( TranspV, Rotation )
        self.Sensitive = Sensitive

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")
        if isinstance(self.Sensitive,str):
            main_lv.params.append(("SensDet",self.Sensitive))
        self.add_volume( main_lv )

        # definition local rotation
        rotation = geom.structure.Rotation( self.name+'_rot', str(self.Rotation[0]),
                                                str(self.Rotation[1]),  str(self.Rotation[2]) )

        # get sub-builders and its logic volume
        el_sb = self.get_builder()
        el_lv = el_sb.get_volume()

        # get the sub-builder dimension, using its shape
        el_shape = geom.store.shapes.get(el_lv.shape)
        el_dim = [el_shape.dx, el_shape.dy, el_shape.dz]

        # calculate half dimension of element plus the gap projected to the transportation vector
        sb_dim_v = [t*(d+0.5*self.InsideGap) for t,d in zip(self.TranspV,el_dim)]

        # lower edge, the ule dimension projected on transportation vector
        low_end_v  = [-t*d+ed for t,d,ed in zip(self.TranspV,main_hDim,sb_dim_v)]

        for element in range(self.NElements):
            # calculate the distance for n elements = i*2*halfdinemsion
            temp_v = [element*2*d for d in sb_dim_v]
            # define the position for the element based on edge
            temp_v = [te+l for te,l in zip(temp_v,low_end_v)]
            # defining position, placement, and finally insert into the ule.
            el_pos = geom.structure.Position(self.name+"_el"+str(element)+'_pos', temp_v[0], temp_v[1], temp_v[2])
            el_pla = geom.structure.Placement(self.name+"_el"+str(element)+'_pla', volume=el_lv,
                                                pos=el_pos, rot =rotation)
            main_lv.placements.append(el_pla.name)
