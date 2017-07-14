#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class SimpleSubDetectorBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, Material=None, NElements=None, BeginGap=None, 
                    InsideGap=None, Rotation=None, BField=None, EField=None, Sensitive=None,
                    TranspV=None, **kwds ):
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.NElements, self.BeginGap = ( NElements, BeginGap )
        self.InsideGap, self.Rotation  = ( InsideGap, Rotation )
        self.BField, self.EField = ( BField, EField )
        self.Sensitive = Sensitive
        self.TranspV = TranspV

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

        if self.NElements != None:
            TranspV = [0,0,1]
            if  self.TranspV != None:
                TranspV = self.TranspV
            ltools.placeBuilders( self, geom, main_lv, TranspV )
        else:
            print "**Warning, no Elements to place inside ", self.name
