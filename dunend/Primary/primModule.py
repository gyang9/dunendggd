#!/usr/bin/env python
## Subbuilder of primModuleBuilder
#

import gegede.builder
from gegede import Quantity as Q

## primModuleBuilder
#
# builder for prim Module
class primModuleBuilder(gegede.builder.Builder):

    ## The configure
    def configure( self, primDimension=None, primMaterial=None, primNElements=None, primTranspV=None, primGap=None, **kwds ):
        self.primDimension, self.primMaterial = ( primDimension, primMaterial )
        self.primNElements = primNElements
        self.primTranspV, self.primGap = ( primTranspV, primGap )
        pass

    ## The construct
    def construct( self, geom ):
        primModuleBox = geom.shapes.Box( self.name, dx=self.primDimension[0], dy=self.primDimension[1], dz=self.primDimension[2] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.primMaterial, shape=primModuleBox )
        self.add_volume( main_lv )

        # get sub-builders and its volume
        el_sb = self.get_builder()
        el_lv = el_sb.get_volume()
        
        transp_v = el_sb.primTranspV # vector of transportation for the elements
        sb_dim_v = [a*(b+0.5*el_sb.primGap) for a,b in zip(transp_v,el_sb.primDimension)] # half dimension of element according to trans
        low_end_v  = [-a*b+c for a,b,c in zip(transp_v,self.primDimension,sb_dim_v)] # lower edg
        
        for element in range(self.primNElements):
            temp_v = [2*a*element for a in sb_dim_v]
            temp_v = [a+b for a,b in zip(temp_v,low_end_v)]
            el_pos = geom.structure.Position(self.name+"_el"+str(element)+'_pos', temp_v[0], temp_v[1], temp_v[2])
            el_pla = geom.structure.Placement(self.name+"_el"+str(element)+'_pla', volume = el_lv, pos = el_pos)
            main_lv.placements.append(el_pla.name)
