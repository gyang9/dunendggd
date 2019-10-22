#!/usr/bin/env python
'''
NDHPgTPC_Builder: Builds the multi purpose tracker
'''

import gegede.builder
from gegede import Quantity as Q
from math import asin, sqrt

class NDHPgTPC_Builder(gegede.builder.Builder):
    '''
    Build a concept of the ND HPgTPC detector. This class directly
    sub-builders for the GArTPC, the ECAL, the Pressure Vessel
    and for the Yoke.

    Arguments:
    innerBField: the magnetic field inside of the magnet
    buildGarTPC: Flag to build the GArTPC
    buildEcal: Flag to build the Ecal
    buildPV: Flag to build the Pressure Vessel
    buildYoke: Flag to build the Yoke

    '''

    defaults=dict( innerBField="0.4 T, 0.0 T, 0.0 T",
                   buildGarTPC=True,
                   buildEcalBarrel=True,
                   buildEcalEndcap=True,
                   buildPV=True,
                   buildYoke=False,
                   buildMagnet=False
                   )

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        ############# build the top level lv ###################
        # it's just a box to hold everything else
        dx_main=Q("4.0m")
        dy_main=Q("4.0m")
        dz_main=Q("5.01m")
        main_shape = geom.shapes.Box('MPD', dx=dx_main, dy=dy_main, dz=dz_main)
        main_lv = geom.structure.Volume('vol'+main_shape.name, material='Air', shape=main_shape)

        self.add_volume(main_lv)

        ##### build a fake volume that contains the MPD without the magnet to define the magnetized volume correctly ###
        fake_lv = self.buildMagnetizedVolume(main_lv, geom)

        ######### build the TPC       ##########################
        # use GArTPC Builder, but "disable" the cyrostat by tweaking
        # EndcapThickness, WallThickness, and ChamberMaterial
        # do that in the cfg file
        if self.buildGarTPC:
            self.build_gartpc(fake_lv, geom)

        ######### build the pressure vessel  ###################
        # Build the Pressure Vessel using the parameters in the cfg file
        # The PV consists of a cylinder for the Barrel and
        # the intersection of the cylinder and a sphere for the Endcaps
        if self.buildPV:
            self.build_pressure_vessel(fake_lv, geom)

        ######### build an ecal ##########################
        # Build the Barrel and Endcaps using the ECALBarrelBuilder and
        # ECALEndcapBuilder in the cfg file
        self.build_ecal(fake_lv, geom)

        ######### magnet yoke ##################################
        # Build the yoke Barrel and Endcaps
        # A description of the return magnetic field and the coils is not implemented
        # if self.buildYoke:
        #     self.build_yoke(main_lv, geom)


        ######### magnet ##################################
        # Build a simple magnet of Al to get the total mass
        # A description of the return magnetic field and the coils is not implemented
        if self.buildMagnet:
            self.build_magnet(main_lv, geom)

        return


    # def build_yoke(self,main_lv,geom):
    #
    #     #### build the barrel ####
    #     yokeb_builder = self.get_builder('YokeBarrelBuilder')
    #     yokeb_vol = yokeb_builder.get_volume()
    #
    #     yoke_shape = geom.store.shapes.get(yokeb_vol.shape)
    #     nsides = yoke_shape.numsides
    #     rot_z = Q("90.0deg")-Q("180.0deg")/nsides
    #
    #     yokeb_rot = geom.structure.Rotation(yokeb_builder.name+"_rot", z=rot_z)
    #     yokeb_pla = geom.structure.Placement(yokeb_builder.name+"_pla", volume=yokeb_vol, rot=yokeb_rot)
    #     # Place it in the main lv
    #     main_lv.placements.append(yokeb_pla.name)
    #
    #     #### build the endcap ####
    #     yokeec_builder = self.get_builder('YokeEndcapBuilder')
    #     yokeec_vol = yokeec_builder.get_volume()
    #
    #     yokeec_rot = geom.structure.Rotation(yokeec_builder.name+"_rot", z=rot_z)
    #     yokeec_pla = geom.structure.Placement(yokeec_builder.name+"_pla", volume=yokeec_vol, rot=yokeec_rot)
    #     # Place it in the main lv
    #     main_lv.placements.append(yokeec_pla.name)
    #     return

    def buildMagnetizedVolume(self, main_lv, geom):

        magnet_shape = geom.get_shape("Magnet")

        fake_shape = geom.shapes.Tubs('NDHPgTPC', rmin=Q("0m"), rmax=magnet_shape.rmin, dz=magnet_shape.dz, sphi="0deg", dphi="360deg")
        fake_lv = geom.structure.Volume('vol'+fake_shape.name, material='Air', shape=fake_shape)
        fake_lv.params.append(("BField", self.innerBField))
        fake_pla = geom.structure.Placement("NDHPgTPC"+"_pla", volume=fake_lv)
        # Place it in the main lv
        main_lv.placements.append(fake_pla.name)

        return fake_lv

    def build_gartpc(self, main_lv, geom):

        #Build TPC
        tpc_builder = self.get_builder('GArTPC')
        if tpc_builder == None:
            return

        tpc_vol = tpc_builder.get_volume()
        # Add the magnetic field to the volume
        tpc_vol.params.append(("BField", self.innerBField))

        tpc_pla = geom.structure.Placement("GArTPC"+"_pla", volume=tpc_vol)
        # Place it in the main lv
        main_lv.placements.append(tpc_pla.name)

    def build_ecal(self, main_lv, geom):

        if self.buildEcalBarrel == True:
            # build the ecalbarrel
            ibb = self.get_builder('ECALBarrelBuilder')
            if ibb == None:
                return

            ib_vol = ibb.get_volume()
            # Add the magnetic field to the volume
            ib_vol.params.append(("BField", self.innerBField))

            ecal_shape = geom.store.shapes.get(ib_vol.shape)
            nsides = ecal_shape.numsides
            rot_z = Q("90.0deg")-Q("180.0deg")/nsides

            ib_rot = geom.structure.Rotation(ibb.name+"_rot", z=rot_z)
            ib_pla = geom.structure.Placement(ibb.name+"_pla", volume=ib_vol, rot=ib_rot)
            # Place it in the main lv
            main_lv.placements.append(ib_pla.name)

        if self.buildEcalEndcap == True:
            # build the ecal endcap
            iecb = self.get_builder("ECALEndcapBuilder")
            if iecb == None:
                return

            iec_vol = iecb.get_volume()
            # Add the magnetic field to the volume
            iec_vol.params.append(("BField", self.innerBField))

            iec_rot = geom.structure.Rotation(iecb.name+"_rot", z=rot_z)
            iec_pla = geom.structure.Placement(iecb.name+"_pla", volume=iec_vol, rot=iec_rot)
            # Place it in the main lv
            main_lv.placements.append(iec_pla.name)

    def build_pressure_vessel(self, main_lv, geom):

        #Build the PV Barrel
        pv_builder = self.get_builder('PVBuilder')
        if pv_builder == None:
            return

        pvb_vol = pv_builder.get_volume("volPVBarrel")
        pvb_vol.params.append(("BField", self.innerBField))

        pvb_pla = geom.structure.Placement("PVBarrel"+"_pla", volume=pvb_vol)
        # Place it in the main lv
        main_lv.placements.append(pvb_pla.name)

        #Build the PV Endcap
        pvec_vol = pv_builder.get_volume("volPVEndcap")
        pvec_vol.params.append(("BField", self.innerBField))
        xpos = pv_builder.get_pv_endcap_position(geom)

        for side in ["L", "R"]:
            yrot = "0deg" if side == 'L' else "180deg"
            if side == 'R':
                xpos = -xpos
            print "xpos = ", xpos
            pvec_rot = geom.structure.Rotation("PVEndcap"+side+"_rot", y=yrot)
            pvec_pos = geom.structure.Position("PVEndcap"+side+"_pos", z=xpos)
            pvec_pla = geom.structure.Placement("PVEndcap"+side+"_pla", volume=pvec_vol, pos=pvec_pos, rot=pvec_rot)
            main_lv.placements.append(pvec_pla.name)

    def build_magnet(self, main_lv, geom):

        #Build the PV Barrel
        magnet_builder = self.get_builder('MagnetBuilder')
        if magnet_builder == None:
            return

        magnet_vol = magnet_builder.get_volume("volMagnet")
        magnet_pla = geom.structure.Placement("Magnet"+"_pla", volume=magnet_vol)
        # Place it in the main lv
        main_lv.placements.append(magnet_pla.name)
