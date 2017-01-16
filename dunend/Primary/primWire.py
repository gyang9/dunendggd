#!/usr/bin/env python
## Subbuilder of primPlaneBuilder
#

import gegede.builder
from gegede import Quantity as Q

## primWireBuilder
#
# builder for primWire
class primWireBuilder(gegede.builder.Builder):

    ## The configure
    def configure( self, primDimension=None, primMaterial=None, primTranspV=None, primGap=None, **kwds ):
        self.primDimension, self.primMaterial = ( primDimension, primMaterial)
        self.primTranspV, self.primGap = ( primTranspV, primGap )
        pass

    ## The construct
    def construct( self, geom ):
        primWireBox = geom.shapes.Box( self.name, dx=self.primDimension[0], dy=self.primDimension[1], dz=self.primDimension[2] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.primMaterial, shape=primWireBox )
        main_lv.params.append(("Color","blue"))
        self.add_volume( main_lv )
        return
