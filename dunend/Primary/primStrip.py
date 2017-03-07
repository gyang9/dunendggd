#!/usr/bin/env python
## Subbuilder of primPlaneBuilder
#

import gegede.builder
from gegede import Quantity as Q

## primStripBuilder
#
# builder for prim Strip
class primStripBuilder(gegede.builder.Builder):

    ## The configure
    def configure( self, primDimension=None, primMaterial=None, primTranspV=None, primGap=None, **kwds ):
        self.primDimension, self.primMaterial = ( primDimension, primMaterial )
        self.primTranspV, self.primGap = ( primTranspV, primGap )
        pass

    ## The construct
    def construct( self, geom ):
        primStripBox = geom.shapes.Box( self.name, dx=self.primDimension[0], dy=self.primDimension[1], dz=self.primDimension[2] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.primMaterial, shape=primStripBox )
        main_lv.params.append(("SensDet","FGD"))
        self.add_volume( main_lv )
