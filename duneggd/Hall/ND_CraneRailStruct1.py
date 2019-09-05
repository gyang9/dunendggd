#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class NDCraneRailStruct1Builder(gegede.builder.Builder):

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
        
        craneRailBlock11 = geom.shapes.Box( 'craneRailBlock11',
                dx = 0.5*self.craneRailBlock1Dim[0],
                dy = 0.5*self.craneRailBlock1Dim[1],
                dz = 0.5*self.craneRailBlock1Dim[2])

        craneRailBlock11Position = geom.structure.Position( 'craneRail11Position',
                self.craneRailBlock1Pos[0],
                self.craneRailBlock1Pos[1],
                self.craneRailBlock1Pos[2])

        craneRailBlock12 = geom.shapes.Box( 'craneRailBlock12',
                dx = 0.5*self.craneRailBlock2Dim[0],
                dy = 0.5*self.craneRailBlock2Dim[1],
                dz = 0.5*self.craneRailBlock2Dim[2])

        craneRailBlock12Position = geom.structure.Position( 'craneRailBlock12Position',
                self.craneRailBlock2Pos[0],
                self.craneRailBlock2Pos[1],
                self.craneRailBlock2Pos[2])

        craneRailBlock12Rot = geom.structure.Rotation( 'craneRailBlock12Rot',
                self.craneRailBlock2Rot[0],
                self.craneRailBlock2Rot[1],
                self.craneRailBlock2Rot[2])

        craneRailBlock13 = geom.shapes.Box( 'craneRailBlock13', 
                dx = 0.5*self.craneRailBlock3Dim[0],
                dy = 0.5*self.craneRailBlock3Dim[1],
                dz = 0.5*self.craneRailBlock3Dim[2])

        craneRailBlock13Position = geom.structure.Position( 'craneRailBlock13Position',
                self.craneRailBlock3Pos[0],
                self.craneRailBlock3Pos[1],
                self.craneRailBlock3Pos[2])

        craneRail1ShapeTemp = geom.shapes.Boolean( 'crainRail1ShapeTemp', type='subtraction', first=craneRailBlock11, second= craneRailBlock12, rot="craneRailBlock12Rot", pos=craneRailBlock12Position)
        craneRail1Shape = geom.shapes.Boolean( 'crainRail1Shape', type='union', first=craneRail1ShapeTemp, second=craneRailBlock13, pos=craneRailBlock13Position)

        craneRail1_lv = geom.structure.Volume( 'craneRail1_lv', material=self.mat, shape=craneRail1Shape)

        self.add_volume( craneRail1_lv )
        
