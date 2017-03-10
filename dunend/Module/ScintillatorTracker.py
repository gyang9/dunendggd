#!/usr/bin/env python
## Subbuilder of ScintillatorTrackerBuilder
#

import gegede.builder
from gegede import Quantity as Q

## ScintillatorTrackerBuilder
#
# builder for mod SubDet
class ScintillatorTrackerBuilder(gegede.builder.Builder):

    ## The configure
    def configure( self, modDimension=None, modMaterial=None, modNElements=None,  modGapV=None, 
                    modTranspV=None, **kwds ):
        self.modDimension, self.modMaterial = ( modDimension, modMaterial )
        self.modNElements, self.modInsideGap = ( modNElements, modGapV )
        self.modTranspV = modTranspV
        pass

    ## The construct
    def construct( self, geom ):
        main_shape = geom.shapes.Box( self.name+"_shape", dx = self.modDimension[0], 
                                        dy = self.modDimension[1], dz = self.modDimension[2] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.modMaterial, shape=main_shape )
        #main_lv.params.append(("SensDet","LArD"))
        self.add_volume( main_lv )

        # get sub-builders and its volume
        el_sb = self.get_builder()
        el_lv = el_sb.get_volume()

        # calculate half dimension of element plus the gap projected to the transportation vector
        sb_dim_v = [t*(d+0.5*self.modInsideGap) for t,d in zip(self.modTranspV,el_sb.plaDimension)] 
        
        # lower edge, the module dimension projected on transportation vector
        low_end_v  = [-t*d+ed for t,d,ed in zip(self.modTranspV,self.modDimension,sb_dim_v)] 
        
        for element in range(self.modNElements):
            # calculate the distance for n elements = i*2*halfdinemsion
            temp_v = [element*2*d for d in sb_dim_v]
            # define the position for the element based on edge
            temp_v = [te+l for te,l in zip(temp_v,low_end_v)]
            # defining position, placement, and finally insert into the module.
            el_pos = geom.structure.Position(self.name+"_el"+str(element)+'_pos', temp_v[0], temp_v[1], temp_v[2])
            el_pla = geom.structure.Placement(self.name+"_el"+str(element)+'_pla', volume=el_lv, pos=el_pos)
            main_lv.placements.append(el_pla.name)
