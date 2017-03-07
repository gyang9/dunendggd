#!/usr/bin/env python
## Subbuilder of DetEncBuilder
#

import gegede.builder
from gegede import Quantity as Q

## primDetBuilder
#
# builder for ID detector
class primDetBuilder(gegede.builder.Builder):

    ## The configure
    def configure( self, primDimension=None, primMaterial=None, primTranspV=None, **kwds ):
        self.primDimension = primDimension
        self.primMaterial, self.primTranspV = (primMaterial, primTranspV)
        pass

    ## The construct
    def construct( self, geom ):
        
        primDetBox = geom.shapes.Box( self.name, dx=self.primDimension[0], dy=self.primDimension[1], dz=self.primDimension[2] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.primMaterial, shape=primDetBox )
        self.add_volume( main_lv )

        postemp = [Q("0m"),Q("0m"),Q("0m")]
        jdet = 0
        for sb in self.get_builders():
            sb_lv = sb.get_volume()
            #sb_shape = geom.store.shapes.get( sb_lv.shape )
            if jdet == 0:
                postemp = [ptemp+sbgap for ptemp,sbgap in zip(postemp, sb.primGapV)]
            else:
                postemp = [ptemp+sbgap+sbdim*trans for ptemp,sbgap,sbdim,trans in zip(postemp, sb.primGapV, sb.primDimension, self.primTranspV)]
            sb_pos = geom.structure.Position( sb_lv.name+'_pos', postemp[0], postemp[1], postemp[2])
            postemp = [ptemp+sbgap+sbdim*trans for ptemp,sbgap,sbdim,trans in zip(postemp, sb.primGapV, sb.primDimension, self.primTranspV)]
            #postemp[0] += (sb_shape.dx)*self.primTranspV[0]
            jdet += 1
            sb_pla = geom.structure.Placement(sb_lv.name+'_pla', volume=sb_lv, pos=sb_pos)
            main_lv.placements.append(sb_pla.name )
        return

