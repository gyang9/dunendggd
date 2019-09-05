#!/usr/bin/env python
import gegede.builder
from duneggd.LocalTools import localtools as ltools
from gegede import Quantity as Q

class NDHallwayStructBuilder(gegede.builder.Builder):

    def configure(self, mat, egressHallwayInnerDim=None, egressHallwayInnerPos=None, egressHallwayOuterDim=None, egressHallwayOuterPos=None, egressHallwayDoorDim=None, egressHallwayDoorPos=None, **kwds):

        self.mat=mat
        self.egressHallwayInnerDim=egressHallwayInnerDim
        self.egressHallwayInnerPos=egressHallwayInnerPos
        self.egressHallwayOuterDim=egressHallwayOuterDim
        self.egressHallwayOuterPos=egressHallwayOuterPos
        self.egressHallwayDoorDim=egressHallwayDoorDim
        self.egressHallwayDoorPos=egressHallwayDoorPos

    def construct(self, geom):

       egressHallwayInner = geom.shapes.Box( 'egressHallwayInner',
               dx = 0.5*self.egressHallwayInnerDim[0],
               dy = 0.5*self.egressHallwayInnerDim[1],
               dz = 0.5*self.egressHallwayInnerDim[2])

       egressHallwayInnerPosition = geom.structure.Position( 'egressHallwayInnerPosition',
               self.egressHallwayInnerPos[0],
               self.egressHallwayInnerPos[1],
               self.egressHallwayInnerPos[2])

       egressHallwayOuter = geom.shapes.Box( 'egressHallwayOuter',
               dx = 0.5*self.egressHallwayOuterDim[0],
               dy = 0.5*self.egressHallwayOuterDim[1],
               dz = 0.5*self.egressHallwayOuterDim[2])

       egressHallwayOuterPosition = geom.structure.Position( 'egressHallwayPosition',
               self.egressHallwayOuterPos[0],
               self.egressHallwayOuterPos[1],
               self.egressHallwayOuterPos[2])
        
       egressHallwayDoor = geom.shapes.Box( 'egressHallwayDoor',
               dx = 0.5*self.egressHallwayDoorDim[0],
               dy = 0.5*self.egressHallwayDoorDim[1],
               dz = 0.5*self.egressHallwayDoorDim[2])

       egressHallwayDoorPosition = geom.structure.Position( 'egressHallwayDoorPosition',
               self.egressHallwayDoorPos[0],
               self.egressHallwayDoorPos[1],
               self.egressHallwayDoorPos[2])

       egressHallwayShapeTemp = geom.shapes.Boolean( 'egressHallwayShapeTemp', type='subtraction', first=egressHallwayOuter, second=egressHallwayInner, pos=egressHallwayInnerPosition)

       egressHallwayShape = geom.shapes.Boolean( 'egressHallwayShape', type='subtraction', first=egressHallwayShapeTemp, second=egressHallwayDoor, pos=egressHallwayDoorPosition)

       egressHallway_lv = geom.structure.Volume( 'egressHallway_lv', material=self.mat, shape=egressHallwayShape)

       self.add_volume( egressHallway_lv )
