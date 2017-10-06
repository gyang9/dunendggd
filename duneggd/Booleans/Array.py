#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class ArrayBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, Material=None, InsideGap=None,
                    BField=None, EField=None, Sensitive=None, TranspV=None,
                    UserPlace=None, Boolean=None, **kwds ):
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.InsideGap = InsideGap
        self.BField, self.EField = ( BField, EField )
        self.Sensitive, self.TranspV = (Sensitive, TranspV)
        self.UserPlace, self.Boolean = (UserPlace, Boolean)

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")

        TranspV = [0,0,1]
        if  self.TranspV != None:
            TranspV = self.TranspV
            ltools.placeBooleanBuilders( self, geom, main_lv, TranspV )
