#!/usr/bin/env python
## Subbuilder of DetEncBuilder
#

import gegede.builder
from gegede import Quantity as Q

## DetEncBuilder
#
# builder for id Plane
class DetEncBuilder(gegede.builder.Builder):

    ## The configure
    def configure(self, detEncDimension=None, detEncMaterial=None, **kwds):
        self.detEncDimension, self.detEncMaterial = ( detEncDimension, detEncMaterial )

    ## The construct
    def construct(self, geom):
        main_shape = geom.shapes.Box( self.name+"_shape", dx = self.detEncDimension[0],
                                        dy = self.detEncDimension[1], dz = self.detEncDimension[2] )
        main_lv = geom.structure.Volume( self.name+"_lv", material=self.detEncMaterial, shape=main_shape )
        self.add_volume( main_lv )

        detEncPos = [Q("0m"),Q("0m"),Q("0m")]
        for sb in self.get_builders():
            sb_lv = sb.get_volume()
            sb_pos = geom.structure.Position( sb_lv.name+'_pos', detEncPos[0], detEncPos[1], detEncPos[2] )
            sb_pla = geom.structure.Placement( sb_lv.name+'_pla', volume=sb_lv, pos=sb_pos )
            main_lv.placements.append( sb_pla.name )
