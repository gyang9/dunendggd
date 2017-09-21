#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class CrossSubDetectorBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, Material=None, InsideGap=None, TranspP=None,
                    BField=None, EField=None, RotLeft=None, RotRight=None, RotTop=None,
                    RotBottom=None, **kwds ):
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.InsideGap, self.TranspP = InsideGap, TranspP
        self.BField, self.EField = ( BField, EField )
        self.RotLeft, self.RotRight = ( RotLeft, RotRight )
        self.RotTop, self.RotBottom = ( RotTop, RotBottom )

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")
        if isinstance(self.BField,str):
            main_lv.params.append(("BField",self.BField))
        if isinstance(self.EField,str):
            main_lv.params.append(("EField",self.EField))
        self.add_volume( main_lv )

        builders = self.get_builders()
        sb_central = builders[0]
        sb_top = builders[1]
        sb_side = builders[2]

        ltools.crossBuilders( main_lv, sb_central, sb_top, sb_side, self, geom )
