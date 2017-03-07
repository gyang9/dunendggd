#!/usr/bin/env python
'''
Subbuilder of TrackerBuilder
'''

import gegede.builder
from gegede import Quantity as Q

class TrackerBuilder(gegede.builder.Builder):
    '''
    Assemble all the subsystems into one bounding box.
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
                  tracDim = [Q('2m'), Q('4m'), Q('4m')], ScinMat = 'Scintillator',
                  **kwds):

        self.tracDim = tracDim 
        self.ScinMat = ScinMat 

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
							        
        # Make detector box
        tracBox = geom.shapes.Box(self.name, self.tracDim[0], self.tracDim[1], self.tracDim[2])
       
        trac_lv = geom.structure.Volume('vol'+self.name, material=self.ScinMat, shape=tracBox )

        self.add_volume(trac_lv)

    	return
