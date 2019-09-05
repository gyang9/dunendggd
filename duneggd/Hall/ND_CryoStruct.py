import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class NDCryoStructBuilder(gegede.builder.Builder):

    def configure(self, matTube=None , matFull=None, fullDim=None, cryoTube1Dim=None, cryoTube1Pos=None, cryoTube2Dim=None, cryoTube2Pos=None, cryoTube3Dim=None, cryoTube3Pos=None, cryoTube4Dim=None, cryoTube4Pos=None, cryoTube5Dim=None, cryoTube5Pos=None, **kwds):

        self.matTube=matTube
        self.matFull=matFull
        self.fullDim=fullDim
        self.cryoTube1Dim=cryoTube1Dim
        self.cryoTube1Pos=cryoTube1Pos
        self.cryoTube2Dim=cryoTube2Dim
        self.cryoTube2Pos=cryoTube2Pos
        self.cryoTube3Dim=cryoTube3Dim
        self.cryoTube3Pos=cryoTube3Pos
        self.cryoTube4Dim=cryoTube4Dim
        self.cryoTube4Pos=cryoTube4Pos
        self.cryoTube5Dim=cryoTube5Dim
        self.cryoTube5Pos=cryoTube5Pos

    def construct(self, geom):

        fullCryoTubeBox = geom.shapes.Box( 'fullCryoTubeBox',
                dx = 0.5*self.fullDim[0],
                dy = 0.5*self.fullDim[1],
                dz = 0.5*self.fullDim[2])

        fullCryoTubeBox_lv = geom.structure.Volume( 'volfullCryoTubeBox', material=self.matFull, shape=fullCryoTubeBox)

        self.add_volume( fullCryoTubeBox_lv )

        self.getCryoTubes( fullCryoTubeBox_lv, geom)

        return

    def getCryoTubes(self, fullCryoTubeBox_lv, geom):


        cryoTube1 = geom.shapes.Tubs( 'cryoTube1',
                rmin = self.cryoTube1Dim[0],
                rmax = self.cryoTube1Dim[1],
                dz = 0.5*self.cryoTube1Dim[2],
                sphi = self.cryoTube1Dim[3],
                dphi = self.cryoTube1Dim[4])
            
        cryoTube1Position = geom.structure.Position('cryoTube1Position',
                self.cryoTube1Pos[0],
                self.cryoTube1Pos[1],
                self.cryoTube1Pos[2])

        cryoTube1_lv = geom.structure.Volume( 'cryoTube1_lv', material=self.matTube, shape=cryoTube1)
        placeCryoTube1 = geom.structure.Placement( 'placeCryoTube1Name', volume=cryoTube1_lv, pos=cryoTube1Position)
        fullCryoTubeBox_lv.placements.append( placeCryoTube1.name )

        ###########################################################

        cryoTube2 = geom.shapes.Tubs( 'cryoTube2',
                rmin = self.cryoTube2Dim[0],
                rmax = self.cryoTube2Dim[1],
                dz = 0.5*self.cryoTube2Dim[2],
                sphi = self.cryoTube2Dim[3],
                dphi = self.cryoTube2Dim[4])
            
        cryoTube2Position = geom.structure.Position('cryoTube2Position',
                self.cryoTube2Pos[0],
                self.cryoTube2Pos[1],
                self.cryoTube2Pos[2])

        cryoTube2_lv = geom.structure.Volume( 'cryoTube2_lv', material=self.matTube, shape=cryoTube2)
        placeCryoTube2 = geom.structure.Placement( 'placeCryoTube2Name', volume=cryoTube2_lv, pos=cryoTube2Position)
        fullCryoTubeBox_lv.placements.append( placeCryoTube2.name )

        ###########################################################

        cryoTube3 = geom.shapes.Tubs( 'cryoTube3',
                rmin = self.cryoTube3Dim[0],
                rmax = self.cryoTube3Dim[1],
                dz = 0.5*self.cryoTube3Dim[2],
                sphi = self.cryoTube3Dim[3],
                dphi = self.cryoTube3Dim[4])
            
        cryoTube3Position = geom.structure.Position('cryoTube3Position',
                self.cryoTube3Pos[0],
                self.cryoTube3Pos[1],
                self.cryoTube3Pos[2])

        cryoTube3_lv = geom.structure.Volume( 'cryoTube3_lv', material=self.matTube, shape=cryoTube3)
        placeCryoTube3 = geom.structure.Placement( 'placeCryoTube3Name', volume=cryoTube3_lv, pos=cryoTube3Position)
        fullCryoTubeBox_lv.placements.append( placeCryoTube3.name )

        ###########################################################

        cryoTube4 = geom.shapes.Tubs( 'cryoTube4',
                rmin = self.cryoTube4Dim[0],
                rmax = self.cryoTube4Dim[1],
                dz = 0.5*self.cryoTube4Dim[2],
                sphi = self.cryoTube4Dim[3],
                dphi = self.cryoTube4Dim[4])
            
        cryoTube4Position = geom.structure.Position('cryoTube4Position',
                self.cryoTube4Pos[0],
                self.cryoTube4Pos[1],
                self.cryoTube4Pos[2])

        cryoTube4_lv = geom.structure.Volume( 'cryoTube4_lv', material=self.matTube, shape=cryoTube4)
        placeCryoTube4 = geom.structure.Placement( 'placeCryoTube4Name', volume=cryoTube4_lv, pos=cryoTube4Position)
        fullCryoTubeBox_lv.placements.append( placeCryoTube4.name )

        ###########################################################

        cryoTube5 = geom.shapes.Tubs( 'cryoTube5',
                rmin = self.cryoTube5Dim[0],
                rmax = self.cryoTube5Dim[1],
                dz = 0.5*self.cryoTube5Dim[2],
                sphi = self.cryoTube5Dim[3],
                dphi = self.cryoTube5Dim[4])
            
        cryoTube5Position = geom.structure.Position('cryoTube5Position',
                self.cryoTube5Pos[0],
                self.cryoTube5Pos[1],
                self.cryoTube5Pos[2])

        cryoTube5_lv = geom.structure.Volume( 'cryoTube5_lv', material=self.matTube, shape=cryoTube5)
        placeCryoTube5 = geom.structure.Placement( 'placeCryoTube5Name', volume=cryoTube5_lv, pos=cryoTube5Position)
        fullCryoTubeBox_lv.placements.append( placeCryoTube5.name )




