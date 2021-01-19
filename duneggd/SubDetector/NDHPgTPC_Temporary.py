#!/usr/bin/env python
'''
NDHPgTPC_Temporary_Builder: Builds the multi purpose tracker
'''

import gegede.builder
from gegede import Quantity as Q
from math import asin, sqrt

class NDHPgTPC_Temporary_Builder(gegede.builder.Builder):
    '''
    Build a concept of the ND HPgTPC detector. This class directly
    sub-builders for the Yoke and the inner scintillator planes

    Arguments:
    innerBField: the magnetic field inside of the magnet
    buildYoke: Flag to build the Yoke
    buildMagnet

    '''

    defaults=dict( innerBField="0.5 T, 0.0 T, 0.0 T",
                  BuildMagnet = True,
                  BuildYoke = True,
                  space = Q("10cm")
                  )

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        ''' Top level volume (MPD) - It is rotated later in the cavern (x, y, z) -> (z, y, x)'''

        magnet_shape = geom.get_shape("Magnet")
        r = magnet_shape.rmax
        dz = magnet_shape.dz

        try:
            byoke_shape = geom.get_shape("YokeBarrel")
            if r < byoke_shape.rmax:
                r = byoke_shape.rmax
            if dz < byoke_shape.dz:
                dz = byoke_shape.dz
        except IndexError:
            pass

        try:
            eyoke_shape = geom.get_shape("YokeEndcap_max")
            if r < eyoke_shape.rmax:
                r = eyoke_shape.rmax
            if dz < eyoke_shape.dz:
                dz = eyoke_shape.dz
        except IndexError:
            pass

        dx_main=r+self.space #dimension along the beam
        dy_main=r+self.space #dimension in height
        dz_main=dz+self.space #dimension perp to the beam

        print("Dimension of the Temporary MPD in along the beam ", dx_main*2, " dimension in height ", dy_main*2, " and dimension perp to the beam ", dz_main*2)

        main_shape = geom.shapes.Box('MPD', dx=dx_main, dy=dy_main, dz=dz_main)
        main_lv = geom.structure.Volume('vol'+main_shape.name, material='Air', shape=main_shape)

        self.add_volume(main_lv)

        ######### tracking layers ##################################
        print("Adding tracking layers to main volume")
        self.build_tracker(main_lv, geom)

        ######### magnet ##################################
        # Build a simple magnet of Al to get the total mass
        # A description of the return magnetic field and the coils is not implemented
        if self.BuildMagnet == True:
            print("Adding Magnet to main volume")
            self.build_magnet(main_lv, geom)

        ######### magnet yoke ##################################
        # Build the yoke Barrel and Endcaps
        # A description of the return magnetic field and the coils is not implemented
        if self.BuildYoke == True:
            print("Adding Yoke to main volume")
            self.build_yoke(main_lv, geom)

        return

    def build_tracker(self, main_lv, geom):

        tracker_builder = self.get_builder('TrackerBuilder')
        if tracker_builder == None:
            return

        tracker_vol = tracker_builder.get_volume("volTracker")
        tracker_vol.params.append(("BField", self.innerBField))
        tracker_pla = geom.structure.Placement("Tracker"+"_pla", volume=tracker_vol)
        # Place it in the main lv
        main_lv.placements.append(tracker_pla.name)

    def build_magnet(self, main_lv, geom):

        #Build the PV Barrel
        magnet_builder = self.get_builder('MagnetBuilder')
        if magnet_builder == None:
            return

        magnet_vol = magnet_builder.get_volume("volMagnet")
        magnet_pla = geom.structure.Placement("Magnet"+"_pla", volume=magnet_vol)
        # Place it in the main lv
        main_lv.placements.append(magnet_pla.name)

    def build_yoke(self,main_lv,geom):

        yoke_builder = self.get_builder('YokeBuilder')
        if yoke_builder == None:
            return

        byoke_vol = yoke_builder.get_volume("volYokeBarrel")
        yoke_shape = geom.store.shapes.get(byoke_vol.shape)
        nsides = yoke_shape.numsides
        print("Number of yoke sides", nsides)

        rot_z = Q("90.0deg")-Q("180.0deg")/nsides
        if nsides == 16:
            rot_z = rot_z + Q("22.5deg")

        byoke_rot = geom.structure.Rotation(byoke_vol.name+"_rot", z=rot_z)
        byoke_pla = geom.structure.Placement("YokeBarrel"+"_pla", volume=byoke_vol, rot=byoke_rot)

        # Place it in the main lv
        main_lv.placements.append(byoke_pla.name)

        try:
            eyoke_vol = yoke_builder.get_volume("volYokeEndcap")
            eyoke_rot = geom.structure.Rotation(eyoke_vol.name+"_rot", z=rot_z)
            eyoke_pla = geom.structure.Placement("YokeEndcap"+"_pla", volume=eyoke_vol, rot=eyoke_rot)
            # Place it in the main lv
            main_lv.placements.append(eyoke_pla.name)
        except IndexError:
            pass
