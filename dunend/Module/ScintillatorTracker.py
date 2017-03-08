#!/usr/bin/env python
## Subbuilder of primSubDetBuilder
#

import gegede.builder
from gegede import Quantity as Q

## primSubDetBuilder
#
# builder for prim SubDet
class ScintilatorTrackerBuilder(gegede.builder.Builder):

    ## The configure
    def configure( self, primDimension=None, primMaterial=None, primNElements=None, primGapV=None, **kwds ):
        self.primDimension, self.primMaterial = ( primDimension, primMaterial )
        self.primNElements, self.primGapV = (primNElements, primGapV)
        pass

    ## The construct
    def construct( self, geom ):
        primSubDetBox = geom.shapes.Box( self.name, dx=self.primDimension[0], dy=self.primDimension[1], dz=self.primDimension[2] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.primMaterial, shape=primSubDetBox )
        self.add_volume( main_lv )

        # get sub-builders and its volume
        el_sb = self.get_builder()
        el_lv = el_sb.get_volume()
        
        
        for element in range(self.primNElements):
            el_pos = geom.structure.Position(self.name+"_el"+str(element)+'_pos', temp_v[0], temp_v[1], temp_v[2])
            el_pla = geom.structure.Placement(self.name+"_el"+str(element)+'_pla', volume = el_lv, pos = el_pos)
            main_lv.placements.append(el_pla.name)
