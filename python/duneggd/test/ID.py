#!/usr/bin/env python
'''
Subbuilder of DetEncBuilder
'''

import gegede.builder
from gegede import Quantity as Q

class IDBuilder(gegede.builder.Builder):
    '''
    Assemble all the subsystems into one bounding box.
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
                  IDDim = [Q('10m'), Q('10m'), Q('10m')], IDMat = 'Air', 
                  LArDPos = [Q('0m'),Q('0m'),Q('0m')],  TrackerPos = [Q('15m'),Q('0m'),Q('0m')],
                  **kwds):

        self.IDMat      = IDMat
        self.IDDim      = IDDim 
        self.TrackerPos = TrackerPos
        self.LArDPos    = LArDPos

        self.LArDBldr   = self.get_builder('LArD')
        self.TrackerBldr= self.get_builder('Tracker')

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        # generate ID lv 

        IDBox = geom.shapes.Box(self.name, self.IDDim[0], self.IDDim[1], self.IDDim[2])
       
        ID_lv = geom.structure.Volume('vol'+self.name, material=self.IDMat, shape=IDBox )

        self.add_volume(ID_lv)

        # Get LArD lv

        LArD_lv  = self.LArDBldr.get_volume('volLArD')
 

        # Position of the LArD

        LArD_Pos = geom.structure.Position('LArD_pos', self.LArDPos[0], self.LArDPos[1], self.LArDPos[2])
							        
        # Make LArD box
       
        pLArD_lv = geom.structure.Placement('place_LArD', volume = LArD_lv, pos = LArD_Pos)

        ID_lv.placements.append(pLArD_lv.name )

        print '########################################'

        # Get Tracker lv

        Tracker_lv  = self.TrackerBldr.get_volume('volTracker')
 

        # Position of the Tracker

        Tracker_Pos = geom.structure.Position('Tracker_pos', self.TrackerPos[0], self.TrackerPos[1], self.TrackerPos[2])
							        
        # Make LArD box
       
        pTracker_lv = geom.structure.Placement('place_Tracker', volume = Tracker_lv, pos = Tracker_Pos)

        ID_lv.placements.append(pTracker_lv.name )

    	return
