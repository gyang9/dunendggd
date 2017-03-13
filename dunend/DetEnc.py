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
    def configure(self, 
                  detEncDim=None, 
                  encBoundToDet_z=None, 
                  detDim=None,
                  blankSite = False,
                  detEncMat = 'Air', **kwds):
        if detEncDim is None:
            raise ValueError("No value given for detEncDim")
        if encBoundToDet_z is None:
            raise ValueError("No value given for encBoundToDet_z")
        if detDim is None:
            self.configDetDim = False
        else: 
            self.configDetDim = True
            self.detDim       = detDim


        self.detEncMat     = detEncMat
        self.detEncDim     = detEncDim
        self.blankSite     = blankSite

        # Space from negative face of volDetEnc to closest face of volDet
        #  This positions the detector in the enclosure
        self.encBoundToDet_z = encBoundToDet_z

    ## The construct
    def construct(self, geom):


        for sb in self.get_builders():

            sb_lv = sb.get_volume()
            sb_shape = geom.store.shapes.get( sb_lv.shape )

        encBox = geom.shapes.Box( self.name,                 dx=0.5*self.detEncDim[0], 
                                  dy=0.5*self.detEncDim[1],  dz=0.5*self.detEncDim[2])
        detEnc_lv = geom.structure.Volume('vol'+self.name, material=self.detEncMat, shape=encBox)
        self.add_volume(detEnc_lv)


        if (self.configDetDim):
            print "DetectorBuilder: Detector box configured:"
        else:
            self.detDim = list(sb.magOutDim)
            print "DetectorBuilder: Detector box calculated:"
        print     "                 x="+str(self.detDim[0])+" y="+str(self.detDim[1])+" z="+str(self.detDim[2])

        self.encBoundToDet = [ 0.5*self.detEncDim[0] - 0.5*self.detDim[0], # x: center it for now
                               Q('0cm'),                                   # y: sit detector on floor
                               self.encBoundToDet_z ]                      # z: configure

        detEncPos = [ -0.5*self.detEncDim[0] + self.encBoundToDet[0] + 0.5*self.detDim[0], 
                   -0.5*self.detEncDim[1] + self.encBoundToDet[1] + 0.5*self.detDim[1], 
                   -0.5*self.detEncDim[2] + self.encBoundToDet[2] + 0.5*self.detDim[2]  ]
        sb_pos = geom.structure.Position( sb_lv.name+'_pos', detEncPos[0], detEncPos[1], detEncPos[2])
        sb_pla = geom.structure.Placement(sb_lv.name+'_pla', volume=sb_lv, pos=sb_pos)
        detEnc_lv.placements.append(sb_pla.name )
