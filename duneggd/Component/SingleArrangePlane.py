#!/usr/bin/env python
import gegede.builder
from gegede import Quantity as Q
import duneggd.localtools as localtools

class SingleArrangePlaneBuilder(gegede.builder.Builder):

    ## The configure
    def configure( self, halfDimension=None, Material=None,
                    NElements=None, InsideGap=None, TranspV=None, Rotation=None, **kwds ):
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.NElements, self.InsideGap = ( NElements, InsideGap )
        self.TranspV, self.Rotation = ( TranspV, Rotation )
        pass

    ## The construct
    def construct( self, geom ):
        main_shape = geom.shapes.Box( self.name, dx=self.halfDimension['dx'],
                                        dy=self.halfDimension['dy'], dz=self.halfDimension['dz'] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.Material, shape=main_shape )
        self.add_volume( main_lv )

        # definition local rotation
        rotation = geom.structure.Rotation( self.name+'_rot', str(self.Rotation[0]),
                                            str(self.Rotation[1]),  str(self.Rotation[2]) )

        # get sub-builders and its logic volume
        el_sb = self.get_builder()
        el_lv = el_sb.get_volume()

        # get the sub-builder dimension, using its shape
        el_shape = geom.store.shapes.get(el_lv.shape)
        el_dim = localtools.getShapeDimensions( el_shape )
        # calculate half dimension of element plus the gap projected to the transportation vector
        sb_dim_v = [t*(d+0.5*self.InsideGap) for t,d in zip(self.TranspV,el_dim)]

        # lower edge, the ule dimension projected on transportation vector
        low_end_v  = [-t*d+ed for t,d,ed in zip(self.TranspV,self.Dimension,sb_dim_v)]

        for element in range(self.NElements):
            # calculate the distance for n elements = i*2*halfdinemsion
            temp_v = [element*2*d for d in sb_dim_v]
            # define the position for the element based on edge
            temp_v = [te+l for te,l in zip(temp_v,low_end_v)]
            # defining position, placement, and finally insert into the ule.
            el_pos = geom.structure.Position(self.name+"_el"+str(element)+'_pos', temp_v[0], temp_v[1], temp_v[2])
            el_pla = geom.structure.Placement(self.name+"_el"+str(element)+'_pla',
                                                volume=el_lv, pos=el_pos, rot =rotation)
            main_lv.placements.append(el_pla.name)
