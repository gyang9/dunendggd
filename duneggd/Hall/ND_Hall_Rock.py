#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class RockBuilder(gegede.builder.Builder):

    def configure(self, mat=None, rockBoxMainDim=None, rockBoxUpstreamDim=None, rockBoxUpstreamPos=None, rockBoxSubtDim=None, rockBoxSubtPos=None, rockTubDim=None, rockTubPos=None, Positions=None, Rotations=None):

        self.mat=mat
        self.rockBoxMainDim=rockBoxMainDim
        self.rockBoxUpstreamDim=rockBoxUpstreamDim
        self.rockBoxUpstreamPos=rockBoxUpstreamPos
        self.rockBoxSubtDim=rockBoxSubtDim
        self.rockBoxSubtPos=rockBoxSubtPos
        self.rockTubDim=rockTubDim
        self.rockTubPos=rockTubPos

        self.Positions=Positions
        self.Rotations=Rotations

    def construct(self, geom):

        rockBoxMain = geom.shapes.Box( 'RockBoxMain',
                dx = 0.5*self.rockBoxMainDim[0],
                dy = 0.5*self.rockBoxMainDim[1],
                dz = 0.5*self.rockBoxMainDim[2])

        rockBoxUpstream = geom.shapes.Box( 'RockBoxUpstream',
                dx = 0.5*self.rockBoxUpstreamDim[0],
                dy = 0.5*self.rockBoxUpstreamDim[1],
                dz = 0.5*self.rockBoxUpstreamDim[2])

        rockBoxUpstreamPosition = geom.structure.Position( 'rockBoxUpstreamPosition',
                self.rockBoxUpstreamPos[0],
                self.rockBoxUpstreamPos[1],
                self.rockBoxUpstreamPos[2])

        rockBoxSubt = geom.shapes.Box( 'RockBoxSubt',
                dx = 0.5*self.rockBoxSubtDim[0],
                dy = 0.5*self.rockBoxSubtDim[1],
                dz = 0.5*self.rockBoxSubtDim[2])

        rockBoxSubtPosition = geom.structure.Position( 'rockBoxSubtPosition',
                self.rockBoxSubtPos[0],
                self.rockBoxSubtPos[1],
                self.rockBoxSubtPos[2])

        rockTub = geom.shapes.Tubs( 'rockTub',
                rmin = self.rockTubDim[0],
                rmax = self.rockTubDim[1],
                dz = 0.5*self.rockTubDim[2],
                sphi = self.rockTubDim[3],
                dphi = self.rockTubDim[4])
        
        rockTubPosition = geom.structure.Position( 'rockTubPosition',
                self.rockTubPos[0],
                self.rockTubPos[1],
                self.rockTubPos[2])

        #rockBoxTemp1 = geom.shapes.Boolean( 'rockBoxTemp1', type='union', first=rockBoxMain, second=rockBoxUpstream, pos=rockBoxUpstreamPosition)
        #rockBoxTemp2 = geom.shapes.Boolean( 'rockBoxTemp2', type='subtraction', first=rockBoxTemp1, second=rockBoxSubt, pos=rockBoxSubtPosition)
        rockBoxTemp2 = geom.shapes.Boolean( 'rockBoxTemp2', type='subtraction', first=rockBoxMain, second=rockBoxSubt, pos=rockBoxSubtPosition)
        rockBox = geom.shapes.Boolean( 'rockBox', type='union', first=rockBoxTemp2, second=rockTub, rot='r90aboutX', pos=rockTubPosition)

        rockBox_lv = geom.structure.Volume( 'rockBox_lv', material=self.mat, shape=rockBoxMain)
        self.add_volume( rockBox_lv )

        for i,sb in enumerate(self.get_builders()):
            Pos = [Q("0m"),Q("0m"),Q("0m")]
            Rot = [Q("0deg"),Q("0deg"),Q("0deg")]
            if self.Positions!=None :
                Pos=self.Positions[i]
            if self.Rotations!=None:
                Rot=self.Rotations[i]
            sb_lv = sb.get_volume()
            sb_pos = geom.structure.Position( sb_lv.name+'_pos', Pos[0], Pos[1], Pos[2] )
            sb_rot = geom.structure.Rotation( sb_lv.name+'_rot', Rot[0], Rot[1], Rot[2] )
            sb_pla = geom.structure.Placement( sb_lv.name+'_pla', volume=sb_lv, pos=sb_pos, rot=sb_rot )
            rockBox_lv.placements.append( sb_pla.name )


