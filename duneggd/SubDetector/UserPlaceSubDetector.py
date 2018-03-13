#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class UserPlaceSubDetectorBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, dx=None, dy=None, dz=None,
                    Material=None, InsideGap=None,
                    AuxParams=None, TranspV=None, UserPlace=None, **kwds ):
        if halfDimension = None:
            halfDimension = {}
            halfDimension['dx'] = dx
            halfDimension['dy'] = dy
            halfDimension['dz'] = dz
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.InsideGap, self.AuxParams = ( InsideGap, AuxParams )
        self.TranspV, self.UserPlace = ( AuxParams,  UserPlace )

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")

        if self.AuxParams != None:
            ltools.addAuxParams( self, main_lv )

        self.add_volume( main_lv )

        TranspV = [0,0,1]
        if  self.TranspV != None:
            TranspV = self.TranspV
            ltools.placeUserLocationBuilders( self, geom, main_lv, TranspV )
