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
    def configure( self, idDimension=None, idMaterial=None, idTranspV=None, idGap=None, **kwds ):
        self.idDimension, self.idMaterial = ( idDimension, idMaterial)
        self.idTranspV, self.idGap = ( idTranspV, idGap )
        pass

    ## The construct
    def construct( self, geom ):
        idWireBox = geom.shapes.Box( self.name, dx=self.idDimension[0], dy=self.idDimension[1], dz=self.idDimension[2] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.idMaterial, shape=idWireBox )
        main_lv.params.append(("Color","blue"))
        self.add_volume( main_lv )
        return
