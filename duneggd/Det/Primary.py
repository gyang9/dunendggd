#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class PrimaryBuilder(gegede.builder.Builder):

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, halfDimension=None, Material=None, BeginGap=None,
                    InsideGap=None,  BField=None, EField=None, **kwds):
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.BeginGap, self.InsideGap = ( BeginGap, InsideGap )
        self.BField, self.EField = ( BField, EField )

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")
        if isinstance(self.BField,str):
            main_lv.params.append(("BField",self.BField))
        if isinstance(self.EField,str):
            main_lv.params.append(("EField",self.EField))
        self.add_volume( main_lv )

        TranspV = [0,0,1]
        begingap = ltools.getBeginGap( self )

        # initial position, based on the dimension projected on transportation vector
        pos = [Q('0m'),Q('0m'),-main_hDim[2]+begingap]

        for i,sb in enumerate(self.get_builders()):
            sb_lv = sb.get_volume()
            sb_dim = ltools.getShapeDimensions( sb_lv, geom )
            pos[2] = pos[2] + sb_dim[2] + self.InsideGap[i]
            # defining position, placement, and finally insert into main logic volume.
            sb_pos = geom.structure.Position(self.name+sb_lv.name+'_pos',
                                                pos[0], pos[1], pos[2])
            sb_pla = geom.structure.Placement(self.name+sb_lv.name+'_pla',
                                                volume=sb_lv, pos=sb_pos )
            main_lv.placements.append(sb_pla.name)
            pos[2] = pos[2] + sb_dim[2]
