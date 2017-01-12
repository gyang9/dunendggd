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
    def configure( self, idDimension=None, idMaterial=None, idTranspV=None, **kwds ):
        self.idDimension = idDimension
        self.idMaterial, self.idTranspV = (idMaterial, idTranspV)
        pass

    ## The construct
    def construct( self, geom ):
        
        idDetBox = geom.shapes.Box( self.name, dx=self.idDimension[0], dy=self.idDimension[1], dz=self.idDimension[2] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.idMaterial, shape=idDetBox )
        self.add_volume( main_lv )

        postemp = [Q("0m"),Q("0m"),Q("0m")]
        jdet = 0
        for sb in self.get_builders():
            sb_lv = sb.get_volume()
            #sb_shape = geom.store.shapes.get( sb_lv.shape )
            if jdet == 0:
                postemp = [ptemp+sbgap for ptemp,sbgap in zip(postemp, sb.idGapV)]
            else:
                postemp = [ptemp+sbgap+sbdim*trans for ptemp,sbgap,sbdim,trans in zip(postemp, sb.idGapV, sb.idDimension, self.idTranspV)]
            sb_pos = geom.structure.Position( sb_lv.name+'_pos', postemp[0], postemp[1], postemp[2])
            postemp = [ptemp+sbgap+sbdim*trans for ptemp,sbgap,sbdim,trans in zip(postemp, sb.idGapV, sb.idDimension, self.idTranspV)]
            #postemp[0] += (sb_shape.dx)*self.idTranspV[0]
            jdet += 1
            sb_pla = geom.structure.Placement(sb_lv.name+'_pla', volume=sb_lv, pos=sb_pos)
            main_lv.placements.append(sb_pla.name )
        return

