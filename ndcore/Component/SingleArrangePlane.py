#!/usr/bin/env python
## Subbuilder of SingleArrangePlaneBuilder
#

import gegede.builder
from gegede import Quantity as Q

## SingleArrangePlaneBuilder
#
# builder for SingleArrangePlane
class SingleArrangePlaneBuilder(gegede.builder.Builder):

    ## The configure
    def configure( self, compDimension=None, compMaterial=None,
                    compNElements=None, compInsideGap=None, compTranspV=None, compRotation=None, **kwds ):
        self.compDimension, self.compMaterial = ( compDimension, compMaterial )
        self.compNElements, self.compInsideGap = ( compNElements, compInsideGap )
        self.compTranspV, self.compRotation = ( compTranspV, compRotation )
        pass

    ## The construct
    def construct( self, geom ):
        main_shape = geom.shapes.Box( self.name, dx=self.compDimension[0], 
                                        dy=self.compDimension[1], dz=self.compDimension[2] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.compMaterial, shape=main_shape )
        self.add_volume( main_lv )

        # definition local rotation
        rotation = geom.structure.Rotation( self.name+'_rot', str(self.compRotation[0]), 
                                            str(self.compRotation[1]),  str(self.compRotation[2]) )

        # get sub-builders and its logic volume
        el_sb = self.get_builder()
        el_lv = el_sb.get_volume()
        
        # get the sub-builder dimension, using its shape
        el_shape = geom.store.shapes.get(el_lv.shape)
        el_dim = [el_shape.dx, el_shape.dy, el_shape.dz]
        
        # calculate half dimension of element plus the gap projected to the transportation vector
        sb_dim_v = [t*(d+0.5*self.compInsideGap) for t,d in zip(self.compTranspV,el_dim)]

        # lower edge, the compule dimension projected on transportation vector
        low_end_v  = [-t*d+ed for t,d,ed in zip(self.compTranspV,self.compDimension,sb_dim_v)]
        
        for element in range(self.compNElements):
            # calculate the distance for n elements = i*2*halfdinemsion
            temp_v = [element*2*d for d in sb_dim_v]
            # define the position for the element based on edge
            temp_v = [te+l for te,l in zip(temp_v,low_end_v)]
            # defining position, placement, and finally insert into the compule.
            el_pos = geom.structure.Position(self.name+"_el"+str(element)+'_pos', temp_v[0], temp_v[1], temp_v[2])
            el_pla = geom.structure.Placement(self.name+"_el"+str(element)+'_pla', 
                                                volume=el_lv, pos=el_pos, rot =rotation)
            main_lv.placements.append(el_pla.name)
