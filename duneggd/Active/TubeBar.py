#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class TubeBarBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, Material=None,  Sensitive=None, **kwds ):
        """
        :param halfDimension: halfDimension for the rectangular bar.
        :type halfDimension: dictionary
        :param Material: Material for the tube bar.
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
        main_lv, main_hDim = ltools.main_lv( self, geom, "Tubs")
        if isinstance(self.Sensitive,str):
            main_lv.params.append(("SensDet",self.Sensitive))
        self.add_volume( main_lv )
