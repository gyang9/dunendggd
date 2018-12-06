#!/usr/bin/env python
'''
CylindricalMPTBuilder: Builds the multi purpose tracker
'''

import gegede.builder
from gegede import Quantity as Q
from math import asin, sqrt

class NDHPgTPC_v02_Builder(gegede.builder.Builder):
    '''
    Build a cylindrical multipurpose tracker. This class directly
    builds the magnet yoke calls sub-builders for the ECAL (for now)
    and for the GArTPC.

        Arguments:
        yokeMaterial: what the yoke is made of
        yokePosition: location of the center of the yoke in the mother volume
        (usually 0,0,0)
        yokeInnerR: Inner radius of the cylindrical magnet yoke

        yokeInnerZ: Half length of the cylindrical magnet yoke
        measured to inner surface

        yokeThicknessR,Z: Thickness of the magnet yoke

        yokeBufferToBoundaryR,Z: buffer between the outer edge
        of the magnet and the rectangular mother volume

        innerBField: the magnetic field inside of the magnet
        '''
    defaults=dict( buildYoke=True,
                   innerBField="0.4 T, 0.0 T, 0.0 T",
                   buildGarTPC=True,
                   buildEcal=True,
                   buildPV=True
                   )

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        ############# build the top level lv ###################
        # it's just a box to hold everything else
        # the z axis of a cylinder is the symmetry axis, but definition
        # for this box it corresponds to x
        dx_main=Q("10m")
        dy_main=Q("10m")
        dz_main=Q("10m")
        main_shape = geom.shapes.Box('NDHgTPC',
                                     dx=dx_main, dy=dy_main, dz=dz_main)

        main_lv = geom.structure.Volume('vol'+self.name,
                                        material='Air', shape=main_shape)

        self.add_volume(main_lv)

        ######### magnet yoke ##################################
        ### build the magnet yoke and coils and place inside the main lv
        if self.buildYoke:
            self.build_yoke(main_lv, geom)

        ######### build the pressure vessel  ###################
        if self.buildPV:
            self.build_pressure_vessel(main_lv, geom)

        ######### build an ecal ##########################
        if self.buildEcal:
            self.build_ecal(main_lv, geom)

        ######### build the TPC       ##########################
        # use GArTPCBuilder, but "disable" the cyrostat by tweaking
        # EndcapThickness, WallThickness, and ChamberMaterial
        # do that in the cfg file
        if self.buildGarTPC:
            self.build_gartpc(main_lv, geom)

        return


    def build_yoke(self,main_lv,geom):

        #### build the barrel ####
        yokeb_builder = self.get_builder('YokeBarrelBuilder')
        yokeb_vol = yokeb_builder.get_volume()

        rot_z = Q("90.0deg")-Q("180.0deg")/8.0

        yokeb_rot = geom.structure.Rotation(yokeb_builder.name+"_rot", z=rot_z)
        yokeb_pla = geom.structure.Placement(yokeb_builder.name+"_pla", volume=yokeb_vol, rot=yokeb_rot)
        main_lv.placements.append(yokeb_pla.name)

        #### build the endcap ####
        yokeec_builder = self.get_builder('YokeEndcapBuilder')
        yokeec_vol = yokeec_builder.get_volume()

        yokeec_rot = geom.structure.Rotation(yokeec_builder.name+"_rot", z=rot_z)
        yokeec_pla = geom.structure.Placement(yokeec_builder.name+"_pla", volume=yokeec_vol, rot=yokeec_rot)
        main_lv.placements.append(yokeec_pla.name)
        return

    def build_gartpc(self, main_lv, geom):
        tpc_builder = self.get_builder('GArTPCBuilder')
        tpc_vol = tpc_builder.get_volume()
        tpc_vol.params.append(("BField", self.innerBField))
        # tpc_rot = geom.structure.Rotation(tpc_builder.name+"_rot",
        #                                   y=Q("90deg"))
        tpc_rot = geom.structure.Rotation(tpc_builder.name+"_rot",
                                          y=Q("0deg"))
        tpc_pla = geom.structure.Placement(tpc_builder.name+"_pla",
                                           volume=tpc_vol, rot=tpc_rot)
        main_lv.placements.append(tpc_pla.name)

    def build_ecal(self, main_lv, geom):
        # build the barrel
        ibb = self.get_builder('ECALBarrelBuilder')
        if ibb == None:
            return
        ib_vol = ibb.get_volume()
        ib_vol.params.append(("BField", self.innerBField))

        rot_z = Q("90.0deg")-Q("180.0deg")/8.0
        ib_rot = geom.structure.Rotation(ibb.name+"_rot",
                                        x=Q("0deg"), y=Q("0deg"), z=rot_z)
        ib_pla = geom.structure.Placement(ibb.name+"_pla",
                                          volume=ib_vol, rot=ib_rot)
        main_lv.placements.append(ib_pla.name)

        # build the endcap
        iecb = self.get_builder("ECALEndcapBuilder")
        iec_vol = iecb.get_volume()
        iec_vol.params.append(("BField", self.innerBField))

        rot_z = Q("90.0deg")-Q("180.0deg")/8.0
        iec_rot = geom.structure.Rotation(iecb.name+"_rot", x=Q("0deg"), y=Q("0deg"), z=rot_z)
        iec_pla = geom.structure.Placement(iecb.name+"_pla",
        volume=iec_vol, rot=iec_rot)
        main_lv.placements.append(iec_pla.name)

    def build_pressure_vessel(self, main_lv, geom):

        pv_builder = self.get_builder('PVBuilder')
        if pv_builder == None:
            return

        pvb_vol = pv_builder.get_volume("PVBarrel_vol")
        pvb_rot = geom.structure.Rotation("PVBarrel"+"_rot", y='0deg')
        pvb_pla = geom.structure.Placement("PVBarrel"+"_pla", volume=pvb_vol, rot=pvb_rot)
        main_lv.placements.append(pvb_pla.name)

        pvec_vol = pv_builder.get_volume("PVEndcap_vol")
        pvec_rot = geom.structure.Rotation("PVEndcap"+"_rot", y='0deg')
        pvec_pla = geom.structure.Placement("PVEndcap"+"_pla", volume=pvec_vol, rot=pvec_rot)
        main_lv.placements.append(pvec_pla.name)
