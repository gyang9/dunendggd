#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class PrimaryAuxBuilder(gegede.builder.Builder):
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, halfDimension=None, Material=None, InsideGap=None,
                        TranspV=None, Rotation=None, **kwds):
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.InsideGap = InsideGap
        self.TranspV, self.Rotation = ( TranspV, Rotation )

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")
        self.add_volume( main_lv )

        # definition local rotation
        rotation = geom.structure.Rotation( self.name+'_rot', str(self.Rotation[0]),
                                                str(self.Rotation[1]),  str(self.Rotation[2]) )

        # get sub-builders and its logic volume
        sb = self.get_builder()
        sb_lv = sb.get_volume()

        #top
        sbtop_pos = geom.structure.Position(self.name+sb_lv.name+'_top_pos',
                                            Q('0m'), Q('4m'), Q('5.2m'))
        sbtop_pla = geom.structure.Placement(self.name+sb_lv.name+'_top_pla',
                                            volume=sb_lv, pos=sbtop_pos, rot =rotation)
        main_lv.placements.append(sbtop_pla.name)

        #bottom
        sbbot_pos = geom.structure.Position(self.name+sb_lv.name+'_bot_pos',
                                            Q('0m'), Q('-4m'), Q('5.2m'))
        sbbot_pla = geom.structure.Placement(self.name+sb_lv.name+'_bot_pla',
                                            volume=sb_lv, pos=sbbot_pos, rot =rotation)
        main_lv.placements.append(sbbot_pla.name)

        #left
        sbleft_pos = geom.structure.Position(self.name+sb_lv.name+'_left_pos',
                                            Q('4m'), Q('0m'), Q('5.2m'))
        sbleft_pla = geom.structure.Placement(self.name+sb_lv.name+'_left_pla',
                                            volume=sb_lv, pos=sbleft_pos, rot =rotation)
        main_lv.placements.append(sbleft_pla.name)

        #right
        sbright_pos = geom.structure.Position(self.name+sb_lv.name+'_right_pos',
                                            Q('-4m'), Q('0m'), Q('5.2m'))
        sbright_pla = geom.structure.Placement(self.name+sb_lv.name+'_right_pla',
                                            volume=sb_lv, pos=sbright_pos, rot =rotation)
        main_lv.placements.append(sbright_pla.name)
