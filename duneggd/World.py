#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q


class WorldBuilder(gegede.builder.Builder):
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, halfDimension=None, Material=None, DetEncPosition=None, **kwds):
        self.halfDimension = halfDimension
        self.Material = Material
        self.DetEncPosition = DetEncPosition

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        ########################### Above is math, below is GGD ###########################

        materials.define_materials(geom)

        noRotate       = geom.structure.Rotation( 'noRotate',      '0deg',  '0deg',  '0deg'  )
        r90aboutX      = geom.structure.Rotation( 'r90aboutX',      '90deg',  '0deg',  '0deg'  )
        rminus90aboutX = geom.structure.Rotation( 'rminus90aboutX', '-90deg', '0deg',  '0deg'  )
        r90aboutY      = geom.structure.Rotation( 'r90aboutY',      '0deg',   '90deg', '0deg'  )
        r180aboutY     = geom.structure.Rotation( 'r180aboutY',     '0deg',   '180deg','0deg'  )
        rminus90aboutY = geom.structure.Rotation( 'rminus90aboutY', '0deg', '-90deg',  '0deg'  )
        r90aboutZ      = geom.structure.Rotation( 'r90aboutZ',      '0deg',   '0deg',  '90deg' )
        r90aboutXZ     = geom.structure.Rotation( 'r90aboutXZ', '90deg',  '0deg', '90deg'  )
        r90aboutYZ     = geom.structure.Rotation( 'r90aboutYZ', '0deg',  '90deg', '90deg'  )
        r90aboutXminusZ     = geom.structure.Rotation( 'r90aboutXminusZ', '-90deg',  '0deg', '90deg'  )
        r90aboutYminusZ     = geom.structure.Rotation( 'r90aboutYminusZ', '0deg',  '-90deg', '90deg'  )

        main_lv, main_hDim = ltools.main_lv( self, geom, "Box")
        self.add_volume(main_lv)

        # get Detector Enclosure and its logic volume
        de_sb = self.get_builder()
        de_lv = de_sb.get_volume()

        postemp = [Q('0m'),Q('0m'),Q('0m')]
        if self.DetEncPosition!=None:
            postemp=self.DetEncPosition
        detEnc_pos = geom.structure.Position(de_lv.name+'_pos', postemp[0], postemp[1], postemp[2])
        detEnc_pla = geom.structure.Placement(de_lv.name+'_pla', volume=de_lv, pos=detEnc_pos)
        main_lv.placements.append(detEnc_pla.name)
