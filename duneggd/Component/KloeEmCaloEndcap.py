#!/usr/bin/env python
import gegede.builder
import math
from duneggd.LocalTools import localtools as ltools
from duneggd.LocalTools import materialdefinition as materials
from gegede import Quantity as Q


class KloeEmCaloEndcapBuilder(gegede.builder.Builder):
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def configure(self, 
		  EndcapSize=None, 
		  ActiveMat=None, 
		  PasMat=None, 
		  PasSlabThickness=None, 
		  ActiveSlabThickness=None, 
		  nSlabs=None, 
		  **kwds):
        self.EndcapSize = EndcapSize
        self.ActiveMat = ActiveMat
        self.PasMat = PasMat
        self.PasSlabThickness = PasSlabThickness
        self.ActiveSlabThickness = ActiveSlabThickness
        self.nSlabs = nSlabs
    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):
        
        KLOEEndcapECALRmin = self.EndcapSize[0]
        KLOEEndcapECALRmax = self.EndcapSize[1]
        KLOEEndcapECALDepth = self.EndcapSize[2]

        ECAL_end_shape = geom.shapes.Tubs('ECAL_end_shape',
                                          rmin=Q("0mm"),   ####< ---- use 0 here, if none zero value, the genie will give weird result 
                                          rmax=KLOEEndcapECALRmax,
                                          dz=KLOEEndcapECALDepth / 2.0)

        ECAL_end_lv = geom.structure.Volume('ECAL_end_lv', material='Air', shape=ECAL_end_shape)
        self.add_volume(ECAL_end_lv)
#	print(self.name)
#       ECAL_position = geom.structure.Position('ECAL_position', Position[0], Position[1], Position[2])
#       ECAL_place = geom.structure.Placement('ECAL_place', volume = ECAL_lv, pos=ECAL_position)
        endECALActiveSlab = geom.shapes.Tubs(
            'endECALActiveSlab',
            rmin=KLOEEndcapECALRmin,# + FrameThickness,
            rmax=KLOEEndcapECALRmax,# - FrameThickness,
            dz=0.5 * self.ActiveSlabThickness)
        
        endECALActiveSlab_lv = geom.structure.Volume(
            'vol_endECALActiveSlab',
            material=self.ActiveMat,
            shape=endECALActiveSlab)
        endECALActiveSlab_lv.params.append(("SensDet","ECAL"))

        endECALPassiveSlab = geom.shapes.Tubs(
            'endECALPassiveSlab',
            rmin=KLOEEndcapECALRmin,# + FrameThickness,
            rmax=KLOEEndcapECALRmax,# - FrameThickness,
            dz=0.5 * self.PasSlabThickness)
        
        endECALPassiveSlab_lv = geom.structure.Volume(
            'vol_endECALPassiveSlab',
            material=self.PasMat,
            shape=endECALPassiveSlab)

        for i in range(self.nSlabs): #nSlabs
            
            xposSlab=Q('0cm')
            yposSlab=Q('0cm')
            
            zposSlabActive =( -KLOEEndcapECALDepth * 0.5 + 
                             (i + 0.5) * self.ActiveSlabThickness +
                              i * self.PasSlabThickness )
                              
            zposSlabPassive = (zposSlabActive + 
                               0.5 * self.ActiveSlabThickness +
                               0.5 * self.PasSlabThickness)
            #print("BhalfPassive= "+ str(BhalfPassive))
            
            ##########creating and appending active slabs to the ECAL endcap##########
            endECALActiveSlabPos = geom.structure.Position(
                    'endecalactiveslabpos' + '_' + str(i),
                    xposSlab, yposSlab, zposSlabActive)

            endECALActiveSlabPlace = geom.structure.Placement(
                    'endecalactiveslabpla' + '_' + str(i),
                    volume=endECALActiveSlab_lv,
                    pos=endECALActiveSlabPos)
#                    copynumber=i)   ## low version ggd doesnot support copynumber

            ECAL_end_lv.placements.append( endECALActiveSlabPlace.name )
            
            ##########creating and appending passive slabs to the ECAL endcap##########

            endECALPassiveSlabPos = geom.structure.Position(
                    'endecalpassiveslabpos' + '_' + str(i),
                    xposSlab, yposSlab, zposSlabPassive)

            endECALPassiveSlabPlace = geom.structure.Placement(
                    'endecalpassiveslabpla' + '_' + str(i),
                    volume=endECALPassiveSlab_lv,
                    pos=endECALPassiveSlabPos)
#                    copynumber=i)  ## low version ggd doesnot support copynumber

            ECAL_end_lv.placements.append( endECALPassiveSlabPlace.name )

