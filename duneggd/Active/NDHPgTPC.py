#!/usr/bin/env python
'''
Builds compontents for the MPD
'''

import gegede.builder
from duneggd.SubDetector import NDHPgTPC as NDHPgTPC
from gegede import Quantity as Q
from math import floor, atan, sin, cos, tan, sqrt, pi, asin

class NDHPgTPCHGLayerBuilder(gegede.builder.Builder):

    """Builds ECAL HG Layers"""

    defaults = dict(dx=Q("10mm"), dy=Q("10mm"),
                dz=[Q('2mm'), Q('10mm'), Q('1mm')],
                lspacing=[Q('0.1mm'), Q('0.1mm'), Q('0.1mm')],
                mat=['Copper', 'Scintillator', 'FR4'],
                active=[False, True, False],
                material='Air',
                type = "Box",
                output_name='MPTECalHGLayer',
                sensdet_name='Ecal',
                nsides = 8,
                rmin = Q("0mm"),
                rmax = Q("0mm"),
                quadr = Q("0mm")
                )

    def depth(self):
        dzm = Q("0mm")
        for dz, lspace in zip(self.dz, self.lspacing):
            dzm += dz + lspace
        return dzm

    def BarrelConfigurationLayer(self, dx = None, dy = None, name = None, sensname = None, type = None):
        # print "---- Barrel ----"
        # print "Layer parameters dx=", dx, "dy=", dy, "layername=", name, "type=", type
        self.dx = dx
        self.dy = dy
        self.output_name = name
        self.sensdet_name = sensname
        self.type = type
        return

    def EndcapConfigurationLayer(self, nsides = None, rmin = None, rmax = None, quadr = None, name = None, sensname = None, type = None):
        # print "---- Endcap ----"
        # print "Layer parameters nsides=", nsides, "rmin=", rmin, "rmax=", rmax, "quadr=", quadr, "layername=", name, "type=", type
        self.nsides = nsides
        self.rmin = rmin
        self.rmax = rmax
        self.quadr = quadr
        self.output_name = name
        self.sensdet_name = sensname
        self.type = type
        return

    def construct(self, geom):

        dzm = self.depth()
        dzm = dzm/2.0  # Box() requires half dimensions

        # make the mother volume
        name = self.output_name

        if self.type == "Box":
            layer_shape = geom.shapes.Box(name, dx=(self.dx)/ 2.0, dy=(self.dy)/2.0, dz=(self.depth()) /2.0)
            layer_lv = geom.structure.Volume(name + "_vol", shape=layer_shape, material=self.material)
        elif self.type == "Intersection":
            layer_shape_full = geom.shapes.PolyhedraRegular(name+"_full", numsides=self.nsides, sphi=pi/8, rmin=self.rmin, rmax=self.rmax, dz=(self.depth()))
            layer_quadrant = geom.shapes.Box(name+"_quadrant", dx=self.quadr, dy=self.quadr, dz=(self.depth()) /2.0)
            layer_quad_pos = geom.structure.Position(name+"_quadrant_pos", x=self.quadr, y=self.quadr)
            layer_shape = geom.shapes.Boolean(name, type='intersection', first=layer_shape_full, second=layer_quadrant, pos=layer_quad_pos)
            layer_lv = geom.structure.Volume(name +"_vol", shape=layer_shape, material=self.material)

        # no skipped space before the first layer
        skip = Q("0mm")
        cntr = 1
        zloc = Q("0mm")

        for dz, lspace, mat, active in zip(self.dz, self.lspacing, self.mat, self.active):
            sname = (layer_shape.name + "_slice%i" % cntr)
            zloc = zloc + skip + dz / 2.0

            if self.type == "Box":
                slice_shape = geom.shapes.Box(sname, self.dx/2.0, self.dy/2.0, dz / 2.0)
                slice_lv = geom.structure.Volume(sname + "_vol", material=mat, shape=slice_shape)
            elif self.type == "Intersection":
                slice_shape_full = geom.shapes.PolyhedraRegular(sname+"_full", numsides=self.nsides, sphi=pi/8, rmin=self.rmin, rmax=self.rmax, dz=dz)
                slice_quadrant = geom.shapes.Box(sname+"_quadrant", dx=self.quadr, dy=self.quadr, dz=dz/2.0)
                slice_quad_pos = geom.structure.Position(sname+"_quadrant_pos", x=self.quadr, y=self.quadr)
                slice_shape = geom.shapes.Boolean(sname, type='intersection', first=slice_shape_full, second=slice_quadrant, pos=slice_quad_pos)
                slice_lv = geom.structure.Volume(sname + "_vol", material=mat, shape=slice_shape)

            if active:
                #slice_lv.params.append(("SensDet", name))
                slice_lv.params.append(("SensDet", self.sensdet_name))

            # dzm is the half depth of the mother volume
            # we need to subtract it off to position layers
            # relative to the center of the mother
            slice_pos = geom.structure.Position(sname + "_pos", x='0mm', y='0mm', z=zloc - dzm)
            slice_pla = geom.structure.Placement(sname + "_pla", volume=slice_lv, pos=slice_pos)
            layer_lv.placements.append(slice_pla.name)

            skip = dz / 2.0 + lspace  # set the skipped space before the next layer
            cntr += 1

        self.add_volume(layer_lv)

