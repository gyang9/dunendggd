#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class DetEncBuilder(gegede.builder.Builder):

    ## The configure
    def configure(self, halfDimension=None, Material=None, **kwds):
        self.halfDimension, self.Material = ( halfDimension, Material )

    ## The construct
    def construct(self, geom):
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")
        self.add_volume( main_lv )

        Pos = [Q("0m"),Q("0m"),Q("0m")]
        for sb in self.get_builders():
            sb_lv = sb.get_volume()
            sb_pos = geom.structure.Position( sb_lv.name+'_pos', Pos[0], Pos[1], Pos[2] )
            sb_pla = geom.structure.Placement( sb_lv.name+'_pla', volume=sb_lv, pos=sb_pos )
            main_lv.placements.append( sb_pla.name )
