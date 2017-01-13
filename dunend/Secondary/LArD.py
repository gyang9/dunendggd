#!/usr/bin/env python
'''
Subbuilder of DetEncBuilder
'''

import gegede.builder
from gegede import Quantity as Q

class DetectorBuilder(gegede.builder.Builder):
    '''
    Assemble all the subsystems into one bounding box.
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
                  detDim = [Q('6m'), Q('4m'), Q('4m')], defMat = 'Air', LArMat = 'LAr',
                  **kwds):

        self.defMat  = defMat
        self.detDim  = detDim 
        self.WireBldr = self.get_builder('Wire')
        self.LArMat  = LArMat

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        wire_lv  = self.WireBldr.get_volume('volWire')

        #self.nWire    = list(self.WireBldr.nWirea) 
        self.lowEnd   = Q('-6m')#list(self.WireBldr.lowEnda) 
        self.wireDis  = Q('10cm')#list(self.WireBldr.wireDisa) 

        # vol is a bounding box ~ not corresponding to physical volume.
        #  assume Barrel biggest in x and y

#        det_Pos = geom.structure.Position('det_pos', '0cm', '0cm', '0cm')
							        
        # Make LArD box
        detBox = geom.shapes.Box(self.name, self.detDim[0], self.detDim[1], self.detDim[2])
       
        det_lv = geom.structure.Volume('vol'+self.name, material=self.defMat, shape=detBox)

#        pdet_lv  = geom.structure.Placement('place_det', volume = det_lv, pos = det_Pos)
        self.add_volume(det_lv)

        print '########################################'


        LArBox = geom.shapes.Box('LArShape', self.detDim[0], self.detDim[1], self.detDim[2])
        LArBox_lv = geom.structure.Volume('volLAr', material=self.LArMat, shape=LArBox)
        LArBox_Pos = geom.structure.Position('LArBox_pos', '0cm', '0cm', '0cm')
        pLArBox_lv  = geom.structure.Placement('place_LAr', volume = LArBox_lv, pos = LArBox_Pos)
        det_lv.placements.append(pLArBox_lv.name )


    	#for j in range(self.nWire):
        for j in range(120):

		tempPos  = self.lowEnd+j*self.wireDis
        	wire_Pos = geom.structure.Position('wie_pos_'+str(j), self.lowEnd+j*self.wireDis, '4m', '0cm')

        	pwire_lv  = geom.structure.Placement('place_wire'+str(j), volume = wire_lv, pos = wire_Pos)

        	det_lv.placements.append(pwire_lv.name )

        print self.name
    	return
