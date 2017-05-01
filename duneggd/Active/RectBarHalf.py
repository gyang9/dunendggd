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
    def configure( self, actDimension=None, actMaterial=None,  Sensitive=None, **kwds ):
        """
        :param actDimension: Dimension for the rectangular bar.
        :type actDimension: list
        :param actMaterial: Material for the rectangular bar.
        :type actMaterial: defined on World.py.
        :param actSensitive: Boolean to define is material is sensitivie for Geant.
        :type actSensitive: bool
        :returns: None
        """
        self.actDimension, self.actMaterial, self.actSensitive = ( actDimension, actMaterial, Sensitive )
        pass

    ## The construct
    def construct( self, geom ):
        """Construct the geometry for Rectangular Bar.
        :returns: None
        """
        main_shape = geom.shapes.Box( self.name, dx=self.actDimension[0]*0.5, dy=self.actDimension[1]*0.5, dz=self.actDimension[2]*0.5 )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.actMaterial, shape=main_shape )
        if isinstance(self.actSensitive,str):
            main_lv.params.append(("SensDet",self.actSensitive))
        self.add_volume( main_lv )

