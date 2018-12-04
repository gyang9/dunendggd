#!/usr/bin/env python
'''
Builds compontents for the MPT ECAL
'''

import gegede.builder
from gegede import Quantity as Q
from math import floor, atan, sin, cos, tan, sqrt, pi

class NDHPgTPCHGLayerBuilder(gegede.builder.Builder):

    """Builds ECAL HG Layers"""

    defaults = dict(dx=Q("10mm"), dy=Q("10mm"),
                dz=[Q('2mm'), Q('10mm'), Q('1mm')],
                lspacing=[Q('0.1mm'), Q('0.1mm'), Q('0.1mm')],
                mat=['Copper', 'Scintillator', 'FR4'],
                active=[False, True, False],
                material='Air',
                type = "Box",
                output_name='MPTECalHGLayer'
                )

    def depth(self):
        dzm = Q("0mm")
        for dz, lspace in zip(self.dz, self.lspacing):
            dzm += dz + lspace
        return dzm

    def changeLayerDim(self, dx = None, dy = None, name = None, type = None):
        # print "Changing param..", dx, dy, name
        self.dx = dx
        self.dy = dy
        self.output_name = name
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
            layer_shape_full = geom.shapes.PolyhedraRegular(name+"_full", numsides=nsides, rmin=Q("0mm"), rmax=Ecal_inner_radius+module_thickness, dz=module_thickness)
            quadr = Ecal_inner_radius+module_thickness
            layer_quadrant = geom.shapes.Box(name+"Quadrant", dx=quadr, dy=quadr, dz=module_thickness)

            layer_pos = geom.structure.Position(name+"_inter"+"_pos", x=quadr - EcalEndcap_inner_radius, y=quadr + EcalEndcap_inner_radius)
            layer_shape = geom.shapes.Boolean(name+"_inter", type='intersection', first=layer_shape_full, second=layer_quadrant, pos=layer_pos)
            layer_lv = geom.structure.Volume(name+"_inter"+"_vol", shape=layer_shape, material=self.material)

        # no skipped space before the first layer
        skip = Q("0mm")
        cntr = 1
        zloc = Q("0mm")
        for dz, lspace, mat, active in zip(self.dz, self.lspacing, self.mat, self.active):
            sname = (layer_shape.name + "_slice%i" % cntr)
            zloc = zloc + skip + dz / 2.0

            if self.type == "Box":
                slice_shape = geom.shapes.Box(sname+"_box", self.dx/2.0, self.dy/2.0, dz / 2.0)
                slice_lv = geom.structure.Volume(sname+"_box" + "_vol", material=mat, shape=slice_shape)
            elif self.type == "Intersection":
                slice_shape_full = geom.shapes.PolyhedraRegular(sname+"_full", numsides=nsides, rmin=Q("0mm"), rmax=Ecal_inner_radius+module_thickness, dz=dz/2.0)
                quadr = Ecal_inner_radius+module_thickness
                slice_quadrant = geom.shapes.Box(sname+"Quadrant", dx=quadr, dy=quadr, dz=dz/2.0)

                slice_pos = geom.structure.Position(sname+"_inter"+"_pos", x=quadr - EcalEndcap_inner_radius, y=quadr + EcalEndcap_inner_radius)
                slice_shape = geom.shapes.Boolean(sname+"_inter", type='intersection', first=layer_shape_full, second=layer_quadrant, pos=slice_pos)
                slice_lv = geom.structure.Volume(sname+"_inter" + "_vol", material=mat, shape=slice_shape)

            if active:
                slice_lv.params.append(("SensDet", self.output_name))
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
                active=[False, True, False],
                material='Air',
                output_name='MPTECalLGLayer'
                )

    def depth(self):
        dzm = Q("0mm")
        for dz, lspace in zip(self.dz, self.lspacing):
            dzm += dz + lspace
        return dzm

    def construct(self, geom):
        #print "dx", self.dx, "dy", self.dy
        dzm = self.depth()
        dzm = dzm/2.0  # Box() requires half dimensions
        #print "layer thickness=", dzm * 2, "mm"
        # make the mother volume
        name = self.output_name

        layer_shape = geom.shapes.Box(name, dx=(self.dx)/ 2.0, dy=(self.dy)/2.0, dz=(self.depth()) /2.0)
        layer_lv = geom.structure.Volume(name + "_vol", shape=layer_shape, material=self.material)

        # no skipped space before the first layer
        skip = Q("0mm")
        cntr = 1
        zloc = Q("0mm")
        for dz, lspace, mat, active in zip(self.dz, self.lspacing, self.mat, self.active):
            sname = (self.output_name + "_slice%i" % cntr)
            slice_shape = geom.shapes.Box(sname, self.dx/2.0, self.dy/2.0, dz / 2.0)
            #print "Material layer shape dx=", layer_shape.dx*2, "dy=", layer_shape.dy*2, "dz=", layer_shape.dz*2
            zloc = zloc + skip + dz / 2.0
            #print dz, lspace, mat, zloc
            slice_lv = geom.structure.Volume(sname + "_vol", material=mat, shape=slice_shape)
            if active:
                slice_lv.params.append(("SensDet", self.output_name))
            # dzm is the half depth of the mother volume
            # we need to subtract it off to position layers
            # relative to the center of the mother
            slice_pos = geom.structure.Position(sname + "_pos", x='0mm', y='0mm', z=zloc - dzm)
            slice_pla = geom.structure.Placement(sname + "_pla", volume=slice_lv, pos=slice_pos)
            layer_lv.placements.append(slice_pla.name)

            skip = dz / 2.0 + lspace  # set the skipped space before the next layer
            cntr += 1

        self.add_volume(layer_lv)
        return

