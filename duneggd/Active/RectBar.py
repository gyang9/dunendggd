#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class RectBarBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, Material=None,  AuxParams=None, **kwds ):
        """
        :param halfDimension: halfDimension for the rectangular bar.
        :type halfDimension: dictionary
        :param Material: Material for the rectangular bar.
        :type Material: defined on World.py.
        :param AuxParams: Dictionary to add aux parameters.
        :type AuxParams: dictionary
        :returns: None
        """
        self.halfDimension, self.Material, self.AuxParams = ( halfDimension, Material, AuxParams )

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        """
        Construct the geometry for Rectangular Bar.
        :returns: None
        """
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")

        if self.AuxParams != None:
            ltools.addAuxParams( self, main_lv )

        self.add_volume( main_lv )
