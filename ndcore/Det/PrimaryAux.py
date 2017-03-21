#!/usr/bin/env python
'''
Subbuilder of Primary
'''

import gegede.builder
from gegede import Quantity as Q

class PrimaryAuxBuilder(gegede.builder.Builder):
    '''
    Assemble all the subsystems into one bounding box.
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, ggdDimension=None, ggdMaterial=None, ggdInsideGap=None,
                        ggdTranspV=None, ggdRotation=None, **kwds):
        self.ggdDimension, self.ggdMaterial = ( ggdDimension, ggdMaterial )
        self.ggdInsideGap = ggdInsideGap
        self.ggdTranspV, self.ggdRotation = ( ggdTranspV, ggdRotation )

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        main_shape = geom.shapes.Box( self.name, dx=self.ggdDimension[0],
                                        dy=self.ggdDimension[1], dz=self.ggdDimension[2] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.ggdMaterial, shape=main_shape )
        self.add_volume( main_lv )

        # definition local rotation
        rotation = geom.structure.Rotation( self.name+'_rot', str(self.ggdRotation[0]),
                                                str(self.ggdRotation[1]),  str(self.ggdRotation[2]) )

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
