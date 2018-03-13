#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class CrossSubDetectorBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, dx=None, dy=None, dz=None,
                    Material=None, InsideGap=None, TranspP=None,
                    AuxParams=None, RotLeft=None, RotRight=None, RotTop=None,
                    RotBottom=None, **kwds ):

        if halfDimension = None:
            halfDimension = {}
            halfDimension['dx'] = dx
            halfDimension['dy'] = dy
            halfDimension['dz'] = dz
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.InsideGap, self.TranspP = InsideGap, TranspP
        self.RotLeft, self.RotRight = ( RotLeft, RotRight )
        self.RotTop, self.RotBottom = ( RotTop, RotBottom )
        self.AuxParams = AuxParams

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")

        if self.AuxParams != None:
            ltools.addAuxParams( self, main_lv )

        self.add_volume( main_lv )

        builders = self.get_builders()
        sb_central = builders[0]
        sb_top = builders[1]
        sb_side = builders[2]

        ltools.placeCrossBuilders( main_lv, sb_central, sb_top, sb_side, self, geom )
