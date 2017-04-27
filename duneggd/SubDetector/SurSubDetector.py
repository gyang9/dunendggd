#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class SurSubDetectorBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, Material=None,
                    Axis=None, Initial_vec=None, Angles=None,
                    InsideGap=None, Rotation=None, **kwds ):
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.Axis, self.Initial_vec = (Axis, Initial_vec)
        self.Angles, self.InsideGap = (Angles, InsideGap)
        self.Rotation = Rotation

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")
        self.add_volume( main_lv )

        # definition local rotation
        rotation = geom.structure.Rotation( self.name+'_rot', str(self.Rotation[0]),
                                                str(self.Rotation[1]),  str(self.Rotation[2]) )

        builders = self.get_builders()
        sb_central = builders[0]
        sb_surr = builders[1]
        ltools.surroundBuilders( main_lv, sb_central, sb_surr, self.Axis, self.Initial_vec, self.InsideGap,
                                        self.Angles, geom )
