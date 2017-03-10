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
    def configure(self, detEncDim=None, detEncMat=None, detEncPos=None, **kwds):
        self.detEncDim, self.detEncMat = (detEncDim, detEncMat)
        self.detEncPos = detEncPos
        pass

    ## The construct
    def construct(self, geom):
        DetEncBox = geom.shapes.Box(self.name, dx=self.detEncDim[0], dy=self.detEncDim[1], dz=self.detEncDim[2])
        main_lv = geom.structure.Volume(self.name+"_lv", material=self.detEncMat, shape=DetEncBox)
        self.add_volume(main_lv)

        for sb in self.get_builders():
            sb_lv = sb.get_volume()
            sb_shape = geom.store.shapes.get( sb_lv.shape )
            sb_pos = geom.structure.Position( sb_lv.name+'_pos', self.detEncPos[0], self.detEncPos[1], self.detEncPos[2])
            sb_pla = geom.structure.Placement(sb_lv.name+'_pla', volume=sb_lv, pos=sb_pos)
            main_lv.placements.append(sb_pla.name )
