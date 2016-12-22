#!/usr/bin/env python
## Subbuilder of idPlaneBuilder
#

import gegede.builder
from gegede import Quantity as Q

## idPlaneBuilder
#
# builder for id Plane
class idPlaneBuilder(gegede.builder.Builder):

    ## The configure
    def configure( self, idPlaneDim, idPlaneMat, **kwds ):
        self.dimension, self.material = ( idPlaneDim, idPlaneMat )
        self.nelements = idPlaneNElemts
        pass

    ## The construct
    def construct( self, geom ):
        idPlaneBox = geom.shapes.Box( self.name, self.dimension[0], self.dimension[1], self.dimension[2] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.material, shape=idPlaneBox )
        self.add_volume( main_lv )

        element_lv = self.builders[0].Volumes[0] #ok?
        low_end = Q('0cm')
        dist = Q('5cm')
        
        for element in range(self.nelements):
            element_pos = geom.structure.Position('element_pos_'+str(j), low_end+element*dist, '4m', '0cm')
            element_pla  = geom.structure.Placement('element_pla_'+str(j), volume = element_lv, pos = element_pos)
            main_lv.placements.append(element_pla.name )

        return
