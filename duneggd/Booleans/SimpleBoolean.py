#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class SimpleBooleanBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure( self, halfDimension=None, Material=None, InsideGap=None,
                    BField=None, EField=None, Sensitive=None,
                    SubBPos=None, Boolean=None, **kwds ):
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.InsideGap = InsideGap
        self.BField, self.EField = ( BField, EField )
        self.Sensitive = Sensitive
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

        if isinstance(self.Sensitive,str):
            sb_boolean_lv.params.append(("SensDet",self.Sensitive))
        if isinstance(self.BField,str):
            sb_boolean_lv.params.append(("BField",self.BField))
        if isinstance(self.EField,str):
            sb_boolean_lv.params.append(("EField",self.EField))

        self.add_volume( sb_boolean_lv )
