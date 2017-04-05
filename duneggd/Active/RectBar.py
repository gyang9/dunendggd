#!/usr/bin/env python
import gegede.builder
from gegede import Quantity as Q

class RectBarBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, Material=None,  Sensitive=None, **kwds ):
        """
        :param halfDimension: halfDimension for the rectangular bar.
        :type halfDimension: dictionary
        :param Material: Material for the rectangular bar.
        :type Material: defined on World.py.
        :param Sensitive: Boolean to define is material is sensitivie for Geant.
        :type Sensitive: bool
        :returns: None
        """
        self.halfDimension, self.Material, self.Sensitive = ( halfDimension, Material, Sensitive )

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        """
        Construct the geometry for Rectangular Bar.
        :returns: None
        """
        main_shape = geom.shapes.Box( self.name, dx=self.halfDimension['dx'], dy=self.halfDimension['dy'], dz=self.halfDimension['dz'] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.Material, shape=main_shape )
        if self.Sensitive == True:
            main_lv.params.append(("SensDet","Active"))
        self.add_volume( main_lv )
