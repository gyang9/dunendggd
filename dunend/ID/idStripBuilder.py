#!/usr/bin/env python
## Subbuilder of idPlaneBuilder
#

import gegede.builder
from gegede import Quantity as Q

## idStripBuilder
#
# builder for id Strip
class IDBuilder(gegede.builder.Builder):

    ## The configure
    def configure( self, idStripDim, idStripMat, **kwds ):
        self.dimension, self.material = ( idStripDim, idStripMat )
        pass

    ## The construct
    def construct( self, geom ):
        idStripBox = geom.shapes.Box( self.name, self.dimension[0], self.dimension[1], self.dimension[2] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.material, shape=idStripBox )
        self.add_volume( main_lv )
