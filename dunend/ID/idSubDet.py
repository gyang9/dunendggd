#!/usr/bin/env python
## Subbuilder of idSubDetBuilder
#

import gegede.builder
from gegede import Quantity as Q

## idSubDetBuilder
#
# builder for id SubDet
class idSubDetBuilder(gegede.builder.Builder):

    ## The configure
    def configure( self, idSubDetDim, idSubDetMat, **kwds ):
        self.dimension, self.material = ( idSubDetDim, idSubDetMat )
        self.nelements = idSubDetNElemts
        pass

    ## The construct
    def construct( self, geom ):
        idSubDetBox = geom.shapes.Box( self.name, self.dimension[0], self.dimension[1], self.dimension[2] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.material, shape=idSubDetBox )
        self.add_volume( main_lv )

        element_lv = self.builders[0].Volumes[0] #ok?
        low_end = Q('0cm')
        dist = Q('5cm')
        
        for element in range(self.nelements):
            element_pos = geom.structure.Position('element_pos_'+str(j), low_end+element*dist, '4m', '0cm')
            element_pla  = geom.structure.Placement('element_pla_'+str(j), volume = element_lv, pos = element_pos)
            main_lv.placements.append(element_pla.name )

        return
