#!/usr/bin/env python
'''
CylindricalMPTBuilder: Builds the multi purpose tracker
'''

import gegede.builder
from gegede import Quantity as Q
from math import asin

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
    defaults=dict( yokeMaterial="Iron",
                   yokeInnerR=Q("3.20m"),
                   yokeInnerZ=Q("3.9m"),
                   yokeThicknessR=Q("0.5m"),
                   yokeThicknessZ=Q("0.5m"),
                   yokeBufferToBoundaryR=Q("0.5m"),
                   yokeBufferToBoundaryZ=Q("0.5m"),
                   yokePhiCutout=Q("90deg"),
                   buildYoke=True,
                   innerBField="0.4 T, 0.0 T, 0.0 T",
                   buildGarTPC=True,
                   buildEcalEndcap=True,
                   buildEcalBarrel=True,
                   IBECalXStart=Q("100cm"),
                   pvInnerRadius=Q("285cm"),
                   pvThickness=Q("3cm"),
                   pvHalfLength=Q("285cm"),
                   pvEndCapBulge=Q("100cm"),
                   pvMaterial='Steel',
                   buildPV=True
                   )

    #^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
    def construct(self, geom):

        ############# build the top level lv ###################
        # it's just a box to hold everything else
        # the z axis of a cylinder is the symmetry axis, but definition
        # for this box it corresponds to x
        dx_main=self.yokeInnerZ+self.yokeThicknessZ+self.yokeBufferToBoundaryZ
        dy_main=self.yokeInnerR+self.yokeThicknessR+self.yokeBufferToBoundaryR
        dz_main=dy_main
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

        ######### build an inner ecal ##########################
        if self.buildEcalBarrel:
            self.build_barrel_ecal(main_lv, geom)

        ######### build an inner ecal endcap ##########################
        if self.buildEcalEndcap:
            self.build_endcap_ecal(main_lv, geom)

        ######### build the TPC       ##########################
        # use GArTPCBuilder, but "disable" the cyrostat by tweaking
        # EndcapThickness, WallThickness, and ChamberMaterial
        # do that in the cfg file
        if self.buildGarTPC:
            self.build_gartpc(main_lv, geom)

        return


    def build_yoke(self,main_lv,geom):

        #### build the barrel ####
        rmin=self.yokeInnerR
        rmax=rmin+self.yokeThicknessR
        dz=self.yokeInnerZ
        sphi=self.yokePhiCutout/2.0
        dphi=Q("360deg")-self.yokePhiCutout
        by_name="YokeBarrel"
        by_shape = geom.shapes.Tubs(by_name,
                                    rmin=rmin,rmax=rmax,dz=dz,
                                    sphi=sphi,dphi=dphi)
        by_lv=geom.structure.Volume(by_name+"_lv",
                                    material=self.yokeMaterial,
                                    shape=by_shape)
        pos=[Q('0m'),Q('0m'),Q('0m')]
        by_pos=geom.structure.Position(by_name+"_pos",pos[0],pos[1],pos[2])
        rot=[Q("0deg"),Q("-90deg"),Q("0deg")]
        by_rot=geom.structure.Rotation(by_name+"_rot",rot[0],rot[1],rot[2])
        by_pla=geom.structure.Placement(by_name+"_pla",volume=by_lv,
                                        pos=by_pos, rot=by_rot)
        main_lv.placements.append(by_pla.name)

        ### build the endcaps ###
        part="A" # eventually may add a multipart endcap (A, B, C... like KLOE)
        for side in ["L","R"] :
            name="YokeEndcap"+part+side
            ec_shape=geom.shapes.Tubs(name,
                                      rmin=Q("0.5m"),
                                      rmax=self.yokeInnerR+self.yokeThicknessR,
                                      dz=self.yokeThicknessZ/2.0)
            ec_lv=geom.structure.Volume(name+"_vol",
                                        material=self.yokeMaterial,
                                        shape=ec_shape)
            pos=[Q('0m'),Q('0m'),Q('0m')]
            pos[0]=self.yokeInnerZ+self.yokeThicknessZ/2.0
            if side=="L":
                pos[0]=-pos[0]

            ec_pos=geom.structure.Position(name+"_pos",pos[0],pos[1],pos[2])
            rot=[Q("0deg"),Q("-90deg"),Q("0deg")]
            ec_rot=geom.structure.Rotation(name+"_rot",rot[0],rot[1],rot[2])
            ec_pla=geom.structure.Placement(name+"_pla",volume=ec_lv,
                                            pos=ec_pos, rot=ec_rot)
            main_lv.placements.append(ec_pla.name)

        return

    def build_gartpc(self, main_lv, geom):
        tpc_builder = self.get_builder('GArTPC')
        tpc_vol = tpc_builder.get_volume()
        tpc_vol.params.append(("BField", self.innerBField))
        # tpc_rot = geom.structure.Rotation(tpc_builder.name+"_rot",
        #                                   y=Q("90deg"))
        tpc_rot = geom.structure.Rotation(tpc_builder.name+"_rot",
                                          y=Q("0deg"))
        tpc_pla = geom.structure.Placement(tpc_builder.name+"_pla",
                                           volume=tpc_vol, rot=tpc_rot)
        main_lv.placements.append(tpc_pla.name)

    def build_barrel_ecal(self, main_lv, geom):
        # build the barrel
        ibb = self.get_builder('ECALBarrelBuilder')
        if ibb == None:
            return
        ib_vol = ibb.get_volume()
        ib_vol.params.append(("BField", self.innerBField))
        #ib_rot = geom.structure.Rotation(ibb.name+"_rot",
        #                                 y=Q("90deg"))

        rot_x = Q("90.0deg")-Q("180.0deg")/8.0
        print rot_x
        #ib_rot = geom.structure.Rotation(ibb.name+"_rot",
        #                                 x=rot_x, y=Q("90deg"), z=Q("0deg"))
        ib_rot = geom.structure.Rotation(ibb.name+"_rot",
                                        x=Q("0deg"), y=Q("0deg"), z=rot_x)
        ib_pla = geom.structure.Placement(ibb.name+"_pla",
                                          volume=ib_vol, rot=ib_rot)
        main_lv.placements.append(ib_pla.name)

    def build_endcap_ecal(self, main_lv, geom):
        # build the barrel
        iecb = self.get_builder("ECALEndcapBuilder")
        iec_vol = iecb.get_volume()
        iec_vol.params.append(("BField", self.innerBField))
        # iec_shape = geom.store.shapes.get(iec_vol.shape)
        # iec_thickness = iec_shape.dz*2.0
        # # build the endcaps
        # for side in ["L", "R"]:
        #     rot = "-90deg" if "L" else "90deg"
        #     xpos = self.IBECalXStart+iec_thickness/2.0
        #     if side == "R":
        #         xpos = -xpos
        #     iec_rot = geom.structure.Rotation(iecb.name+side+"_rot", y=rot)
        #     iec_pos = geom.structure.Position(iecb.name+side+"_pos", x=xpos)
        #     iec_pla = geom.structure.Placement(iecb.name+side+"_pla",
        #                                        volume=iec_vol, rot=iec_rot,pos=iec_pos)
        #     main_lv.placements.append(iec_pla.name)

        rot_x = Q("90.0deg")-Q("180.0deg")/8.0
        print rot_x
        iec_rot = geom.structure.Rotation(iecb.name+"_rot", x=Q("0deg"), y=Q("0deg"), z=rot_x)
        iec_pla = geom.structure.Placement(iecb.name+"_pla",
        volume=iec_vol, rot=iec_rot)
        main_lv.placements.append(iec_pla.name)



    def build_pressure_vessel(self, main_lv, geom):
        rmin = self.pvInnerRadius
        thickness = self.pvThickness
        # build the pressure vessel barrel
        pvb_name = "PVBarrel"
        pvb_shape = geom.shapes.Tubs(pvb_name,
                                     rmin=rmin,
                                     rmax=rmin+thickness,
                                     dz=self.pvHalfLength,
                                     sphi="0deg", dphi="360deg")
        pvb_vol = geom.structure.Volume(pvb_name+"_vol", shape=pvb_shape,
                                        material=self.pvMaterial)
        pvb_rot = geom.structure.Rotation(pvb_name+"_rot", y='90deg')
        pvb_pla = geom.structure.Placement(pvb_name+"_pla",
                                           volume=pvb_vol, rot=pvb_rot)
        main_lv.placements.append(pvb_pla.name)
        # build the pressure vessel endcaps
        # some euclidean geometry documented in my notebook
        h = self.pvEndCapBulge
        x = rmin
        q = ((h/Q("1mm"))**2 + (x/Q("1mm"))**2)
        R = q/(2*h/Q("1mm"))*Q("1mm")
        dtheta=asin( 2*(h/Q("1mm"))*(x/Q("1mm"))/q)
        print "h, x, q, R, dtheta = ", h, x, q, R, dtheta
        pvec_name = "PVEndcap"
        pvec_shape = geom.shapes.Sphere(pvec_name, rmin=R, rmax=R+thickness,
                                        sphi="0deg", dphi="360deg",
                                        stheta="0deg", dtheta=dtheta)
        pvec_vol = geom.structure.Volume(pvec_name+"_vol", shape=pvec_shape,
                                         material=self.pvMaterial)
        for side in ["L", "R"]:
            yrot = "-90deg" if side == 'L' else "90deg"
            # some euclidean geometry documened in my notebook
            xpos = self.pvHalfLength-(R-h)
            if side == 'R':
                xpos = -xpos
            print "xpos = ", xpos
            pvec_rot = geom.structure.Rotation(
                pvec_name+side+"_rot", y=yrot)
            pvec_pos = geom.structure.Position(
                pvec_name+side+"_pos", x=xpos)
            pvec_pla = geom.structure.Placement(
                pvec_name+side+"_pla", volume=pvec_vol,
                pos=pvec_pos, rot=pvec_rot)
            main_lv.placements.append(pvec_pla.name)
