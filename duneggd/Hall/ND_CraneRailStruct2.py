#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class NDCraneRailStruct2Builder(gegede.builder.Builder):

    def configure(self, mat=None, craneRailBlock1Dim=None, craneRailBlock1Pos=None, craneRailBlock2Dim=None, craneRailBlock2Pos=None, craneRailBlock2Rot=None, craneRailBlock3Dim=None, craneRailBlock3Pos=None, **kwds):

        self.mat=mat
        self.craneRailBlock1Dim=craneRailBlock1Dim
        self.craneRailBlock1Pos=craneRailBlock1Pos
        self.craneRailBlock2Dim=craneRailBlock2Dim
        self.craneRailBlock2Pos=craneRailBlock2Pos
        self.craneRailBlock2Rot=craneRailBlock2Rot
        self.craneRailBlock3Dim=craneRailBlock3Dim
        self.craneRailBlock3Pos=craneRailBlock3Pos

    def construct(self, geom):

        craneRailBlock21 = geom.shapes.Box( 'craneRailBlock21',
                dx = 0.5*self.craneRailBlock1Dim[0],
                dy = 0.5*self.craneRailBlock1Dim[1],
                dz = 0.5*self.craneRailBlock1Dim[2])

        craneRailBlock21Position = geom.structure.Position( 'craneRail21Position',
                self.craneRailBlock1Pos[0],
                self.craneRailBlock1Pos[1],
                self.craneRailBlock1Pos[2])

        craneRailBlock22 = geom.shapes.Box( 'craneRailBlock22',
                dx = 0.5*self.craneRailBlock2Dim[0],
                dy = 0.5*self.craneRailBlock2Dim[1],
                dz = 0.5*self.craneRailBlock2Dim[2])

        craneRailBlock22Position = geom.structure.Position( 'craneRailBlock22Position',
                self.craneRailBlock2Pos[0],
                self.craneRailBlock2Pos[1],
                self.craneRailBlock2Pos[2])

        craneRailBlock22Rot = geom.structure.Rotation( 'craneRailBlock22Rot',
                self.craneRailBlock2Rot[0],
                self.craneRailBlock2Rot[1],
                self.craneRailBlock2Rot[2])

        craneRailBlock23 = geom.shapes.Box( 'craneRailBlock23',
                dx = 0.5*self.craneRailBlock3Dim[0],
                dy = 0.5*self.craneRailBlock3Dim[1],
                dz = 0.5*self.craneRailBlock3Dim[2])

        craneRailBlock23Position = geom.structure.Position( 'craneRailBlock23Position',
                self.craneRailBlock3Pos[0],
                self.craneRailBlock3Pos[1],
                self.craneRailBlock3Pos[2])

        craneRail2ShapeTemp = geom.shapes.Boolean( 'crainRail2ShapeTemp', type='subtraction', first=craneRailBlock21, second= craneRailBlock22, rot="craneRailBlock22Rot", pos=craneRailBlock22Position)
        craneRail2Shape = geom.shapes.Boolean( 'crainRail2Shape', type='union', first=craneRail2ShapeTemp, second=craneRailBlock23, pos=craneRailBlock23Position)

        craneRail2_lv = geom.structure.Volume( 'craneRail2_lv', material=self.mat, shape=craneRail2Shape)

        self.add_volume( craneRail2_lv )


