#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class SimpleBooleanBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, Material=None, InsideGap=None,
                    AuxParams=None, SubBPos=None, Boolean=None, **kwds ):
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.InsideGap, self.AuxParams = ( InsideGap, AuxParams )
        self.SubBPos, self.Boolean = (SubBPos, Boolean)

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct( self, geom ):

        builders = self.get_builders()
        sb_0 = builders[0]
        sb_0_lv = sb_0.get_volume()
        sb_0_shape = geom.store.shapes.get(sb_0_lv.shape)
        sb_1 = builders[1]
        sb_1_lv = sb_1.get_volume()
        sb_1_shape = geom.store.shapes.get(sb_1_lv.shape)

        sb_pos = geom.structure.Position(self.name+'_pos', self.SubBPos[0], self.SubBPos[1], self.SubBPos[2] )
        sb_boolean_shape = geom.shapes.Boolean( self.name+'_'+self.Boolean,
                                                type=self.Boolean, first=sb_0_shape,
                                                second=sb_1_shape, pos=sb_pos)

        sb_boolean_lv = geom.structure.Volume('vol'+sb_boolean_shape.name, material=self.Material,
                                                shape=sb_boolean_shape)

        if self.AuxParams != None:
            ltools.addAuxParams( self, sb_boolean_lv )

        self.add_volume( sb_boolean_lv )
