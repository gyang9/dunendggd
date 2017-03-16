#!/usr/bin/env python
## Subbuilder of primPlaneBuilder
#

import gegede.builder
from gegede import Quantity as Q

## RectBarBuilder
#
# builder for prim Strip
class RectBarBuilder(gegede.builder.Builder):

    ## The configure
    def configure( self, actDimension=None, actMaterial=None,  actSensitive=None, **kwds ):
        self.actDimension, self.actMaterial, self.actSensitive = ( actDimension, actMaterial, actSensitive )
        pass

    ## The construct
    def construct( self, geom ):
        main_shape = geom.shapes.Box( self.name, dx=self.actDimension[0], dy=self.actDimension[1], dz=self.actDimension[2] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.actMaterial, shape=main_shape )
        if self.actSensitive == True:
            main_lv.params.append(("SensDet","FGD"))
        self.add_volume( main_lv )