class NDHPgTPCLGLayerBuilder(gegede.builder.Builder):

    """Builds ECAL LG Layers"""

    defaults = dict(dx=Q("10mm"), dy=Q("10mm"),
                dz=[Q('4mm'), Q('5mm'), Q('5mm')],
                lspacing=[Q('0.1mm'), Q('0.1mm'), Q('0.1mm')],
                mat=['Copper', 'Scintillator', 'Scintillator'],
                active=[False, True, True],
                material='Air',
                type = "Box",
                output_name='MPTECalLGLayer',
                sensdet_name='Ecal',
                nsides = 8,
                rmin = Q("0mm"),
                rmax = Q("0mm"),
                quadr = Q("0mm"),
                )

    def depth(self):
        dzm = Q("0mm")
        for dz, lspace in zip(self.dz, self.lspacing):
            dzm += dz + lspace
        return dzm

    def BarrelConfigurationLayer(self, dx = None, dy = None, name = None, sensname = None, type = None):
        # print "---- Barrel ----"
        # print "Layer parameters dx=", dx, "dy=", dy, "layername=", name, "type=", type
        self.dx = dx
        self.dy = dy
        self.output_name = name
        self.sensdet_name = sensname
        self.type = type
        return

    def EndcapConfigurationLayer(self, nsides = None, rmin = None, rmax = None, quadr = None, name = None, sensname = None, type = None):
        # print "---- Endcap ----"
        # print "Layer parameters nsides=", nsides, "rmin=", rmin, "rmax=", rmax, "quadr=", quadr, "layername=", name, "type=", type
        self.nsides = nsides
        self.rmin = rmin
        self.rmax = rmax
        self.quadr = quadr
        self.output_name = name
        self.sensdet_name = sensname
        self.type = type
        return

    def construct(self, geom):

        dzm = self.depth()
        dzm = dzm/2.0  # Box() requires half dimensions

        # make the mother volume
        name = self.output_name

        if self.type == "Box":
            layer_shape = geom.shapes.Box(name, dx=(self.dx)/ 2.0, dy=(self.dy)/2.0, dz=(self.depth()) /2.0)
            layer_lv = geom.structure.Volume(name + "_vol", shape=layer_shape, material=self.material)
        elif self.type == "Intersection":
            layer_shape_full = geom.shapes.PolyhedraRegular(name+"_full", numsides=self.nsides, sphi=pi/8, rmin=self.rmin, rmax=self.rmax, dz=(self.depth()))
            layer_quadrant = geom.shapes.Box(name+"_quadrant", dx=self.quadr, dy=self.quadr, dz=(self.depth()) /2.0)
            layer_quad_pos = geom.structure.Position(name+"_quadrant_pos", x=self.quadr, y=self.quadr)
            layer_shape = geom.shapes.Boolean(name, type='intersection', first=layer_shape_full, second=layer_quadrant, pos=layer_quad_pos)
            layer_lv = geom.structure.Volume(name+"_vol", shape=layer_shape, material=self.material)

        # no skipped space before the first layer
        skip = Q("0mm")
        cntr = 1
        zloc = Q("0mm")
        orientation = ['','_H','_V']

        for dz, lspace, mat, active in zip(self.dz, self.lspacing, self.mat, self.active):
            sname = (layer_shape.name + "_slice%i" % cntr)
            zloc = zloc + skip + dz / 2.0

            if self.type == "Box":
                slice_shape = geom.shapes.Box(sname, self.dx/2.0, self.dy/2.0, dz / 2.0)
                slice_lv = geom.structure.Volume(sname + "_vol", material=mat, shape=slice_shape)
            elif self.type == "Intersection":
                slice_shape_full = geom.shapes.PolyhedraRegular(sname+"_full", numsides=self.nsides, sphi=pi/8, rmin=self.rmin, rmax=self.rmax, dz=dz)
                slice_quadrant = geom.shapes.Box(sname+"_quadrant", dx=self.quadr, dy=self.quadr, dz=dz/2.0)
                quad_pos = geom.structure.Position(sname+"_quadrant_pos", x=self.quadr, y=self.quadr)
                slice_shape = geom.shapes.Boolean(sname, type='intersection', first=slice_shape_full, second=slice_quadrant, pos=quad_pos)
                slice_lv = geom.structure.Volume(sname + "_vol", material=mat, shape=slice_shape)

            if active:
                #slice_lv.params.append(("SensDet", name + orientation[cntr-1]))
                slice_lv.params.append(("SensDet", self.sensdet_name))

            # dzm is the half depth of the mother volume
            # we need to subtract it off to position layers
            # relative to the center of the mother
            slice_pos = geom.structure.Position(sname + "_pos", x='0mm', y='0mm', z=zloc - dzm)
            slice_pla = geom.structure.Placement(sname + "_pla", volume=slice_lv, pos=slice_pos)
            layer_lv.placements.append(slice_pla.name)

            skip = dz / 2.0 + lspace  # set the skipped space before the next layer
            cntr += 1

        self.add_volume(layer_lv)

