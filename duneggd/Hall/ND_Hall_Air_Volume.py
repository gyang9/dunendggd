#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class NDHallAirVolumeBuilder(gegede.builder.Builder):

    def configure(self, Positions=None, Rotations=None, mat=None, NDHallSpace1Dim=None, NDHallSpace2Dim=None, NDHallSpace2Pos=None, NDHallSpace3Dim=None, NDHallSpace3Pos=None, NDHallSpace4Dim=None, NDHallSpace4Pos=None, NDHallSpace5Dim=None, NDHallSpace5Pos=None, NDHallSpace6Dim=None, NDHallSpace6Pos=None, NDHallSpace7Dim=None, NDHallSpace7Pos=None, **kwds):

        self.Positions = Positions
        self.Rotations = Rotations

        self.mat=mat
        self.NDHallSpace1Dim=NDHallSpace1Dim
        self.NDHallSpace2Dim=NDHallSpace2Dim
        self.NDHallSpace2Pos=NDHallSpace2Pos
        self.NDHallSpace3Dim=NDHallSpace3Dim
        self.NDHallSpace3Pos=NDHallSpace3Pos
        self.NDHallSpace4Dim=NDHallSpace4Dim
        self.NDHallSpace4Pos=NDHallSpace4Pos
        self.NDHallSpace5Dim=NDHallSpace5Dim
        self.NDHallSpace5Pos=NDHallSpace5Pos
        self.NDHallSpace6Dim=NDHallSpace6Dim
        self.NDHallSpace6Pos=NDHallSpace6Pos
        self.NDHallSpace7Dim=NDHallSpace7Dim
        self.NDHallSpace7Pos=NDHallSpace7Pos

    def construct(self, geom):

        NDHallAirVolSpace1 = geom.shapes.Box( 'NDHallAirVolSpace1',
                dx = 0.5*self.NDHallSpace1Dim[0],
                dy = 0.5*self.NDHallSpace1Dim[1],
                dz = 0.5*self.NDHallSpace1Dim[2])

        NDHallAirVolSpace2 = geom.shapes.Box( 'NDHallAirVolSpace2',
                dx = 0.5*self.NDHallSpace2Dim[0],
                dy = 0.5*self.NDHallSpace2Dim[1],
                dz = 0.5*self.NDHallSpace2Dim[2])

        NDHallAirVolSpace2Position = geom.structure.Position( 'NDHallSpaceAirVol2Position',
                self.NDHallSpace2Pos[0],
                self.NDHallSpace2Pos[1],
                self.NDHallSpace2Pos[2])

        NDHallAirVolSpace3 = geom.shapes.Tubs( 'NDHallAirVolSpace3',
                rmin = self.NDHallSpace3Dim[0],
                rmax = self.NDHallSpace3Dim[1],
                dz = 0.5*self.NDHallSpace3Dim[2],
                sphi = self.NDHallSpace3Dim[3],
                dphi = self.NDHallSpace3Dim[4])

        NDHallAirVolSpace3Position = geom.structure.Position( 'NDHallSpace3AirVolPosition',
                self.NDHallSpace3Pos[0],
                self.NDHallSpace3Pos[1],
                self.NDHallSpace3Pos[2])

        NDHallAirVolSpace4 = geom.shapes.Tubs( 'NDHallAirVolSpace4',
                rmin = self.NDHallSpace4Dim[0],
                rmax = self.NDHallSpace4Dim[1],
                dz = 0.5*self.NDHallSpace4Dim[2],
                sphi = self.NDHallSpace4Dim[3],
                dphi = self.NDHallSpace4Dim[4])

        NDHallAirVolSpace4Position = geom.structure.Position( 'NDHallAirVolSpace4Position',
                self.NDHallSpace4Pos[0],
                self.NDHallSpace4Pos[1],
                self.NDHallSpace4Pos[2])

        NDHallAirVolSpace5 = geom.shapes.Box( 'NDHallAirVolSpace5',
                dx = 0.5*self.NDHallSpace5Dim[0],
                dy = 0.5*self.NDHallSpace5Dim[1],
                dz = 0.5*self.NDHallSpace5Dim[2])

        NDHallAirVolSpace5Position = geom.structure.Position( 'NDHallAirVolSpace5Position',
                self.NDHallSpace5Pos[0],
                self.NDHallSpace5Pos[1],
                self.NDHallSpace5Pos[2])

        NDHallAirVolSpace6 = geom.shapes.Box( 'NDHallAirVolSpace6',
                dx = 0.5*self.NDHallSpace6Dim[0],
                dy = 0.5*self.NDHallSpace6Dim[1],
                dz = 0.5*self.NDHallSpace6Dim[2])

        NDHallAirVolSpace6Position = geom.structure.Position( 'NDHallAirVolSpace6Position',
                self.NDHallSpace6Pos[0],
                self.NDHallSpace6Pos[1],
                self.NDHallSpace6Pos[2])

        NDHallAirVolSpace7 = geom.shapes.Box( 'NDHallAirVolSpace7',
                dx = 0.5*self.NDHallSpace7Dim[0],
                dy = 0.5*self.NDHallSpace7Dim[1],
                dz = 0.5*self.NDHallSpace7Dim[2])

        NDHallAirVolSpace7Position = geom.structure.Position( 'NDHallAirVolSpace7Position',
                self.NDHallSpace7Pos[0],
                self.NDHallSpace7Pos[1],
                self.NDHallSpace7Pos[2])

        NDHallAirVolTemp1 = geom.shapes.Boolean( 'NDHallAirVolTemp1', type='union', first=NDHallAirVolSpace1, second=NDHallAirVolSpace2, pos=NDHallAirVolSpace2Position)

        NDHallAirVolTemp2 = geom.shapes.Boolean( 'NDHallAirVolTemp2', type='union', first=NDHallAirVolTemp1, second=NDHallAirVolSpace3, rot='r90aboutX', pos=NDHallAirVolSpace3Position)

        NDHallAirVolTemp3 = geom.shapes.Boolean( 'NDHallAirVolTemp3', type='union', first=NDHallAirVolTemp2, second=NDHallAirVolSpace4, rot='r90aboutY', pos=NDHallAirVolSpace4Position)

        NDHallAirVolTemp4 = geom.shapes.Boolean( 'NDHallAirVolTemp4', type='union', first=NDHallAirVolTemp3, second=NDHallAirVolSpace5, pos=NDHallAirVolSpace5Position)
        
        NDHallAirVolTemp5 = geom.shapes.Boolean( 'NDHallAirVolTemp5', type='union', first=NDHallAirVolTemp4, second=NDHallAirVolSpace6, pos=NDHallAirVolSpace6Position)

        NDHallAirVolShape = geom.shapes.Boolean( 'NDHallAirVolShape', type='union', first=NDHallAirVolTemp5, second=NDHallAirVolSpace7, pos=NDHallAirVolSpace7Position)

        NDHallAirVol_lv = geom.structure.Volume( 'volDetEnclosure', material=self.mat, shape=NDHallAirVolShape)
        self.add_volume( NDHallAirVol_lv )

        for i,sb in enumerate(self.get_builders()):
            Pos = [Q("0m"),Q("0m"),Q("0m")]
            Rot = [Q("0deg"),Q("0deg"),Q("0deg")]
            if self.Positions!=None :
                Pos=self.Positions[i]
            if self.Positions!=None:
                Rot=self.Rotations[i]
            sb_lv = sb.get_volume()
            sb_pos = geom.structure.Position( sb_lv.name+'_pos', Pos[0], Pos[1], Pos[2] )
            sb_rot = geom.structure.Rotation( sb_lv.name+'_rot', Rot[0], Rot[1], Rot[2] )
            sb_pla = geom.structure.Placement( sb_lv.name+'_pla', volume=sb_lv, pos=sb_pos, rot=sb_rot )
            NDHallAirVol_lv.placements.append( sb_pla.name )



