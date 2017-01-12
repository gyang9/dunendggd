#!/usr/bin/env python
## Subbuilder of idModuleBuilder
#

import gegede.builder
from gegede import Quantity as Q

## idModuleBuilder
#
# builder for id Module
class idModuleBuilder(gegede.builder.Builder):

    ## The configure
    def configure( self, idDimension=None, idMaterial=None, idNElements=None, idTranspV=None, idGap=None, **kwds ):
        self.idDimension, self.idMaterial = ( idDimension, idMaterial )
        self.idNElements = idNElements
        self.idTranspV, self.idGap = ( idTranspV, idGap )
        pass

    ## The construct
    def construct( self, geom ):
        idModuleBox = geom.shapes.Box( self.name, dx=self.idDimension[0], dy=self.idDimension[1], dz=self.idDimension[2] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.idMaterial, shape=idModuleBox )
        self.add_volume( main_lv )

        # get sub-builders and its volume
        el_sb = self.get_builder()
        el_lv = el_sb.get_volume()
        
        transp_v = el_sb.idTranspV # vector of transportation for the elements
        sb_dim_v = [a*(b+0.5*el_sb.idGap) for a,b in zip(transp_v,el_sb.idDimension)] # half dimension of element according to trans
        low_end_v  = [-a*b+c for a,b,c in zip(transp_v,self.idDimension,sb_dim_v)] # lower edg
        
        for element in range(self.idNElements):
            temp_v = [2*a*element for a in sb_dim_v]
            temp_v = [a+b for a,b in zip(temp_v,low_end_v)]
            el_pos = geom.structure.Position(self.name+"_el"+str(element)+'_pos', temp_v[0], temp_v[1], temp_v[2])
            el_pla = geom.structure.Placement(self.name+"_el"+str(element)+'_pla', volume = el_lv, pos = el_pos)
            main_lv.placements.append(el_pla.name)
