#!/usr/bin/env python
## Subbuilder of DoubleArrangeArrangePlaneBuilder
#

import gegede.builder
from gegede import Quantity as Q

class DoubleArrangePlaneBuilder(gegede.builder.Builder):

    ## The configure
    def configure( self, compDimension=None, compMaterial=None,
                    compNElements1=None, compInsideGap1=None,
                    compTranspV1=None, compRotation1=None,
                    compNElements2=None, compInsideGap2=None,
                    compTranspV2=None, **kwds ):
        self.compDimension, self.compMaterial = ( compDimension, compMaterial )
        self.compNElements1, self.compInsideGap1 = ( compNElements1, compInsideGap1 )
        self.compNElements2, self.compInsideGap2 = ( compNElements2, compInsideGap2 )
        self.compTranspV1, self.compRotation1 = ( compTranspV1, compRotation1 )
        self.compTranspV2 = compTranspV2

    ## The construct
    def construct( self, geom ):
        main_shape = geom.shapes.Box( self.name, dx=self.compDimension[0],
                                        dy=self.compDimension[1], dz=self.compDimension[2] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.compMaterial, shape=main_shape )
        self.add_volume( main_lv )

        # definition local rotation
        rotation1 = geom.structure.Rotation( self.name+'_rot1', str(self.compRotation1[0]),
                                            str(self.compRotation1[1]),  str(self.compRotation1[2]) )

        # get sub-builders and its logic volume
        el_sb = self.get_builder()
        el_lv = el_sb.get_volume()

        # get the sub-builder dimension, using its shape
        el_shape = geom.store.shapes.get(el_lv.shape)
        el_dim = [el_shape.dx, el_shape.dy, el_shape.dz]

        # calculate half dimension of element plus the gap projected to the transportation vector
        sb_dim_v1 = [t*(d+0.5*self.compInsideGap1) for t,d in zip(self.compTranspV1,el_dim)]
        sb_dim_v2 = [t*(d+0.5*self.compInsideGap2) for t,d in zip(self.compTranspV2,el_dim)]

        # lower edge, the compule dimension projected on transportation vector
        low_end_v1  = [-t*d+ed for t,d,ed in zip(self.compTranspV1,self.compDimension,sb_dim_v1)]
        low_end_v2  = [-t*d+ed for t,d,ed in zip(self.compTranspV2,self.compDimension,sb_dim_v2)]

        for elem2 in range(self.compNElements2):
            for elem1 in range(self.compNElements1):
                # calculate the distance for n elements = i*2*halfdinemsion
                temp_v = [elem1*2*d1+elem2*2*d2 for d1,d2 in zip(sb_dim_v1,sb_dim_v2)]
                # define the position for the element based on edge
                temp_v = [te+l1+l2 for te,l1,l2 in zip(temp_v,low_end_v1,low_end_v2)]
                # defining position, placement, and finally insert into the compule.
                el_pos = geom.structure.Position(self.name+"_el"+str(elem1)+'_'+str(elem2)+'_pos',
                                                    temp_v[0], temp_v[1], temp_v[2])
                el_pla = geom.structure.Placement(self.name+"_el"+str(elem1)+'_'+str(elem2)+'_pla',
                                                    volume=el_lv, pos=el_pos, rot =rotation1)
                main_lv.placements.append(el_pla.name)
