#!/usr/bin/env python
## Subbuilder of idSubDetBuilder
#

import gegede.builder
from gegede import Quantity as Q

## idSubDetBuilder
#
# builder for id SubDet
class idSubDetBuilder(gegede.builder.Builder):

    ## The configure
    def configure( self, idDimension=None, idMaterial=None, idNElements=None, **kwds ):
        self.idDimension, self.idMaterial = ( idDimension, idMaterial )
        self.idNElements = idNElements
        pass

    ## The construct
    def construct( self, geom ):
        idSubDetBox = geom.shapes.Box( self.name, dx=self.idDimension[0], dy=self.idDimension[1], dz=self.idDimension[2] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.idMaterial, shape=idSubDetBox )
        main_lv.params.append(("Color","green"))
        self.add_volume( main_lv )

        """
        LArBox = geom.shapes.Box('LArShape', self.idDimension[0], self.idDimension[1], self.idDimension[2])
        LAr_lv = geom.structure.Volume('LAr_lv', material="LAr", shape=LArBox)
        LAr_pos = geom.structure.Position('LAr_pos', '0cm', '0cm', '0cm')
        LAr_pla  = geom.structure.Placement('LAr_pla', volume = LAr_lv, pos = LAr_pos)
        main_lv.placements.append(LAr_pla.name )
        """

        element_lv = self.get_builder().get_volume()
        print element_lv
        low_end = self.idDimension[0]
        dist = Q('30cm')

        for element in range(self.idNElements):
            element_pos = geom.structure.Position(self.name+"_el"+str(element)+'_pos', low_end-dist, '0m', '0m')
            element_pla = geom.structure.Placement(self.name+"_el"+str(element)+'_pla', volume = element_lv, pos = element_pos)
            main_lv.placements.append(element_pla.name )

        return
