#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class UserPlaceSubDetectorBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, Material=None, InsideGap=None,
                    BField=None, EField=None, Sensitive=None, TranspV=None,
                    UserPlace=None, **kwds ):
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.InsideGap = InsideGap
        self.BField, self.EField = ( BField, EField )
        self.Sensitive, self.TranspV = (Sensitive, TranspV)
        self.UserPlace = UserPlace

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")
        if isinstance(self.Sensitive,str):
            main_lv.params.append(("SensDet",self.Sensitive))
        if isinstance(self.BField,str):
            main_lv.params.append(("BField",self.BField))
        if isinstance(self.EField,str):
            main_lv.params.append(("EField",self.EField))
        self.add_volume( main_lv )

        TranspV = [0,0,1]
        if  self.TranspV != None:
            TranspV = self.TranspV
            ltools.placeUserPlaceBuilders( self, geom, main_lv, TranspV )
