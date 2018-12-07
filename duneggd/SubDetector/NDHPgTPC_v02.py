#!/usr/bin/env python
'''
CylindricalMPTBuilder: Builds the multi purpose tracker
'''

import gegede.builder
from gegede import Quantity as Q
from math import asin, sqrt

class NDHPgTPC_v02_Builder(gegede.builder.Builder):
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
                   buildEcal=True,
                   buildPV=True,
                   buildYoke=True
                   )

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        ############# build the top level lv ###################
        # it's just a box to hold everything else
        dx_main=Q("7m")
        dy_main=Q("7m")
        dz_main=Q("7m")
        main_shape = geom.shapes.Box('NDHPgTPC', dx=dx_main, dy=dy_main, dz=dz_main)
        main_lv = geom.structure.Volume('vol'+self.name, material='Air', shape=main_shape)

        self.add_volume(main_lv)

        ######### build the TPC       ##########################
        # use GArTPC Builder, but "disable" the cyrostat by tweaking
        # EndcapThickness, WallThickness, and ChamberMaterial
        # do that in the cfg file
        if self.buildGarTPC:
            self.build_gartpc(main_lv, geom)

        ######### build an ecal ##########################
        # Build the Barrel and Endcaps using the ECALBarrelBuilder and
        # ECALEndcapBuilder in the cfg file
        if self.buildEcal:
            self.build_ecal(main_lv, geom)

        ######### build the pressure vessel  ###################
        # Build the Pressure Vessel using the parameters in the cfg file
        # The PV consists of a cylinder for the Barrel and
        # the intersection of the cylinder and a sphere for the Endcaps
        if self.buildPV:
            self.build_pressure_vessel(main_lv, geom)

        ######### magnet yoke ##################################
        # Build the yoke Barrel and Endcaps
        # A description of the return magnetic field and the coils is not implemented
        if self.buildYoke:
            self.build_yoke(main_lv, geom)

        return


    def build_yoke(self,main_lv,geom):

        #### build the barrel ####
        yokeb_builder = self.get_builder('YokeBarrelBuilder')
        yokeb_vol = yokeb_builder.get_volume()

        yoke_shape = geom.store.shapes.get(yokeb_vol.shape)
        nsides = yoke_shape.numsides
        rot_z = Q("90.0deg")-Q("180.0deg")/nsides

        yokeb_rot = geom.structure.Rotation(yokeb_builder.name+"_rot", z=rot_z)
        yokeb_pla = geom.structure.Placement(yokeb_builder.name+"_pla", volume=yokeb_vol, rot=yokeb_rot)
        # Place it in the main lv
        main_lv.placements.append(yokeb_pla.name)

        #### build the endcap ####
        yokeec_builder = self.get_builder('YokeEndcapBuilder')
        yokeec_vol = yokeec_builder.get_volume()

        yokeec_rot = geom.structure.Rotation(yokeec_builder.name+"_rot", z=rot_z)
        yokeec_pla = geom.structure.Placement(yokeec_builder.name+"_pla", volume=yokeec_vol, rot=yokeec_rot)
        # Place it in the main lv
        main_lv.placements.append(yokeec_pla.name)
        return

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

        pvb_vol = pv_builder.get_volume("PVBarrel_vol")
        pvb_pla = geom.structure.Placement("PVBarrel"+"_pla", volume=pvb_vol)
        # Place it in the main lv
        main_lv.placements.append(pvb_pla.name)

        #Build the PV Endcap
        pvec_vol = pv_builder.get_volume("PVEndcap_vol")
        pvec_pla = geom.structure.Placement("PVEndcap"+"_pla", volume=pvec_vol)
        # Place it in the main lv
        main_lv.placements.append(pvec_pla.name)
