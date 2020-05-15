#!/usr/bin/env python
'''
Subbuilder of DetEncBuilder
'''

import gegede.builder
from gegede import Quantity as Q

class Secondary2Builder(gegede.builder.Builder):
    '''
    Assemble all the subsystems into one bounding box.
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, defMat = 'Air',  
                  magInDim=None,  magPos=None, 
                  ecalInDim=None, ecalDnPos=None, ecalUpPos=None, ecalBaPos=None, ecalDownRot=None, ecalUpRot=None, ecalBarRot=None,EcalBField=None, **kwds):

        self.defMat      = defMat
        self.magPos      = list(magPos)

        # Get all of the detector subsystems to position and place
        self.ecalDownBldr = self.get_builder('ECALDownstream')        
        #self.ecalUpBldr = self.get_builder('ECALUpstream')
        self.ecalBarBldr  = self.get_builder('ECALBarrel')
        self.MagnetBldr   = self.get_builder('Magnet')
        self.EcalBField = EcalBField

        self.ecalDownRot  = ecalDownRot
        self.ecalUpRot  = ecalUpRot
        self.ecalBarRot   = ecalBarRot
        
        self.magPos       = list(magPos)
        self.ecalDnPos    = list(ecalDnPos)
        #self.ecalUpPos    = list(ecalUpPos)
        self.ecalBaPos    = list(ecalBaPos)

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        
        # Get subsystem dimensions, 
        ecalDownDim    = list(self.ecalDownBldr.ecalModDim)
        ecalBarOutDim  = list(self.ecalBarBldr.ecalOutDim)
        ecalBarInDim   = list(self.ecalBarBldr.ecalInDim)
        magBoxOutDim   = list(self.MagnetBldr.MagnetOutt)
        magBoxInDim    = list(self.MagnetBldr.MagnetInn)

        magPos      = list(self.magPos) 
        ecalBarPos  = list(self.ecalBaPos)
        ecalDnPos   = list(self.ecalDnPos)
        #ecalUpPos   = list(self.ecalUpPos)


        detOut = geom.shapes.Box( 'detOut',              dx=0.5*magBoxOutDim[0], 
                                  dy=0.5*magBoxOutDim[1],  dz=0.5*magBoxOutDim[2]*2)
        detIn = geom.shapes.Box(  'detIn',                  dx=0.5*ecalBarInDim[0],
                                   dy=0.5*ecalBarInDim[1],  dz=0.5*ecalBarInDim[2])
        detBox = geom.shapes.Boolean( self.name, type='subtraction', first=detOut, second=detIn )

        det_lv = geom.structure.Volume('vol'+self.name, material=self.defMat, shape=detBox)
        self.add_volume(det_lv)

        magnet_lv = self.MagnetBldr.get_volume('volMagnet')
        magnet_in_det = geom.structure.Position('magnet_in_det', magPos[0], magPos[1], magPos[2])
        pMagnet_in_det = geom.structure.Placement('placeMagnet_in_det',
                                                  volume = magnet_lv,
                                                  pos = magnet_in_det)

        det_lv.placements.append(pMagnet_in_det.name)


        # Get volECALDownstream, volECALUpstream, volECALBarrel volumes and place in volDetector

        ecalDown_lv = self.ecalDownBldr.get_volume('volECALDownstream')
        if isinstance(self.EcalBField,str):
            ecalDown_lv.params.append(("BField",self.EcalBField))

        ecalDown_in_det = geom.structure.Position('ECALDown_in_MagInner', ecalDnPos[0], ecalDnPos[1], ecalDnPos[2])
        pecalDown_in_MagInner = geom.structure.Placement('placeECALDown_in_MagInner',
                                                  volume = ecalDown_lv,
                                                  pos = ecalDown_in_det,
                                                  rot=self.ecalDownRot)
        det_lv.placements.append(pecalDown_in_MagInner.name)

        #ecalUp_lv = self.ecalUpBldr.get_volume('volECALUpstream')
        if isinstance(self.EcalBField,str):
            ecalUp_lv.params.append(("BField",self.EcalBField))

        #ecalUp_in_det = geom.structure.Position('ECALUp_in_MagInner', ecalUpPos[0], ecalUpPos[1], ecalUpPos[2])
        #pecalUp_in_MagInner = geom.structure.Placement('placeECALUp_in_MagInner',
        #                                          volume = ecalUp_lv,
        #                                          pos = ecalUp_in_det,
        #                                          rot=self.ecalUpRot)
        #det_lv.placements.append(pecalUp_in_MagInner.name)


        ecalBar_lv = self.ecalBarBldr.get_volume('volECALBarrel')
        if isinstance(self.EcalBField,str):
            ecalBar_lv.params.append(("BField",self.EcalBField))

        ecalBar_in_det = geom.structure.Position('ECALBar_in_MagInner', ecalBarPos[0], ecalBarPos[1], ecalBarPos[2])
        pecalBar_in_MagInner = geom.structure.Placement('placeECALBar_in_MagInner',
                                                 volume = ecalBar_lv,
                                                 pos = ecalBar_in_det,
                                                 rot=self.ecalBarRot)
        det_lv.placements.append(pecalBar_in_MagInner.name)


        return
