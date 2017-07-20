#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class DetEncBuilder(gegede.builder.Builder):

    ## The configure
    def configure(self, halfDimension=None, Material=None, Positions=None, Rotations=None, **kwds):
        self.halfDimension, self.Material = ( halfDimension, Material )
        self.Positions=Positions
        self.Rotations=Rotations
        

    ## The construct
    def construct(self, geom):
        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")
        self.add_volume( main_lv )
        
        for i,sb in enumerate(self.get_builders()):
            Pos = [Q("0m"),Q("0m"),Q("0m")]
            Rot = [Q("0deg"),Q("0deg"),Q("0deg")]
            if self.Positions!=None:                
                Pos=self.Positions[i]
            if self.Rotations!=None:                
                Rot=self.Rotations[i]
            
            print "Pos=",Pos
            print "Rot=",Rot
            sb_lv = sb.get_volume()
            sb_pos = geom.structure.Position( sb_lv.name+'_pos', Pos[0], Pos[1], Pos[2] )
            sb_rot = geom.structure.Rotation( sb_lv.name+'_rot', Rot[0], Rot[1], Rot[2] )
            sb_pla = geom.structure.Placement( sb_lv.name+'_pla', volume=sb_lv, pos=sb_pos, rot=sb_rot )
            main_lv.placements.append( sb_pla.name )
