#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class TubeBarBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, rmin=None, rmax=None, dz=None,
                    Material=None,  AuxParams=None, **kwds ):
        """
        :param halfDimension: halfDimension for the rectangular bar.
        :type halfDimension: dictionary
        :param Material: Material for the tube bar.
        :type Material: defined on World.py.
        :param AuxParams: Dictionary to add aux parameters.
        :type AuxParams: dictionary
        :returns: None
        """
        if halfDimension == None:
            halfDimension = {}
            halfDimension['rmin'] = rmin
            halfDimension['rmax'] = rmax
            halfDimension['dz'] = dz

        self.halfDimension = halfDimension
        self.Material, self.AuxParams = ( Material, AuxParams )

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        """
        Construct the geometry for Rectangular Bar.
        :returns: None
        """
        main_lv, main_hDim = ltools.main_lv( self, geom, "Tubs")

        if self.AuxParams != None:
            ltools.addAuxParams( self, main_lv )

        self.add_volume( main_lv )
