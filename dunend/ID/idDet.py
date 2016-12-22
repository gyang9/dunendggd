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
    def configure( self, idDetMat, **kwds ):
        self.material = idDetMat
        pass

    ## The construct
    def construct( self, geom ):
        
        idDim = [0,0,0]

        for sb in self.builders:
            sb_shape = geom.store.shapes.get( geom.store.structure.get(sb).shape )
            idDim += sb_shape.dx 
            idDim = sb_shape.dy
            idDim = sb_shape.dz 

        idDetBox = geom.shapes.Box( self.name, idDim[0], idDim[1], idDim[2] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.idDetMat, shape=idDetBox )
        self.add_volume( main_lv )

        xtemp = 0
        for sb in self.builders:
            lv = sb.volumes[0]
            sb_shape = geom.store.shapes.get( geom.store.structure.get(sb).shape )
            sb_pos = geom.structure.Position(lv.name+'_pos', xtemp+sb_shape.dx, '0cm', '0cm')
            xtemp += sb_shape.dx
            sb_pla = geom.structure.Placement(lv.name+'_pla', volumen=lv, pos=sb_pos)
            main_lv.placements.append(sb_pla.name )

        return 