class NDHPgTPCDetElementBuilder(gegede.builder.Builder):

    """Builds a detector element (ECAL Barrel, ECAL Endcap, PV, Yoke, GArTPC) for the ND HPgTPC"""

    defaults = dict(geometry = 'Barrel',
                    phi_range = [Q("0deg"), Q("360deg")],
                    material = 'Air',
                    nsides = 8,
                    nModules = 5,
                    output_name = 'MPTECalDetElement',
                    HGlayerType1_builder_name = "NDHPgTPCHGLayerBuilder1",
                    HGlayerType2_builder_name = "NDHPgTPCHGLayerBuilder2",
                    LGlayerType1_builder_name = "NDHPgTPCLGLayerBuilder1",
                    LGlayerType2_builder_name = "NDHPgTPCLGLayerBuilder2",
                    pvMaterial = "Steel",
                    pvThickness = Q("20mm"),
                    yokeMaterial = "Steel",
                    yokeThickness = Q("500mm"),
                    yokePhiCutout = Q("90deg"),
                    rInnerTPC = Q("2740mm"),
                    TPC_halfZ = Q('2600mm'),
                    nLayers = [30, 20],
                    typeLayers = ['HG1', 'LG1'],
                    magnetMaterial = "Aluminum",
                    magnetThickness = Q("130mm"),
                    magnetInnerR = Q("3250cm"),
                    magnetHalfLength = Q("5m")
                    )

    #def configure(self, **kwds):
        #super(NDHPgTPCDetElementBuilder, self).configure(**kwds)

    def checkVariables(self):
        if len(self.nLayers) != len(self.typeLayers):
            return False
        else:
            return True

    def get_ecal_module_thickness(self, geom):
        HGLayerType1_builder = self.get_builder(self.HGlayerType1_builder_name)
        HGLayerType2_builder = self.get_builder(self.HGlayerType2_builder_name)
        LGLayerType1_builder = self.get_builder(self.LGlayerType1_builder_name)
        LGLayerType2_builder = self.get_builder(self.LGlayerType2_builder_name)

        HGLayerType1_lv = HGLayerType1_builder.get_volume()
        HGLayerType2_lv = HGLayerType2_builder.get_volume()
        LGLayerType1_lv = LGLayerType1_builder.get_volume()
        LGLayerType2_lv = LGLayerType2_builder.get_volume()

        HGLayerType1_shape = geom.store.shapes.get(HGLayerType1_lv.shape)
        HGLayerType2_shape = geom.store.shapes.get(HGLayerType2_lv.shape)
        LGLayerType1_shape = geom.store.shapes.get(LGLayerType1_lv.shape)
        LGLayerType2_shape = geom.store.shapes.get(LGLayerType2_lv.shape)

        HG_layer_type1_thickness = HGLayerType1_shape.dz * 2
        HG_layer_type2_thickness = HGLayerType2_shape.dz * 2
        LG_layer_type1_thickness = LGLayerType1_shape.dz * 2
        LG_layer_type2_thickness = LGLayerType2_shape.dz * 2

        ecal_module_thickness = Q("0mm")

        for nlayer, type in zip(self.nLayers, self.typeLayers):
            if type == "HG1":
                layer_thickness = HG_layer_type1_thickness
            if type == "HG2":
                layer_thickness = HG_layer_type2_thickness
            if type == "LG1":
                layer_thickness = LG_layer_type1_thickness
            if type == "LG2":
                layer_thickness = LG_layer_type2_thickness

            ecal_module_thickness += nlayer * layer_thickness

        return ecal_module_thickness

    def get_pv_endcap_length(self, geom):

        safety = Q("0.1mm")
        pv_rInner = self.rInnerTPC
        pvHalfLength = self.TPC_halfZ
        pv_rmin = sqrt((pv_rInner/Q("1mm"))**2)*Q("1mm")
        pv_rmax = pv_rmin + self.pvThickness

        rmin_sph = sqrt((pvHalfLength/Q("1mm"))**2 + (pv_rmax/Q("1mm"))**2)*Q("1mm")
        rmax_sph = rmin_sph + self.pvThickness

        return rmax_sph

    def construct(self, geom):

        if self.checkVariables() == False:
            print "The variables nLayers and typeLayers have different sizes! for builder", self.name
            exit()

        if self.geometry == 'ECALBarrel':
            self.construct_ecal_barrel_staves(geom)
        elif self.geometry == 'ECALEndcap':
            self.construct_ecal_endcap_staves(geom)
        elif self.geometry == 'PV':
            self.construct_pv(geom)
        elif self.geometry == 'Magnet':
            self.construct_magnet(geom)
        # elif self.geometry == 'YokeBarrel':
        #     self.construct_yoke_barrel_staves(geom)
        # elif self.geometry == 'YokeEndcap':
        #     self.construct_yoke_endcap_staves(geom)
        else:
            print "Could not find the geometry asked!"
            return
        return

    def construct_magnet(self, geom):
        ''' construct the Magnet '''

        print "Construct Magnet"

        magnet_name = self.output_name
        magnet_shape = geom.shapes.Tubs(magnet_name, rmin=self.magnetInnerR, rmax=self.magnetInnerR+self.magnetThickness, dz=self.magnetHalfLength, sphi="0deg", dphi="360deg")
        magnet_vol = geom.structure.Volume(magnet_name+"_vol", shape=magnet_shape, material=self.magnetMaterial)

        self.add_volume(magnet_vol)

    def construct_pv(self, geom):
        ''' construct the Pressure Vessel '''

        print "Construct PV Barrel"

        nsides = self.nsides
        pv_rInner = self.rInnerTPC
        pvHalfLength = self.TPC_halfZ
        pv_rmin = sqrt((pv_rInner/Q("1mm"))**2)*Q("1mm")
        pv_rmax = pv_rmin + self.pvThickness

        # build the pressure vessel barrel
        pvb_name = self.output_name + "Barrel"
        pvb_shape = geom.shapes.Tubs(pvb_name, rmin=pv_rmin, rmax=pv_rmax, dz=pvHalfLength, sphi="0deg", dphi="360deg")
        pvb_vol = geom.structure.Volume(pvb_name+"_vol", shape=pvb_shape, material=self.pvMaterial)

        self.add_volume(pvb_vol)

        print "Construct PV Endcap"

        # build the pressure vessel endcaps
        pv_endcap_shape_tub = geom.shapes.Tubs("PVEndcap_tubs", rmin=Q("0mm"), rmax=pv_rmax, dz=2*pvHalfLength, sphi="0deg", dphi="360deg")
        rmin_sph = sqrt((pvHalfLength/Q("1mm"))**2 + (pv_rmax/Q("1mm"))**2)*Q("1mm")
        rmax_sph = rmin_sph + self.pvThickness
        pv_endcap_shape_sphere = geom.shapes.Sphere("PVEndcap_sphere", rmin=rmin_sph, rmax=rmax_sph, sphi="0deg", dphi="360deg", stheta="0deg", dtheta="179.99999deg")

        pv_endcap_shape_inter = geom.shapes.Boolean( self.output_name + "Endcap", type='intersection', first=pv_endcap_shape_tub, second=pv_endcap_shape_sphere)
        pvec_vol = geom.structure.Volume( self.output_name+"Endcap"+"_vol", shape=pv_endcap_shape_inter, material=self.pvMaterial )

        self.add_volume(pvec_vol)

    def construct_ecal_barrel_staves(self, geom):
        ''' construct a set of ECAL staves for the Barrel '''

        #       ECAL stave
        #   /----------------\         //Small side
        #  /                  \
        # /____________________\       //Large side
        #
        # z
        # ^
        # |
        # |-----> x
        #
        # need to create the layer based on the position in depth z -> different layer sizes

        print "Construct ECAL Barrel"

        # ECAL Barrel
        safety = Q("0.1mm")
        nsides = self.nsides
        dphi = (2*pi/nsides)
        hphi = dphi/2;

        #ecal module thickness
        ecal_module_thickness = self.get_ecal_module_thickness(geom)
        ecal_module_thickness_noSupport = ecal_module_thickness - safety
        #inner radius ecal (TPC + pv + safety)
        rInnerEcal = self.rInnerTPC + self.pvThickness
        #barrel length (TPC + PV)
        Barrel_halfZ = self.get_pv_endcap_length(geom)
        #outer radius ecal (inner radius ecal + ecal module)
        rOuterEcal = rInnerEcal + ecal_module_thickness

        #maximum dimension of the stave
        max_dim_stave = 2 * tan( pi/nsides ) * rInnerEcal + ecal_module_thickness_noSupport / sin( 2*pi/nsides )
        #minimum dimension of the stave
        min_dim_stave = max_dim_stave - 2*ecal_module_thickness / tan( 2*pi/nsides )

        Ecal_Barrel_halfZ = Barrel_halfZ
        Ecal_Barrel_n_modules = self.nModules
        #dimension of a module along the ND x direction
        Ecal_Barrel_module_dim = Ecal_Barrel_halfZ * 2 / Ecal_Barrel_n_modules

        print "Large side of the stave", max_dim_stave
        print "Small side of the stave", min_dim_stave
        print "Barrel module dim in z", Ecal_Barrel_module_dim
        print "Module thickness", ecal_module_thickness

        #Position of the stave in the Barrel (local coordinates)
        X = rInnerEcal + safety + ecal_module_thickness / 2.
        Y = (ecal_module_thickness_noSupport / 2.) / sin(2.*pi/nsides)


        #Mother volume Barrel
        barrel_shape = geom.shapes.PolyhedraRegular(self.output_name, numsides=nsides, rmin=rInnerEcal, rmax=rOuterEcal+2*safety, dz=Ecal_Barrel_halfZ+safety)
        barrel_lv = geom.structure.Volume(self.output_name+"_vol", shape=barrel_shape, material=self.material)

        sensname = self.output_name + "_vol"
        for istave in range(nsides):
            stave_id = istave+1
            dstave = int( nsides/4.0 )
            phirot =  hphi + pi/2.0
            phirot += (istave - dstave)*dphi
            phirot2 =  (istave - dstave) * dphi + hphi

            for imodule in range(Ecal_Barrel_n_modules):
                module_id = imodule+1
                print "Placing stave ", stave_id, " and module ", module_id

                stave_name = self.output_name + "_stave%02i" % (stave_id) + "_module%02i" % (module_id)
                stave_volname = self.output_name + "_stave%02i" % (stave_id) + "_module%02i" % (module_id) + "_vol"

                stave_shape = geom.shapes.Trapezoid(stave_name, dx1=max_dim_stave/2.0, dx2=min_dim_stave/2.0,
                dy1=(Ecal_Barrel_module_dim-safety)/2.0, dy2=(Ecal_Barrel_module_dim-safety)/2.0,
                dz=ecal_module_thickness/2.0)

                stave_lv = geom.structure.Volume(stave_volname, shape=stave_shape, material=self.material)

                zPos = Q("0mm")
                layer_id = 1

                for nlayer, type in zip(self.nLayers, self.typeLayers):
                    for ilayer in range(nlayer):

                        layername = self.output_name + "_stave%02i" % (stave_id) + "_module%02i" % (module_id) + "_layer_%02i" % (layer_id)

                        if type == 'HG1':
                            #Configure the layer length based on the zPos in the stave
                            HGLayer_builder = self.get_builder(self.HGlayerType1_builder_name)
                            layer_thickness = NDHPgTPCHGLayerBuilder.depth(HGLayer_builder)
                            l_dim_x = max_dim_stave - 2 * (zPos + layer_thickness) / tan(2.* pi / nsides)
                            l_dim_y = Ecal_Barrel_module_dim - safety

                            NDHPgTPCHGLayerBuilder.BarrelConfigurationLayer(HGLayer_builder, l_dim_x, l_dim_y, layername, sensname, "Box")
                            NDHPgTPCHGLayerBuilder.construct(HGLayer_builder, geom)
                            layer_lv = HGLayer_builder.get_volume(layername+"_vol")

                        if type == 'HG2':
                            #Configure the layer length based on the zPos in the stave
                            HGLayer_builder = self.get_builder(self.HGlayerType2_builder_name)
                            layer_thickness = NDHPgTPCHGLayerBuilder.depth(HGLayer_builder)
                            l_dim_x = max_dim_stave - 2 * (zPos + layer_thickness) / tan(2.* pi / nsides)
                            l_dim_y = Ecal_Barrel_module_dim - safety

                            NDHPgTPCHGLayerBuilder.BarrelConfigurationLayer(HGLayer_builder, l_dim_x, l_dim_y, layername, sensname, "Box")
                            NDHPgTPCHGLayerBuilder.construct(HGLayer_builder, geom)
                            layer_lv = HGLayer_builder.get_volume(layername+"_vol")

                        if type == 'LG1':
                            LGLayer_builder = self.get_builder(self.LGlayerType1_builder_name)
                            layer_thickness = NDHPgTPCLGLayerBuilder.depth(LGLayer_builder)
                            l_dim_x = max_dim_stave - 2 * (zPos + layer_thickness) / tan(2.* pi / nsides)
                            l_dim_y = Ecal_Barrel_module_dim - safety

                            NDHPgTPCLGLayerBuilder.BarrelConfigurationLayer(LGLayer_builder, l_dim_x, l_dim_y, layername, sensname, "Box")
                            NDHPgTPCLGLayerBuilder.construct(LGLayer_builder, geom)
                            layer_lv = LGLayer_builder.get_volume(layername+"_vol")

                        if type == 'LG2':
                            LGLayer_builder = self.get_builder(self.LGlayerType2_builder_name)
                            layer_thickness = NDHPgTPCLGLayerBuilder.depth(LGLayer_builder)
                            l_dim_x = max_dim_stave - 2 * (zPos + layer_thickness) / tan(2.* pi / nsides)
                            l_dim_y = Ecal_Barrel_module_dim - safety

                            NDHPgTPCLGLayerBuilder.BarrelConfigurationLayer(LGLayer_builder, l_dim_x, l_dim_y, layername, sensname, "Box")
                            NDHPgTPCLGLayerBuilder.construct(LGLayer_builder, geom)
                            layer_lv = LGLayer_builder.get_volume(layername+"_vol")

                        #Placement layer in stave
                        layer_pos = geom.structure.Position(layername+"_pos", z=zPos + layer_thickness/2.0 - ecal_module_thickness/2.0)
                        layer_pla = geom.structure.Placement(layername+"_pla", volume=layer_lv, pos=layer_pos)

                        stave_lv.placements.append(layer_pla.name)

                        zPos += layer_thickness;
                        layer_id += 1

                #Placement staves in Barrel
                name = stave_lv.name
                pos = geom.structure.Position(name + "_pos", x=(X*cos(phirot2)-Y*sin(phirot2)), y=(( X*sin(phirot2)+Y*cos(phirot2) )), z=( imodule+0.5 )*Ecal_Barrel_module_dim - Barrel_halfZ )
                rot = geom.structure.Rotation(name + "_rot", x=pi/2.0, y=phirot+pi, z=Q("0deg"))
                pla = geom.structure.Placement(name + "_pla", volume=stave_lv, pos=pos, rot=rot)

                barrel_lv.placements.append(pla.name)

        self.add_volume(barrel_lv)

    def construct_ecal_endcap_staves(self, geom):
        ''' construct a set of ECAL staves for the Endcap '''

        print "Construct ECAL Endcap"

        # ECAL Endcap
        safety = Q("0.1mm")
        nsides = self.nsides
        ecal_module_thickness = self.get_ecal_module_thickness(geom)
        rInnerEcal = self.rInnerTPC + self.pvThickness + safety
        Barrel_halfZ = self.get_pv_endcap_length(geom) + safety

        EcalEndcap_inner_radius = Q("0mm")
        EcalEndcap_outer_radius = rInnerEcal + ecal_module_thickness
        Ecal_Barrel_halfZ = Barrel_halfZ
        EcalEndcap_min_z = Ecal_Barrel_halfZ
        EcalEndcap_max_z = Ecal_Barrel_halfZ + ecal_module_thickness
        Ecal_Barrel_n_modules = self.nModules

        rmin = EcalEndcap_inner_radius
        rmax = EcalEndcap_outer_radius

        #Mother volume Endcap
        endcap_shape_min = geom.shapes.PolyhedraRegular("ECALEndcap_min", numsides=nsides, rmin=rmin, rmax=rmax, dz=EcalEndcap_min_z)
        endcap_shape_max = geom.shapes.PolyhedraRegular("ECALEndcap_max", numsides=nsides, rmin=rmin, rmax=rmax, dz=EcalEndcap_max_z)

        endcap_shape = geom.shapes.Boolean( self.output_name, type='subtraction', first=endcap_shape_max, second=endcap_shape_min )
        endcap_lv = geom.structure.Volume( self.output_name+"_vol", shape=endcap_shape, material=self.material )

        # Place staves in the Endcap Volume
        sensname = self.output_name + "_vol"
        module_id = -1
        for iend in range(2):
            if iend == 0:
                module_id = 0
            else:
                module_id = Ecal_Barrel_n_modules + 1

            this_module_z_offset = (EcalEndcap_min_z + EcalEndcap_max_z)/2.
            if iend == 0:
                this_module_z_offset *= -1

            this_module_rotY = 0.;
            if iend == 0:
                this_module_rotY = pi;

            rotZ_offset = (pi/8. + 3.*pi/4.)

            if iend == 0:
                rotZ_offset = (pi/8. - pi/2.)

            for iquad in range(4):
                stave_id = iquad+1
                this_module_rotZ = 0
                if iend == 0:
                    this_module_rotZ = rotZ_offset - (iquad-2) * pi/2.
                else:
                    this_module_rotZ = rotZ_offset + (iquad+1) * pi/2.

                print "Placing stave ", stave_id, " and module ", module_id

                #Create a template module
                stave_name = self.output_name + "_stave%02i" % (stave_id) + "_module%02i" % (module_id)
                stave_volname = self.output_name + "_stave%02i" % (stave_id) + "_module%02i" % (module_id) + "_vol"

                endcap_stave_full = geom.shapes.PolyhedraRegular(stave_name+"_full", numsides=nsides, sphi=pi/8, dphi=Q("360deg"), rmin=rmin, rmax=rmax, dz=ecal_module_thickness)
                quadr = rmax
                quadrant = geom.shapes.Box(stave_name+"_quadrant", dx=quadr, dy=quadr, dz=ecal_module_thickness/2)

                endcap_stave_pos = geom.structure.Position(stave_name+"_pos", x=quadr, y=quadr, z=Q("0mm"))
                endcap_stave_shape = geom.shapes.Boolean(stave_name, type='intersection', first=endcap_stave_full, second=quadrant, pos=endcap_stave_pos)
                endcap_stave_lv = geom.structure.Volume(stave_volname, shape=endcap_stave_shape, material=self.material)

                zPos = Q("0mm")
                layer_id = 1

                for nlayer, type in zip(self.nLayers, self.typeLayers):
                    for ilayer in range(nlayer):
                        layername = self.output_name + "_stave%02i" % (stave_id) + "_module%02i" % (module_id) + "_layer_%02i" % (layer_id)

                        if type == 'HG1':
                            HGLayer_builder = self.get_builder(self.HGlayerType1_builder_name)
                            NDHPgTPCHGLayerBuilder.EndcapConfigurationLayer(HGLayer_builder, nsides, rmin, rmax, quadr, layername, sensname, "Intersection")
                            NDHPgTPCHGLayerBuilder.construct(HGLayer_builder, geom)
                            layer_lv = HGLayer_builder.get_volume(layername+"_vol")
                            layer_thickness = NDHPgTPCHGLayerBuilder.depth(HGLayer_builder)

                        if type == 'HG2':
                            HGLayer_builder = self.get_builder(self.HGlayerType2_builder_name)
                            NDHPgTPCHGLayerBuilder.EndcapConfigurationLayer(HGLayer_builder, nsides, rmin, rmax, quadr, layername, sensname, "Intersection")
                            NDHPgTPCHGLayerBuilder.construct(HGLayer_builder, geom)
                            layer_lv = HGLayer_builder.get_volume(layername+"_vol")
                            layer_thickness = NDHPgTPCHGLayerBuilder.depth(HGLayer_builder)

                        if type == 'LG1':
                            LGLayer_builder = self.get_builder(self.LGlayerType1_builder_name)
                            NDHPgTPCLGLayerBuilder.EndcapConfigurationLayer(LGLayer_builder, nsides, rmin, rmax, quadr, layername, sensname, "Intersection")
                            NDHPgTPCLGLayerBuilder.construct(LGLayer_builder, geom)
                            layer_lv = LGLayer_builder.get_volume(layername+"_vol")
                            layer_thickness = NDHPgTPCLGLayerBuilder.depth(LGLayer_builder)

                        if type == 'LG2':
                            LGLayer_builder = self.get_builder(self.LGlayerType2_builder_name)
                            NDHPgTPCLGLayerBuilder.EndcapConfigurationLayer(LGLayer_builder, nsides, rmin, rmax, quadr, layername, sensname, "Intersection")
                            NDHPgTPCLGLayerBuilder.construct(LGLayer_builder, geom)
                            layer_lv = LGLayer_builder.get_volume(layername+"_vol")
                            layer_thickness = NDHPgTPCLGLayerBuilder.depth(LGLayer_builder)

                        # Placement layer in stave
                        layer_pos = geom.structure.Position(layername+"_pos", z=zPos + layer_thickness/2.0 - ecal_module_thickness/2.0)
                        layer_pla = geom.structure.Placement(layername+"_pla", volume=layer_lv, pos=layer_pos)

                        endcap_stave_lv.placements.append(layer_pla.name)

                        zPos += layer_thickness;
                        layer_id += 1

                #Placement staves in Endcap
                name = endcap_stave_lv.name
                endcap_stave_pos = geom.structure.Position(name + "_pos", z=this_module_z_offset )
                endcap_stave_rot = geom.structure.Rotation(name + "_rot", x=Q("0deg"), y=this_module_rotY, z=this_module_rotZ+pi/4)
                endcap_stave_pla = geom.structure.Placement(name + "_pla", volume=endcap_stave_lv, pos=endcap_stave_pos, rot=endcap_stave_rot)

                endcap_lv.placements.append(endcap_stave_pla.name)

        self.add_volume(endcap_lv)

    # def construct_yoke_barrel_staves(self, geom):
    #     print "Construct Yoke Barrel"
    #
    #     safety = Q("1mm")
    #     ecal_module_thickness = self.get_ecal_module_thickness(geom)
    #
    #     nsides = self.nsides
    #     pv_rInner = self.rInnerEcal + ecal_module_thickness + safety
    #     pvHalfLength = self.Barrel_halfZ + ecal_module_thickness
    #     half_max_dim_x = 0.5*(2 * tan( pi/nsides ) * self.rInnerEcal + ecal_module_thickness / sin( 2*pi/nsides ))
    #     pv_rmin = sqrt((pv_rInner/Q("1mm"))**2 + (half_max_dim_x/Q("1mm"))**2)*Q("1mm")
    #     pv_rmax = pv_rmin + self.pvThickness
    #
    #     distYoke_PV_barrel = Q("15cm")
    #     yoke_rmin = pv_rmax + safety + distYoke_PV_barrel
    #     yoke_rmax = yoke_rmin + self.yokeThickness
    #     Yoke_Barrel_n_modules = self.nModules
    #
    #     rmin_sph = sqrt((pvHalfLength/Q("1mm"))**2 + (pv_rmax/Q("1mm"))**2)*Q("1mm")
    #     rmax_sph = rmin_sph + self.pvThickness
    #
    #     dz = pvHalfLength + (rmax_sph - pvHalfLength) + distYoke_PV_barrel
    #     by_name="YokeBarrel"
    #
    #     # sphi=self.yokePhiCutout/2.0
    #     # dphi=Q("360deg")-self.yokePhiCutout
    #
    #     #Mother volume Barrel
    #     by_shape = geom.shapes.PolyhedraRegular(by_name, numsides=nsides, rmin=yoke_rmin, rmax=yoke_rmax, dz=dz)
    #     by_lv = geom.structure.Volume(by_name+"_vol", shape=by_shape, material='Air')
    #
    #     #Create a template module
    #     yoke_stave_name = by_name + "_stave"
    #     yoke_stave_volname = by_name + "_stave" + "_vol"
    #
    #     Yoke_Barrel_halfZ = dz
    #     Yoke_Barrel_module_dim = Yoke_Barrel_halfZ * 2 / Yoke_Barrel_n_modules
    #     yoke_max_dim_x = 2 * tan( pi/nsides ) * yoke_rmin + self.yokeThickness / sin( 2*pi/nsides ) #large side
    #     yoke_min_dim_x = yoke_max_dim_x - 2*self.yokeThickness / tan( 2*pi/nsides ) # small side
    #
    #     yoke_stave_shape = geom.shapes.Trapezoid(yoke_stave_name, dx1=yoke_max_dim_x/2.0, dx2=yoke_min_dim_x/2.0,
    #     dy1=Yoke_Barrel_module_dim/2.0, dy2=Yoke_Barrel_module_dim/2.0,
    #     dz=self.yokeThickness/2.0)
    #
    #     yoke_stave_lv = geom.structure.Volume(yoke_stave_volname, shape=yoke_stave_shape, material=self.yokeMaterial)
    #
    #     X = yoke_rmin + self.yokeThickness / 2.
    #     Y = (self.yokeThickness / 2.) / sin(2.*pi/nsides)
    #     dphi = (2*pi/nsides)
    #     hphi = dphi/2;
    #
    #     #Placing the staves and modules
    #     for istave in range(nsides):
    #         stave_id = istave+1
    #         dstave = int( nsides/4.0 )
    #         phirot =  hphi + pi/2.0
    #         phirot += (istave - dstave) * dphi
    #         phirot2 =  (istave - dstave) * dphi + hphi
    #
    #         for imodule in range(Yoke_Barrel_n_modules):
    #             module_id = imodule+1
    #             print "Placing stave ", stave_id, " and module ", module_id
    #
    #             #Placement staves in Barrel
    #             name = yoke_stave_lv.name + "_%i" % (stave_id) + "_module%i" % (module_id)
    #             pos = geom.structure.Position(name + "_pos", x=(X*cos(phirot2)-Y*sin(phirot2)), y=(( X*sin(phirot2)+Y*cos(phirot2) )), z=( imodule+0.5 )*Yoke_Barrel_module_dim - Yoke_Barrel_halfZ )
    #             rot = geom.structure.Rotation(name + "_rot", x=pi/2.0, y=phirot+pi, z=Q("0deg"))
    #             pla = geom.structure.Placement(name + "_pla", volume=yoke_stave_lv, pos=pos, rot=rot)
    #
    #             by_lv.placements.append(pla.name)
    #
    #     self.add_volume(by_lv)
    #
    # def construct_yoke_endcap_staves(self, geom):
    #     print "Construct Yoke Endcap"
    #
    #     safety = Q("1mm")
    #     ecal_module_thickness = self.get_ecal_module_thickness(geom)
    #
    #     nsides = self.nsides
    #     pv_rInner = self.rInnerEcal + ecal_module_thickness + safety
    #     pvHalfLength = self.Barrel_halfZ + ecal_module_thickness
    #     half_max_dim_x = 0.5*(2 * tan( pi/nsides ) * self.rInnerEcal + ecal_module_thickness / sin( 2*pi/nsides ))
    #     pv_rmin = sqrt((pv_rInner/Q("1mm"))**2 + (half_max_dim_x/Q("1mm"))**2)*Q("1mm")
    #     pv_rmax = pv_rmin + self.pvThickness
    #
    #     distYoke_PV_barrel = Q("15cm")
    #     yoke_rmin = pv_rmax + safety + distYoke_PV_barrel
    #     yoke_rmax = yoke_rmin + self.yokeThickness
    #
    #     rmin_sph = sqrt((pvHalfLength/Q("1mm"))**2 + (pv_rmax/Q("1mm"))**2)*Q("1mm")
    #     rmax_sph = rmin_sph + self.pvThickness
    #
    #     YokeEndcap_min_z = pvHalfLength + (rmax_sph - pvHalfLength) + safety + distYoke_PV_barrel
    #     YokeEndcap_max_z = pvHalfLength + (rmax_sph - pvHalfLength) + safety + distYoke_PV_barrel + self.yokeThickness
    #
    #     #Mother volume Endcap
    #     yoke_endcap_shape_min = geom.shapes.PolyhedraRegular("YokeEndcap_min", numsides=nsides, rmin=Q("0mm"), rmax=yoke_rmax, dz=YokeEndcap_min_z)
    #     yoke_endcap_shape_max = geom.shapes.PolyhedraRegular("YokeEndcap_max", numsides=nsides, rmin=Q("0mm"), rmax=yoke_rmax, dz=YokeEndcap_max_z)
    #
    #     yoke_endcap_shape = geom.shapes.Boolean( "YokeEndcap_sub", type='subtraction', first=yoke_endcap_shape_max, second=yoke_endcap_shape_min )
    #     center_hole = geom.shapes.Tubs("center_hole", rmin=Q("0mm"), rmax=Q("0.5m"), dz=YokeEndcap_max_z, sphi=Q("0deg"), dphi=Q("360deg"))
    #
    #     yoke_endcap_shape_whole = geom.shapes.Boolean( "YokeEndcap", type='subtraction', first=yoke_endcap_shape, second=center_hole )
    #     yoke_endcap_lv = geom.structure.Volume( self.output_name+"_vol", shape=yoke_endcap_shape_whole, material='Air' )
    #
    #     #Create endcap stave template
    #     ecy_name = "YokeEndcap"
    #     yoke_endcap_stave_name = ecy_name + "_stave"
    #     yoke_endcap_stave_volname = ecy_name + "_stave" + "_vol"
    #
    #     yoke_endcap_stave_shape = geom.shapes.PolyhedraRegular(yoke_endcap_stave_name+"_full", numsides=nsides, rmin=Q("0mm"), rmax=yoke_rmax, dz=self.yokeThickness/2.0)
    #
    #     yoke_endcap_stave_shape_whole = geom.shapes.Boolean(yoke_endcap_stave_name, type='subtraction', first=yoke_endcap_stave_shape, second=center_hole )
    #     yoke_endcap_stave_lv = geom.structure.Volume(yoke_endcap_stave_volname, shape=yoke_endcap_stave_shape_whole, material=self.yokeMaterial)
    #
    #     Yoke_Barrel_n_modules = self.nModules
    #     module_id = -1
    #     for iend in range(2):
    #         if iend == 0:
    #             module_id = 0
    #         else:
    #             module_id = Yoke_Barrel_n_modules + 1
    #
    #         this_module_z_offset = (YokeEndcap_min_z + YokeEndcap_max_z)/2.
    #         if iend == 0:
    #             this_module_z_offset *= -1
    #
    #         print "Placing yoke endcap module ", module_id
    #
    #         #Placement staves in Endcap
    #         name = yoke_endcap_stave_lv.name + "_module%i" % (module_id)
    #         yoke_endcap_stave_pos = geom.structure.Position(name + "_pos", x=Q("0mm"), y=Q("0mm"), z=this_module_z_offset)
    #         #yoke_endcap_stave_rot = geom.structure.Rotation(name + "_rot", x=Q("180deg"), y=this_module_rotY, z=Q("0deg"))
    #         #yoke_endcap_stave_pla = geom.structure.Placement(name + "_pla", volume=yoke_endcap_stave_lv, pos=yoke_endcap_stave_pos, rot=yoke_endcap_stave_rot)
    #         yoke_endcap_stave_pla = geom.structure.Placement(name + "_pla", volume=yoke_endcap_stave_lv, pos=yoke_endcap_stave_pos)
    #
    #         yoke_endcap_lv.placements.append(yoke_endcap_stave_pla.name)
    #
    #     self.add_volume(yoke_endcap_lv)
