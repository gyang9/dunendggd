#!/usr/bin/env python
'''
Subbuilder of DetEncBuilder
'''

import gegede.builder
from gegede import Quantity as Q

class IronDipoleBuilder(gegede.builder.Builder):
    '''
    Assemble all the subsystems into one bounding box.
    '''

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, defMat = 'Air',  
                  magInDim=None,  magPos=None, 
                  ecalInDim=None, ecalDnPos=None, ecalUpPos=None, ecalBaPos=None, ecalDownRot=None, 
                  ecalUpRot=None, ecalBarRot=None,innerDetBField=None, STTPos=None, buildSTT=False, 
                  A3DSTPos=None, buildA3DST=False, 
                  GArTPCPos=None, GArTPCRot=None,buildGArTPC=False,**kwds):
        
        self.defMat      = defMat
        self.magPos      = list(magPos)

        # Get all of the detector subsystems to position and place
        self.ecalDownBldr = self.get_builder('ECALDownstream')        
        self.ecalUpBldr = self.get_builder('ECALUpstream')
        self.ecalBarBldr  = self.get_builder('ECALBarrel')
        self.MagnetBldr   = self.get_builder('Magnet')
        # only get an STT builder if we want to build the STT
        self.STTBldr   = None 
        if buildSTT:
            self.STTBldr=self.get_builder('STT')
        # only get a 3DST builder if we want to build the 3DST
        self.A3DSTBldr = None
        if buildA3DST:
            self.A3DSTBldr=self.get_builder('3DST')

        # only get a GArTPC builder if we want to build the 3DST
        self.GArTPCBldr = None
        if buildGArTPC:
            self.GArTPCBldr=self.get_builder('GArTPC')

        self.innerDetBField = innerDetBField

        self.ecalDownRot  = ecalDownRot
        self.ecalUpRot  = ecalUpRot
        self.ecalBarRot   = ecalBarRot
        
	self.magPos       = list(magPos) #MAK: inherited this code... why list(...) here?
        self.ecalDnPos    = list(ecalDnPos)
        self.ecalUpPos    = list(ecalUpPos)
	self.ecalBaPos    = list(ecalBaPos)
        
        self.STTPos=STTPos 
        self.buildSTT=buildSTT
        
        self.A3DSTPos=A3DSTPos
        self.buildA3DST=buildA3DST

        self.GArTPCPos=GArTPCPos
        self.GArTPCRot=GArTPCRot
        self.buildGArTPC=buildGArTPC

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        
        # Get subsystem dimensions, 
        # one has to go to the builders to see/understand these
        ecalDownDim    = list(self.ecalDownBldr.ecalModDim)
        ecalBarOutDim  = list(self.ecalBarBldr.ecalOutDim)
        ecalBarInDim   = list(self.ecalBarBldr.ecalInDim)
        # dimensions of the outside of the magnet yoke
        # includes gaps between yoke segments
	magBoxOutDim   = list(self.MagnetBldr.MagnetSystemOuterDimension)
        print "IronDipoleBuilder::construct():  magBoxOutDim = ",magBoxOutDim

