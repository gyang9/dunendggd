#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class GenSolidBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, Shape=None, Material=None,
                    Sensitive=None, **kwds ):
        """
        :param halfDimension: halfDimension for the rectangular bar.
        :type halfDimension: dictionary
        :param Material: Material for the rectangular bar.
        :type Material: defined on World.py.
        :param AuxParams: Dictionary to add aux parameters.
        :type AuxParams: dictionary
        :returns: None
        """
        self.halfDimension, self.Shape = ( halfDimension, Shape )
        self.Material, self.AuxParams = ( Material, AuxParams )

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        """
        Construct the geometry for Generic Shape.
        :returns: None
        """
        main_lv, main_hDim = ltools.main_lv( self, geom, self.Shape )

        if self.AuxParams != None:
            ltools.addAuxParams( self, main_lv )

        self.add_volume( main_lv )
