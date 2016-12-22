#!/usr/bin/env python
## Subbuilder of idPlaneBuilder
#

import gegede.builder
from gegede import Quantity as Q

## idWireBuilder
#
# builder for idWire
class idWireBuilder(gegede.builder.Builder):

    ## The configure
    def configure( self, idWireDim, idWireMat, **kwds ):
        self.dimension, self.material = ( idWireDim, idWireMat )
        pass

    ## The construct
    def construct( self, geom ):
        idWireBox = geom.shapes.Box( self.name, self.dimension[0], self.dimension[1], self.dimension[2] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.material, shape=idWireBox )
        self.add_volume( main_lv )
