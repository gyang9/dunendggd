#!/usr/bin/env python
## Subbuilder of DetEncBuilder
#

import gegede.builder
from gegede import Quantity as Q

## idDetBuilder
#
# builder for ID detector
class idDetBuilder(gegede.builder.Builder):

    ## The configure
    def configure( self, idMaterial=None, **kwds ):
        self.idMaterial = idMaterial
        pass

    ## The construct
    def construct( self, geom ):
        
        idDim = [Q("0m"),Q("0m"),Q("0m")]
        for sb in self.get_builders():
            sb_lv = sb.get_volume()
            sb_shape = geom.store.shapes.get( sb_lv.shape )
            idDim[0] = sb_shape.dx 
            idDim[1] = sb_shape.dy
            idDim[2] += sb_shape.dz 

        print "dimension of idDet ", idDim

        idDetBox = geom.shapes.Box( self.name, dx=idDim[0], dy=idDim[1], dz=idDim[2] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.idMaterial, shape=idDetBox )
        self.add_volume( main_lv )

        ztemp = -idDim[2]
        for sb in self.get_builders():
            sb_lv = sb.get_volume()
            sb_shape = geom.store.shapes.get( sb_lv.shape )
            ztemp += sb_shape.dz
            sb_pos = geom.structure.Position( sb_lv.name+'_pos', '0m', '0m', ztemp)
            ztemp += sb_shape.dz
            sb_pla = geom.structure.Placement(sb_lv.name+'_pla', volume=sb_lv, pos=sb_pos)
            main_lv.placements.append(sb_pla.name )
        return