class NDHPgTPCDetElementBuilder(gegede.builder.Builder):

    """Builds a detector element of ECAL layers"""

    defaults = dict(geometry='Barrel',
                    r=Q("2.5m"),
                    phi_range=[Q("0deg"), Q("360deg")],
                    Barrel_halfZ=Q("1000mm"),
                    material='Air',
                    nLayers=1,
                    nModules=1,
                    output_name='MPTECalDetElement',
                    HGlayer_builder_name="NDHPgTPCHGLayerBuilder",
                    LGlayer_builder_name="NDHPgTPCLGLayerBuilder"
                    )

    #def configure(self, **kwds):
        #super(NDHPgTPCDetElementBuilder, self).configure(**kwds)

    def construct(self, geom):
        if self.geometry == 'Barrel':
            self.construct_barrel_staves(geom)
        elif self.geometry == 'Endcap':
            self.construct_endcap_staves(geom)
        else:
            print "Could not find the geometry asked!"
            return
        return

    def construct_barrel_staves(self, geom):
        ''' construct a set of staves for the Barrel '''

        #       ECAL stave
        #   /----------------\         //Small side
        #  /                  \
        # /____________________\       //Large side

        # need to create the layer based on the position in depth z -> different layer sizes

        print "Construct ECAL Barrel"

        HGLayer_builder = self.get_builder(self.HGlayer_builder_name)
        LGLayer_builder = self.get_builder(self.LGlayer_builder_name)

        HGLayer_lv = HGLayer_builder.get_volume()
        LGLayer_lv = LGLayer_builder.get_volume()

        HGLayer_shape = geom.store.shapes.get(HGLayer_lv.shape)

        # ECAL Barrel
        nsides = self.nsides

        Ecal_inner_radius = self.r
        layer_thickness = HGLayer_shape.dz * 2
        safety = Q("1mm")
        module_thickness = self.nLayers * layer_thickness + safety

        max_dim_x = 2 * tan( pi/nsides ) * Ecal_inner_radius + module_thickness / sin( 2*pi/nsides ) #large side
        min_dim_x = max_dim_x - 2*module_thickness / tan( 2*pi/nsides ) # small side

        Ecal_Barrel_halfZ = self.Barrel_halfZ
        Ecal_Barrel_n_modules = self.nModules
        Ecal_Barrel_module_dim = Ecal_Barrel_halfZ * 2 / Ecal_Barrel_n_modules

        X = Ecal_inner_radius + module_thickness / 2.
        #end of slabs aligned to inner face of support plate in next stave (not the outer surface)
        Y = (module_thickness / 2.) / sin(2.*pi/nsides)
        dphi = (2*pi/nsides)
        hphi = dphi/2;

        #Mother volume Barrel
        barrel_shape = geom.shapes.PolyhedraRegular(self.output_name, numsides=nsides, rmin=Ecal_inner_radius, rmax=Ecal_inner_radius+module_thickness, dz=Ecal_Barrel_halfZ)
        barrel_lv = geom.structure.Volume(self.output_name+"_vol", shape=barrel_shape, material=self.material)

        #Create a template module
        stave_name = self.output_name + "_stave"
        stave_volname = self.output_name + "_stave" + "_vol"

        stave_shape = geom.shapes.Trapezoid(stave_name, dx1=max_dim_x/2.0, dx2=min_dim_x/2.0,
        dy1=Ecal_Barrel_module_dim/2.0, dy2=Ecal_Barrel_module_dim/2.0,
        dz=module_thickness/2.0)

        stave_lv = geom.structure.Volume(stave_volname, shape=stave_shape, material=self.material)

        zPos = Q("0mm")
        layer_id = 0
        for ilayer in range(self.nLayers):
            layer_id = ilayer + 1

            #Configure the layer length based on the zPos in the stave
            l_dim_x = max_dim_x - 2 * (zPos + layer_thickness) / tan(2.* pi / nsides)
            l_dim_y = Ecal_Barrel_module_dim
            layername = self.output_name + "_stave" + "_module" + "_layer_%i" % (layer_id)

            HGLayer_builder = self.get_builder(self.HGlayer_builder_name)
            NDHPgTPCHGLayerBuilder.changeLayerDim(HGLayer_builder, l_dim_x, l_dim_y, layername, "Box")
            NDHPgTPCHGLayerBuilder.construct(HGLayer_builder, geom)
            layer_lv = HGLayer_builder.get_volume(layername+"_vol")

            #Placement layer in stave
            layer_pos = geom.structure.Position(layername+"_pos", z=zPos + layer_thickness/2.0 - module_thickness/2.0)
            layer_pla = geom.structure.Placement(layername+"_pla", volume=layer_lv, pos=layer_pos)

            stave_lv.placements.append(layer_pla.name)

            zPos += layer_thickness;

        #Placing the staves and modules
        for istave in range(nsides):
            stave_id = istave+1
            dstave = int( nsides/4.0 )
            phirot =  hphi + pi/2.0
            phirot += (istave - dstave)*dphi
            phirot2 =  (istave - dstave) * dphi + hphi

            for imodule in range(Ecal_Barrel_n_modules):
                module_id = imodule+1
                print "Placing stave ", stave_id, " and module ", module_id

                #Placement staves in Barrel
                name = stave_lv.name + "_%i" % (stave_id) + "_module%i" % (module_id)
                pos = geom.structure.Position(name + "_pos", x=(X*cos(phirot2)-Y*sin(phirot2)), y=(( X*sin(phirot2)+Y*cos(phirot2) )), z=( imodule+0.5 )*Ecal_Barrel_module_dim - Ecal_Barrel_halfZ )
                rot = geom.structure.Rotation(name + "_rot", x=pi/2.0, y=phirot+pi, z=Q("0deg"))
                pla = geom.structure.Placement(name + "_pla", volume=stave_lv, pos=pos, rot=rot)

                barrel_lv.placements.append(pla.name)

        self.add_volume(barrel_lv)

    def construct_endcap_staves(self, geom):
        ''' construct a set of staves for the Endcap '''

        print "Construct ECAL Endcap"

        HGLayer_builder = self.get_builder(self.HGlayer_builder_name)
        LGLayer_builder = self.get_builder(self.LGlayer_builder_name)

        HGLayer_lv = HGLayer_builder.get_volume()
        LGLayer_lv = LGLayer_builder.get_volume()

        HGLayer_shape = geom.store.shapes.get(HGLayer_lv.shape)

        # ECAL Endcap
        nsides = self.nsides
        Ecal_inner_radius = self.r
        layer_thickness = HGLayer_shape.dz * 2
        safety = Q("1mm")
        module_thickness = self.nLayers * layer_thickness + safety
        Ecal_Barrel_halfZ = self.Barrel_halfZ
        EcalEndcap_min_z = Ecal_Barrel_halfZ
        EcalEndcap_max_z = Ecal_Barrel_halfZ + module_thickness
        Ecal_inner_radius = self.r

        #Mother volume Endcap
        endcap_shape_min = geom.shapes.PolyhedraRegular("ECALEndcap_min", numsides=nsides, rmin=Q("0mm"), rmax=Ecal_inner_radius+module_thickness, dz=EcalEndcap_min_z)
        endcap_shape_max = geom.shapes.PolyhedraRegular("ECALEndcap_max", numsides=nsides, rmin=Q("0mm"), rmax=Ecal_inner_radius+module_thickness, dz=EcalEndcap_max_z)

        endcap_shape = geom.shapes.Boolean( self.output_name, type='subtraction', first=endcap_shape_max, second=endcap_shape_min )
        endcap_lv = geom.structure.Volume(self.output_name+"_vol", shape=endcap_shape, material=self.material)

        #Create a template module
        endcap_stave_full = geom.shapes.PolyhedraRegular("ECAL_stave_full", numsides=nsides, rmin=Q("0mm"), rmax=Ecal_inner_radius+module_thickness, dz=module_thickness)
        quadr = Ecal_inner_radius+module_thickness
        quadrant = geom.shapes.Box("Quadrant", dx=quadr, dy=quadr, dz=module_thickness)

        endcap_stave_pos = geom.structure.Position("EcalEndcapQuadrant"+"_pos", x=quadr - Ecal_inner_radius, y=quadr + Ecal_inner_radius)
        endcap_stave_shape = geom.shapes.Boolean("EcalEndcapQuadrant", type='intersection', first=endcap_stave_full, second=quadrant, pos=endcap_stave_pos)
        endcap_stave_lv = geom.structure.Volume("EcalEndcapQuadrant"+"_vol", shape=endcap_stave_shape, material=self.material)

        max_dim_x = 2 * tan( pi/nsides ) * Ecal_inner_radius + module_thickness / sin( 2*pi/nsides ) #large side
        zPos = Q("0mm")
        layer_id = 0
        for ilayer in range(self.nLayers):
            layer_id = ilayer + 1

            #Configure the layer length based on the zPos in the stave
            l_dim_x = max_dim_x
            l_dim_y = max_dim_x
            layername = self.output_name + "_stave" + "_module" + "_layer_%i" % (layer_id)

            HGLayer_builder = self.get_builder(self.HGlayer_builder_name)
            NDHPgTPCHGLayerBuilder.changeLayerDim(HGLayer_builder, l_dim_x, l_dim_y, layername, "Intersection")
            NDHPgTPCHGLayerBuilder.construct(HGLayer_builder, geom)
            layer_lv = HGLayer_builder.get_volume(layername+"_vol")

            # Placement layer in stave
            layer_pos = geom.structure.Position(layername+"_pos", z=zPos + layer_thickness/2.0 - module_thickness/2.0)
            layer_pla = geom.structure.Placement(layername+"_pla", volume=layer_lv, pos=layer_pos)

            endcap_stave_lv.placements.append(layer_pla.name)

            zPos += layer_thickness;

        #Place staves in the Endcap Volume
        module_id = -1
        for iend in range(2):
            if iend == 0:
                module_id = 0
            else:
                module_id = 6

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

                #Placement staves in Endcap
                name = endcap_stave_lv.name + "_%i" % (stave_id) + "_module%i" % (module_id)
                pos = geom.structure.Position(name + "_pos", z=this_module_z_offset )
                rot = geom.structure.Rotation(name + "_rot", y=this_module_rotY, z=this_module_rotZ)
                pla = geom.structure.Placement(name + "_pla", volume=endcap_stave_lv, pos=pos, rot=rot)

                endcap_lv.placements.append(pla.name)

        self.add_volume(endcap_lv)
