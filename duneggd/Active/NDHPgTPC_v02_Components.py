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
                output_name='MPTECalHGLayer'
                )

    def depth(self):
        dzm = Q("0mm")
        for dz, lspace in zip(self.dz, self.lspacing):
            dzm += dz + lspace
        return dzm

    def changeLayerDim(self, dx = None, dy = None, name = None):
        #print "Changing param..", dx, dy, name
        self.dx = dx
        self.dy = dy
        self.output_name = name
        return

    def construct(self, geom):
        #print "dx", self.dx, "dy", self.dy
        dzm = self.depth()
        dzm = dzm/2.0  # Box() requires half dimensions
        #print "layer thickness=", dzm * 2, "mm"
        # make the mother volume
        name = self.output_name
        #print "In strip builder: strip_length=", strip_length
        #print "Compared to length=", self.length
        #print "Number of tiles to fit=", ntiles
        layer_shape = geom.shapes.Box(name, dx=(self.dx)/ 2.0, dy=(self.dy)/2.0, dz=(self.depth()) /2.0)
        #print "HG Layer shape dx=", layer_shape.dx*2, "dy=", layer_shape.dy*2, "dz=", layer_shape.dz*2
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
        #print "In strip builder: strip_length=", strip_length
        #print "Compared to length=", self.length
        #print "Number of tiles to fit=", ntiles
        layer_shape = geom.shapes.Box(name, dx=(self.dx)/ 2.0, dy=(self.dy)/2.0, dz=(self.depth()) /2.0)
        #print "LG Layer shape dx=", layer_shape.dx*2, "dy=", layer_shape.dy*2, "dz=", layer_shape.dz*2
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

        for istave in range(nsides):
            stave_id = istave+1
            dstave = int( nsides/4.0 )
            phirot =  hphi + pi/2.0
            phirot += (istave - dstave)*dphi
            phirot2 =  (istave - dstave) * dphi + hphi

            for imodule in range(Ecal_Barrel_n_modules):

                module_id = imodule+1
                stave_name = self.output_name + "_stave_%i" % (stave_id) + "_module_%i" % (module_id)
                stave_volname = self.output_name + "_stave_%i" % (stave_id) + "_module_%i" % (module_id) + "_vol"

                print "Creating ", stave_name

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
                    layername = self.output_name + "_stave_%i" % (stave_id) + "_module_%i" % (module_id) + "_layer_%i" % (layer_id)

                    HGLayer_builder = self.get_builder(self.HGlayer_builder_name)
                    NDHPgTPCHGLayerBuilder.changeLayerDim(HGLayer_builder, l_dim_x, l_dim_y, layername)
                    NDHPgTPCHGLayerBuilder.construct(HGLayer_builder, geom)
                    layer_lv = HGLayer_builder.get_volume(layername+"_vol")

                    #Placement layer in stave
                    layer_pos = geom.structure.Position(layername+"_pos", z=zPos + layer_thickness/2.0 - module_thickness/2.0)
                    layer_pla = geom.structure.Placement(layername+"_pla", volume=layer_lv, pos=layer_pos)

                    stave_lv.placements.append(layer_pla.name)

                    zPos += layer_thickness;

                #Placement staves in Barrel
                pos = geom.structure.Position(stave_volname+"_pos", x=(X*cos(phirot2)-Y*sin(phirot2)), y=(( X*sin(phirot2)+Y*cos(phirot2) )), z=( imodule+0.5 )*Ecal_Barrel_module_dim - Ecal_Barrel_halfZ )
                rot = geom.structure.Rotation(stave_volname+"_rot", x=pi/2.0, y=phirot+pi, z=Q("0deg"))
                pla = geom.structure.Placement(stave_volname+"_pla", volume=stave_lv, pos=pos, rot=rot)

                barrel_lv.placements.append(pla.name)

        self.add_volume(barrel_lv)
