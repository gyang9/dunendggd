#!/usr/bin/env python
'''
Top level builder of the Fine-Grained Tracker (FGT)
'''

import gegede.builder
import math
from gegede import Quantity as Q


class WorldBuilder(gegede.builder.Builder):
    '''
    Build a big box world volume.
    N.B. -- Global convention: index 0,1,2 = x,y,z
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, worldDim  =  [Q('100m'),Q('100m'),Q('100m')], 
                  servBuildingDim =  [Q('45ft'),Q('37.5ft'),Q('135.5ft')], 
                  secondHallDim   =  [Q('47ft'),Q('11ft'),Q('19ft')], 
                  encBackWallToHall_z = Q('46.25ft'),
                  overburden          = Q('155.94ft'),
                  dirtDepth           = Q('50ft'),
                  primaryShaft_r      = Q('11ft'), 
                  secondaryShaft_r    = Q('8.5ft'),
                  shaftToEndBuilding  = Q('79ft'),
                  worldMat='Rock', **kwds):
        self.worldDim = worldDim
        self.material   = worldMat
        self.detEncBldr  = self.get_builder("Secondary")

        self.servBDim            = servBuildingDim
        self.overburden          = overburden
        self.dirtDepth           = dirtDepth
        self.primaryShaft_r      = primaryShaft_r
        self.secondaryShaft_r    = secondaryShaft_r
        self.secondHallDim       = secondHallDim
        self.encBackWallToHall_z = encBackWallToHall_z
        self.shaftToEndBuilding  = shaftToEndBuilding

        self.secHallMat = 'Air'
        self.servBMat   = 'Air'
        self.shaftMat   = 'Air'


    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        # Get relevant dimensions
        detEncDim     = list(self.detEncBldr.detEncDim)
        secShaft_y    = self.overburden + detEncDim[1] - self.secondHallDim[1]

        encBoundToDet = list(self.detEncBldr.encBoundToDet)
        detDim        = list(self.detEncBldr.detDim)
        

        ########################### SET THE ORIGIN  #############################
        #                                                                       #
        # Position volDetEnclosure in the World Volume, displacing the world    #
        #  origin relative to the detector enclosure, thereby putting it        #
        #  anywhere in or around the detector we need.                          #
        #                                                                       #
        # Bring x=0 to -x of detEnc, then to det face, then to center of det    #
        setXCenter    =   0.5*detEncDim[0] - encBoundToDet[0] - 0.5*detDim[0]   #
                                                                                #
        # Bring y=0 to bottom of detEnc, then to center of detector             #
        setYCenter    =   0.5*detEncDim[1] - encBoundToDet[1] - 0.5*detDim[1]   #
                                                                                #
        # Bring z=0 to back of detEnc, then to upstream face of detector.       #
        setZCenter    =   0.5*detEncDim[2] - encBoundToDet[2]                   #
        #  should we leave this at the back of the enclosure?:                  #
        #setZCenter    =  -0.5*detEncDim[2]                                     #
                                                                                #
        detEncPos     = [ setXCenter, setYCenter, setZCenter ]                  #
        #########################################################################


        worldBox = geom.shapes.Box( self.name,               dx=0.5*self.worldDim[0], 
                                    dy=0.5*self.worldDim[1], dz=0.5*self.worldDim[2])
        world_lv = geom.structure.Volume('vol'+self.name, material=self.material, shape=worldBox)
        self.add_volume(world_lv)

        # Get volDetEnclosure and place it
        detEnc_lv = self.detEncBldr.get_volume("volSecondary")
        detEnc_in_world = geom.structure.Position('DetEnc_in_World', detEncPos[0], detEncPos[1], detEncPos[2])
        pD_in_W = geom.structure.Placement('placeDetEnc_in_World',
                                           volume = detEnc_lv,
                                           pos = detEnc_in_world)
        world_lv.placements.append(pD_in_W.name)