#	ecalBarPos  = list(self.ecalBaPos)


        ############# build the top level lv ###################
        main_shape = geom.shapes.Box('IronDipole', dx=0.5*magBoxOutDim[0], 
                                     dy=0.5*magBoxOutDim[1],  dz=0.5*magBoxOutDim[2])
        main_lv = geom.structure.Volume('vol'+self.name, material=self.defMat, shape=main_shape)
        self.add_volume(main_lv)
        ######### magnet yoke ##################################
        ### build the magnet yoke and coils and place inside the main lv
        self.build_magnet(main_lv,geom)
        
        ######### inner detector region ########################
        ### then build a lv to contain detectors, it will be located in the main_lv
        ### but sized and oriented to fit inside the magnet coils
        ### this is the region with a simple dipole field
        ### this is the main reason to build the detector nested like this
        
        # MagnetBuilder.MagnetInn --> need to read that code
        # dimensions of the inside of the magnet coils
        # includes gaps between coil segments
        innerDet_dim=self.MagnetBldr.MagnetInn
        innerDet_shape = geom.shapes.Box('innerDet', dx=0.5*innerDet_dim[0],
                                         dy=0.5*innerDet_dim[1],dz=0.5*innerDet_dim[2])
        innerDet_lv= geom.structure.Volume('innerDet_volume',material='Air',shape=innerDet_shape)
        print "Setting IronDipole inner detector field to ",self.innerDetBField
        innerDet_lv.params.append(("BField",self.innerDetBField))
        ######### ecal and trackers inside inner detector ######
        self.build_ecal(innerDet_lv,geom)
        if self.buildSTT:
            self.build_stt(innerDet_lv,geom)

        if self.buildA3DST:
            self.build_a3dst(innerDet_lv,geom)

        if self.buildGArTPC:
            self.build_gartpc(innerDet_lv,geom)

        ######### finally, place the inner detector volume #####
        pos = [Q('0m'),Q('0m'),Q('0m')]
        innerDet_pos=geom.structure.Position("innerDet_pos",
                                             pos[0],pos[1], pos[2])
        innerDet_pla=geom.structure.Placement("innerDet_pla",
                                              volume=innerDet_lv,
                                              pos=innerDet_pos)
        print "appending ",innerDet_pla.name, " to ", main_lv.name

        main_lv.placements.append(innerDet_pla.name)



    def build_magnet(self,det_lv,geom):
	magnet_lv = self.MagnetBldr.get_volume('volMagnet')
        magnet_in_det = geom.structure.Position('magnet_in_det', self.magPos[0], self.magPos[1], self.magPos[2])
        pMagnet_in_det = geom.structure.Placement('placeMagnet_in_det',
                                                  volume = magnet_lv,
                                                  pos = magnet_in_det)

        det_lv.placements.append(pMagnet_in_det.name)
        return

    def build_ecal(self,det_lv,geom):
        # Get volECALDownstream, volECALUpstream, volECALBarrel volumes and place in volDetector

        ecalDown_lv = self.ecalDownBldr.get_volume('volECALDownstream')
        ecalDown_in_det = geom.structure.Position('ECALDown_in_MagInner', 
                                                  self.ecalDnPos[0], self.ecalDnPos[1], self.ecalDnPos[2])
        pecalDown_in_MagInner = geom.structure.Placement('placeECALDown_in_MagInner',
                                                  volume = ecalDown_lv,
                                                  pos = ecalDown_in_det,
                                                  rot=self.ecalDownRot)
        det_lv.placements.append(pecalDown_in_MagInner.name)

        ecalUp_lv = self.ecalUpBldr.get_volume('volECALUpstream')
        ecalUp_in_det = geom.structure.Position('ECALUp_in_MagInner', 
                                                self.ecalUpPos[0], self.ecalUpPos[1], self.ecalUpPos[2])
        pecalUp_in_MagInner = geom.structure.Placement('placeECALUp_in_MagInner',
                                                  volume = ecalUp_lv,
                                                  pos = ecalUp_in_det,
                                                  rot=self.ecalUpRot)
        det_lv.placements.append(pecalUp_in_MagInner.name)


        ecalBar_lv = self.ecalBarBldr.get_volume('volECALBarrel')
        ecalBar_in_det = geom.structure.Position('ECALBar_in_MagInner', 
                                                 self.ecalBaPos[0], self.ecalBaPos[1], self.ecalBaPos[2])
        pecalBar_in_MagInner = geom.structure.Placement('placeECALBar_in_MagInner',
                                                 volume = ecalBar_lv,
                                                 pos = ecalBar_in_det,
                                                 rot=self.ecalBarRot)
        det_lv.placements.append(pecalBar_in_MagInner.name)


        
    def build_stt(self,det_lv,geom):
        print "IronDipoleBuilder::build_stt(...) called"
	stt_lv = self.STTBldr.get_volume('volSTT')
        print "IronDipoleBuilder::build_stt(...) STT placed at ", self.STTPos
        stt_pos = geom.structure.Position('STT_pos', 
                                          self.STTPos[0], self.STTPos[1], self.STTPos[2])
        stt_pla = geom.structure.Placement('STT_pla',
                                           volume = stt_lv,
                                           pos = stt_pos)

        det_lv.placements.append(stt_pla.name)


    def build_a3dst(self,det_lv,geom):
        
        print "IronDipoleBuilder::build_a3dst(...) called"
	a3dst_lv = self.A3DSTBldr.get_volume('volA3DST')
        print "IronDipoleBuilder::build_a3dst(...) A3DST placed at ", self.A3DSTPos
        a3dst_pos = geom.structure.Position('a3DST_pos', 
                                            self.A3DSTPos[0], self.A3DSTPos[1], self.A3DSTPos[2])
        a3dst_pla = geom.structure.Placement('a3DST_pla',
                                           volume = a3dst_lv,
                                           pos = a3dst_pos)

        det_lv.placements.append(a3dst_pla.name)


    def build_gartpc(self,det_lv,geom):
        print "IronDipoleBuilder::build_gartpc(...) called"
	gartpc_lv = self.GArTPCBldr.get_volume('volGArTPC')
        print "IronDipoleBuilder::build_gartpc(...) GArTPC placed at ", self.GArTPCPos
        gartpc_pos = geom.structure.Position('GArTPC_pos', 
                                             self.GArTPCPos[0], self.GArTPCPos[1], self.GArTPCPos[2])
        gartpc_rot = geom.structure.Rotation('GArTPC_rot', 
                                             self.GArTPCRot[0], self.GArTPCRot[1], self.GArTPCRot[2])
        gartpc_pla = geom.structure.Placement('GArTPC_pla',
                                              volume = gartpc_lv,
                                              pos = gartpc_pos,
                                              rot = gartpc_rot)

        det_lv.placements.append(gartpc_pla.name)
