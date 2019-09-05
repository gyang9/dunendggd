import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class NDElevatorStructBuilder(gegede.builder.Builder):

    def configure(self, mat=None, elevatorBlock1Dim=None, elevatorBlock2Dim=None, elevatorBlock2Pos=None, elevatorBlock3Dim=None, elevatorBlock3Pos=None,  **kwds):

        self.mat=mat
        self.elevatorBlock1Dim=elevatorBlock1Dim
        self.elevatorBlock2Dim=elevatorBlock2Dim
        self.elevatorBlock2Pos=elevatorBlock2Pos
        self.elevatorBlock3Dim=elevatorBlock3Dim
        self.elevatorBlock3Pos=elevatorBlock3Pos

    def construct(self, geom):

        elevatorBlock1 = geom.shapes.Box( 'elevatorBlock1',
                dx = 0.5*self.elevatorBlock1Dim[0],
                dy = 0.5*self.elevatorBlock1Dim[1],
                dz = 0.5*self.elevatorBlock1Dim[2])

        elevatorBlock2 = geom.shapes.Tubs( 'elevatorBlock2',
                rmin = self.elevatorBlock2Dim[0],
                rmax = self.elevatorBlock2Dim[1],
                dz = 0.5*self.elevatorBlock2Dim[2],
                sphi = self.elevatorBlock2Dim[3],
                dphi = self.elevatorBlock2Dim[4])

        elevatorBlock2Position = geom.structure.Position( 'elevatorBlock2Position',
                self.elevatorBlock2Pos[0],
                self.elevatorBlock2Pos[1],
                self.elevatorBlock2Pos[2])

        elevatorBlock3 = geom.shapes.Tubs( 'elevatorBlock3',
                rmin = self.elevatorBlock3Dim[0],
                rmax = self.elevatorBlock3Dim[1],
                dz = 0.5*self.elevatorBlock3Dim[2],
                sphi = self.elevatorBlock3Dim[3],
                dphi = self.elevatorBlock3Dim[4])

        elevatorBlock3Position = geom.structure.Position( 'elevatorBlock3Position',
                self.elevatorBlock3Pos[0],
                self.elevatorBlock3Pos[1],
                self.elevatorBlock3Pos[2])

        elevatorBlockShapeTemp = geom.shapes.Boolean( 'elevatorBlockShapeTemp', type='union', first=elevatorBlock1, second=elevatorBlock2, rot="r90aboutX180aboutY", pos=elevatorBlock2Position)
        elevatorBlockShape = geom.shapes.Boolean( 'elevatorBlockShape', type='subtraction', first=elevatorBlockShapeTemp, second=elevatorBlock3, rot="r90aboutX180aboutY", pos=elevatorBlock3Position)

        elevatorBlock_lv = geom.structure.Volume( 'elevatorBlock_lv', material=self.mat, shape=elevatorBlockShape)

        self.add_volume( elevatorBlock_lv )

